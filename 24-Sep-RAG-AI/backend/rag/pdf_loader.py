from pathlib import Path
from pypdf import PdfReader


def load_pdf(pdf_path: str) -> str:
    """
    Read a PDF and return all extracted text.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(path)

    pages_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages_text.append(text)

    return "\n".join(pages_text)


if __name__ == "__main__":
    pdf_path = "../documents/restaurant_policy.pdf"

    text = load_pdf(pdf_path)

    print("\n========== PDF TEXT ==========\n")
    print(text)
    print("\n========== END ==========\n")