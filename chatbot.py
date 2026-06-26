"""
Rule-based Chatbot
A simple chatbot that uses pattern matching to respond to user inputs.
"""

import re
import random
import json
from typing import Dict, List, Tuple, Optional


class RuleBasedChatbot:
    """A rule-based chatbot using pattern matching and response generation."""
    
    def __init__(self, rules_file: str = "rules.json"):
        """
        Initialize the chatbot with rules from a JSON file.
        
        Args:
            rules_file: Path to the JSON file containing rules
        """
        self.rules = []
        self.fallback_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "Interesting! Tell me more.",
            "I don't have a rule for that yet. Can you ask differently?",
            "Hmm, I'm still learning. Could you try asking in another way?",
            "That's beyond my current knowledge. Let's talk about something else."
        ]
        self.load_rules(rules_file)
    
    def load_rules(self, rules_file: str) -> None:
        """
        Load rules from a JSON file.
        
        Each rule should have:
        - 'patterns': list of regex patterns
        - 'responses': list of possible responses (can include {variable} placeholders)
        - 'priority': integer (lower = higher priority)
        """
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.rules = data.get('rules', [])
                # Sort rules by priority
                self.rules.sort(key=lambda x: x.get('priority', 999))
        except FileNotFoundError:
            print(f"Warning: {rules_file} not found. Using default rules.")
            self._load_default_rules()
        except json.JSONDecodeError:
            print(f"Error: {rules_file} is not valid JSON. Using default rules.")
            self._load_default_rules()
    
    def _load_default_rules(self) -> None:
        """Load a set of default rules if no file is found."""
        self.rules = [
            {
                "name": "greeting",
                "patterns": [r"hello", r"hi", r"hey", r"howdy", r"greetings"],
                "responses": [
                    "Hello! How can I help you today?",
                    "Hi there! What brings you here?",
                    "Hey! Nice to see you!"
                ],
                "priority": 1
            },
            {
                "name": "goodbye",
                "patterns": [r"bye", r"goodbye", r"see you", r"farewell", r"exit"],
                "responses": [
                    "Goodbye! Have a great day!",
                    "See you later! Take care!",
                    "Farewell! It was nice chatting with you!"
                ],
                "priority": 1
            },
            {
                "name": "how_are_you",
                "patterns": [r"how are you", r"how do you do", r"how's it going"],
                "responses": [
                    "I'm doing great, thanks for asking! How about you?",
                    "All systems operational! How can I assist you?",
                    "I'm functioning perfectly! What can I do for you?"
                ],
                "priority": 2
            },
            {
                "name": "name",
                "patterns": [r"what is your name", r"who are you", r"your name"],
                "responses": [
                    "I'm ChatBot, your friendly rule-based assistant!",
                    "I'm called ChatBot. Nice to meet you!",
                    "I'm a simple rule-based chatbot. You can call me ChatBot."
                ],
                "priority": 2
            },
            {
                "name": "help",
                "patterns": [r"help", r"assist", r"support", r"what can you do"],
                "responses": [
                    "I can help with general questions, greetings, and simple conversations. "
                    "Try saying hello, asking how I am, or asking about my name!",
                    "I'm a rule-based chatbot. I respond to patterns you provide. "
                    "You can ask me about my name, how I am, or just have a chat!",
                    "I'm here to help! I can respond to greetings, answer simple questions, "
                    "or just have a conversation with you."
                ],
                "priority": 2
            },
            {
                "name": "weather",
                "patterns": [r"weather", r"temperature", r"rain", r"snow", r"forecast"],
                "responses": [
                    "I don't have access to real-time weather data, but I hope it's nice where you are!",
                    "I wish I could check the weather for you, but I'm just a simple chatbot.",
                    "Weather? I'm not connected to any weather API, sorry!"
                ],
                "priority": 3
            },
            {
                "name": "time",
                "patterns": [r"what time", r"time is it", r"current time", r"date"],
                "responses": [
                    "I don't have a clock, but you can check your device for the current time!",
                    "I'm not connected to a time service, sorry! Check your system clock.",
                    "Time flies when you're having fun! But seriously, check your device."
                ],
                "priority": 3
            },
            {
                "name": "default",
                "patterns": [r".*"],
                "responses": [
                    "I'm not sure I follow. Could you ask differently?",
                    "Interesting point! Tell me more.",
                    "I don't have a response for that yet. Can you rephrase?",
                    "Let's talk about something else. What's on your mind?"
                ],
                "priority": 999
            }
        ]
    
    def extract_variables(self, text: str, pattern: str) -> Dict[str, str]:
        """
        Extract variables from user input based on pattern groups.
        
        Args:
            text: User input text
            pattern: Regex pattern with named groups
            
        Returns:
            Dictionary of variable names and values
        """
        variables = {}
        try:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                variables = match.groupdict()
        except Exception:
            pass
        return variables
    
    def get_response(self, user_input: str) -> str:
        """
        Get a response based on the user input.
        
        Args:
            user_input: The user's message
            
        Returns:
            A response string
        """
        user_input = user_input.strip()
        
        if not user_input:
            return "You didn't say anything! Please type a message."
        
        # Check each rule
        for rule in self.rules:
            patterns = rule.get('patterns', [])
            responses = rule.get('responses', [])
            
            for pattern in patterns:
                try:
                    if re.search(pattern, user_input, re.IGNORECASE):
                        # Found a matching pattern
                        if responses:
                            # Choose a random response
                            response = random.choice(responses)
                            # Extract variables and format response
                            variables = self.extract_variables(user_input, pattern)
                            if variables:
                                try:
                                    response = response.format(**variables)
                                except (KeyError, ValueError):
                                    # If formatting fails, use response as-is
                                    pass
                            return response
                except re.error:
                    # Skip invalid regex patterns
                    continue
        
        # No rules matched - use fallback
        return random.choice(self.fallback_responses)
    
    def add_rule(self, name: str, patterns: List[str], responses: List[str], priority: int = 5) -> None:
        """
        Add a new rule to the chatbot.
        
        Args:
            name: Rule name
            patterns: List of regex patterns
            responses: List of response strings
            priority: Priority (lower = higher)
        """
        self.rules.append({
            "name": name,
            "patterns": patterns,
            "responses": responses,
            "priority": priority
        })
        # Re-sort rules by priority
        self.rules.sort(key=lambda x: x.get('priority', 999))
    
    def save_rules(self, filename: str = "rules.json") -> None:
        """
        Save current rules to a JSON file.
        
        Args:
            filename: File to save rules to
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({"rules": self.rules}, f, indent=2, ensure_ascii=False)


def main():
    """Main function to run the chatbot interactively."""
    print("=" * 60)
    print("🤖 Rule-Based Chatbot")
    print("=" * 60)
    print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    print("Type 'help' for assistance.")
    print("Type 'save' to save current rules to rules.json")
    print("-" * 60)
    
    # Initialize chatbot
    chatbot = RuleBasedChatbot()
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\nChatBot: Goodbye! Have a great day! 👋")
                break
            
            # Save rules command
            if user_input.lower() == 'save':
                chatbot.save_rules()
                print("\nChatBot: Rules saved to rules.json ✓")
                continue
            
            # Get response
            response = chatbot.get_response(user_input)
            print(f"\nChatBot: {response}")
            
        except KeyboardInterrupt:
            print("\n\nChatBot: Goodbye! 👋")
            break
        except Exception as e:
            print(f"\nChatBot: Oops! Something went wrong: {e}")
            print("ChatBot: Let's try again!")


if __name__ == "__main__":
    main()
