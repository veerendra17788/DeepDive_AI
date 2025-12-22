from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from groq import Groq
from pydantic import BaseModel
from typing import List, Optional
import os
import requests
from bs4 import BeautifulSoup
import re
import random
import logging
import concurrent.futures
from urllib.parse import urlparse, urljoin, quote_plus
from io import BytesIO
import json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors

from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/api", tags=["research"])
templates = Jinja2Templates(directory="templates")

@router.get("/research_page", include_in_schema=False)
async def research_page(request: Request):
    # Deprecated/Redundant: Logic handled in main.py, but kept for router completeness if mounted differently
    return templates.TemplateResponse("research.html", {"request": request, "active_page": "research"})

# Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)
DEFAULT_MODEL = "llama-3.3-70b-versatile"
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
]
MAX_WORKERS = 10
SNIPPET_LENGTH = 15000

class ResearchRequest(BaseModel):
    query: str
    engines: List[str] = ["duckduckgo"]
    format: str = "markdown"
    max_iterations: int = 3
    options: List[str] = [] 

class PDFRequest(BaseModel):
    title: str
    content: str
    links: Optional[List[str]] = []

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def escape_xml(text):
    if not text: return ""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

def generate_pdf_flowable(title, content, links):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leading=16, spaceAfter=12, fontSize=11, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='Header1', parent=styles['Heading1'], spaceAfter=16, spaceBefore=12, textColor=colors.HexColor('#1e3a8a'), fontSize=18, leading=22))
    styles.add(ParagraphStyle(name='Header2', parent=styles['Heading2'], spaceAfter=12, spaceBefore=10, textColor=colors.HexColor('#1f2937'), fontSize=14))
    styles.add(ParagraphStyle(name='LinkStyle', parent=styles['BodyText'], textColor=colors.blue, fontSize=9))
    
    story = []
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 24))
    
    # Process content (Simple markdown-ish parsing for PDF)
    # Replacing **text** with <b>text</b> for reportlab
    formatted_content = content.replace('**', '<b>').replace('**', '</b>')
    
    for line in formatted_content.split('\n'):
        if not line.strip(): continue
        
        if line.strip().startswith('# '):
            story.append(Paragraph(line.strip()[2:], styles['Header1']))
        elif line.strip().startswith('## '):
             story.append(Paragraph(line.strip()[3:], styles['Header2']))
        elif line.strip().startswith('- '):
             story.append(Paragraph(f"• {line.strip()[2:]}", styles['Justify']))
        else:
            story.append(Paragraph(line, styles['Justify']))
            
    if links:
        story.append(PageBreak())
        story.append(Paragraph("References & Sources", styles['Header1']))
        story.append(Paragraph("The following sources were analyzed to generate this report:", styles['Justify']))
        story.append(Spacer(1, 12))
        
        for link in links:
            safe_link = escape_xml(link)
            # Limit link display length
            display_link = safe_link[:80] + "..." if len(safe_link) > 80 else safe_link
            story.append(Paragraph(f'<a href="{safe_link}" color="blue"><u>{display_link}</u></a>', styles['LinkStyle']))
            story.append(Spacer(1, 8))
            
    doc.build(story)
    buffer.seek(0)
    return buffer

def scrape_search_engine(query, engine="duckduckgo"):
    results = []
    if engine == "duckduckgo":
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        try:
            res = requests.get(url, headers={'User-Agent': get_random_user_agent()}, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                for a in soup.find_all('a', class_='result__a', href=True):
                    href = a['href']
                    if 'duckduckgo.com' not in href and href.startswith('http'):
                        results.append(href)
        except Exception as e:
            logging.error(f"DDG Error: {e}")
    return list(set(results))

def fetch_page_content(url):
    try:
        res = requests.get(url, headers={'User-Agent': get_random_user_agent()}, timeout=10)
        if res.status_code != 200: return "", [], []
        
        soup = BeautifulSoup(res.content, 'html.parser')
        
        # Extract emails
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.get_text())
        
        # Extract links
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]

        for s in soup(["script", "style"]): s.decompose()
        text = soup.get_text(separator=' ', strip=True)[:SNIPPET_LENGTH]
        return text, list(set(emails)), list(set(links))
    except:
        return "", [], []

def generate_llm_response(prompt):
    try:
        completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=DEFAULT_MODEL,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return str(e)

@router.post("/deep_research")
async def deep_research(req: ResearchRequest):
    query = req.query
    iterations = min(req.max_iterations, 5) 
    
    all_content = []
    all_emails = []
    all_links = []
    
    # Initial Search
    urls = []
    for engine in req.engines:
        urls.extend(scrape_search_engine(query, engine))
    
    urls = list(set(urls))[:iterations*2]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_page_content, u): u for u in urls}
        for future in concurrent.futures.as_completed(futures):
            text, emails, links_found = future.result()
            if text:
                all_content.append(text)
                if "extract_emails" in req.options: all_emails.extend(emails)
                if "extract_links" in req.options: all_links.extend(links_found)
                # Always track source URLs for the report logic, even if not extracted for the user list
                all_links.extend([futures[future]]) 

    # Format-specific instructions
    format_type = req.format if hasattr(req, 'format') else 'markdown'
    
    formatting_instructions = {
        'textual': """
        Format as **Textual Output** for research papers:
        - Write in formal academic tone
        - Include: Introduction, Observations, Analysis, Findings, Conclusion
        - Use full sentences and paragraphs
        - Cite sources inline
        - No tables or equations, pure narrative
        """,
        'tabular': """
        Format as **Tabular Output** for research papers:
        - Present data in Markdown tables
        - Include: Comparison tables, Metrics tables, Statistics tables
        - Use headers: | Metric | Value | Source |
        - Add summary statistics
        - Include data interpretation below each table
        """,
        'graphical': """
        Format as **Graphical Output Description** for research papers:
        - Describe charts and visualizations needed
        - Suggest: Bar charts, Line graphs, Pie charts, Confusion matrices
        - Format: "Figure 1: [Description]", "Chart Type: [Type]", "Data Points: [List]"
        - Include axis labels and legends
        - Provide data for plotting
        """,
        'mathematical': """
        Format as **Mathematical Output** for research papers:
        - Use LaTeX-style equations: $$equation$$
        - Include: Formulas, Models, Algorithms
        - Define all variables
        - Show derivations and proofs
        - Format: "Equation 1:", "Where: x = variable"
        """,
        'statistical': """
        Format as **Statistical Output** for research papers:
        - Include: Mean, Median, Standard Deviation, Variance
        - Show: Confidence Intervals, p-values, Hypothesis tests
        - Present statistical significance
        - Use format: "Mean ± SD", "CI: [lower, upper]"
        - Include interpretation of statistics
        """,
        'json': """
        Format as **Structured JSON**:
        - Return clean JSON structure
        - Include: {findings: [], metrics: {}, sources: []}
        - Use proper JSON syntax
        - Make it parseable
        """,
        'markdown': """
        Format as **Comprehensive Markdown Report**:
        - **Tone**: Academic, executive, high-level
        - **Structure**:
          1. **Executive Summary**: Concise overview
          2. **Key Findings**: Bullet points
          3. **Detailed Analysis**: Sections with headers (##)
          4. **Conclusion**: Strategic implications
        - **Formatting**: Use **bold**, clear headings, cite sources
        """
    }
    
    selected_format = formatting_instructions.get(format_type, formatting_instructions['markdown'])
    
    # Summarize with format-specific instructions
    combined_content = "\n\n".join(all_content[:15])
    prompt = f"Conduct a comprehensive deep research analysis on: '{query}'. {selected_format}\n\n**Source Material**:\n{combined_content}"
    
    report = generate_llm_response(prompt)
    
    response_data = {
        "explanation": report,
        "format": format_type,
        "emails": list(set(all_emails)) if "extract_emails" in req.options else [],
        "links": list(set(all_links))[:20], # Return top 20 links for PDF generation even if 'extract_links' option wasn't checked by user (frontend can filter display) allow user to see citations
    }
    
    return JSONResponse(response_data)

@router.post("/generate_pdf")
async def generate_pdf_endpoint(req: PDFRequest):
    try:
        pdf_buffer = generate_pdf_flowable(req.title, req.content, req.links)
        
        return StreamingResponse(
            pdf_buffer, 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={req.title.replace(' ', '_')}_Report.pdf"}
        )
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        return JSONResponse({"detail": f"PDF Error: {str(e)}"}, status_code=500)
