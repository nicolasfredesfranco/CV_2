# Contributing to CV Generator

We welcome contributions to improve the precision and capabilities of this CV generator.

## Development Standards

### Code Style
- **Language**: Python 3.10+
- **Docstrings**: All public classes and methods must have Google-style docstrings in English.
- **Typing**: Use type hints (`typing` module) for all function arguments and return values.

### Data Integrity
- Never modify `data/objective_dictionary.json` manually. It should only be updated via the extraction scripts if the source PDF changes.
- Ensure `coordinates.json` validation passes before committing (`src/validators.py` runs automatically on build).

### Pull Request Process
1. Update the `README.md` with details of changes to the interface.
2. Increase the version numbers in any examples files and the README to the new version that this Pull Request would represent.
3. You may merge the Pull Request in once you have the sign-off of two other developers.

## Reporting Bugs
- If you find a visual alignment error, please include a screenshot comparing the `objective` vs `generated` PDF.
