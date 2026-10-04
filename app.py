import fitz

pdf_path = "documents/Complete_Revision_Notes_OS_CN_DBMS.pdf"

pdf = fitz.open(pdf_path)

print("Number of pages:", len(pdf))

for page_number, page in enumerate(pdf):
    text = page.get_text()

    print("\n" + "=" * 60)
    print("PAGE", page_number + 1)
    print("=" * 60)

    print(text[:1000])

pdf.close()