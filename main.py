from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from services import process_pdf_to_html
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.post("/upload_resume", response_class=HTMLResponse)
async def upload_resume(file: UploadFile = File(...), api_key: str = Form(...)):
    if not api_key:
        return {"error": "OpenAI API key is required."}

    resume_html = await process_pdf_to_html(file, api_key)

    return templates.TemplateResponse(
        "resume_template.html", {"request": {}, "resume_html": resume_html}
    )


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume Generator</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f9;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    background-color: #fff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    max-width: 400px;
                    text-align: center;
                }
                h1 {
                    color: #333;
                    margin-bottom: 20px;
                }
                input[type="file"] {
                    margin-bottom: 15px;
                }
                label {
                    display: block;
                    margin-bottom: 10px;
                    font-weight: bold;
                    color: #555;
                }
                input[type="password"],
                input[type="file"] {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                input[type="submit"] {
                    background-color: #007bff;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
                .tooltip {
                    position: relative;
                    display: inline-block;
                    border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
                }

                /* Tooltip text */
                .tooltip .tooltiptext {
                    visibility: hidden;
                    width: 120px;
                    background-color: #555;
                    color: #fff;
                    text-align: center;
                    padding: 5px 0;
                    border-radius: 6px;

                    /* Position the tooltip text */
                    position: absolute;
                    z-index: 1;
                    bottom: 100%; /* Place the tooltip above the text */
                    left: 50%;
                    margin-left: -60px; /* Use half of the width to center the tooltip */

                    /* Fade in tooltip */
                    opacity: 0;
                    transition: opacity 0.3s;
                }

                /* Tooltip arrow */
                .tooltip .tooltiptext::after {
                    content: "";
                    position: absolute;
                    top: 100%; /* Below the tooltip */
                    left: 50%;
                    margin-left: -5px;
                    border-width: 5px;
                    border-style: solid;
                    border-color: #555 transparent transparent transparent;
                }

                /* Show the tooltip text when you mouse over the tooltip container */
                .tooltip:hover .tooltiptext {
                    visibility: visible;
                    opacity: 1;
}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Upload LinkedIn Resume</h1>
                <form action="/upload_resume" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required><br>
                    <label>Enter OpenAI API Key:</label>
                    <input type="password" name="api_key" required><br>
                    <div class="tooltip">Info
                        <span class="tooltiptext">Make sure the API key has enough credits. This website makes a call to GPT 3.5 Turbo.</span>
                    </div><br><br>
                    <input type="submit" value="Generate Resume">
                </form>
            </div>
        </body>
    </html>
    """
