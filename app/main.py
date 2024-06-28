import io
import PyPDF2

from fastapi import FastAPI, UploadFile

app = FastAPI()


# Отправка текстовых файлов
@app.post("/upload_text/")
async def upload_file(uploaded_file: UploadFile):
    content = await uploaded_file.read()
    print(content)

    with open(r'uploaded_files/test.txt', 'wb') as file:
        file.write(content)

    return {"filename": uploaded_file.filename,
            "content": content}


# отправка pdf файлов
@app.post("/upload_pdf/")
async def upload_file(uploaded_file: UploadFile):
    content = await uploaded_file.read()

    pdf_writer = PyPDF2.PdfWriter()
    pdf_writer.add_page(PyPDF2.PdfReader(io.BytesIO(content)).pages[0])

    with open('uploaded_files/test.pdf', 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    return {'pdf_filename': uploaded_file.filename}

if __name__ == '__main__':
    pass


