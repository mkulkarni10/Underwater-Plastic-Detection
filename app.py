from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ✅ UPDATED MODEL VERSION
ROBOFLOW_API_KEY = 'i3HLHjjhvWCpehLbgiSW'
MODEL_ID = 'trash-detection-in-water-hp6yd'
MODEL_VERSION = '2'  # Updated to version 2

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.json
        image_base64 = data.get('imageBase64')
        confidence = float(data.get('confidence', 40))

        if not image_base64:
            return jsonify({'error': 'No image provided'}), 400

        url = f"https://detect.roboflow.com/{MODEL_ID}/{MODEL_VERSION}"

        import base64
        image_bytes = base64.b64decode(image_base64)

        headers = {
            "Content-Type": "multipart/form-data"
        }

        response = requests.post(
            url,
            params={
                "api_key": ROBOFLOW_API_KEY,
                "confidence": confidence / 100
            },
            files={
                "file": ("image.jpg", image_bytes, "image/jpeg")
            }
        )

        print("📡 Roboflow Status:", response.status_code)
        print("📨 Roboflow Response:", response.text)

        if response.status_code != 200:
            return jsonify({
                'error': 'Roboflow error',
                'details': response.text
            }), 500

        return jsonify(response.json())

    except Exception as e:
        print("💥 Exception:", str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    return jsonify({
        "status": "running",
        "model": MODEL_ID,
        "version": MODEL_VERSION
    })


if __name__ == '__main__':
    print("🌊 AquaVision AI Backend Running")
    print("Model:", MODEL_ID, "Version:", MODEL_VERSION)
    app.run(debug=True, port=5000)