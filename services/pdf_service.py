import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def sliding_window_chunking(text, window_size, overlap_size):
    tokens = text.split()
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + window_size
        chunks.append(" ".join(tokens[start:end]))
        start += window_size - overlap_size
    return chunks
