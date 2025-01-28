from transformers import T5ForConditionalGeneration, T5Tokenizer
from utils.content_processor import ContentProcessor
from utils.question_handler import QuestionHandler
from utils.result_handler import ResultHandler
import torch

class QuizGenerator:
    def __init__(self):
        print("Initializing Quiz Generator...")
        print("Loading T5 model (this might take a few moments)...")
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')
        self.model = T5ForConditionalGeneration.from_pretrained('t5-base')
        self.content_processor = ContentProcessor()
        self.question_handler = QuestionHandler()
        self.result_handler = ResultHandler()
        self.current_quiz = None

    def _generate_question_from_text(self, text: str) -> str:
        """Generate a question using T5 model"""
        # Prepare input text
        input_text = f"generate question: {text}"
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt', max_length=512, truncation=True)

        # Generate question
        outputs = self.model.generate(
            input_ids,
            max_length=64,
            min_length=10,
            num_beams=4,
            no_repeat_ngram_size=2,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            num_return_sequences=1
        )

        # Decode and return the generated question
        question = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return question

    def generate_quiz(self, topic: str, num_questions: int):
        """Generate a quiz for the given topic"""
        # Get content for the topic
        content = self.content_processor.get_content(topic)
        training_data = self.content_processor.get_training_data(topic)

        if not content:
            available_topics = self.content_processor.get_available_topics()
            print(f"\nTopic not found.")
            print(f"Available topics: {', '.join(available_topics)}")
            return None

        try:
            # Split content into meaningful sections
            sections = [s.strip() for s in content.split('\n') if len(s.strip()) > 50]
            questions = []

            for _ in range(min(num_questions, len(sections))):
                section = sections[_]

                # Generate question using T5
                generated_question = self._generate_question_from_text(section)

                # Use training data to help generate better options
                if training_data:
                    # Use existing options from training data as templates
                    template = random.choice(training_data)
                    options_style = template['wrong_answers']
                else:
                    # Generate basic options if no training data
                    options_style = [
                        f"This is incorrect because...",
                        f"This is a common misconception...",
                        f"This is not accurate because..."
                    ]

                # Create question dict with generated content
                question = {
                    'question': generated_question,
                    'options': [section] + options_style[:3],  # Use first 3 wrong answers
                    'correct_answer': section
                }

                # Shuffle options
                random.shuffle(question['options'])
                questions.append(question)

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

                print("\nGenerating quiz using T5 model...")
                quiz = self.generate_quiz(topic, num_questions)

                if quiz:
                    # Display the quiz questions
                    self.result_handler.display_quiz(quiz)

                    # Ask if user wants to see answers
                    while True:
                        show_answers = input("\nWould you like to see the answers? (yes/no): ").lower()
                        if show_answers in ['yes', 'no']:
                            break
                        print("Please enter 'yes' or 'no'")

                    # Show answers if requested
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
        print("Starting Quiz Generator...")
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
