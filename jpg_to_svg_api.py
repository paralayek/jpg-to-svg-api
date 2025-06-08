from flask import Flask, request, send_file
from PIL import Image
import numpy as np
import cv2
import potrace
import io

app = Flask(__name__)

@app.route('/api/jpg-to-svg', methods=['POST'])
def convert_jpg_to_svg():
    file = request.files['jpgFile']
    img = Image.open(file).convert("L")
    img = img.resize((512, 512))
    bitmap = np.array(img)
    _, bitmap = cv2.threshold(bitmap, 127, 255, cv2.THRESH_BINARY)

    bmp = potrace.Bitmap(bitmap)
    path = bmp.trace()

    output = io.StringIO()
    output.write('<?xml version="1.0" standalone="no"?>\n')
    output.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.0">\n')

    for curve in path:
        output.write('<path d="')
        for segment in curve:
            if segment.is_corner:
                output.write(f'M {segment.c[1][0]} {segment.c[1][1]} ')
            else:
                c = segment.c
                output.write(f'C {c[0][0]} {c[0][1]}, {c[1][0]} {c[1][1]}, {c[2][0]} {c[2][1]} ')
        output.write('Z" fill="black"/>\n')
    output.write('</svg>\n')

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='image/svg+xml', as_attachment=True, download_name='converted.svg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
