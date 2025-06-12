
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

# Initialize chatbot with OpenAI
chatbot = ChatBot(model_type='openai')

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
    Or multipart form data with optional image file(s)
    Returns JSON: {"response": "bot response"}
    """
    print(f"=== Received chat request ===")
    print(f"Request method: {request.method}")
    print(f"Content type: {request.content_type}")
    print(f"Is JSON: {request.is_json}")
    
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            user_message = data.get('message', '')
            image_paths = []
        else:
            user_message = request.form.get('message', '')
            image_paths = []
            
            # Handle image upload(s) if present
            if 'image' in request.files:
                files = request.files.getlist('image')
                for file in files:
                    if file and file.filename != '' and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        # Add timestamp to avoid conflicts
                        import time
                        filename = f"{int(time.time())}_{filename}"
                        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(image_path)
                        image_paths.append(image_path)
        
        if not user_message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        print(f"User message: {user_message}")
        print(f"Image paths: {image_paths}")
        print(f"Chatbot model type: {chatbot.model_type}")
        
        # Get chatbot response with image support
        response = chatbot.get_response(user_message, image_paths if image_paths else None)
        
        print(f"Bot response: {response[:100]}...")
        
        # Clean up uploaded images after processing (optional)
        # TODO: Decide retention policy for uploaded images
        # for image_path in image_paths:
        #     if os.path.exists(image_path):
        #         os.remove(image_path)
        
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy',
        'model_type': chatbot.model_type,
        'openrouter_configured': bool(os.getenv('OPENROUTER_API_KEY'))
    })

if __name__ == '__main__':
    # Use port 5000 as recommended for Replit
    app.run(host='0.0.0.0', port=5000, debug=True)
