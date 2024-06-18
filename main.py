from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from script import XlsReader

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
def mainpage():
    return FileResponse('static/index.html')


@app.post('/uploadfile/')
async def upload_file(file: UploadFile, col_num: int = Form(...), page_num: int = Form(...)):
    content = await file.read()
    try:
        reader = XlsReader(file=content, col_num=col_num, page_num=page_num)
        new_file = reader.read_file()
    except Exception as e:
        return JSONResponse({
            'error': str(e),
            'solution': 'Вероятно, вы пытаетесь обработать не буквенные строки'
        })
    return StreamingResponse(new_file, media_type='application/vnd.ms-excel')
