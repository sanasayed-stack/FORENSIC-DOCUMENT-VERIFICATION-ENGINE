from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from explainability import ExplainabilityLayer
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============ ROUTES ============

@app.route('/', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'message': 'Document Forgery Detection API running'})

@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    """
    Main endpoint to analyze document
    Expects: multipart/form-data with 'file' field
    Returns: JSON with detection results
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: JPG, PNG, PDF'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"File saved: {filepath}")
        
        # Run detection
        print("Running detection...")
        from detector import analyze_document as detect_forgery
        detection_results = detect_forgery(filepath)
        
        # Generate heatmap
        print("Generating heatmap...")
        explainer = ExplainabilityLayer(filepath)
        heatmap_path = os.path.join(app.config['UPLOAD_FOLDER'], 'heatmap.jpg')
        explainer.generate_heatmap(detection_results, heatmap_path)
        
        # Prepare response
        response = {
            'success': True,
            'verdict': detection_results.get('verdict', 'Unknown'),
            'confidence': detection_results.get('confidence', 0),
            'level': 'HIGH' if detection_results.get('verdict') == 'Forged' else 'LOW',
            'heatmap_url': '/api/heatmap/heatmap.jpg',
            'pixel_analysis': {
                'ela_detection': detection_results.get('confidence', 0),
                'compression_artifacts': 0,
                'font_inconsistency': 0
            },
            'text_integrity': {},
            'rule_based_score': {
                'total_points': 0,
                'max_points': 100
            },
            'all_flags': [
                {
                    'type': 'ELA/Metadata',
                    'description': flag,
                    'severity': 'HIGH',
                    'points': 10,
                    'details': flag
                }
                for flag in detection_results.get('all_flags', [])
            ]
        }
        
        print(f"Analysis complete: {response['verdict']}")
        return jsonify(response)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/heatmap/<filename>', methods=['GET'])
def get_heatmap(filename):
    """Serve heatmap image"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except:
        return jsonify({'error': 'Heatmap not found'}), 404

@app.route('/index.html', methods=['GET'])
def serve_html():
    """Serve the HTML frontend"""
    try:
        return send_from_directory('.', 'index.html')
    except:
        return jsonify({'error': 'HTML file not found'}), 404

if __name__ == '__main__':
    print("🚀 Starting Flask API...")
    print("Server running at http://localhost:5000")
    print("Open in browser: http://localhost:5000/index.html")
    app.run(debug=True, host='0.0.0.0', port=5000)