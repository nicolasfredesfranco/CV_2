# Contributing to Professional CV Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)

---

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Python version** and operating system
- **Screenshots** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why would this be useful?
- **Proposed solution** (if you have one)
- **Examples** from other projects (if relevant)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest test_main.py -v`)
5. Commit with meaningful messages
6. Push to your fork
7. Open a Pull Request

---

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/CV_2.git
cd CV_2

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

---

## Pull Request Process

1. **Ensure all tests pass**
   ```bash
   pytest test_main.py -v
   ```

2. **Update documentation**
   - Update README.md if adding features
   - Add docstrings to new functions
   - Update CHANGELOG.md

3. **Verify CV output unchanged** (if not intentional)
   ```bash
   python main.py
   # Check that generated PDF matches expected output
   ```

4. **Code formatting**
   ```bash
   black src/ test_main.py main.py
   flake8 src/ test_main.py main.py
   ```

5. **Meaningful commit messages**
   - Use present tense ("Add feature" not "Added feature")
   - Reference issues when applicable
   - Keep first line under 50 characters

---

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where beneficial

### Documentation

- Add docstrings to all public functions
- Use Google-style docstrings:
  ```python
  def example_function(param1: str, param2: int) -> bool:
      """Brief description of function.
      
      Args:
          param1: Description of param1
          param2: Description of param2
          
      Returns:
          Description of return value
          
      Raises:
          ValueError: When param2 is negative
      """
      pass
  ```

### File Organization

- Keep modules focused and single-purpose
- Place utility functions in `src/` modules
- Keep configuration in `src/config.py`
- Store data files in `data/`

---

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Aim for >80% code coverage
- Use descriptive test names
- Group related tests in classes

```python
class TestNewFeature:
    def test_basic_functionality(self):
        """Test description here."""
        # Arrange
        expected = "something"
        
        # Act
        result = my_function()
        
        # Assert
        assert result == expected
```

### Running Tests

```bash
# Run all tests
pytest test_main.py -v

# Run specific test
pytest test_main.py::TestClassName::test_method_name -v

# Generate coverage report
pytest --cov=src --cov-report=html test_main.py
```

### Test Categories

- **Unit tests**: Test individual functions
- **Integration tests**: Test component interactions
- **Visual tests**: Verify PDF output quality

---

## Adding New Features

### Example: Adding a New Section

1. **Create data file** (`data/certifications.json`):
   ```json
   [
     {
       "name": "Certification Name",
       "issuer": "Issuing Organization",
       "date": "Month YYYY"
     }
   ]
   ```

2. **Update data loader** (`src/data_loader.py`):
   ```python
   def load_certifications() -> List[Dict]:
       """Load certifications data from JSON file."""
       return load_json_file(CONFIG.DATA_DIR / 'certifications.json')
   ```

3. **Add rendering logic** (`src/generator.py`):
   ```python
   def render_certifications(self, certifications: List[Dict]):
       """Render certifications section on the CV."""
       # Implementation here
       pass
   ```

4. **Add tests** (`test_main.py`):
   ```python
   def test_certifications_rendering(self):
       """Test that certifications render correctly."""
       # Test implementation
       pass
   ```

5. **Update documentation**:
   - Add section to README.md
   - Document in CHANGELOG.md

---

## Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code formatting (no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Example

```
feat: Add certifications section

- Created certifications.json data file
- Implemented rendering logic in generator.py
- Added tests for certification rendering
- Updated README with customization guide

Closes #42
```

---

## Questions?

If you have questions about contributing:

1. Check existing [documentation](README.md)
2. Search [existing issues](https://github.com/nicolasfredesfranco/CV_2/issues)
3. Create a [new issue](https://github.com/nicolasfredesfranco/CV_2/issues/new)

---

**Thank you for contributing!** 🙏
