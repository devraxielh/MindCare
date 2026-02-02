import os

def merge_original():
    docs_dir = "/Users/raxielh/Desktop/MentalHealth/mental_health_project/documentation/ieee_sdd/"
    output_file = os.path.join(docs_dir, "MindCare_IEEE_SDD_Original.md")
    
    files = sorted([f for f in os.listdir(docs_dir) if f.endswith(".md") and f[0].isdigit()])
    
    full_content = """# MindCare - Software Design Description (IEEE 1016)

**Autores:** Grupo Sócrates (Rodrigo García, Samir Castaño, Mario Macea)  
**Institución:** Universidad de Córdoba, Departamento de Ingeniería de Sistemas  
---

"""
    
    for filename in files:
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            full_content += content + "\n\n***\n\n"
            
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"Documento consolidado (Original) creado en: {output_file}")
    return output_file

if __name__ == "__main__":
    merge_original()
