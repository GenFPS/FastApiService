import io
import PyPDF2

from fastapi import APIRouter, UploadFile

from app.miniApp_recognizer import mini_app

pdf_service = APIRouter()


@pdf_service.get("/")
async def router_main():
    return {"router": "pdfService_route"}


@pdf_service.post("/upload_pdf/", status_code=201)
async def upload_file(uploaded_file: UploadFile):
    # � ���������� content ���������� ����-��� ����������� pdf (����������� ����� POST �������)
    content = await uploaded_file.read()
    # ���������� ���� (��������� ���������� �����)
    pdf_writer = PyPDF2.PdfWriter()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    # ���������� �� ������ �������� � ��������� �� � pdf_writer
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])
    # ���������� ���������� ��� �����
    file_name: str = uploaded_file.filename
    with open(f'uploaded_files/pdf_files/posted_{file_name}', 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    # �������� ����-���������� miniApp_recognizer
    data: str = mini_app.mini_app(pdf_filename=file_name)

    return {"pdf_filename": file_name,
            r"inn/kpp": data}
