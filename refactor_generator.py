#!/usr/bin/env python3
"""
Script to generate the refactored CV generator code.
Transforms the original flat structure into hierarchical OOP structure.
"""

# Read original file
with open('generate_cv.py', 'r') as f:
    original = f.read()

# Extract CV_CONTENT from original
import ast
tree = ast.parse(original)

# Find CV_CONTENT assignment
cv_content_elements = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'CV_CONTENT':
                # Found CV_CONTENT
                if isinstance(node.value, ast.List):
                    cv_content_elements = [ast.literal_eval(ast.unparse(elt)) for elt in node.value.elts]
                break

# Extract BANNERS
banners = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'BANNERS':
                if isinstance(node.value, ast.List):
                    banners = [ast.literal_eval(ast.unparse(elt)) for elt in node.value.elts]
                break

# Extract LINKS
links = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'LINKS':
                if isinstance(node.value, ast.List):
                    links = [ast.literal_eval(ast.unparse(elt)) for elt in node.value.elts]
                break

print(f"Extracted {len(cv_content_elements)} CV elements")
print(f"Extracted {len(banners)} banners")
print(f"Extracted {len(links)} links")

# Organize CV_CONTENT by sections
def organize_by_sections(elements):
    """Organize elements into hierarchical structure by Y position and content."""
    
    # Contact info: y > 668
    contact = [e for e in elements if e.get('y', 0) > 668]
    
    # Education section: 440 < y <= 668 and x < 200
    education = [e for e in elements if 440 < e.get('y', 0) <= 668 and e.get('x', 0) < 200]
    
    # Skills section: 107 < y <= 440 and x < 200
    skills = [e for e in elements if 107 < e.get('y', 0) <= 440 and e.get('x', 0) < 200]
    
    # Languages section: y <= 107 and x < 200
    languages = [e for e in elements if e.get('y', 0) <= 107 and e.get('x', 0) < 200]
    
    # Right column header name: y > 710 and x >= 200
    header_name = [e for e in elements if e.get('y', 0) > 710 and e.get('x', 0) >= 200]
    
    # Experience section: 92 < y <= 710 and x >= 200
    experience = [e for e in elements if 92 < e.get('y', 0) <= 710 and e.get('x', 0) >= 200]
    
    # Papers section: y <= 92 and x >= 200
    papers = [e for e in elements if e.get('y', 0) <= 92 and e.get('x', 0) >= 200]
    
    return {
        'contact': contact,
        'education': education,
        'skills': skills,
        'languages': languages,
        'header_name': header_name,
        'experience': experience,
        'papers': papers
    }

sections = organize_by_sections(cv_content_elements)

for section, elems in sections.items():
    print(f"{section}: {len(elems)} elements")

# Now organize experience by company
def organize_experience(exp_elements):
    """Organize experience elements by company."""
    companies = {}
    current_company = None
    
    # Sort by Y descending (top to bottom)
    sorted_exp = sorted(exp_elements, key=lambda e: e.get('y', 0), reverse=True)
    
    for elem in sorted_exp:
        text = elem.get('text', '').strip()
        y = elem.get('y', 0)
        
        # Detect company headers (bold, size 14, y positions for companies)
        if elem.get('bold') and elem.get('size') == 14.0:
            if 'DEUNA' in text:
                current_company = 'deuna'
                companies[current_company] = {'elements': []}
            elif 'SPOT' in text:
                current_company = 'spot'
                companies[current_company] = {'elements': []}
            elif 'EPAM' in text:
                current_company = 'epam'
                companies[current_company] = {'elements': []}
            elif 'WALMART' in text:
                current_company = 'walmart'
                companies[current_company] = {'elements': []}
            elif 'LAMNGEN' in text:
                current_company = 'lamngen'
                companies[current_company] = {'elements': []}
        
        if current_company and current_company in companies:
            companies[current_company]['elements'].append(elem)
    
    return companies

companies_data = organize_experience(sections['experience'])
for company, data in companies_data.items():
    print(f"  {company}: {len(data['elements'])} elements")

print("\nOrganization complete! Ready to generate refactored code.")

