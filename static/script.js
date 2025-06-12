class ChatBot {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.chatMessages = document.getElementById('chatMessages');
        this.chatForm = document.getElementById('chatForm');
        this.sendButton = document.getElementById('sendButton');
        this.imageInput = document.getElementById('imageInput');
        this.imagePreview = document.getElementById('imagePreview');
        this.previewImg = document.getElementById('previewImg');
        this.removeImageBtn = document.getElementById('removeImage');
        this.loadingIndicator = document.getElementById('loadingIndicator');

        this.selectedImage = null;

        this.init();
    }

    init() {
        // Bind event listeners
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        this.imageInput.addEventListener('change', (e) => this.handleImageSelect(e));
        this.removeImageBtn.addEventListener('click', () => this.removeImage());

        // Enable enter key to send message
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.chatForm.dispatchEvent(new Event('submit'));
            }
        });
    }

    handleImageSelect(event) {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            this.selectedImage = file;

            // Show preview
            const reader = new FileReader();
            reader.onload = (e) => {
                this.previewImg.src = e.target.result;
                this.imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    }

    removeImage() {
        this.selectedImage = null;
        this.imageInput.value = '';
        this.imagePreview.style.display = 'none';
        this.previewImg.src = '';
    }

    addMessage(message, sender, imageFile = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';

        // Add image if present
        if (imageFile && sender === 'user') {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(imageFile);
            img.style.maxWidth = '200px';
            img.style.borderRadius = '8px';
            img.style.marginBottom = '8px';
            img.style.display = 'block';
            messageContent.appendChild(img);
        }

        // Add text content
        const textContent = document.createElement('div');
        textContent.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Bot'}:</strong> ${message}`;
        messageContent.appendChild(textContent);

        // Add timestamp
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString();

        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(messageTime);

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();

        // Clear image after adding user message
        if (sender === 'user' && imageFile) {
            this.removeImage();
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    setLoading(loading) {
        this.sendButton.disabled = loading;
        this.sendButton.textContent = loading ? 'Sending...' : 'Send';

        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = loading ? 'block' : 'none';
        }
    }

    async handleSubmit(event) {
        event.preventDefault();

        const message = this.messageInput.value.trim();
        if (!message && !this.selectedImage) {
            return;
        }

        // Add user message to chat
        this.addMessage(message, 'user', this.selectedImage);

        // Clear input and disable form
        this.messageInput.value = '';
        this.setLoading(true);

        try {
            // Prepare form data
            const formData = new FormData();
            formData.append('message', message);

            if (this.selectedImage) {
                formData.append('image', this.selectedImage);
            }

            // Send to backend
            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            // Add bot response to chat
            this.addMessage(data.response, 'bot');

        } catch (error) {
            console.error('Error:', error);
            this.addMessage(
                'Sorry, I encountered an error. Please try again.',
                'bot'
            );
        } finally {
            this.setLoading(false);
        }
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatBot();
});

// Service Worker registration for PWA (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}