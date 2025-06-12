
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from chatbot import ChatBot

app = Flask(__name__)
CORS(app)  # Enable CORS for Android app integration

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'temp_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize chatbot
chatbot = ChatBot()

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    API endpoint for chat messages
    Accepts JSON: {"message": "user message"}
    Or multipart form data with optional image file
    Returns JSON: {"response": "bot response"}
    """
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            user_message = data.get('message', '')
            image_path = None
        else:
            user_message = request.form.get('message', '')
            image_path = None
            
            # Handle image upload if present
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid conflicts
                    import time
                    filename = f"{int(time.time())}_{filename}"
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(image_path)
        
        if not user_message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get chatbot response
        response = chatbot.get_response(user_message, image_path)
        
        # Clean up uploaded image (optional - you might want to keep them)
        if image_path and os.path.exists(image_path):
            # TODO: Decide if you want to keep images or delete them immediately
            pass  # os.remove(image_path)
        
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint for deployment"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Use port 5000 as recommended for Replit
    app.run(host='0.0.0.0', port=5000, debug=True)
