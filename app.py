from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
import svgtrace

app = FastAPI()

@app.post("/api/jpg-to-svg")
async def convert(file: UploadFile = File(...)):
    input_path = "input.jpg"
    output_path = "output.svg"

    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Open image and convert to grayscale
    image = Image.open(input_path).convert("L")
    image.save("temp.pbm")  # Save as PBM for svgtrace

    # Trace to SVG
    svg = svgtrace.trace("temp.pbm")

    # Save the SVG content
    with open(output_path, "w") as f:
        f.write(svg)

    return FileResponse(output_path, media_type="image/svg+xml", filename="converted.svg")
