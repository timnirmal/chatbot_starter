from pypdf import PdfReader


def read_local_pdf(file_path):
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    print(number_of_pages)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    # print(text)
    return text
