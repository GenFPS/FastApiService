import io
import json
import PyPDF2
import sys

from fastapi import FastAPI, UploadFile

sys.path.append(r'C:\Users\fedser\PycharmProjects\fastApi_test\app')
from models.models import ParsedData

app = FastAPI()


@app.get("/")
async def main():
    return {"main": "page"}


# Отправка текстового файла
@app.post("/upload_txt/")
async def upload_file(uploaded_file: UploadFile):
    content = await uploaded_file.read()
    # Получаем название текстового файла
    file_name = uploaded_file.filename
    with open(file=f'app/uploaded_files/txt_files/posted_{file_name}', mode='wb') as file:
        file.write(content)
    return {"filename": uploaded_file.filename,
            "content": content}


# отправка pdf файла
@app.post("/upload_pdf/")
async def upload_file(uploaded_file: UploadFile):
    # В переменной content содержится байт-код содержимого pdf (полученного через POST запросы)
    content = await uploaded_file.read()
    # Записываем файл (сохраняем содержимое файла)
    pdf_writer = PyPDF2.PdfWriter()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    # Проходимся по каждой странице и добавляем ее к pdf_writer
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])
    # Записываем полученное имя файла
    filename = uploaded_file.filename
    with open(f'app/uploaded_files/pdf_files/posted_{filename}', 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    return {'pdf_filename': uploaded_file.filename}


# Тестовая версия отправки данных в формате json
@app.post("/parsed_data/")
async def post_json(parsed_data: ParsedData):
    print(parsed_data)
    return parsed_data


# Тестовая версия получения данных в формате json
@app.get("/json_data/{json_file}")
async def get_json(json_file: str):
    with open(file=f'app/uploaded_files/json_files/{json_file}', mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return {
        "inn_kpp": data["inn_kpp"],
        "invoice": data["invoice"],
        "data_table": data["data_table"],
        "total_without_tax": data["total_without_tax"],
        "amount_of_tax":  data["amount_of_tax"],
        "total_amount": data["total_amount"]
    }


if __name__ == '__main__':
    pass


