import os
import re
from pathlib import Path

data_folder = Path("data")

input_dir = data_folder / "processed"
output_dir = data_folder / "lower"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def apply_proper_capitalization(text):
    """
    Convert all-caps text to proper capitalization for all 6 UN languages.
    Works for Latin-script (EN, FR, ES), Cyrillic (RU), Arabic (AR), and Chinese (ZH).
    """
    # Detect if this is Chinese text (if it contains Chinese characters, don't convert case)
    if re.search(r'[\u4e00-\u9fff]', text):
        # For Chinese, just clean up spacing and return as-is since Chinese doesn't have case
        return text
    
    # Detect if this is Arabic text
    if re.search(r'[\u0600-\u06ff]', text):
        # For Arabic, just clean up spacing and return as-is since Arabic doesn't have case
        return text
    
    # For Latin and Cyrillic scripts, convert to lowercase first
    text = text.lower()
    
    # Comprehensive proper nouns for all languages that use case
    proper_nouns = {
        # English
        "united nations", "security council", "general assembly", 
        "international court of justice", "economic and social council",
        "trusteeship council", "secretariat", "charter", "peoples",
        "member states", "secretary-general", "chapter", "article",
        "purposes", "principles", "we the peoples", "san francisco",
        
        # French
        "nations unies", "conseil de sécurité", "assemblée générale",
        "cour internationale de justice", "conseil économique et social",
        "conseil de tutelle", "secrétariat", "charte", "peuples",
        "états membres", "secrétaire général", "chapitre", "article",
        "buts", "principes", "nous peuples des nations unies",
        
        # Spanish
        "naciones unidas", "consejo de seguridad", "asamblea general",
        "corte internacional de justicia", "consejo económico y social",
        "consejo de administración fiduciaria", "secretaría", "carta",
        "pueblos", "estados miembros", "secretario general", "capítulo",
        "artículo", "propósitos", "principios", "nosotros los pueblos",
        
        # Russian
        "организация объединенных наций", "совет безопасности", 
        "генеральная ассамблея", "международный суд",
        "экономический и социальный совет", "совет по опеке",
        "секретариат", "устав", "народы", "государства-члены",
        "генеральный секретарь", "глава", "статья", "цели", "принципы",
        "мы народы объединенных наций"
    }
    
    # Apply proper noun capitalization
    for noun in proper_nouns:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(noun) + r'\b'
        # Capitalize each word in the proper noun
        capitalized = ' '.join(word.capitalize() for word in noun.split())
        text = re.sub(pattern, capitalized, text, flags=re.IGNORECASE)
    
    # Capitalize first letter of sentences and beginning of text
    # For Latin scripts (English, French, Spanish)
    text = re.sub(r'(^|[.!?]\s+)([a-zà-ÿ])', 
                  lambda m: m.group(1) + m.group(2).upper(), text, flags=re.UNICODE)
    
    # For Cyrillic script (Russian)
    text = re.sub(r'(^|[.!?]\s+)([а-я])', 
                  lambda m: m.group(1) + m.group(2).upper(), text, flags=re.UNICODE)
    
    # Special handling for common opening phrases in each language
    openings = [
        (r'^we\s+the\s+peoples\s+of\s+the\s+united\s+nations', 'We the peoples of the United Nations'),
        (r'^nous\s+peuples\s+des\s+nations\s+unies', 'Nous peuples des Nations Unies'),
        (r'^nosotros\s+los\s+pueblos\s+de\s+las\s+naciones\s+unidas', 'Nosotros los pueblos de las Naciones Unidas'),
        (r'^мы\s+народы\s+объединенных\s+наций', 'Мы народы Объединенных Наций'),
    ]
    
    for pattern, replacement in openings:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

# Iterate through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_dir, filename)
        output_filename = filename.replace("clean_", "lower_")
        output_path = os.path.join(output_dir, output_filename)

        # Read the content of the file
        with open(input_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Apply proper capitalization
        normalized_content = apply_proper_capitalization(content)

        # Write the normalized content to the output file
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(normalized_content)
        
        print(f"Processed {filename} -> {output_filename}")
