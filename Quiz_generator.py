from utils.content_processor import ContentProcessor
from utils.result_handler import ResultHandler

class QuizGenerator:
    def __init__(self):
        print("Initializing Quiz Generator...")
        self.content_processor = ContentProcessor()
        self.result_handler = ResultHandler()
        self.current_quiz = None

    def generate_quiz(self, topic: str, num_questions: int):
        """Generate a quiz for the given topic"""
        sections = self.content_processor.get_content_sections(topic)

        if not sections:
            print(f"Topic not found. Available topics: {', '.join(self.content_processor.get_available_topics())}")
            return None

        questions = []
        try:
            for _ in range(min(num_questions, len(sections))):
                section = random.choice(sections)
                sections.remove(section)  # Avoid duplicate questions

                question_dict = self.content_processor.create_question(section)
                if question_dict:
                    questions.append(question_dict)

            self.current_quiz = questions
            return questions

        except Exception as e:
            print(f"Error generating quiz: {e}")
            return None

    def run_quiz(self):
        """Run the quiz application"""
        while True:
            print("\n=== Quiz Generator ===")
            print("Available topics:", ", ".join(self.content_processor.get_available_topics()))

            topic = input("\nEnter topic (or 'exit' to quit): ").lower()
            if topic == 'exit':
                break

            try:
                num_questions = int(input("How many questions would you like? "))
                if num_questions <= 0:
                    raise ValueError("Number of questions must be positive")

                print("\nGenerating quiz...")
                quiz = self.generate_quiz(topic, num_questions)

                if quiz:
                    self.result_handler.display_quiz(quiz)

                    while True:
                        show_answers = input("\nWould you like to see the answers? (yes/no): ").lower()
                        if show_answers in ['yes', 'no']:
                            break
                        print("Please enter 'yes' or 'no'")

                    if show_answers == 'yes':
                        self.result_handler.show_answers(quiz)

            except ValueError as e:
                print(f"Error: {e}")
                print("Please enter a valid number of questions.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Please try again.")

def main():
    try:
        quiz_gen = QuizGenerator()
        quiz_gen.run_quiz()
    except KeyboardInterrupt:
        print("\nQuiz Generator terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        print("\nThank you for using Quiz Generator!")

if __name__ == "__main__":
    main()
