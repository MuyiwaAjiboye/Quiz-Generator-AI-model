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

        # More specific computing-related prompt
        prompt_template = {
            'easy': f"Generate a basic multiple choice question testing {topic} knowledge. The question should be clear and end with a question mark.",
            'medium': f"Create an intermediate multiple choice question about {topic}. The question should be specific and end with a question mark.",
            'hard': f"Write an advanced multiple choice question about {topic}. The question should be challenging and end with a question mark."
        }

        for _ in range(num_questions):
            try:
                # Generate the question
                output = self.generator(
                    prompt_template[difficulty],
                    max_length=100,
                    min_length=20,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9
                )

                generated_text = output[0]['generated_text'].strip()
                print(f"DEBUG: Generated raw text: {generated_text}")  # Debug line

                # Clean up the question
                clean_question = self._clean_question(generated_text)
                print(f"DEBUG: Cleaned question: {clean_question}")  # Debug line

                if clean_question:
                    # Create question with options
                    question = self.question_handler.create_question(
                        clean_question,
                        topic,
                        difficulty
                    )
                    questions.append(question)
                    print(f"Question generated successfully: {clean_question}")  # Success message
                else:
                    print("Failed to generate a valid question, trying again...")
                    continue

            except Exception as e:
                print(f"Error during question generation: {e}")
                continue

        # If we couldn't generate any questions
        if not questions:
            print("\nTroubleshooting tips:")
            print("1. Try a more specific computing topic")
            print("2. Check if the topic is computing-related")
            print("3. Try a different difficulty level")
            print("4. Make sure the topic is spelled correctly")

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
