from typing import List, Dict
import random

class QuestionHandler:
    def __init__(self):
        self.option_count = 4

    def create_question(self, generated_text: str, topic: str, difficulty: str) -> Dict:
        """Create a complete question with relevant options"""
        # Clean and format the generated question
        question = self._format_question(generated_text)

        # Use the generated text to create relevant options
        options = self._generate_options_from_text(generated_text, difficulty)

        # First option is correct, then shuffle
        correct_answer = options[0]
        random.shuffle(options)

        return {
            'question': question,
            'options': options,
            'correct_answer': correct_answer,
            'difficulty': difficulty
        }

    def _format_question(self, text: str) -> str:
        """Format the generated text into a clear question"""
        # Clean up the generated text
        text = text.strip()
        if not text.endswith('?'):
            text += '?'
        return text

    def _generate_options_from_text(self, text: str, difficulty: str) -> List[str]:
        """Generate relevant options based on the question content"""
        # This method will create options based on the generated question
        # The model should generate both the question and potential answers

        # Split the generated text if it contains answer options
        parts = text.split('\n')

        if len(parts) > 1:
            # If the model generated options, use them
            options = [p.strip() for p in parts[1:] if p.strip()]
            if len(options) >= 4:
                return options[:4]

        # If we need to generate options
        # Add placeholder options that make sense for the question
        # These will be replaced by proper generated options in the future
        options = [
            "Option 1 - Main concept",
            "Option 2 - Related concept",
            "Option 3 - Similar concept",
            "Option 4 - Alternative concept"
        ]

        return options
