
import os
from openai import OpenAI
from typing import Optional, List
import random
import re

class ChatBot:
    """
    Modular chatbot class with OpenAI GPT-3.5 integration and placeholder for local image processing.
    """
    
    def __init__(self, model_type='openai'):
        """
        Initialize chatbot with specified model type
        
        Args:
            model_type (str): Type of model to use ('openai', 'rule_based')
        """
        self.model_type = model_type
        self._init_model()
    
    def _init_model(self):
        """Initialize the selected model"""
        if self.model_type == 'openai':
            self._init_openai()
        else:
            self._init_rule_based()
    
    def _init_openai(self):
        """Initialize OpenAI API client"""
        try:
            api_key = os.environ['OPENAI_API_KEY']
            if not api_key:
                print("Warning: OPENAI_API_KEY not found. Falling back to rule-based responses.")
                self._init_rule_based()
                self.model_type = 'rule_based'
            else:
                self.client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"OpenAI initialization error: {e}. Falling back to rule-based.")
            self._init_rule_based()
            self.model_type = 'rule_based'
    
    def _init_rule_based(self):
        """Initialize rule-based response patterns (fallback)"""
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
                "I'm here to help! You can ask me questions, have a conversation, or even upload images.",
                "I can chat with you about various topics. What would you like to talk about?",
                "Feel free to ask me anything! I'm here to assist and chat with you."
            ],
            'default': [
                "That's interesting! Tell me more about that.",
                "I see. What else would you like to discuss?",
                "Thanks for sharing! Is there anything specific you'd like to know?",
                "Hmm, that's a good point. What are your thoughts on that?",
                "I understand. How can I help you with that?"
            ]
        }
        
        self.patterns = {
            'greeting': r'\b(hello|hi|hey|greetings?|good morning|good afternoon|good evening)\b',
            'how_are_you': r'\b(how are you|how\'re you|how do you do|what\'s up|how\'s it going)\b',
            'goodbye': r'\b(bye|goodbye|see you|farewell|take care|gtg|got to go)\b',
            'help': r'\b(help|assist|support|what can you do|capabilities)\b'
        }
    
    def get_bot_response(self, message: str) -> str:
        """
        Main function to get chatbot response for text messages
        
        Args:
            message (str): User message
            
        Returns:
            str: Chatbot response
        """
        if self.model_type == 'openai':
            return self._get_openai_response(message)
        else:
            return self._get_rule_based_response(message)
    
    def _get_openai_response(self, message: str) -> str:
        """
        Get response from OpenAI GPT-3.5 API
        
        Args:
            message (str): User message
            
        Returns:
            str: GPT-3.5 response
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful, friendly AI assistant. Be conversational and engaging."},
                    {"role": "user", "content": message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to rule-based response
            return self._get_rule_based_response(message)
    
    def _get_rule_based_response(self, message: str) -> str:
        """
        Generate rule-based response (fallback)
        
        Args:
            message (str): User message
            
        Returns:
            str: Rule-based response
        """
        message_lower = message.lower()
        
        # Check for patterns
        for intent, pattern in self.patterns.items():
            if re.search(pattern, message_lower, re.IGNORECASE):
                return random.choice(self.responses[intent])
        
        # Default response
        return random.choice(self.responses['default'])
    
    def process_images(self, image_paths: List[str]) -> str:
        """
        Process uploaded images using local model (placeholder for future implementation)
        
        Args:
            image_paths (List[str]): List of paths to uploaded image files
            
        Returns:
            str: Summary or description of processed images
        """
        # TODO: Implement local model image processing here
        # This function will:
        # 1. Load and preprocess images from image_paths
        # 2. Run local model inference (e.g., llama.cpp, HuggingFace)
        # 3. Generate descriptions/analysis of the images
        # 4. Return summary that can be sent to GPT-3.5 for conversational response
        
        if len(image_paths) == 0:
            return ""
        
        # Placeholder response for now
        image_count = len(image_paths)
        if image_count == 1:
            return f"I can see you've uploaded an image! Image processing with local models is coming soon. For now, I can chat with you about anything else."
        else:
            return f"I can see you've uploaded {image_count} images! Batch image processing with local models is coming soon. For now, I can chat with you about anything else."
    
    def get_response(self, message: str, image_paths: Optional[List[str]] = None) -> str:
        """
        Combined response function that handles both text and images
        
        Args:
            message (str): User message
            image_paths (Optional[List[str]]): List of uploaded image file paths
            
        Returns:
            str: Combined chatbot response
        """
        # Process images if provided
        image_context = ""
        if image_paths and len(image_paths) > 0:
            image_context = self.process_images(image_paths)
        
        # Get text response
        if image_context:
            # If we have image context, combine it with the user message for GPT
            combined_message = f"User message: {message}\n\nImage context: {image_context}"
            text_response = self.get_bot_response(combined_message)
        else:
            text_response = self.get_bot_response(message)
        
        return text_response
