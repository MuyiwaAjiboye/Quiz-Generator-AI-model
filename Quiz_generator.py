from transformers import pipeline
from utils.question_handler import QuestionHandler
from utils.result_handler import ResultHandler
from utils.quiz_history import QuizHistory
import random

class QuizGenerator:
    def __init__(self):
        print("Loading pre-trained model...")
        # Change this part to use BART
        self.generator = pipeline('text2text-generation', model='facebook/bart-large-cnn')
        self.question_handler = QuestionHandler()
        self.history = QuizHistory()
        self.result_handler = ResultHandler()
        self.current_quiz = None

    # The generate_quiz method needs to be adjusted for BART's output format
    def generate_quiz(self, topic: str, difficulty: str, num_questions: int) -> dict:
        """Generate a quiz with specified number of questions"""
        questions = []

        # Better structured prompts based on difficulty
        difficulty_prompts = {
            'easy': f"Write a straightforward multiple-choice question about {topic} that tests basic understanding.",
            'medium': f"Create a challenging multiple-choice question about {topic} that requires good knowledge.",
            'hard': f"Generate a complex multiple-choice question about {topic} that tests advanced concepts."
        }

        for _ in range(num_questions):
            prompt = f"""
Question: {difficulty_prompts[difficulty]}
Requirements:
- Must be clear and concise
- Focus on {topic} concepts
- Include context if needed
Example format:
What is the primary purpose of inheritance in object-oriented programming?"""

            try:
                # BART specific generation
                output = self.generator(
                    prompt,
                    max_length=100,
                    min_length=20,
                    do_sample=True,
                    temperature=0.7,
                    no_repeat_ngram_size=2
                )

                # Clean up generated question
                generated_question = output[0]['generated_text']
                generated_question = self._clean_question(generated_question)

                # Create full question with options
                if generated_question:
                    question = self.question_handler.create_question(
                        generated_question,
                        topic,
                        difficulty
                    )
                    questions.append(question)

            except Exception as e:
                print(f"Error generating question: {e}")
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

    def _clean_question(self, text: str) -> str:
        """Clean up the generated question text"""
        # Get the first line that ends with a question mark
        for line in text.split('\n'):
            line = line.strip()
            if line.endswith('?'):
                # Remove any prefixes like "Question:", "Q:", etc.
                for prefix in ["question:", "q:", "answer:", "example:"]:
                    if line.lower().startswith(prefix):
                        line = line[len(prefix):].strip()
                return line

        # If no good question found, return empty string
        return ""

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
