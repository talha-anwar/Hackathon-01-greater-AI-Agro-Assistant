
import random
import re
from typing import Optional

class ChatBot:
    """
    Modular chatbot class that can be easily extended to use different models.
    Currently implements rule-based responses, but can be switched to:
    - OpenAI API (if free tier available)
    - Local models via llama.cpp
    - HuggingFace transformers
    - Any other chat model API
    """
    
    def __init__(self, model_type='rule_based'):
        """
        Initialize chatbot with specified model type
        
        Args:
            model_type (str): Type of model to use ('rule_based', 'openai', 'local', etc.)
        """
        self.model_type = model_type
        self._init_model()
    
    def _init_model(self):
        """Initialize the selected model"""
        if self.model_type == 'rule_based':
            self._init_rule_based()
        elif self.model_type == 'openai':
            self._init_openai()
        elif self.model_type == 'local':
            self._init_local_model()
        # Add more model types as needed
    
    def _init_rule_based(self):
        """Initialize rule-based response patterns"""
        self.responses = {
            'greeting': [
                "Hello! How can I help you today?",
                "Hi there! What's on your mind?",
                "Hey! How's it going?",
                "Greetings! What would you like to chat about?"
            ],
            'how_are_you': [
                "I'm doing great, thank you for asking!",
                "I'm fine, thanks! How about you?",
                "All good here! How can I assist you?",
                "I'm doing well! What brings you here today?"
            ],
            'goodbye': [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Bye! Feel free to come back anytime!",
                "Farewell! Hope to chat again soon!"
            ],
            'help': [
                "I'm here to help! You can ask me questions, have a conversation, or even upload images (though I can't process them yet).",
                "I can chat with you about various topics. What would you like to talk about?",
                "Feel free to ask me anything! I'm here to assist and chat with you."
            ],
            'default': [
                "That's interesting! Tell me more about that.",
                "I see. What else would you like to discuss?",
                "Thanks for sharing! Is there anything specific you'd like to know?",
                "Hmm, that's a good point. What are your thoughts on that?",
                "I understand. How can I help you with that?",
                "That sounds important to you. Can you elaborate?",
                "Interesting perspective! What made you think about that?"
            ]
        }
        
        self.patterns = {
            'greeting': r'\b(hello|hi|hey|greetings?|good morning|good afternoon|good evening)\b',
            'how_are_you': r'\b(how are you|how\'re you|how do you do|what\'s up|how\'s it going)\b',
            'goodbye': r'\b(bye|goodbye|see you|farewell|take care|gtg|got to go)\b',
            'help': r'\b(help|assist|support|what can you do|capabilities)\b'
        }
    
    def _init_openai(self):
        """
        Initialize OpenAI API (free tier if available)
        TODO: Implement OpenAI integration
        """
        try:
            # import openai
            # self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            print("OpenAI model initialization - TODO: Implement")
            # Fallback to rule-based for now
            self._init_rule_based()
        except ImportError:
            print("OpenAI package not installed. Falling back to rule-based.")
            self._init_rule_based()
    
    def _init_local_model(self):
        """
        Initialize local model (llama.cpp, HuggingFace, etc.)
        TODO: Implement local model integration
        """
        try:
            # Example for HuggingFace transformers:
            # from transformers import pipeline
            # self.generator = pipeline('text-generation', model='microsoft/DialoGPT-medium')
            print("Local model initialization - TODO: Implement")
            # Fallback to rule-based for now
            self._init_rule_based()
        except ImportError:
            print("Required packages for local model not installed. Falling back to rule-based.")
            self._init_rule_based()
    
    def get_response(self, message: str, image_path: Optional[str] = None) -> str:
        """
        Get chatbot response for given message and optional image
        
        Args:
            message (str): User message
            image_path (str, optional): Path to uploaded image file
            
        Returns:
            str: Chatbot response
        """
        if self.model_type == 'rule_based':
            return self._get_rule_based_response(message, image_path)
        elif self.model_type == 'openai':
            return self._get_openai_response(message, image_path)
        elif self.model_type == 'local':
            return self._get_local_response(message, image_path)
        else:
            return "Sorry, I'm not configured properly. Please try again."
    
    def _get_rule_based_response(self, message: str, image_path: Optional[str] = None) -> str:
        """Generate rule-based response"""
        message_lower = message.lower()
        
        # Handle image if provided
        if image_path:
            return f"I can see you've uploaded an image! Unfortunately, I can't process images yet, but I received your message: '{message}'. Image processing is coming soon!"
        
        # Check for patterns
        for intent, pattern in self.patterns.items():
            if re.search(pattern, message_lower, re.IGNORECASE):
                return random.choice(self.responses[intent])
        
        # Default response
        return random.choice(self.responses['default'])
    
    def _get_openai_response(self, message: str, image_path: Optional[str] = None) -> str:
        """
        Get response from OpenAI API
        TODO: Implement OpenAI integration
        """
        # Placeholder implementation
        try:
            # Example OpenAI call:
            # response = self.openai_client.chat.completions.create(
            #     model="gpt-3.5-turbo",  # Use free tier model if available
            #     messages=[{"role": "user", "content": message}]
            # )
            # return response.choices[0].message.content
            
            # For now, fallback to rule-based
            return self._get_rule_based_response(message, image_path)
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._get_rule_based_response(message, image_path)
    
    def _get_local_response(self, message: str, image_path: Optional[str] = None) -> str:
        """
        Get response from local model
        TODO: Implement local model integration
        """
        # Placeholder implementation
        try:
            # Example for local model:
            # response = self.generator(message, max_length=100, num_return_sequences=1)
            # return response[0]['generated_text']
            
            # For now, fallback to rule-based
            return self._get_rule_based_response(message, image_path)
        except Exception as e:
            print(f"Local model error: {e}")
            return self._get_rule_based_response(message, image_path)
