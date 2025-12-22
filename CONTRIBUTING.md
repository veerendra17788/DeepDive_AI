# Contributing to DeepDive AI 🚀

Thank you for your interest in contributing to **DeepDive AI**! This document provides guidelines and instructions for contributing to our AI-powered research and job search platform.

## 🌟 Ways to Contribute

- 🐛 **Bug Reports**: Found a bug? Let us know!
- 💡 **Feature Requests**: Have an idea? Share it with us!
- 🔧 **Code Contributions**: Fix bugs, add features, improve performance
- 📚 **Documentation**: Improve docs, add examples, create tutorials
- 🎨 **Design**: UI/UX improvements, icons, graphics
- 🧪 **Testing**: Write tests, test new features, report issues

## 🛠️ Development Setup

### Prerequisites
- Python 3.11+
- Git
- API Keys (Gemini AI & Groq)

### Quick Setup

**Option 1: Automated Setup (Recommended)**
```bash
# Clone the repository
git clone https://github.com/veerendra17788/DeepDive_AI.git
cd DeepDive_AI

# Run setup script
# On Windows:
setup_dev.bat
# On macOS/Linux:
chmod +x setup_dev.sh && ./setup_dev.sh
```

**Option 2: Manual Setup**
```bash
# Clone and setup virtual environment
git clone https://github.com/veerendra17788/DeepDive_AI.git
cd DeepDive_AI
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Edit with your API keys
```

### Running the Development Server
```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

## 📝 Development Guidelines

### Code Style
- **Python**: Follow PEP 8 style guide
- **JavaScript**: Use ES6+ features, consistent indentation
- **HTML/CSS**: Semantic HTML, responsive design principles
- **Comments**: Clear, concise, and meaningful

### Commit Convention
We follow the [Conventional Commits](https://conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Build process or auxiliary tool changes

**Examples:**
```bash
git commit -m "feat(search): add multi-engine parallel scraping"
git commit -m "fix(auth): resolve JWT token expiration issue"
git commit -m "docs: update installation instructions"
```

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/feature-name`: New features
- `fix/issue-description`: Bug fixes
- `docs/documentation-update`: Documentation changes

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_research.py
```

### Writing Tests
- Write tests for new features
- Maintain or improve test coverage
- Use descriptive test names
- Include both positive and negative test cases

## 🚀 Pull Request Process

### Before Submitting
1. **Fork** the repository
2. **Create** a feature branch from `develop`
3. **Make** your changes
4. **Test** your changes thoroughly
5. **Update** documentation if needed
6. **Commit** using conventional commit messages

### PR Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated for changes
- [ ] Documentation updated (if applicable)
- [ ] No merge conflicts
- [ ] Descriptive PR title and description

### PR Template
```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] New tests added
- [ ] All tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Additional Notes
Any additional information or context.
```

## 🐛 Bug Reports

Use the bug report template:

```markdown
**Bug Description**
Clear description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Windows 10, macOS Big Sur]
 - Browser: [e.g. Chrome, Firefox]
 - Version: [e.g. v1.2.3]

**Additional Context**
Any other context about the problem.
```

## 💡 Feature Requests

Use the feature request template:

```markdown
**Feature Description**
Clear description of the feature you'd like to see.

**Problem It Solves**
What problem does this feature address?

**Proposed Solution**
How you envision this feature working.

**Alternatives Considered**
Other solutions you've considered.

**Additional Context**
Any other context, mockups, or examples.
```

## 📚 Documentation

### Documentation Standards
- **Clear and Concise**: Easy to understand
- **Examples**: Include code examples
- **Up-to-date**: Keep documentation current
- **Comprehensive**: Cover all features

### Areas Needing Documentation
- API endpoints and parameters
- Configuration options
- Deployment guides
- Troubleshooting guides
- Feature tutorials

## 🎨 Design Guidelines

### UI/UX Principles
- **Responsive**: Works on all device sizes
- **Accessible**: Follows WCAG guidelines
- **Intuitive**: Easy to navigate and understand
- **Consistent**: Uniform design patterns
- **Fast**: Optimized for performance

### Design Assets
- Use consistent color scheme
- Follow material design principles
- Optimize images and icons
- Maintain accessibility standards

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributor insights
- Special thanks in documentation

## 📞 Getting Help

- **Discord**: [Join our community](https://discord.gg/deepdive-ai)
- **GitHub Issues**: For bug reports and feature requests
- **Email**: [Contact maintainers](mailto:21131A05C6@gvpce.ac.in)
- **Documentation**: Check our comprehensive docs

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You

Every contribution, no matter how small, helps make DeepDive AI better for everyone. We appreciate your time and effort in improving this project!

---

<div align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">
  <h3>Happy Contributing! 🎉</h3>
</div>