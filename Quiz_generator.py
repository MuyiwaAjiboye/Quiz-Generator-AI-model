from transformers import pipeline
from utils.question_handler import QuestionHandler
from utils.quiz_history import QuizHistory
from utils.result_handler import ResultHandler

class QuizGenerator:
    def __init__(self):
        print("Loading pre-trained model...")
        self.generator = pipeline('text2text-generation', model='facebook/bart-large-cnn')
        self.question_handler = QuestionHandler()
        self.history = QuizHistory()
        self.result_handler = ResultHandler()
        self.current_quiz = None

    def generate_quiz(self, topic: str, difficulty: str, num_questions: int) -> dict:
        """Generate a quiz with specified number of questions"""
        questions = []

        for _ in range(num_questions):
            # Generate question text
            prompt = f"""Generate a {difficulty} multiple choice question about {topic}.
            Include 4 possible answers, with the correct answer first.
            Each answer should be on a new line."""

            try:
                output = self.generator(
                    prompt,
                    max_length=200,
                    min_length=20,
                    temperature=0.7,
                    do_sample=True,
                    num_return_sequences=1
                )

                # Create question with options
                question = self.question_handler.create_question(
                    output[0]['generated_text'],
                    topic,
                    difficulty
                )
                questions.append(question)

            except Exception as e:
                print(f"Error generating question: {e}")
                continue

        # Create quiz
        quiz = {
            'topic': topic,
            'difficulty': difficulty,
            'questions': questions,
            'timestamp': self.history.get_timestamp()
        }

        self.current_quiz = quiz
        self.history.add_quiz(quiz)
        return quiz

def main():
    quiz_gen = QuizGenerator()

    while True:
        print("\n=== Quiz Generator ===")
        print("1. Generate new quiz")
        print("2. View history")
        print("3. Exit")

        choice = input("\nChoice: ")

        if choice == '1':
            topic = input("Enter topic (e.g., Python, JavaScript, Databases): ")
            difficulty = input("Enter difficulty (easy/medium/hard): ").lower()
            while difficulty not in ['easy', 'medium', 'hard']:
                print("Invalid difficulty! Please choose easy, medium, or hard.")
                difficulty = input("Enter difficulty: ").lower()

            try:
                num_questions = int(input("How many questions would you like? "))
                if num_questions <= 0:
                    raise ValueError
            except ValueError:
                print("Please enter a valid number greater than 0")
                continue

            quiz = quiz_gen.generate_quiz(topic, difficulty, num_questions)
            user_answers = quiz_gen.result_handler.take_quiz(quiz)
            quiz_gen.result_handler.show_results(quiz, user_answers)

        elif choice == '2':
            quizzes = quiz_gen.history.get_all()
            if not quizzes:
                print("No quiz history found!")
            for quiz in quizzes:
                print(f"\nTopic: {quiz['topic']}")
                print(f"Date: {quiz['timestamp']}")
                print(f"Number of questions: {len(quiz['questions'])}")

        elif choice == '3':
            break

if __name__ == "__main__":
    main()
