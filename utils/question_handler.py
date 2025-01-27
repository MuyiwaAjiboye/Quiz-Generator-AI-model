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
            option_prompt = f"""
    Question: {question}
    Task: Generate exactly 4 brief answer options for this {difficulty} question about {topic}.
    Format: One answer per line.
    The first line must be the correct answer.

    Example format:
    Correct answer here
    Wrong answer 1
    Wrong answer 2
    Wrong answer 3
    """

            output = self.option_generator(
                option_prompt,
                max_length=150,
                min_length=20,
                temperature=0.7,
                do_sample=True,
                num_return_sequences=1
            )

            # Extract options, skip any lines that look like instructions
            options = []
            generated_lines = output[0]['generated_text'].split('\n')
            for line in generated_lines:
                line = line.strip()
                if line and not any(word in line.lower() for word in ['question:', 'task:', 'format:', 'example:']):
                    options.append(line)

            if len(options) >= 4:
                return options[:4]

            # If we don't have enough options, create topic-specific ones
            topic_options = [
                f"This is the correct answer about {topic}",
                f"This is incorrect but plausible for {topic}",
                f"This is another incorrect option for {topic}",
                f"This is the final incorrect option for {topic}"
            ]

            while len(options) < 4:
                options.append(topic_options[len(options)])

            return options

        except Exception as e:
            print(f"Error in option generation: {e}")
            return [
                f"This is the correct answer about {topic}",
                f"This is incorrect but plausible for {topic}",
                f"This is another incorrect option for {topic}",
                f"This is the final incorrect option for {topic}"
            ]
