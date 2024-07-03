from .miniApp_classes.pdf import PdfTextReader
from .miniApp_classes.text_extracter import DataExtraction


def mini_app(pdf_filename: str) -> str | Exception:
    pdf = PdfTextReader(path_dir='uploaded_files/pdf_files', pdf_file=f'posted_{pdf_filename}')
    pdf_text = pdf.extract_text_from_pdf()

    data_extractor = DataExtraction(text=pdf_text)
    inn_kpp = data_extractor.inn_and_kpp_extract()
    return inn_kpp



