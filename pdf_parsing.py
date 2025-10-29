import fitz  # PyMuPDF library for PDF parsing
import re    # Regular expressions, used for searching text patterns

def parse_pdf_to_text(pdf_path):                                    # Extracts clean text from each page of the PDF.

    doc = fitz.open(pdf_path)
    full_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()

        text = re.sub(r'(?m)^\s*(Page\s*\d+|\d+)\s*$', '', text)    # Removes headers/footers and lines having page numbers 

        full_text.append(text.strip())                              # Remove leading/trailing whitespace

    return "\n".join(full_text)                                     # Returns a single string containing all text.

def clean_text(text):                   # Removes duplicate headers & unwanted special symbols

    text = re.sub(r'[■◆○●♦•]', '', text)
    return text

def chunk_text(text, chunk_size=1024):                  # Chunks the text into blocks of given token size

    sentences = re.split(r'(?<=[.!?]) +', text)         # Split by sentence boundaries ( Para -> sentences )

    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())            # Add final chunk

    return chunks

def pdf_to_chunks(pdf_path, chunk_size):

    raw_text = parse_pdf_to_text(pdf_path)          # Parses pdf
    cleaned_text = clean_text(raw_text)             # Cleans text
    return chunk_text(cleaned_text, chunk_size)     # Returns readable text chunks


def main():
    pdf_path = "sample-pdf.pdf"
    chunk_size = 1024
    chunks = pdf_to_chunks(pdf_path, chunk_size)
    
    for i, chunk in enumerate(chunks, 1):
        print(f"--- Chunk {i} ---")
        print(chunk)
        print()
if __name__ == "__main__":
    main()
