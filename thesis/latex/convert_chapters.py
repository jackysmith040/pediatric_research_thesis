import subprocess
import os

PANDOC = r".\pandoc_bin2\pandoc-3.1.8\pandoc.exe"

def replace_unicode_box_drawing(text):
    text = text.replace('┌', '+').replace('─', '-').replace('┐', '+')
    text = text.replace('│', '|').replace('└', '+').replace('┘', '+')
    text = text.replace('├', '+').replace('┤', '+').replace('┬', '+')
    text = text.replace('┴', '+').replace('┼', '+')
    return text

def merge_and_convert(files, out_file, title):
    merged_md = ""
    # Add the main chapter title
    if title:
        merged_md += f"# {title}\n\n"
    
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            content = replace_unicode_box_drawing(content)
            # Downgrade headers by 1 level
            content = content.replace('\n# ', '\n## ')
            if content.startswith('# '):
                content = '## ' + content[2:]
            merged_md += content + "\n\n"
            
    # Write to a temp file
    temp_md = "temp.md"
    with open(temp_md, 'w', encoding='utf-8') as f:
        f.write(merged_md)
        
    # Convert using pandoc
    cmd = [PANDOC, temp_md, "-f", "markdown", "-t", "latex", "--top-level-division=chapter", "--no-highlight", "-o", out_file]
    subprocess.run(cmd)

merge_and_convert(["../02_LITERATURE_REVIEW.md"], "chapter2.tex", "Literature Review")
merge_and_convert(["../03_SYSTEM_ARCHITECTURE.md", "../04_COMPUTER_VISION_AND_DEEP_LEARNING.md", "../05_TRACKING_SCENE_ANALYSIS_AND_DEBOUNCING.md"], "chapter3.tex", "Methodology & System Architecture")
merge_and_convert(["../06_CLINICAL_MONITORING_AND_USER_INTERFACE.md", "../07_EXPERIMENTS_BENCHMARKS_AND_RESULTS.md"], "chapter4.tex", "Implementation, Experiments & Results")
merge_and_convert(["../08_ETHICAL_PRIVACY_AND_DEPLOYMENT.md", "../09_CONCLUSION_AND_FUTURE_WORK.md"], "chapter5.tex", "Conclusion & Future Work")
merge_and_convert(["../11_APPENDICES.md"], "appendix.tex", None)

print("Done")
