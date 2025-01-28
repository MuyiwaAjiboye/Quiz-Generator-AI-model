import json
from datetime import datetime
import os

class ResultHandler:
    def __init__(self):
        self.results_dir = "quiz_results"
        self.ensure_results_directory()

    def ensure_results_directory(self):
        """Create results directory if it doesn't exist"""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def display_quiz(self, quiz: list):
        """Display quiz questions without answers"""
        if not quiz:
            print("No questions available.")
            return

        print("\n=== Quiz Questions ===")
        for i, q in enumerate(quiz, 1):
            print(f"\nQuestion {i}:")
            print("=" * 40)
            print(self._format_text(q['question']))
            print("-" * 40)

            for j, option in enumerate(q['options']):
                option_text = self._format_text(option)
                print(f"{chr(65+j)}. {option_text}")

            print("-" * 40)

    def show_answers(self, quiz: list):
        """Display correct answers for the quiz"""
        if not quiz:
            print("No answers to display.")
            return

        print("\n=== Quiz Answers ===")
        for i, q in enumerate(quiz, 1):
            print(f"\nQuestion {i}:")
            print("=" * 40)
            print(self._format_text(q['question']))
            print("-" * 40)

            for j, option in enumerate(q['options']):
                option_text = self._format_text(option)
                is_correct = option == q['correct_answer']
                marker = " ✓ (Correct Answer)" if is_correct else ""
                print(f"{chr(65+j)}. {option_text}{marker}")

            print("-" * 40)

        self._save_quiz_result(quiz)

    def _format_text(self, text: str, max_length: int = 80) -> str:
        """Format text for better readability"""
        if len(text) <= max_length:
            return text

        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(' '.join(current_line))

        return '\n   '.join(lines)

    def _save_quiz_result(self, quiz: list):
        """Save quiz results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.results_dir, f"quiz_result_{timestamp}.json")

        result_data = {
            "timestamp": timestamp,
            "questions": []
        }

        for q in quiz:
            question_data = {
                "question": q['question'],
                "options": q['options'],
                "correct_answer": q['correct_answer']
            }
            result_data["questions"].append(question_data)

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=4, ensure_ascii=False)
            print(f"\nQuiz results saved to: {filename}")
        except Exception as e:
            print(f"\nError saving quiz results: {e}")
