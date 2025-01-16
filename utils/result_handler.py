class ResultHandler:
    def take_quiz(self, quiz: dict) -> list:
        """Handle the quiz-taking process"""
        user_answers = []
        print("\n=== Quiz Started ===")

        for i, q in enumerate(quiz['questions'], 1):
            print(f"\nQuestion {i}:")
            print(q['question'])
            for j, option in enumerate(q['options']):
                print(f"{chr(65+j)}. {option}")

            while True:
                answer = input("\nYour answer (A/B/C/D): ").upper()
                if answer in ['A', 'B', 'C', 'D']:
                    user_answers.append(answer)
                    break
                print("Please enter A, B, C, or D")

        return user_answers

    def show_results(self, quiz: dict, user_answers: list):
        """Display quiz results"""
        print("\n=== Quiz Results ===")
        correct_count = 0

        for i, (question, user_answer) in enumerate(zip(quiz['questions'], user_answers), 1):
            print(f"\nQuestion {i}:")
            correct_letter = self.get_correct_option_letter(question)

            # Display question and options
            print(question['question'])
            for j, option in enumerate(question['options']):
                letter = chr(65+j)
                if letter == user_answer:
                    mark = "✓" if letter == correct_letter else "✗"
                    print(f"{letter}. {option} {mark}")
                else:
                    print(f"{letter}. {option}")

            # Show if answer was correct
            if user_answer == correct_letter:
                correct_count += 1
                print("Correct! ✓")
            else:
                print(f"Incorrect ✗ (Correct answer: {correct_letter})")

        # Show final score
        print(f"\nFinal Score: {correct_count}/{len(user_answers)} "
              f"({(correct_count/len(user_answers)*100):.1f}%)")

    def get_correct_option_letter(self, question: dict) -> str:
        """Get the letter (A, B, C, D) of the correct answer"""
        correct_answer = question['correct_answer']
        for i, option in enumerate(question['options']):
            if option == correct_answer:
                return chr(65 + i)
        return "?"
