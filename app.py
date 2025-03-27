from flask import Flask, render_template, request, send_file, jsonify
import os
from svg_to_geojson import svg_to_geojson
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'svg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': '不支持的文件格式，请上传SVG文件'}), 400

    try:
        # 获取控制点参数
        x = float(request.form.get('control_x', '185.39'))
        y = float(request.form.get('control_y', '289.54'))
        lon = float(request.form.get('control_lon', '-117.716728'))
        lat = float(request.form.get('control_lat', '33.683458'))
        scale_x = float(request.form.get('scale_x', '0.0000163'))
        scale_y = float(request.form.get('scale_y', '-0.0000127'))

        control_point = (x, y, lon, lat)
        scale = (scale_x, scale_y)

        # 保存上传的文件
        filename = secure_filename(file.filename)
        svg_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(svg_path)

        # 生成输出文件名
        output_filename = os.path.splitext(filename)[0] + '.json'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # 转换文件
        svg_to_geojson(svg_path, output_path, control_point, scale)

        # 返回转换后的文件
        return send_file(output_path, as_attachment=True, download_name=output_filename)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
