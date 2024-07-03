import PyPDF2


class PdfAnalyzer:
    def __init__(self, path_dir: str, pdf_file: str):
        self._path_dir = path_dir
        self._pdf_file = pdf_file
        self._full_path = f'{self._path_dir}/{self._pdf_file}'

    @property
    def full_path(self) -> str:
        return self._full_path

    def get_pages(self) -> int:
        pdf_file = open(self._full_path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        pdf_file.close()
        return num_pages


class PdfTextReader(PdfAnalyzer):
    # Наследуем метод __init__ из PdfAnalyzer
    def __init__(self, path_dir: str, pdf_file: str):
        super().__init__(path_dir, pdf_file)

    def extract_text_from_pdf(self) -> str:
        text = ''

        with open(self._full_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text
