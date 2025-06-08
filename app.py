from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
from vectorizer import Vectorizer
import os

app = FastAPI()

@app.post("/api/jpg-to-svg")
async def convert(file: UploadFile = File(...)):
    input_path = "input.jpg"
    output_path = "output.svg"

    # Save uploaded image
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Open and convert to grayscale
    img = Image.open(input_path).convert("L")

    # Convert to SVG
    v = Vectorizer(img)
    svg = v.get_svg()

    with open(output_path, "w") as f:
        f.write(svg)

    return FileResponse(output_path, media_type="image/svg+xml", filename="converted.svg")
