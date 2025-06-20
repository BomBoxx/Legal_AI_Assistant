import fitz  # PyMuPDF

def extract_pdf_text(file_path):
    doc = fitz.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text

def split_text_by_word(text, word):
    # Keep the split word as part of each chunk
    parts = text.split(word)
    realparts=[]
    for i in parts:
        realparts.append(word+i)
    return realparts

# Example usage
pdf_path = "testing.pdf"  # Replace with your actual PDF file
split_word = "Article"

text = extract_pdf_text(pdf_path)
sections = split_text_by_word(text, split_word)

# Print each section (optional)
print(sections)
