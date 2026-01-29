# User Guide - CV Generator

This guide will help you customize the CV generator to create your own professional resume.

## Table of Contents

- [Quick Start](#quick-start)
- [Customizing Your CV](#customizing-your-cv)
- [Data Files Reference](#data-files-reference)
- [Advanced Customization](#advanced-customization)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## Quick Start

### 1. Install and Generate

```bash
# Install dependencies
pip install -r requirements.txt

# Generate CV
python main.py

# Find your CV at: outputs/Nicolas_Fredes_CV.pdf
```

### 2. Customize Your Information

Edit the JSON files in the `data/` directory:

- `personal.json` - Your name, contact info
- `experience.json` - Work history
- `education.json` - Academic background  
- `skills.json` - Technical and language skills

### 3. Regenerate

```bash
python main.py
```

That's it! Your customized CV is ready.

---

## Customizing Your CV

### Personal Information

**File**: `data/personal.json`

```json
{
  "name": "Your Full Name",
  "title": "Your Professional Title",
  "phone": "your-phone-number",
  "email": "your.email@example.com",
  "location": "City, Country",
  "linkedin": "linkedin-username",
  "github": "github-username"
}
```

**Tips**:
- Keep your title concise (e.g., "Software Engineer", "Data Scientist")
- Use professional email address
- LinkedIn and GitHub usernames (not full URLs)

### Work Experience

**File**: `data/experience.json`

```json
[
  {
    "position": "Senior Software Engineer",
    "company": "Tech Company Inc",
    "location": "San Francisco, USA",
    "dates": "Jan 2022 - Present",
    "description": "Led development of cloud-native applications..."
  },
  {
    "position": "Software Engineer",
    "company": "Startup Corp",
    "location": "Remote",
    "dates": "Jun 2019 - Dec 2021",
    "description": "Developed microservices architecture..."
  }
]
```

**Tips**:
- List most recent job first
- Use action verbs ("Led", "Developed", "Implemented")
- Quantify achievements when possible
- Keep descriptions concise but impactful

### Education

**File**: `data/education.json`

```json
[
  {
    "degree": "M.S. in Computer Science",
    "institution": "Stanford University",
    "location": "Stanford, USA",
    "graduation": "June 2019",
    "thesis": "Deep Learning for Natural Language Processing",
    "gpa": "4.0/4.0"
  },
  {
    "degree": "B.S. in Software Engineering",
    "institution": "UC Berkeley",
    "location": "Berkeley, USA",
    "graduation": "May 2017",
    "gpa": "3.9/4.0"
  }
]
```

**Tips**:
- List highest degree first
- Include GPA if strong (>3.5)
- Thesis is optional
- Include relevant coursework if recent graduate

### Skills

**File**: `data/skills.json`

```json
{
  "programming_languages": [
    "Python",
    "JavaScript",
    "Java",
    "C++"
  ],
  "frameworks": [
    "React",
    "Django",
    "TensorFlow",
    "PyTorch"
  ],
  "tools": [
    "Git",
    "Docker",
    "Kubernetes",
    "AWS"
  ],
  "languages": [
    "English (Native)",
    "Spanish (Fluent)",
    "French (Conversational)"
  ]
}
```

**Tips**:
- List skills in order of proficiency
- Be honest about skill levels
- Include only relevant skills
- Update regularly as you learn new technologies

---

## Data Files Reference

### coordinates.json

**Purpose**: Controls exact positioning of all text elements

**Structure**:
```json
{
  "text": "Text to display",
  "x": 50.0,          # Horizontal position (points from left)
  "y": 700.0,         # Vertical position (points from bottom)
  "fontsize": 12,     # Font size in points
  "fontname": "Helvetica-Bold",
  "color": [0, 0, 0], # RGB color (0-1)
  "align": "left"     # Text alignment
}
```

**Font Names Available**:
- `Helvetica`
- `Helvetica-Bold`
- `Helvetica-Oblique`
- `Times-Roman`
- `Times-Bold`
- `Courier`

### shapes.json

**Purpose**: Defines colored backgrounds, lines, and visual elements

**Structure**:
```json
{
  "type": "rect",               # Shape type
  "rect": [x0, y0, x1, y1],    # Coordinates
  "color": [r, g, b],           # RGB (0-1)
  "fill_opacity": 1.0           # Transparency (0-1)
}
```

**Common Shapes**:
- Section headers (blue rectangles)
- Skill bars
- Decorative elements

---

## Advanced Customization

### Changing Colors

**File**: `src/config.py`

```python
# Primary blue color (section headers)
COLOR_PRIMARY_BLUE = (0.168627, 0.450980, 0.701961)  # RGB values 0-1

# To change to red:
COLOR_PRIMARY_BLUE = (0.8, 0.1, 0.1)

# To change to green:
COLOR_PRIMARY_BLUE = (0.1, 0.6, 0.2)
```

**RGB Converter**: Use [https://colorpicker.me](https://colorpicker.me) to convert colors

### Page Dimensions

```python
# Standard letter size (default)
PAGE_WIDTH = 623.0
PAGE_HEIGHT = 806.0

# A4 size
PAGE_WIDTH = 595.0
PAGE_HEIGHT = 842.0
```

### Fine-Tuning Vertical Alignment

```python
# Adjust global Y offset if text appears too high/low
Y_GLOBAL_OFFSET = 39.30  # Increase to move everything down
```

### Adding Custom Sections

See [CONTRIBUTING.md](CONTRIBUTING.md#adding-new-features) for detailed guide on adding new sections.

---

## Troubleshooting

### Common Issues

**Problem**: PDF doesn't generate

**Solution**:
```bash
# Check dependencies are installed
pip install -r requirements.txt

# Run tests
pytest test_main.py -v

# Check for errors
python main.py
```

---

**Problem**: Text appears in wrong position

**Solution**:
- Don't modify `coordinates.json` unless you know what you're doing
- Check `Y_GLOBAL_OFFSET` in `src/config.py`
- Ensure JSON files are valid (use [JSONLint](https://jsonlint.com))

---

**Problem**: Links don't work

**Solution**:
- Ensure LinkedIn/GitHub usernames are correct (not full URLs)
- Check `personal.json` format
- Verify special characters are escaped

---

**Problem**: Colors look wrong

**Solution**:
- RGB values must be 0-1, not 0-255
- To convert: divide by 255 (e.g., 255 → 1.0, 128 → 0.5)
- Check `shapes.json` and `coordinates.json` for color values

---

## FAQ

**Q: Can I change the font?**

A: Yes, but it requires modifying `coordinates.json`. Standard PDF fonts are: Helvetica, Times-Roman, Courier.

**Q: How do I add a photo?**

A: This requires code changes. See CONTRIBUTING.md for adding new features.

**Q: Can I have multiple pages?**

A: The current design is optimized for one page. Multi-page support requires significant code changes.

**Q: Is my data secure?**

A: Yes! Everything runs locally on your machine. No data is sent anywhere.

**Q: Can I sell CVs made with this?**

A: Yes, under MIT license. However, give credit to the original project.

**Q: How do I update the generator?**

A:
```bash
git pull origin master
pip install -r requirements.txt
```

---

## Need More Help?

1. Check [README.md](README.md)
2. Read [CONTRIBUTING.md](CONTRIBUTING.md)
3. Search [GitHub Issues](https://github.com/nicolasfredesfranco/CV_2/issues)
4. Create a [new issue](https://github.com/nicolasfredesfranco/CV_2/issues/new)

---

**Happy CV building!** 🚀
