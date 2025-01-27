from typing import List, Dict
import random
from transformers import pipeline

class QuestionHandler:
    def __init__(self):
        self.option_count = 4
        print("Initializing question handler...")
        self.option_generator = pipeline('text2text-generation', model='facebook/bart-large-cnn')

    def create_question(self, generated_text: str, topic: str, difficulty: str) -> Dict:
        """Create a complete question with relevant options"""
        # Clean and format the generated question
        question = self._format_question(generated_text)

        # Generate options using AI
        options = self._generate_options_from_text(question, topic, difficulty)

        # First option is correct, then shuffle
        correct_answer = options[0]  # The AI generates correct answer first
        random.shuffle(options)

        return {
            'question': question,
            'options': options,
            'correct_answer': correct_answer,
            'difficulty': difficulty
        }

    def _format_question(self, text: str) -> str:
        """Format the generated text into a clear question"""
        # Split into lines and get the first line (the question)
        lines = text.strip().split('\n')
        question = lines[0].strip()

        # Ensure it's a question
        if not question.endswith('?'):
            question += '?'

        return question

    def _generate_options_from_text(self, question: str, topic: str, difficulty: str) -> List[str]:
        """Generate relevant options using AI"""
        try:
            # Create a specific prompt for generating options
            option_prompt = f"Generate 4 multiple choice answers for this question: {question}"

            # Generate options using the model
            output = self.option_generator(
                option_prompt,
                max_length=150,
                min_length=20,
                temperature=0.7,
                do_sample=True,
                num_return_sequences=1
            )

            # Process the generated options
            generated_text = output[0]['generated_text']
            options = [
                line.strip()
                for line in generated_text.split('\n')
                if line.strip() and not line.strip().lower().startswith(('question:', 'generate', 'options'))
            ]

            # If we got enough options, use them
            if len(options) >= 4:
                return options[:4]

            # If we need more options
            default_options = [
                f"Correct answer for {topic}",
                f"First incorrect answer for {topic}",
                f"Second incorrect answer for {topic}",
                f"Third incorrect answer for {topic}"
            ]

            # Combine generated options with default ones if needed
            while len(options) < 4:
                options.append(default_options[len(options)])

            return options

        except Exception as e:
            print(f"Error generating options: {e}")
            return [
                f"Correct answer for {topic}",
                f"First incorrect answer for {topic}",
                f"Second incorrect answer for {topic}",
                f"Third incorrect answer for {topic}"
            ]
