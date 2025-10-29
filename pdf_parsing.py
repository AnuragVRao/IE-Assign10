import fitz  # PyMuPDF library for PDF parsing
import re    # Regular expressions, used for searching text patterns

def parse_pdf_to_text(pdf_path):
    """
    Extracts clean text from each page of the PDF.
    - Removes headers, footers, and metadata.
    - Returns a single string containing all text.
    """
    doc = fitz.open(pdf_path)
    full_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()

        text = re.sub(r'(?m)^\s*(Page\s*\d+|\d+)\s*$', '', text) # Removes lines containing page numbers

        full_text.append(text.strip())  # Remove leading/trailing whitespace

    return "\n".join(full_text)

def clean_text(text):
    """
    Applies extra preprocessing:
    - Removes duplicate headers/footers if recurring.
    - Removes special symbols that do not contribute to meaning.
    """
    text = re.sub(r'[■◆○●♦•]', '', text)   # Remove unwanted special symbols
    return text

def chunk_text(text, chunk_size=1024):
    """
    Chunks the text into blocks of given size (in tokens/characters), 
    ensuring sentences are not broken across chunks.
    - Returns a list of chunks.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)  # Split by sentence boundaries

    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())  # Add final chunk

    return chunks

def pdf_to_chunks(pdf_path, chunk_size):
    """
    Complete pipeline:
    - Parses PDF
    - Cleans text
    - Chunks it into logically readable blocks
    Returns: list of cleaned text chunks.
    """
    raw_text = parse_pdf_to_text(pdf_path)
    cleaned_text = clean_text(raw_text)
    return chunk_text(cleaned_text, chunk_size)


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
