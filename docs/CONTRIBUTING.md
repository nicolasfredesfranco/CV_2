# 🤝 Contributing to Precision CV Generator

First off, thank you for considering contributing to this project! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Important Note](#important-note)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Issue Guidelines](#issue-guidelines)

---

## Code of Conduct

This project adheres to a **Code of Conduct** that all contributors are expected to follow:

###Our Pledge

We pledge to make participation in this project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity
- Gender identity and expression
- Level of experience, nationality
- Personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive behaviors:**
- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing viewpoints
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what is best for the community
- ✅ Showing empathy towards others

**Unacceptable behaviors:**
- ❌ Trolling, insulting/derogatory comments
- ❌ Public or private harassment
- ❌ Publishing others' private information
- ❌ Other conduct which could reasonably be considered inappropriate

---

## Important Note

> [!CAUTION]
> **This is a Personal CV Generator**
>
> While the **code** is open source (MIT License), the **CV content** (personal information, professional experience, achievements) is proprietary intellectual property of Nicolás Ignacio Fredes Franco.
>
> ### What You CAN Do ✅
> - Fork and modify the **code** for your own CV
> - Contribute improvements to the **generation system**
> - Share techniques and optimizations
> - Create your own CV using this codebase
>
> ### What You CANNOT Do ❌
> - Use, copy, or redistribute Nicolás Fredes Franco's personal data
> - Misrepresent someone else's professional experience
> - Modify `data/coordinates.json` to include someone else's information
> - Remove or alter attribution to the original author

---

## How Can I Contribute?

### 🐛 Reporting Bugs

**Before submitting a bug report:**
- Check the [issue tracker](https://github.com/nicolasfredesfranco/CV/issues) for existing reports
- Verify you're using the latest version
- Collect relevant information (Python version, OS, error messages)

**When submitting a bug report, include:**

```markdown
### Bug Description
Clear and concise description of the bug.

### Steps to Reproduce
1. Run command '...'
2. See error '...'

### Expected Behavior
What you expected to happen.

### Actual Behavior
What actually happened.

### Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.10.5]
- ReportLab: [e.g., 4.0.4]

### Additional Context
- Error logs
- Screenshots
- Relevant code snippets
```

### 💡 Suggesting Enhancements

**Enhancement categories:**

1. **New Precision Techniques** - Better rendering accuracy
2. **Performance Optimizations** - Faster generation
3. **Compression Strategies** - Better PDF size management
4. **Verification Tools** - Quality assurance improvements
5. **Documentation** - Clearer explanations

**Enhancement proposal template:**

```markdown
### Feature Description
Clear description of the proposed feature.

### Motivation
Why is this feature valuable?

### Proposed Implementation
How would you implement this?

### Alternatives Considered
What other approaches did you consider?

### Additional Context
Mockups, references, examples.
```

### 📝 Improving Documentation

Documentation improvements are **highly valued**!

**Areas needing documentation:**
- API documentation for classes/functions
- More code examples
- Tutorial for creating CV from scratch
- Video walkthrough (if applicable)
- Translations (Spanish docs exist, could expand)

### 🔧 Contributing Code

**Types of code contributions:**

1. **Bug Fixes** - Fix rendering errors, coordinate miscalculations
2. **New Precision Patches** - Improve similarity score
3. **Utility Scripts** - New tools for extraction/verification
4. **Compression Algorithms** - Better PDF optimization
5. **Test Coverage** - Unit tests, integration tests

---

## Development Process

### 1. Fork the Repository

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/CV.git
cd CV

# Add upstream remote
git remote add upstream https://github.com/nicolasfredesfranco/CV.git
```

### 2. Create a Branch

**Branch naming convention:**

```bash
# Feature branches
git checkout -b feature/add-bold-text-simulation

# Bug fix branches
git checkout -b fix/coordinate-transformation-error

# Documentation branches
git checkout -b docs/improve-architecture-diagrams
```

**Naming patterns:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test additions

### 3. Make Changes

**Development workflow:**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make your changes
# ... edit files ...

# Test changes
python3 main.py
python3 scripts/verification/verify_links.py

# Format code
black main.py

# Lint code
flake8 main.py --max-line-length=100
```

### 4. Commit Changes

See [Commit Guidelines](#commit-guidelines) below.

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Open Pull Request

Use the [Pull Request Template](#pull-request-process).

---

## Pull Request Process

### PR Template

When opening a PR, include:

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Motivation
Why is this change necessary?

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How did you test this?
- [ ] Manual testing
- [ ] Automated tests added
- [ ] Existing tests pass

## Screenshots (if applicable)
Before/after screenshots or diagrams.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex areas
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally

## Related Issues
Closes #123
```

### Review Process

1. **Automated Checks** (if CI/CD configured)
   - Linting (flake8)
   - Formatting (black --check)
   - Tests (pytest)

2. **Manual Review**
   - Code quality review
   - Functionality verification
   - Documentation completeness

3. **Feedback Incorporation**
   - Address reviewer comments
   - Make requested changes
   - Re-request review

4. **Merge**
   - Squash and merge (preferred)
   - Rebase and merge (for clean history)

---

## Coding Standards

### Python Style Guide

**Follow PEP 8 with modifications:**

```python
# ✅ Good: Descriptive names, proper spacing
def transform_coordinate(x: float, y: float, page_height: float) -> Tuple[float, float]:
    """Transform PDF coordinates to ReportLab space."""
    y_reportlab = page_height - y
    return (x, y_reportlab)

# ❌ Bad: Unclear names, poor formatting
def tr(a,b,c):
    return (a,c-b)
```

**Line length:** 100 characters (not 79)

```python
# ✅ Good: Fits within 100 characters
message = f"Rendering element '{elem['text']}' at position ({elem['x']}, {elem['y']})"

# ❌ Bad: Exceeds 100 characters
very_long_variable_name_that_makes_this_line_exceed_one_hundred_characters_and_is_hard_to_read = "text"
```

**Imports:** Group and sort

```python
# ✅ Good: Organized imports
import os
import sys
from typing import List, Dict, Tuple

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# ❌ Bad: Disorganized
from reportlab.lib.pagesizes import A4
import sys
from typing import List
import os
```

### Documentation

**Docstrings required for:**
- All public functions
- All classes
- Complex logic blocks

**Format:** Google style

```python
def rgb_from_int(color_int: int) -> Tuple[float, float, float]:
    """Convert integer color value to normalized RGB tuple.
    
    Args:
        color_int: Integer representation of RGB color (0x00RRGGBB)
    
    Returns:
        Tuple of (r, g, b) with values in range [0.0, 1.0]
    
    Example:
        >>> rgb_from_int(0)
        (0.0, 0.0, 0.0)
        >>> rgb_from_int(16777215)
        (1.0, 1.0, 1.0)
    """
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return (r/255.0, g/255.0, b/255.0)
```

### Comments

**Use comments for:**
- Complex algorithms
- Non-obvious decisions
- Workarounds for library limitations

```python
# ✅ Good: Explains WHY
# ReportLab uses bottom-up coordinates, but PDF uses top-down.
# We must invert the Y-axis to match the target layout.
y_reportlab = page_height - y_pdf

# ❌ Bad: Explains WHAT (obvious from code)
# Subtract y from page height
y_reportlab = page_height - y_pdf
```

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Scope (optional):**
- `main`: Main generation engine
- `compression`: Compression scripts
- `verification`: Verification tools
- `docs`: Documentation
- `config`: Configuration files

**Examples:**

```bash
# Good commits
git commit -m "feat(main): add italic text compensation patch"
git commit -m "fix(compression): correct qpdf file size calculation"
git commit -m "docs(readme): add installation troubleshooting section"

# Example with body
git commit -m "feat(main): implement smart bullet detection

Add heuristic logic to detect and inject bullet points based on:
- Column position (right column)
- Text style (non-bold, non-italic)
- Content pattern (uppercase start, min 3 chars)

Improves structural similarity by ~0.5%"
```

**Bad commits:**
```bash
# ❌ Too vague
git commit -m "fix stuff"
git commit -m "updates"

# ❌ Too many unrelated changes
git commit -m "Add feature X, fix bug Y, update docs"
```

### Commit Best Practices

- **Atomic commits**: One logical change per commit
- **Present tense**: "Add feature" not "Added feature"
- **Imperative mood**: "Fix bug" not "Fixes bug"
- **Line length**: Subject < 72 chars, body < 100 chars per line

---

## Issue Guidelines

### Issue Labels

| Label | Description |
|-------|-------------|
| `bug` | Something isn't working |
| `enhancement` | New feature or request |
| `documentation` | Documentation improvements |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention needed |
| `question` | General questions |
| `wontfix` | Will not be addressed |

### Issue Templates

#### Bug Report

```markdown
**Describe the bug**
A clear and concise description.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Run '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.10]
- Version: [e.g., 1.2.3]

**Additional context**
Any other relevant information.
```

#### Feature Request

```markdown
**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution you'd like**
Clear description of desired solution.

**Describe alternatives you've considered**
Alternative solutions or features.

**Additional context**
Mockups, examples, references.
```

---

## Recognition

### Contributors

All contributors will be recognized in:
- GitHub Contributors page
- CHANGELOG.md (for significant contributions)
- README.md Acknowledgments section (optional)

### Types of Contributions

We value **all** contributions:
- 💻 Code contributions
- 📝 Documentation improvements
- 🐛 Bug reports
- 💡 Feature suggestions
- 🎨 Design improvements
- 🌐 Translations
- 📣 Spreading the word

---

## Questions?

**Don't hesitate to ask!**

- **GitHub Discussions**: For general questions
- **GitHub Issues**: For bug reports and feature requests
- **Email**: nico.fredes.franco@gmail.com (for sensitive matters)

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](../LICENSE).

**Attribution Requirement:** All uses must maintain attribution to the original author, Nicolás Ignacio Fredes Franco.

---

<div align="center">

**Thank you for contributing! 🙏**

Made with ❤️ by the community

</div>
