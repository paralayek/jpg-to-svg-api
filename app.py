from flask import Flask, request, send_file
from PIL import Image
import numpy as np
from skimage import measure
import io

app = Flask(__name__)

@app.route('/api/jpg-to-svg', methods=['POST'])
def convert_to_svg():
    file = request.files['jpgFile']
    image = Image.open(file).convert('L').resize((512, 512))
    image_np = np.array(image)
    threshold = image_np > 128
    contours = measure.find_contours(threshold, 0.5)

    svg_data = '<?xml version="1.0" standalone="no"?>\n'
    svg_data += '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n'

    for contour in contours:
        path_data = "M " + " L ".join(f"{x:.2f} {y:.2f}" for y, x in contour)
        svg_data += f'<path d="{path_data}" stroke="black" fill="none"/>\n'

    svg_data += '</svg>'

    return send_file(io.BytesIO(svg_data.encode()), mimetype='image/svg+xml', as_attachment=True, download_name='converted.svg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
