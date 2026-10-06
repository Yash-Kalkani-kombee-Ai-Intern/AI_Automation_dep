from pdf_loader import load_pdf
from chunker import chunk_text


pdf_path = "../documents/restaurant_policy.pdf"

text = load_pdf(pdf_path)

chunks = chunk_text(text)

print(f"\nTotal characters: {len(text)}")
print(f"Total chunks: {len(chunks)}")

for index, chunk in enumerate(chunks[:5], start=1):
    print(f"\n========== CHUNK {index} ==========\n")
    print(chunk)