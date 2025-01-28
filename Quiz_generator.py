from transformers import T5ForConditionalGeneration, T5Tokenizer
from utils.question_handler import QuestionHandler
from utils.result_handler import ResultHandler
from utils.quiz_history import QuizHistory
import random

class QuizGenerator:
    def __init__(self):
        print("Loading pre-trained model...")
        self.model_name = "t5-base"
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        self.question_handler = QuestionHandler()
        self.history = QuizHistory()
        self.result_handler = ResultHandler()
        self.current_quiz = None

    def generate_quiz(self, topic: str, difficulty: str, num_questions: int) -> dict:
        """Generate a quiz with specified number of questions"""
        questions = []

        # Simplified, direct prompts
        template = {
            'easy': f"Create a basic question about {topic} that tests fundamental knowledge.",
            'medium': f"Create an intermediate question about {topic} that tests understanding.",
            'hard': f"Create an advanced question about {topic} that tests deep knowledge."
        }

        for _ in range(num_questions):
            prompt = f"""
            {template[difficulty]}
            Requirements:
            - Clear, single-sentence question
            - Must end with a question mark
            - Focus on specific concepts
            - No instructions or prefixes
            """

            try:
                inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
                outputs = self.model.generate(
                    inputs,
                    max_length=100,
                    min_length=20,
                    do_sample=True,
                    temperature=0.8,
                    top_p=0.9,
                    num_return_sequences=1
                )

                generated_question = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

                # Clean up the question
                clean_question = self._clean_generated_text(generated_question)

                if clean_question:
                    question = self.question_handler.create_question(
                        clean_question,
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

    def _clean_generated_text(self, text: str) -> str:
        """Clean up generated text to create a proper question"""
        # Remove multiple spaces and newlines
        text = ' '.join(text.split())

        # Remove any prefixes like "Question:", "Q:", etc.
        prefixes_to_remove = ["question:", "q:", "task:", "generate"]
        for prefix in prefixes_to_remove:
            if text.lower().startswith(prefix):
                text = text[len(prefix):].strip()

        # Ensure it ends with a question mark
        if not text.endswith('?'):
            text += '?'

        # Remove any remaining instruction-like text
        if 'generate' in text.lower() or 'create' in text.lower():
            return ""

        return text

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
