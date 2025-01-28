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

        # More directive prompts for different difficulties
        prompts = {
            'easy': [
                f"What is the basic purpose of {topic}?",
                f"Which HTML tag is used for {topic}?",
                f"What is the main function of {topic}?",
                f"How do you create a {topic}?"
            ],
            'medium': [
                f"What is the difference between {topic} and related concepts?",
                f"How does {topic} work in practice?",
                f"When should you use {topic}?",
                f"What are the key features of {topic}?"
            ],
            'hard': [
                f"What are the advanced applications of {topic}?",
                f"How do you optimize {topic}?",
                f"What are the best practices for {topic}?",
                f"Explain the complex aspects of {topic}?"
            ]
        }

        for _ in range(num_questions):
            try:
                # Select a random prompt template
                base_prompt = random.choice(prompts[difficulty])

                # Generate the question
                output = self.generator(
                    base_prompt,
                    max_length=100,
                    min_length=20,
                    do_sample=True,
                    temperature=0.8,
                    top_p=0.9,
                    num_beams=4
                )

                generated_text = output[0]['generated_text'].strip()
                print(f"Generated question: {generated_text}")  # Debug line

                # Clean up the question
                clean_question = self._clean_question(generated_text)

                if clean_question and "generate" not in clean_question.lower():
                    question = self.question_handler.create_question(
                        clean_question,
                        topic,
                        difficulty
                    )
                    questions.append(question)
                    print(f"Successfully generated question: {clean_question}")
                else:
                    print("Retrying question generation...")
                    continue

            except Exception as e:
                print(f"Error during question generation: {e}")
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
        # Split into lines and process each one
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Look for a line that ends with a question mark
            if line.endswith('?'):
                # Remove common prefixes
                prefixes = ["question:", "q:", "answer:", "example:"]
                for prefix in prefixes:
                    if line.lower().startswith(prefix):
                        line = line[len(prefix):].strip()
                return line

        # If no line ends with ?, try to fix the text
        text = text.strip()
        if text and not text.endswith('?'):
            text += '?'
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

            # Check if questions were generated successfully
            if not quiz['questions']:
                print("\nFailed to generate questions. Please try again.")
                continue

            user_answers = quiz_gen.result_handler.take_quiz(quiz)

            # Only show results if there are answers
            if user_answers:
                quiz_gen.result_handler.show_results(quiz, user_answers)

if __name__ == "__main__":
    main()
