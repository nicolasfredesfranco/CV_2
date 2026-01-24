import json
import shutil
import math

def inject_skills():
    json_path = "objetivo_coords.json"
    
    # Backup
    shutil.copy(json_path, json_path + ".bak")
    
    with open(json_path, 'r') as f:
        elements = json.load(f)
        
    # Remove existing items in SKILLS region to avoid duplicates/overlap
    # Region: X < 200, 410 < Y < 700
    # Keep main headers if they point to the right things, but simpler to remove and rewrite fully
    # "SKILLS" title is at 409. We keep that.
    # Start deleting from 415 downwards.
    
    new_elements = [e for e in elements if not (e['x'] < 200 and 415 < e['y'] < 700)]
    
    print(f"Removed {len(elements) - len(new_elements)} elements from SKILLS region.")
    
    # Define Content
    # Format: (Text, RelativeY, IsBold, IsHeader)
    # Start Base Y for "PROGRAMMING LANGUAGES" = 427.12
    
    base_x = 43.63
    line_height = 13.0
    header_gap = 14.0 # Extra gap before header
    
    # Structure
    # Text, dy (from prev)
    
    sections = [
        # PROGRAMMING LANGUAGES
        {"text": "PROGRAMMING LANGUAGES", "y": 427.12, "bold": True, "size": 11.0, "header": True},
        {"text": "• Python  • C  • C++", "y": 427.12 + 15, "bold": False, "size": 10.0},
        {"text": "• MySQL  • SQL", "y": 427.12 + 15 + line_height, "bold": False, "size": 10.0},
        
        # FRAMEWORKS
        {"text": "FRAMEWORKS", "y": 468.39, "bold": True, "size": 11.0, "header": True},
        {"text": "• PyTorch  • TensorFlow", "y": 468.39 + 15, "bold": False, "size": 10.0},
        {"text": "• Keras  • Pandas", "y": 468.39 + 15 + line_height*1, "bold": False, "size": 10.0},
        {"text": "• Threading  • OpenCV", "y": 468.39 + 15 + line_height*2, "bold": False, "size": 10.0},
        {"text": "• NVIDIA Deepstream", "y": 468.39 + 15 + line_height*3, "bold": False, "size": 10.0},
        {"text": "• Vertex AI Agent Engine", "y": 468.39 + 15 + line_height*4, "bold": False, "size": 10.0},
        {"text": "• Google-ADK  • LangChain", "y": 468.39 + 15 + line_height*5, "bold": False, "size": 10.0},
        
        # CLOUD
        {"text": "CLOUD", "y": 563.11, "bold": True, "size": 11.0, "header": True},
        {"text": "• AWS  • Snowflake  • GCP", "y": 563.11 + 15, "bold": False, "size": 10.0},
        
        # CONCEPTS
        {"text": "CONCEPTS", "y": 591.07, "bold": True, "size": 11.0, "header": True},
        {"text": "• Machine Learning", "y": 591.07 + 15, "bold": False, "size": 10.0},
        {"text": "• Computer Vision", "y": 591.07 + 15 + line_height*1, "bold": False, "size": 10.0},
        {"text": "• Natural Language Processing", "y": 591.07 + 15 + line_height*2, "bold": False, "size": 10.0},
        {"text": "• IoT  • Forecasting", "y": 591.07 + 15 + line_height*3, "bold": False, "size": 10.0},
        {"text": "• Object-Oriented Programming", "y": 591.07 + 15 + line_height*4, "bold": False, "size": 10.0},
        {"text": "• Parallel Computing", "y": 591.07 + 15 + line_height*5, "bold": False, "size": 10.0},
        {"text": "• GPU-Accelerated Computing", "y": 591.07 + 15 + line_height*6, "bold": False, "size": 10.0},
        {"text": "• Generative AI", "y": 591.07 + 15 + line_height*7, "bold": False, "size": 10.0},
    ]
    
    for s in sections:
        elem = {
            "text": s["text"],
            "x": base_x,
            "y": s["y"],
            "font": "TrebuchetMS-Bold" if s["bold"] else "TrebuchetMS",
            "size": s["size"],
            "color": 0, # Black
            "bold": s["bold"],
            "italic": False
        }
        new_elements.append(elem)
        
    # Sort by Y then X
    new_elements.sort(key=lambda k: (k['y'], k['x']))
    
    with open(json_path, 'w') as f:
        json.dump(new_elements, f, indent=2)
        
    print(f"Injected {len(sections)} skills items. Total elements: {len(new_elements)}")

if __name__ == "__main__":
    inject_skills()
