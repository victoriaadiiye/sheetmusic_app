from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from tab_creation.converter import convert

app = FastAPI(title="Tab Creation API")

UPLOAD_DIR = Path("/tmp/uploads")
OUTPUT_DIR = Path("/tmp/output")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>Tab Creation</title></head>
        <body>
            <h1>Upload a Music File to Generate PDF Tab</h1>
            <form action="/convert_form" enctype="multipart/form-data" method="post">
                <input name="file" type="file" required>
                <label>Tuning:</label>
                <select name="tuning">
                    <option value="standard">Standard</option>
                    <option value="drop-d">Drop D</option>
                    <option value="open-g">Open G</option>
                    <option value="dadgad">DADGAD</option>
                    <option value="guitar-cello-tuning">Guitar-Cello Tuning</option>
                    <option value="bouzouki">Bouzouki</option>
                </select>
                <label>Transpose:</label>
                <input type="checkbox" name="transpose" checked>
                <button type="submit">Convert</button>
            </form>
        </body>
    </html>
    """


@app.post("/convert_form", response_class=HTMLResponse)
async def convert_form(
    file: UploadFile, tuning: str = Form("standard"), transpose: bool = Form(False)
):
    transpose = transpose if transpose is not None else False
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    pdf_path = convert(
        file_path=str(file_path),
        tuning_arg=tuning,
        transpose=transpose,
        output_dir=str(OUTPUT_DIR),
    )

    return f"""
    <html>
        <body>
            <h2>PDF Generated!</h2>
            <p><a href="/download/{Path(pdf_path).name}">Download PDF</a></p>
            <p><a href="/">Back</a></p>
        </body>
    </html>
    """


@app.get("/download/{filename}")
async def download(filename: str):
    file_path = OUTPUT_DIR / filename
    if file_path.exists():
        return FileResponse(file_path, media_type="application/pdf", filename=filename)
    return HTMLResponse("File not found", status_code=404)
