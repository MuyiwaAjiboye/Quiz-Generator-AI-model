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
            # Display question with formatting
            print(f"\nQuestion {i}:")
            print("=" * 40)
            print(self._format_text(q['question']))
            print("-" * 40)

            # Display options with letter choices
            for j, option in enumerate(q['options']):
                # Format long options for better readability
                option_text = self._format_text(option)
                print(f"{chr(65+j)}. {option_text}")

            print("-" * 40)

    def show_answers(self, quiz: list):
        """Display correct answers for the quiz"""
        if not quiz:
            print("No answers to display.")
            return

        print("\n=== Quiz Answers ===")
        score = 0
        total = len(quiz)

        for i, q in enumerate(quiz, 1):
            print(f"\nQuestion {i}:")
            print("=" * 40)
            print(self._format_text(q['question']))
            print("-" * 40)

            # Display all options, highlighting the correct one
            for j, option in enumerate(q['options']):
                option_text = self._format_text(option)
                is_correct = option == q['correct_answer']
                marker = " ✓ (Correct Answer)" if is_correct else ""
                print(f"{chr(65+j)}. {option_text}{marker}")

            print("-" * 40)

        # Save quiz results
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
            word_length = len(word) + 1  # +1 for space
            if current_length + word_length <= max_length:
                current_line.append(word)
                current_length += word_length
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length

        if current_line:
            lines.append(' '.join(current_line))

        return '\n   '.join(lines)  # Indent continued lines

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

    def take_quiz(self, quiz: list):
        """Interactive quiz taking with immediate feedback"""
        if not quiz:
            print("No questions available.")
            return

        user_answers = []
        score = 0
        total_questions = len(quiz)

        print("\n=== Quiz Started ===")
        start_time = datetime.now()

        for i, q in enumerate(quiz, 1):
            print(f"\nQuestion {i} of {total_questions}:")
            print("=" * 40)
            print(self._format_text(q['question']))
            print("-" * 40)

            # Display options
            for j, option in enumerate(q['options']):
                print(f"{chr(65+j)}. {self._format_text(option)}")

            # Get user answer
            while True:
                answer = input("\nYour answer (A/B/C/D): ").upper()
                if answer in ['A', 'B', 'C', 'D']:
                    user_answers.append(answer)

                    # Convert letter answer to option
                    answer_index = ord(answer) - ord('A')
                    selected_answer = q['options'][answer_index]

                    # Check if correct
                    is_correct = selected_answer == q['correct_answer']
                    if is_correct:
                        score += 1
                        print("✓ Correct!")
                    else:
                        correct_index = q['options'].index(q['correct_answer'])
                        print(f"✗ Incorrect. The correct answer was: {chr(65+correct_index)}")

                    break
                else:
                    print("Please enter A, B, C, or D")

        # Calculate and display results
        end_time = datetime.now()
        duration = (end_time - start_time).seconds
        percentage = (score / total_questions) * 100

        print("\n=== Quiz Results ===")
        print(f"Score: {score}/{total_questions}")
        print(f"Percentage: {percentage:.1f}%")
        print(f"Time taken: {duration} seconds")

        # Save results
        self._save_quiz_result(quiz)

        return user_answers
