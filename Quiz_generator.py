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

        # More specific prompts for computing questions
        prompts = [
            f"Generate a multiple choice question testing knowledge of {topic}",
            f"Create a quiz question to test understanding of {topic}",
            f"Write a question that tests {topic} concepts",
            f"Form a question to evaluate {topic} knowledge"
        ]

        for _ in range(num_questions):
            prompt = f"""
            Task: {random.choice(prompts)}
            Difficulty: {difficulty}
            Format: Generate only the question without any prefixes or instructions.
            Example output format:
            What is the primary purpose of a constructor in object-oriented programming?
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
                    num_return_sequences=1,
                    no_repeat_ngram_size=2
                )

                generated_question = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

                # Clean up the generated question
                generated_question = generated_question.replace("Question:", "").strip()
                generated_question = generated_question.split("\n")[0]  # Take only first line

                # Create full question with options
                question = self.question_handler.create_question(
                    generated_question,
                    topic,
                    difficulty
                )

                if not any(q['question'] == question['question'] for q in questions):
                    questions.append(question)
                else:
                    continue

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
