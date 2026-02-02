import os

def clean_html():
    html_file = "/Users/raxielh/Desktop/MentalHealth/mental_health_project/documentation/ieee_sdd/MindCare_IEEE_SDD_Full.html"
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace <pre class="mermaid"><code>...</code></pre> with <pre class="mermaid">...</pre>
    # Pandoc usually escapes HTML inside <code>, so we might need to unescape.
    # But for a simpler approach, let's just use a script in the HTML to handle it.
    
    # Adding a script to the end of body to clean mermaid blocks
    cleanup_script = """
<script>
  document.querySelectorAll('pre.mermaid').forEach(pre => {
    const code = pre.querySelector('code');
    if (code) {
      pre.textContent = code.textContent;
    }
  });
</script>
</body>
"""
    new_content = content.replace("</body>", cleanup_script)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("HTML limpiado para Mermaid.")

if __name__ == "__main__":
    clean_html()
