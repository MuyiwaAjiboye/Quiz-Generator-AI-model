import random
from transformers import T5ForConditionalGeneration, T5Tokenizer

class QuestionHandler:
    def __init__(self):
        print("Initializing Question Handler...")
        # Initialize T5 model and tokenizer for option generation
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')
        self.model = T5ForConditionalGeneration.from_pretrained('t5-base')

    def create_questions(self, training_data: list, content_section: str, num_questions: int) -> list:
        """Create questions using T5 model and training data"""
        questions = []

        try:
            for _ in range(num_questions):
                # Generate question using T5
                question_text = self._generate_question(content_section)

                # Generate options including correct answer
                options = self._generate_options(content_section, question_text, training_data)

                if question_text and options:
                    question = {
                        'question': question_text,
                        'options': options['all_options'],
                        'correct_answer': options['correct_answer']
                    }
                    questions.append(question)

        except Exception as e:
            print(f"Error in question creation: {e}")

        return questions

    def _generate_question(self, content: str) -> str:
        """Generate a question using T5 model"""
        try:
            # Prepare input for question generation
            input_text = f"generate question: {content}"
            input_ids = self.tokenizer.encode(
                input_text,
                return_tensors='pt',
                max_length=512,
                truncation=True
            )

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

            # Decode and clean up the generated question
            question = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return self._clean_question(question)

        except Exception as e:
            print(f"Error in question generation: {e}")
            return None

    def _generate_options(self, content: str, question: str, training_data: list) -> dict:
        """Generate options including correct and wrong answers"""
        try:
            # Extract correct answer using T5
            answer_input = f"answer question: {question} context: {content}"
            answer_ids = self.tokenizer.encode(
                answer_input,
                return_tensors='pt',
                max_length=512,
                truncation=True
            )

            answer_outputs = self.model.generate(
                answer_ids,
                max_length=64,
                min_length=5,
                num_beams=4,
                no_repeat_ngram_size=2,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1
            )

            correct_answer = self.tokenizer.decode(answer_outputs[0], skip_special_tokens=True)

            # Generate wrong options
            wrong_options = self._generate_wrong_options(
                content,
                correct_answer,
                question,
                training_data
            )

            # Combine and shuffle options
            all_options = [correct_answer] + wrong_options
            random.shuffle(all_options)

            return {
                'all_options': all_options,
                'correct_answer': correct_answer
            }

        except Exception as e:
            print(f"Error in option generation: {e}")
            return None

    def _generate_wrong_options(self, content: str, correct_answer: str, question: str, training_data: list) -> list:
        """Generate wrong options using T5 and training data"""
        wrong_options = []

        try:
            # First, try to use training data as templates
            if training_data:
                template = random.choice(training_data)
                wrong_options.extend(template['wrong_answers'][:2])

            # Generate additional wrong options using T5
            wrong_input = f"generate incorrect answer: {question} correct answer: {correct_answer}"
            wrong_ids = self.tokenizer.encode(
                wrong_input,
                return_tensors='pt',
                max_length=512,
                truncation=True
            )

            wrong_outputs = self.model.generate(
                wrong_ids,
                max_length=64,
                min_length=5,
                num_beams=4,
                no_repeat_ngram_size=2,
                do_sample=True,
                temperature=0.9,
                top_p=0.9,
                num_return_sequences=2
            )

            # Add model-generated wrong options
            for output in wrong_outputs:
                wrong_option = self.tokenizer.decode(output, skip_special_tokens=True)
                if wrong_option != correct_answer and wrong_option not in wrong_options:
                    wrong_options.append(wrong_option)

            # Ensure we have exactly 3 wrong options
            while len(wrong_options) < 3:
                wrong_options.append(f"Alternative explanation of {content.split()[0]}")

            return wrong_options[:3]  # Return exactly 3 wrong options

        except Exception as e:
            print(f"Error in wrong option generation: {e}")
            return [
                f"Alternative explanation 1",
                f"Alternative explanation 2",
                f"Alternative explanation 3"
            ]

    def _clean_question(self, question: str) -> str:
        """Clean up the generated question"""
        question = question.strip()

        # Remove common prefixes
        prefixes = ['question:', 'q:', 'generate question:', 'ask:']
        for prefix in prefixes:
            if question.lower().startswith(prefix):
                question = question[len(prefix):].strip()

        # Ensure question ends with question mark
        if not question.endswith('?'):
            question += '?'

        return question

    def validate_question(self, question: dict) -> bool:
        """Validate generated question and options"""
        if not question.get('question') or not question.get('options'):
            return False

        # Check if question ends with question mark
        if not question['question'].endswith('?'):
            return False

        # Check if we have exactly 4 options
        if len(question['options']) != 4:
            return False

        # Check if correct answer is in options
        if question['correct_answer'] not in question['options']:
            return False

        return True
