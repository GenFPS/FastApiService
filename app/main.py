import io
import PyPDF2

from fastapi import FastAPI, UploadFile

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

if __name__ == '__main__':
    pass


