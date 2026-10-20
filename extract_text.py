
import pymupdf

PDF_PATH = "documents/Complete_Revision_Notes_OS_CN_DBMS.pdf"


def extract_pdf_text(pdf_path=PDF_PATH):
    pages = []

    with pymupdf.open(pdf_path) as pdf:
        print("Number of pages:", len(pdf))

        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page_number": page_number,
                    "text": text
                })

    print("Total characters:", sum(len(p["text"]) for p in pages))

    return pages


if __name__ == "__main__":
    extracted_pages = extract_pdf_text()
    print("Pages with extracted text:", len(extracted_pages))
