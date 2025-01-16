import json
from datetime import datetime
from typing import List, Dict

class QuizHistory:
    def __init__(self, filename: str = 'quiz_history.json'):
        self.filename = filename
        self.history = self.load_history()

    def add_quiz(self, quiz: Dict):
        """Add a new quiz to history"""
        self.history.append(quiz)
        self.save_history()

    def get_all(self) -> List[Dict]:
        """Get all saved quizzes"""
        return self.history

    def get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_history(self):
        """Save quiz history to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.history, f, indent=4)

    def load_history(self) -> List[Dict]:
        """Load quiz history from file"""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
