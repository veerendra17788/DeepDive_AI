import os
import sys
from fastapi.templating import Jinja2Templates
from fastapi import Request
from starlette.datastructures import URL

# Mock a simple request
class MockRequest:
    def __init__(self):
        self.url_for = lambda name, **path_params: f"/{name}"
        self.scope = {"type": "http"}

try:
    print(f"CWD: {os.getcwd()}")
    if os.path.exists("templates"):
        print("templates/ directory exists.")
        print(f"Contents: {os.listdir('templates')}")
        if os.path.exists("templates/auth"):
             print(f"templates/auth contents: {os.listdir('templates/auth')}")
    else:
        print("templates/ directory NOT FOUND!")

    print("Initializing Jinja2Templates...")
    templates = Jinja2Templates(directory="templates")
    
    print("Attempting to render auth/register.html...")
    # We need a dummy request context usually
    mock_request = MockRequest()
    
    # Render
    response = templates.get_template("auth/register.html").render({"request": mock_request})
    print("SUCCESS: Template rendered.")
    print(response[:100] + "...")
    
except Exception as e:
    print(f"TEMPLATE ERROR: {e}")
    import traceback
    traceback.print_exc()
