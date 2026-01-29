# Contributing to Professional CV Generator

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features or enhancements
- 📝 Improve documentation
- 🧪 Add or improve tests
- 💻 Submit code improvements

## 🚀 Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- pip

### Setup Instructions

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/CV.git
cd CV

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests to ensure everything works
pytest test_main.py -v
```

## 📋 Code Style Guidelines

### Python Code Style

- **Follow PEP 8** for code formatting
- **Use type hints** for function signatures
- **Write docstrings** for all public functions and classes (Google style)
- **Keep functions focused** - single responsibility principle
- **Use meaningful names** - descriptive variable and function names

### Example

```python
from typing import Tuple

def transform_coordinates(x: float, y: float, offset: float = 32.0) -> Tuple[float, float]:
    """
    Transform PDF coordinates to ReportLab canvas coordinates.
    
    Args:
        x: X-coordinate in PDF space
        y: Y-coordinate in PDF space (top-down)
        offset: Global Y offset for alignment correction
        
    Returns:
        Tuple of (x_transformed, y_transformed) in ReportLab space
        
    Raises:
        ValueError: If coordinates are negative
    """
    if x < 0 or y < 0:
        raise ValueError("Coordinates must be non-negative")
        
    y_transformed = CONFIG.PAGE_HEIGHT - y + offset
    return x, y_transformed
```

### Documentation Standards

- **All documentation in English**
- **Use clear, concise language**
- **Include code examples** where helpful
- **Keep README.md up to date**

## 🧪 Testing Requirements

All contributions must include appropriate tests:

```bash
# Run full test suite
pytest test_main.py -v

# Check test coverage
pytest test_main.py --cov=src --cov-report=term-missing

# Aim for >90% coverage on new code
```

### Writing Tests

```python
def test_coordinate_transformation():
    """Test PDF to ReportLab coordinate transformation."""
    x_result, y_result = CoordinateTransformer.transform_coordinates(100, 200)
    
    assert x_result == 100
    assert y_result == CONFIG.PAGE_HEIGHT - 200 + CONFIG.Y_GLOBAL_OFFSET
```

## 📝 Commit Message Guidelines

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat(renderer): add support for custom fonts

Implemented dynamic font loading from data/assets directory.
Users can now add custom TTF fonts without code changes.

Closes #42
```

```
fix(shapes): correct rectangle coordinate interpretation

Changed shape['rect'] unpacking from [x,y,w,h] to [x0,y0,x1,y1].
This fixes the sidebar rendering bug that caused 33% similarity loss.

Fixes #38
```

## 🔄 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add/update tests
   - Update documentation

3. **Test your changes**
   ```bash
   pytest test_main.py -v
   python main.py --validate-only
   python main.py  # Generate PDF
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(scope): your descriptive message"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub and create a PR
   - Fill in the PR template
   - Link related issues
   - Request review

### PR Checklist

- [ ] Tests pass locally (`pytest test_main.py -v`)
- [ ] Code follows style guidelines
- [ ] Documentation updated (README, docstrings)
- [ ] CHANGELOG.md updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts
- [ ] PR description explains changes clearly

## 🐛 Bug Reports

When filing a bug report, please include:

### Required Information

- **Python version**: `python --version`
- **OS and version**: e.g., Ubuntu 22.04, macOS 14.0, Windows 11
- **Steps to reproduce**: Detailed steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Full stack trace if applicable
- **Screenshot**: If visual issue

### Issue Template

```markdown
## Bug Description
Brief description of the bug

## Environment
- Python version: 3.11.5
- OS: Ubuntu 22.04
- Branch/Commit: main@abc1234

## Steps to Reproduce
1. Run `python main.py`
2. Observe output in outputs/
3. See error

## Expected Behavior
Should generate PDF without errors

## Actual Behavior
Raises ValueError on line 142

## Error Message
```
Traceback...
```

## Additional Context
- Happens only with custom fonts
- Works fine on macOS
```

## 💡 Feature Requests

For feature requests, please:

1. **Search existing issues** to avoid duplicates
2. **Describe the problem** this feature would solve
3. **Propose a solution** if you have one in mind
4. **Consider alternatives** you've thought about

## 🏗️ Architecture Guidelines

### Module Responsibilities

- **`config.py`**: Constants and configuration only
- **`fonts.py`**: Font registration and management
- **`validators.py`**: JSON schema validation
- **`transformations.py`**: Coordinate transformations
- **`hyperlinks.py`**: URL detection and generation
- **`renderer.py`**: PDF canvas operations

### Adding New Modules

If adding a new module to `src/`:

1. Create module with clear purpose
2. Add `__init__.py` imports
3. Write comprehensive docstring
4. Add unit tests in `test_main.py`
5. Update architecture diagram in README

## 📚 Resources

- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/en/stable/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: nicolas.fredes@example.com (for private inquiries)

## 🙏 Recognition

Contributors will be acknowledged in:
- README.md (Contributors section)
- CHANGELOG.md (for significant contributions)

---

**Thank you for contributing!** Every improvement, no matter how small, makes this project better. 🎉
