
class AgriAssistant {
    constructor() {
        this.homepage = document.getElementById('homepage');
        this.chatInterface = document.getElementById('chatInterface');
        this.startDiagnosisBtn = document.getElementById('startDiagnosis');
        this.backButton = document.getElementById('backButton');
        
        this.chatMessages = document.getElementById('chatMessages');
        this.chatForm = document.getElementById('chatForm');
        this.messageInput = document.getElementById('messageInput');
        this.imageInput = document.getElementById('imageInput');
        this.imagePreview = document.getElementById('imagePreview');
        this.previewImg = document.getElementById('previewImg');
        this.removeImageBtn = document.getElementById('removeImage');
        this.sendButton = document.getElementById('sendButton');
        this.loadingIndicator = document.getElementById('loadingIndicator');

        this.setupEventListeners();
    }

    setupEventListeners() {
        // Navigation
        this.startDiagnosisBtn.addEventListener('click', () => this.showChatInterface());
        this.backButton.addEventListener('click', () => this.showHomepage());
        
        // Chat functionality
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        this.imageInput.addEventListener('change', (e) => this.handleImageSelect(e));
        this.removeImageBtn.addEventListener('click', () => this.removeImage());

        // Auto-resize input
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });
    }

    showChatInterface() {
        this.homepage.style.display = 'none';
        this.chatInterface.style.display = 'block';
        this.messageInput.focus();
    }

    showHomepage() {
        this.chatInterface.style.display = 'none';
        this.homepage.style.display = 'block';
        // Clear chat if needed
        this.messageInput.value = '';
        this.removeImage();
    }

    handleImageSelect(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                this.previewImg.src = e.target.result;
                this.imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    }

    removeImage() {
        this.imageInput.value = '';
        this.imagePreview.style.display = 'none';
        this.previewImg.src = '';
    }

    async handleSubmit(event) {
        event.preventDefault();

        const message = this.messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');

        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';

        // Show loading
        this.showLoading(true);

        try {
            // Prepare form data
            const formData = new FormData();
            formData.append('message', message);

            // Add image if selected
            if (this.imageInput.files[0]) {
                formData.append('image', this.imageInput.files[0]);
                this.removeImage(); // Clear image after sending
            }

            // Send to backend
            console.log('Sending agricultural query to assistant:', message);
            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Agricultural assistant response:', data);

            if (data.error) {
                throw new Error(data.error);
            }

            // Add bot response to chat
            this.addMessage(data.response, 'bot');

        } catch (error) {
            console.error('Error communicating with agricultural assistant:', error);
            this.addMessage('Sorry, I encountered an error while analyzing your request. Please try again or contact our support team.', 'bot');
        } finally {
            this.showLoading(false);
        }
    }

    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const now = new Date();
        const timeString = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        const senderName = sender === 'user' ? 'You' : 'AgriBot';

        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>${senderName}:</strong> ${content}
            </div>
            <div class="message-time">${timeString}</div>
        `;

        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showLoading(show) {
        this.loadingIndicator.style.display = show ? 'flex' : 'none';
        this.sendButton.disabled = show;
    }
}

// Initialize the agricultural assistant when DOM loads
document.addEventListener('DOMContentLoaded', function() {
    const agriAssistant = new AgriAssistant();
});
