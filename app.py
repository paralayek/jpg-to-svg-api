@app.post("/api/jpg-to-svg")
async def convert(file: UploadFile = File(...)):
    try:
        print("📥 Received file:", file.filename)

        input_path = "input.jpg"
        output_path = "output.svg"

        # Save uploaded file
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Convert image to grayscale
        from PIL import Image
        image = Image.open(input_path).convert("L")
        image.save("temp.pbm")

        # Generate SVG
        import svgtrace
        svg = svgtrace.trace("temp.pbm")

        with open(output_path, "w") as f:
            f.write(svg)

        print("✅ Conversion complete")
        return FileResponse(output_path, media_type="image/svg+xml", filename="converted.svg")

    except Exception as e:
        print("❌ Error:", str(e))
        return {"error": str(e)}
