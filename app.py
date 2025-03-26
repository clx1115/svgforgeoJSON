from flask import Flask, request, render_template, send_file, jsonify
import os
from svg_to_geojson import convert_svg_to_geojson
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.svg'):
        return jsonify({'error': 'File must be SVG'}), 400

    # Save the uploaded SVG file
    svg_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(svg_path)
    
    # Convert SVG to GeoJSON
    try:
        geojson_data = convert_svg_to_geojson(svg_path)
        return jsonify(geojson_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8881)
