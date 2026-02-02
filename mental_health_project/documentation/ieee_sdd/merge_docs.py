import os
import re
import base64
import json

def merge_and_convert():
    docs_dir = "/Users/raxielh/Desktop/MentalHealth/mental_health_project/documentation/ieee_sdd/"
    output_file = os.path.join(docs_dir, "MindCare_IEEE_SDD_Full.md")
    
    # Get all markdown files except the index and the output file itself
    files = sorted([f for f in os.listdir(docs_dir) if f.endswith(".md") and f[0].isdigit()])
    
    full_content = "# MindCare - Software Design Description (IEEE 1016)\n\n"
    full_content += "Este documento compila las 50 secciones de ingeniería generadas para el proyecto.\n\n---\n\n"
    
    for filename in files:
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            full_content += content + "\n\n<br>\n\n***\n\n<br>\n\n"

            
    # Convert mermaid blocks to mermaid.ink images for Pandoc compatibility
    def mermaid_to_img(match):
        code = match.group(1).strip()
        # Create JSON for mermaid.ink
        data = {
            "code": code,
            "mermaid": {"theme": "default"}
        }
        json_str = json.dumps(data)
        b64 = base64.urlsafe_b64encode(json_str.encode('utf-8')).decode('utf-8')
        return f"![Diagrama Mermaid](https://mermaid.ink/img/{b64})"

    # Regex to find mermaid blocks
    mermaid_pattern = re.compile(r'```mermaid\s*([\s\S]*?)\s*```', re.MULTILINE)
    final_content = mermaid_pattern.sub(mermaid_to_img, full_content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Documento consolidado creado en: {output_file}")
    return output_file

if __name__ == "__main__":
    merge_and_convert()
