# ThinkRoot x Vortex'26 - Forensic Document Verification Engine

🚀 **AI-powered neural document forensics system for detecting forged documents**

## Features
✅ Pixel Analysis (ELA detection, compression artifacts)
✅ Text Integrity Checking (character spacing, font analysis)
✅ Rule-Based Scoring System
✅ Real-time Heatmap Visualization
✅ Regional Language Support (Hindi, Urdu, etc.)

## Tech Stack
- **Frontend:** HTML5, CSS3, Tailwind CSS, JavaScript
- **Backend:** Flask, Python
- **Detection:** OpenCV, NumPy, Custom ML Models
- **Visualization:** Explainability Layer with heatmaps

## Installation

### Prerequisites
```bash
pip install flask flask-cors opencv-python numpy werkzeug
```

### Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ThinkRoot-Vortex-26.git
cd ThinkRoot-Vortex-26

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

### Access
Open your browser: **http://localhost:5000/index.html**

## How It Works

1. **Upload Document** → PDF, PNG, or JPG format
2. **Analysis** → System runs pixel + text analysis
3. **Detection** → Identifies forgery indicators
4. **Verdict** → GREEN (Authentic) or RED (Forged)
5. **Confidence** → Shows how sure the system is

## Results Interpretation

### 🟢 CLEAN (Authentic)
- No major anomalies detected
- Low forgery confidence
- Document appears genuine

### 🔴 FORGED (Suspicious)
- Anomalies found in pixels/text
- High forgery confidence  
- Heatmap shows suspicious areas

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| POST | `/api/analyze` | Analyze document |
| GET | `/api/heatmap/<filename>` | Get heatmap image |

## Project Structure