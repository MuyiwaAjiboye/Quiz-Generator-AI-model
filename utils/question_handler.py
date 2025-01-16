import random
from typing import List, Dict

class QuestionHandler:
    def __init__(self):
        self.option_count = 4  # Number of options per question

    def create_question(self, question_text: str, topic: str, difficulty: str) -> Dict:
        """Create a complete question with options and answer"""
        options = self._generate_options(topic, question_text)
        correct_answer = options[0]  # First option is correct
        # Shuffle options
        random.shuffle(options)

        return {
            'question': question_text,
            'options': options,
            'correct_answer': correct_answer,
            'difficulty': difficulty
        }

    def _generate_options(self, topic: str, question: str) -> List[str]:
        """Generate multiple choice options based on topic"""
        # This is a simple example - you might want to enhance this
        if "programming" in topic.lower():
            options = [
                "Using variables and functions",
                "Using loops and conditions",
                "Using classes and objects",
                "Using data structures"
            ]
        elif "database" in topic.lower():
            options = [
                "Using SQL queries",
                "Using database tables",
                "Using indexes",
                "Using joins"
            ]
        else:
            # Generic tech options
            options = [
                "Using appropriate tools",
                "Following best practices",
                "Implementing solutions",
                "Analyzing requirements"
            ]

        return random.sample(options, self.option_count)
