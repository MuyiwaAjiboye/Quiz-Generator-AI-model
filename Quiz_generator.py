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
        questions = []

        difficulty_levels = {
            'easy': "basic concepts and fundamental principles",
            'medium': "intermediate concepts and practical applications",
            'hard': "advanced concepts and complex scenarios"
        }

        for i in range(num_questions):
            # Create a more detailed prompt for better question generation
            prompt = f"""Generate a unique multiple choice question about {topic}.
            Difficulty level: {difficulty} ({difficulty_levels[difficulty]})
            Include 4 possible answers, with the correct answer first.
            Format:
            [Question]
            [Correct Answer]
            [Wrong Answer 1]
            [Wrong Answer 2]
            [Wrong Answer 3]
            Make it specific to {topic} and appropriate for the {difficulty} difficulty level."""

            try:
                output = self.generator(
                    prompt,
                    max_length=200,
                    min_length=50,
                    temperature=0.8,
                    num_return_sequences=1,
                    do_sample=True
                )

                question = self.question_handler.create_question(
                    output[0]['generated_text'],
                    topic,
                    difficulty
                )
                questions.append(question)

            except Exception as e:
                print(f"Error generating question {i+1}: {e}")
                continue

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
