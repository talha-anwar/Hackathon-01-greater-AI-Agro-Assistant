document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const imageInput = document.getElementById('imageInput');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const removeImageBtn = document.getElementById('removeImage');
    const loadingIndicator = document.getElementById('loadingIndicator');

    let selectedFile = null;

    // Handle image selection
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            selectedFile = file;
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;
                imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Remove selected image
    removeImageBtn.addEventListener('click', function() {
        selectedFile = null;
        imageInput.value = '';
        imagePreview.style.display = 'none';
    });

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, 'user');
        messageInput.value = '';

        // Show loading indicator
        showLoading(true);

        try {
            // Prepare form data
            const formData = new FormData();
            formData.append('message', message);

            if (selectedFile) {
                formData.append('image', selectedFile);
            }

            // Send request to backend
            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                addMessage(data.response, 'bot');
            } else {
                addMessage(`Error: ${data.error || 'Unknown error occurred'}`, 'bot');
            }

        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, I encountered an error while processing your request. Please try again.', 'bot');
        } finally {
            showLoading(false);
            // Clear image after sending
            if (selectedFile) {
                removeImageBtn.click();
            }
        }
    });

    function addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Bot'}:</strong> ${message}`;

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString();

        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        chatMessages.appendChild(messageDiv);

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showLoading(show) {
        if (loadingIndicator) {
            loadingIndicator.style.display = show ? 'block' : 'none';
        }
    }

    // Focus on input when page loads
    messageInput.focus();
});