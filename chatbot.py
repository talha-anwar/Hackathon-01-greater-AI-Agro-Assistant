
import os
from openai import OpenAI
from typing import Optional, List
import random
import re

class AgriAssistant:
    """
    Agricultural AI assistant using OpenRouter API with Llama models for crop diagnosis and farming advice.
    Includes image processing capabilities for plant disease identification.
    """
    
    def __init__(self, model_type='openrouter'):
        """
        Initialize agricultural assistant with specified model type
        
        Args:
            model_type (str): Type of model to use ('openrouter', 'rule_based')
        """
        self.model_type = model_type
        self.conversation_history = []  # Track conversation for context
        self._init_model()
    
    def _init_model(self):
        """Initialize the selected model"""
        if self.model_type == 'openrouter':
            self._init_openrouter()
        else:
            self._init_rule_based()
    
    def _init_openrouter(self):
        """Initialize OpenRouter API client for Llama models"""
        try:
            api_key = os.environ.get('OPENROUTER_API_KEY')
            print(f"OpenRouter API key found: {bool(api_key)}")
            if not api_key:
                print("Warning: OPENROUTER_API_KEY not found. Falling back to rule-based agricultural responses.")
                self._init_rule_based()
                self.model_type = 'rule_based'
            else:
                self.client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key
                )
                print("OpenRouter client with Llama model initialized successfully for agricultural assistance")
        except Exception as e:
            print(f"OpenRouter initialization error: {e}. Falling back to agricultural rule-based responses.")
            self._init_rule_based()
            self.model_type = 'rule_based'
    
    def _init_rule_based(self):
        """Initialize rule-based response patterns (fallback)"""
        self.responses = {
            'greeting': [
                "Hello! I'm your agricultural assistant. How can I help with your crops today?",
                "Hi there! What farming challenge can I help you solve?",
                "Welcome to AgriDiagnose! How can I assist with your agricultural needs?",
                "Greetings! I'm here to help with crop diagnosis and farming advice."
            ],
            'how_are_you': [
                "I'm doing great and ready to help with your agricultural needs!",
                "All systems green here! How are your crops doing?",
                "I'm functioning well! How can I assist with your farming today?",
                "Ready to help with any agricultural challenges you're facing!"
            ],
            'goodbye': [
                "Happy farming! Come back anytime for more agricultural advice!",
                "Take care of your crops! I'm here whenever you need agricultural support!",
                "Good luck with your farming! Feel free to return for more diagnosis help!",
                "Until next time - may your harvests be bountiful!"
            ],
            'help': [
                "I'm your agricultural AI assistant! I can help diagnose plant diseases, identify nutrient deficiencies, provide farming advice, and analyze crop images.",
                "I specialize in crop health diagnosis, pest identification, soil advice, and general farming guidance. What agricultural challenge are you facing?",
                "Upload crop photos for disease analysis, ask about farming techniques, or get advice on plant nutrition. How can I help your farm today?"
            ],
            'default': [
                "That's an interesting agricultural observation! Can you tell me more about your crops or farming situation?",
                "I see. What specific crops or farming challenges would you like help with?",
                "Thanks for sharing! Are you dealing with any plant diseases, pests, or nutrient issues?",
                "Interesting farming question! What crops are you growing and what symptoms are you observing?",
                "I'd love to help with your agricultural needs. Can you describe your crops and any issues you're seeing?"
            ]
        }
        
        self.patterns = {
            'greeting': r'\b(hello|hi|hey|greetings?|good morning|good afternoon|good evening)\b',
            'how_are_you': r'\b(how are you|how\'re you|how do you do|what\'s up|how\'s it going)\b',
            'goodbye': r'\b(bye|goodbye|see you|farewell|take care|gtg|got to go)\b',
            'help': r'\b(help|assist|support|what can you do|capabilities|diagnose|disease|pest|crop|plant|farming)\b'
        }
    
    def get_bot_response(self, message: str) -> str:
        """
        Main function to get agricultural assistant response for text messages
        
        Args:
            message (str): User message about agricultural topics
            
        Returns:
            str: Agricultural assistant response
        """
        if self.model_type == 'openrouter':
            return self._get_openrouter_response(message)
        else:
            return self._get_rule_based_response(message)
    
    def _get_openrouter_response(self, message: str) -> str:
        """
        Get response from OpenRouter API using Llama model for agricultural assistance
        
        Args:
            message (str): User message about agricultural topics
            
        Returns:
            str: Llama model response via OpenRouter for agricultural guidance
        """
        try:
            print(f"Sending agricultural query to OpenRouter Llama model: {message[:50]}...")
            if not hasattr(self, 'client'):
                print("OpenRouter client not initialized, using agricultural rule-based response")
                return self._get_rule_based_response(message)
            
            # Add current message to conversation history
            self.conversation_history.append({"role": "user", "content": message})
            
            # Keep conversation history manageable (last 10 messages)
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            # Build messages with agricultural context
            messages = [
                {"role": "system", "content": "You are an expert agricultural AI assistant specializing in crop diagnosis, plant disease identification, pest management, soil health, and farming advice. Provide practical, actionable guidance for farmers and agricultural professionals. Be specific and helpful with agricultural recommendations."}
            ] + self.conversation_history
            
            response = self.client.chat.completions.create(
                model="meta-llama/llama-3.2-3b-instruct:free",
                messages=messages,
                max_tokens=200,
                temperature=0.7,
                timeout=20,
                extra_headers={
                    "HTTP-Referer": "https://your-repl-url.replit.app",
                    "X-Title": "AgriDiagnose Assistant"
                }
            )
            result = response.choices[0].message.content.strip()
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": result})
            
            print(f"OpenRouter Llama agricultural response received: {result[:50]}...")
            return result
        
        except Exception as e:
            print(f"OpenRouter API error: {e}")
            print(f"Error type: {type(e).__name__}")
            print(f"Full error details: {str(e)}")
            
            # Check if it's an authentication error
            if "authentication" in str(e).lower() or "api key" in str(e).lower():
                print("Authentication error detected, switching to agricultural rule-based mode")
                self._init_rule_based()
                self.model_type = 'rule_based'
                return "I'm having trouble with my OpenRouter API configuration. Let me help you with my built-in agricultural knowledge instead!"
            elif "quota" in str(e).lower() or "billing" in str(e).lower():
                print("Quota limit reached, switching to agricultural rule-based mode")
                self._init_rule_based()
                self.model_type = 'rule_based'
                return "I've reached my OpenRouter usage limit for now. Don't worry though - I can still provide agricultural advice using my built-in farming knowledge!"
            elif "rate limit" in str(e).lower():
                print("Rate limit detected, switching to agricultural rule-based mode temporarily")
                self._init_rule_based()
                return "I'm being rate limited at the moment. Here's my agricultural advice using built-in knowledge: " + self._get_rule_based_response(message)
            else:
                print("Unknown error, falling back to agricultural rule-based response")
                self._init_rule_based()
                self.model_type = 'rule_based'
                return "I'm experiencing some technical difficulties, but I can still help with your agricultural needs! " + self._get_rule_based_response(message)
    
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
    
    def process_crop_images(self, image_paths: List[str]) -> str:
        """
        Process uploaded crop images for disease/pest identification (placeholder for future implementation)
        
        Args:
            image_paths (List[str]): List of paths to uploaded crop image files
            
        Returns:
            str: Agricultural analysis summary of processed crop images
        """
        # TODO: Implement agricultural image processing here
        # This function will:
        # 1. Load and preprocess crop images from image_paths
        # 2. Run agricultural computer vision models for disease/pest detection
        # 3. Identify plant species, diseases, nutrient deficiencies, pest damage
        # 4. Return agricultural analysis that can be sent to Llama for detailed recommendations
        
        if len(image_paths) == 0:
            return ""
        
        # Placeholder response for now
        image_count = len(image_paths)
        if image_count == 1:
            return f"I can see you've uploaded a crop image! Advanced plant disease detection and analysis is coming soon. For now, please describe what you're observing in your crops and I'll provide agricultural guidance."
        else:
            return f"I can see you've uploaded {image_count} crop images! Multi-image agricultural analysis is coming soon. Please describe the issues you're seeing in your crops and I'll help with diagnosis and treatment recommendations."
    
    def get_response(self, message: str, image_paths: Optional[List[str]] = None) -> str:
        """
        Combined response function that handles both agricultural text queries and crop images
        
        Args:
            message (str): User message about agricultural topics
            image_paths (Optional[List[str]]): List of uploaded crop image file paths
            
        Returns:
            str: Combined agricultural assistant response
        """
        # Process crop images if provided
        image_context = ""
        if image_paths and len(image_paths) > 0:
            image_context = self.process_crop_images(image_paths)
        
        # Get agricultural text response
        if image_context:
            # If we have crop image context, combine it with the user message for Llama
            combined_message = f"Agricultural query: {message}\n\nCrop image context: {image_context}"
            text_response = self.get_bot_response(combined_message)
        else:
            text_response = self.get_bot_response(message)
        
        return text_response
