
# AI Chatbot Web Application

A modular Flask-based chatbot website with support for text and image inputs. Built with scalability in mind to easily switch between different AI models.

## Features

- 🤖 **Modular Chatbot Logic**: Easy to switch between rule-based, OpenAI, or local models
- 💬 **Clean Chat Interface**: Responsive design with real-time messaging
- 📷 **Image Upload Support**: Frontend and backend ready for image processing
- 🌐 **CORS Enabled**: Ready for mobile app integration
- 🚀 **Deployment Ready**: Configured for Replit hosting

## Project Structure

```
├── app.py                 # Main Flask application
├── chatbot.py            # Modular chatbot logic
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Chat interface
├── static/
│   ├── style.css        # Styling
│   └── script.js        # Frontend JavaScript
└── temp_uploads/        # Temporary image storage
```

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Chat**: Open your browser to `http://localhost:5000`

## Deployment on Replit

### Automatic Deployment
1. Fork this repl or upload the files
2. Click the "Run" button to start the application
3. Your app will be available at your repl's URL

### Manual Configuration
The app is configured to run on port 5000, which Replit automatically forwards to ports 80 and 443 for public access.

### Environment Variables (Optional)
If you plan to use external APIs:
- Go to Secrets tab in Replit
- Add your API keys (e.g., `OPENAI_API_KEY`)

## Extending the Chatbot

### Adding OpenAI Integration
1. Uncomment OpenAI dependencies in `requirements.txt`
2. Set your API key in Replit Secrets
3. Modify `chatbot.py` to implement `_get_openai_response()`

### Adding Local Models
1. Uncomment transformers dependencies in `requirements.txt`
2. Implement `_get_local_response()` in `chatbot.py`
3. Consider model size limitations on free hosting

### Adding Image Processing
1. Uncomment Pillow/OpenCV in `requirements.txt`
2. Implement image analysis in `chatbot.py`
3. Update `get_response()` to handle image data

## API Endpoints

- `GET /`: Main chat interface
- `POST /chat`: Send message and get response
  - Accepts JSON: `{"message": "text"}`
  - Or form data with optional image file
  - Returns: `{"response": "bot response"}`
- `GET /health`: Health check endpoint

## Mobile App Integration

The API is CORS-enabled and ready for mobile app integration. Use the `/chat` endpoint with POST requests.

Example Android/iOS integration:
```javascript
fetch('https://your-repl-url.replit.app/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Hello chatbot!'
  })
})
```

## Free AI Model Options

- **Rule-based**: Current implementation (no API costs)
- **HuggingFace Inference API**: Free tier available for many models
- **Cohere**: Free tier with API limits
- **AI21 Labs**: Free tier available
- **Local Models**: Run on your server (resource intensive)

## TODO

- [ ] Implement image processing logic
- [ ] Add conversation memory/context
- [ ] Implement user sessions
- [ ] Add more sophisticated NLP
- [ ] Optimize for mobile performance
- [ ] Add typing indicators
- [ ] Implement message persistence

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
