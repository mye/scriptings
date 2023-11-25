from io import BytesIO

import pypdfium2 as pdfium

PDFIUM_ZERO_WIDTH_NO_BREAK_SPACE = "\ufffe"


def postprocess(extracted_texts: list[str], page_labels: list[str]) -> str:
    """Pass a list of all extracted texts from all pages."""
    extracted_texts = [replace_ligatures(t) for t in extracted_texts]
    extracted_texts = [remove_hyphens(t) for t in extracted_texts]
    extracted_texts = remove_footer(extracted_texts, page_labels)
    return "\n".join(extracted_texts)


def replace_ligatures(text: str) -> str:
    ligatures_dict = {
        "ﬀ": "ff",
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "ft",
        "ﬆ": "st",
        # "Ꜳ": "AA",
        # "Æ": "AE",
        "ꜳ": "aa",
    }
    for search, replace in ligatures_dict.items():
        text = text.replace(search, replace)
    return text


def remove_hyphens(text: str) -> str:
    lines = [line.rstrip() for line in text.split("\n")]

    # Find dashes
    line_numbers = []
    for line_no, line in enumerate(lines[:-1]):
        if line.endswith("-") or line.endswith(PDFIUM_ZERO_WIDTH_NO_BREAK_SPACE):
            line_numbers.append(line_no)

    # Replace
    for line_no in line_numbers:
        lines = dehyphenate(lines, line_no)

    return "\n".join(lines)


def dehyphenate(lines: list[str], line_no: int) -> list[str]:
    next_line = lines[line_no + 1]
    word_suffix = next_line.split(" ")[0]

    lines[line_no] = lines[line_no][:-1] + word_suffix
    lines[line_no + 1] = lines[line_no + 1][len(word_suffix) :]
    return lines


def remove_footer(extracted_texts: list[str], page_labels: list[str]):
    def remove_page_labels(extracted_texts, page_labels):
        processed = []
        for text, label in zip(extracted_texts, page_labels):
            text_left = text.lstrip()
            if text_left.startswith(label):
                text = text_left[len(label) :]

            text_right = text.rstrip()
            if text_right.endswith(label):
                text = text_right[: -len(label)]

            processed.append(text)
        return processed

    extracted_texts = remove_page_labels(extracted_texts, page_labels)
    return extracted_texts


def pdfium_new_line_after_hyphens(text):
    return text.replace(
        PDFIUM_ZERO_WIDTH_NO_BREAK_SPACE, PDFIUM_ZERO_WIDTH_NO_BREAK_SPACE + "\n"
    )


def pdfium_get_text(data: bytes) -> str:
    texts = []
    page_labels = []
    pdf = pdfium.PdfDocument(data)

    for i in range(len(pdf)):
        if not (label := pdf.get_page_label(i)):
            label = str(i + 1)
        page_labels.append(label)
        page = pdf.get_page(i)
        textpage = page.get_textpage()
        texts.append(pdfium_new_line_after_hyphens(textpage.get_text_range()))
    text = postprocess(texts, page_labels)
    return text


def pdfium_image_extraction(data: bytes) -> list[tuple[str, bytes]]:
    images = []
    try:
        pdf = pdfium.PdfDocument(data)
        for i in range(len(pdf)):
            page = pdf.get_page(i)
            index = 1
            for obj in page.get_objects():
                if isinstance(obj, pdfium.PdfImage):
                    img = BytesIO()
                    obj.extract(img)
                    images.append((f"page-{i+1}-image-{index}.jpg", img.getvalue()))
                    index += 1
    except Exception as exc:
        print(f"pdfium Image extraction failure: {exc}")
    return images


with open("algometa.pdf", "rb") as f:
    data = f.read()
    text = pdfium_get_text(data)
    print(text)
