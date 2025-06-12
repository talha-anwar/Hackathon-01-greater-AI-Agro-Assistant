
class ChatBot {
    constructor() {
        this.chatForm = document.getElementById('chatForm');
        this.messageInput = document.getElementById('messageInput');
        this.imageInput = document.getElementById('imageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.imagePreview = document.getElementById('imagePreview');
        this.previewImg = document.getElementById('previewImg');
        this.removeImageBtn = document.getElementById('removeImage');
        this.loadingIndicator = document.getElementById('loadingIndicator');
        
        this.selectedImage = null;
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Image upload
        this.imageInput.addEventListener('change', (e) => this.handleImageSelect(e));
        
        // Remove image
        this.removeImageBtn.addEventListener('click', () => this.removeImage());
        
        // Enter key to send message
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.chatForm.dispatchEvent(new Event('submit'));
            }
        });
        
        // Auto-resize input (if needed)
        this.messageInput.addEventListener('input', () => this.autoResizeInput());
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
            this.removeImage();
            this.messageInput.focus();
        }
    }
    
    handleImageSelect(event) {
        const file = event.target.files[0];
        if (file) {
            // Validate file type
            if (!file.type.startsWith('image/')) {
                alert('Please select an image file.');
                return;
            }
            
            // Validate file size (16MB limit)
            if (file.size > 16 * 1024 * 1024) {
                alert('Image size must be less than 16MB.');
                return;
            }
            
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
    
    addMessage(content, sender, imageFile = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Add sender label and content
        const senderLabel = sender === 'user' ? 'You' : 'Bot';
        messageContent.innerHTML = `<strong>${senderLabel}:</strong> ${this.escapeHtml(content)}`;
        
        // Add image if present (for user messages)
        if (imageFile && sender === 'user') {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.className = 'message-image';
                img.alt = 'Uploaded image';
                messageContent.appendChild(img);
            };
            reader.readAsDataURL(imageFile);
        }
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();
        
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(messageTime);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    setLoading(isLoading) {
        this.sendButton.disabled = isLoading;
        this.messageInput.disabled = isLoading;
        this.imageInput.disabled = isLoading;
        
        if (isLoading) {
            this.loadingIndicator.style.display = 'flex';
            this.sendButton.textContent = 'Sending...';
        } else {
            this.loadingIndicator.style.display = 'none';
            this.sendButton.textContent = 'Send';
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    getCurrentTime() {
        return new Date().toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    autoResizeInput() {
        // Optional: Auto-resize textarea if you convert input to textarea
        // this.messageInput.style.height = 'auto';
        // this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
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
