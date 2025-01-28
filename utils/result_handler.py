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
            print(q['question'])
            print("-" * 40)

            # Display options with letter choices
            for j, option in enumerate(q['options']):
                # Format long options for better readability
                option_text = self._format_option_text(option)
                print(f"{chr(65+j)}. {option_text}")

            print("-" * 40)

    def show_answers(self, quiz: list):
        """Display correct answers for the quiz"""
        if not quiz:
            print("No answers to display.")
            return

        print("\n=== Quiz Answers ===")
        total_questions = len(quiz)

        for i, q in enumerate(quiz, 1):
            print(f"\nQuestion {i}:")
            print("=" * 40)
            print(q['question'])
            print("-" * 40)

            # Display all options, highlighting the correct one
            for j, option in enumerate(q['options']):
                option_text = self._format_option_text(option)
                if option == q['correct_answer']:
                    print(f"{chr(65+j)}. {option_text} ✓ (Correct Answer)")
                else:
                    print(f"{chr(65+j)}. {option_text}")

            print("-" * 40)

    def take_quiz(self, quiz: list):
        """Interactive quiz taking with immediate feedback option"""
        if not quiz:
            print("No questions available.")
            return

        user_answers = []
        score = 0
        total_questions = len(quiz)

        print("\n=== Quiz Started ===")
        start_time = datetime.now()

        for i, q in enumerate(quiz, 1):
            # Display question
            print(f"\nQuestion {i} of {total_questions}:")
            print("=" * 40)
            print(q['question'])
            print("-" * 40)

            # Display options
            for j, option in enumerate(q['options']):
                option_text = self._format_option_text(option)
                print(f"{chr(65+j)}. {option_text}")

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

        # Calculate results
        end_time = datetime.now()
        duration = (end_time - start_time).seconds
        percentage = (score / total_questions) * 100

        # Display results
        self._display_results(score, total_questions, duration, percentage)

        # Save results
        self._save_results(quiz, user_answers, score, total_questions, duration, percentage)

        return user_answers

    def _format_option_text(self, text: str, max_length: int = 100) -> str:
        """Format option text for better readability"""
        if len(text) <= max_length:
            return text

        # Split long text into multiple lines
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

        return '\n   '.join(lines)  # Indent continuation lines

    def _display_results(self, score: int, total: int, duration: int, percentage: float):
        """Display quiz results with formatting"""
        print("\n=== Quiz Results ===")
        print("=" * 40)
        print(f"Score: {score}/{total}")
        print(f"Percentage: {percentage:.1f}%")
        print(f"Time taken: {duration} seconds")
        print("-" * 40)

        # Display performance message
        if percentage >= 90:
            print("Excellent performance! 🌟")
        elif percentage >= 70:
            print("Good job! 👍")
        elif percentage >= 50:
            print("Fair attempt. Keep practicing! 📚")
        else:
            print("More practice needed. Don't give up! 💪")
        print("=" * 40)

    def _save_results(self, quiz: list, user_answers: list, score: int, total: int,
                     duration: int, percentage: float):
        """Save quiz results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.results_dir, f"quiz_result_{timestamp}.json")

        results = {
            "timestamp": timestamp,
            "score": score,
            "total_questions": total,
            "percentage": percentage,
            "duration_seconds": duration,
            "questions": []
        }

        # Save detailed question and answer information
        for q, user_answer in zip(quiz, user_answers):
            answer_index = ord(user_answer) - ord('A')
            selected_answer = q['options'][answer_index]

            question_data = {
                "question": q['question'],
                "options": q['options'],
                "correct_answer": q['correct_answer'],
                "user_answer": user_answer,
                "user_answer_text": selected_answer,
                "is_correct": selected_answer == q['correct_answer']
            }
            results["questions"].append(question_data)

        # Save to file
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
