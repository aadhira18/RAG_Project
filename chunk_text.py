
import re
from extract_text import extract_pdf_text


CHUNK_SIZE = 3
OVERLAP = 1


def split_into_chunks(pages):
    sentences = []

    # Split each page separately and retain its page number
    for page in pages:
        page_sentences = re.split(
            r"(?<=[.!?])\s+",
            page["text"]
        )

        for sentence in page_sentences:
            sentence = sentence.strip()

            if sentence:
                sentences.append({
                    "text": sentence,
                    "page_number": page["page_number"]
                })

    chunks = []
    step = CHUNK_SIZE - OVERLAP

    if CHUNK_SIZE <= 0 or OVERLAP < 0 or OVERLAP >= CHUNK_SIZE:
        raise ValueError("Require CHUNK_SIZE > OVERLAP >= 0")

    for start in range(0, len(sentences), step):
        selected = sentences[start:start + CHUNK_SIZE]

        chunk_text = " ".join(
            sentence["text"] for sentence in selected
        )

        chunks.append({
            "chunk_id": len(chunks),
            "text": chunk_text,
            "page_number": selected[0]["page_number"]
        })

    return chunks


if __name__ == "__main__":
    pages = extract_pdf_text()
    chunks = split_into_chunks(pages)

    print("Total sentences:", sum(
        len(re.split(r"(?<=[.!?])\s+", page["text"]))
        for page in pages
    ))
    print("Total chunks:", len(chunks))

    for chunk in chunks[:5]:
        print("\n" + "=" * 60)
        print("CHUNK", chunk["chunk_id"] + 1)
        print("Page:", chunk["page_number"])
        print(chunk["text"])
