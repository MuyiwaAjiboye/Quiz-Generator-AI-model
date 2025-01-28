from typing import List, Dict
import random
from transformers import pipeline

class QuestionHandler:
    def __init__(self):
        print("Initializing question handler...")
        self.generator = pipeline('text2text-generation', model='facebook/bart-large-cnn')
        self.option_count = 4

    def create_question(self, question_text: str, topic: str, difficulty: str) -> Dict:
        """Create a complete question with options"""
        # Format the question
        question = self._format_question(question_text)

        # Generate options including correct answer
        options = self._generate_options_from_text(question, topic, difficulty)

        # Store correct answer before shuffling
        correct_answer = options[0]

        # Randomly shuffle options
        random.shuffle(options)

        return {
            'question': question,
            'options': options,
            'correct_answer': correct_answer,
            'difficulty': difficulty
        }

    def _format_question(self, text: str) -> str:
        """Format the question text properly"""
        text = text.strip()
        if not text.endswith('?'):
            text += '?'
        return text

    def _generate_options_from_text(self, question: str, topic: str, difficulty: str) -> List[str]:
        """Generate relevant options for the question"""
        try:
            # More direct prompt
            option_prompt = f"""
    Question: {question}
    Generate exactly 4 answer choices where:
    - First must be the correct answer
    - Others must be incorrect but plausible
    - Each must be brief and clear
    - All must relate to {topic}
    """

            output = self.generator(
                option_prompt,
                max_length=150,
                min_length=20,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )

            options = []
            generated_text = output[0]['generated_text']
            print(f"DEBUG: Generated options text: {generated_text}")  # Debug line

            # Process the generated text
            lines = generated_text.split('\n')
            for line in lines:
                clean_option = self._clean_option_text(line)
                if clean_option and clean_option not in options:
                    options.append(clean_option)

            # If we don't have enough options, generate more
            while len(options) < 4:
                new_option = self._generate_single_option(question, topic)
                if new_option and new_option not in options:
                    options.append(new_option)

            return options[:4]

        except Exception as e:
            print(f"Error in option generation: {e}")
            return [
                f"The main concept in {topic}",
                f"A related but incorrect concept in {topic}",
                f"Another incorrect concept in {topic}",
                f"A different incorrect concept in {topic}"
            ]

    def _generate_single_option(self, question: str, topic: str) -> str:
        """Generate a single option"""
        try:
            prompt = f"Generate one plausible but incorrect answer for this question about {topic}: {question}"
            output = self.generator(
                prompt,
                max_length=50,
                min_length=10,
                do_sample=True,
                temperature=0.8
            )
            return self._clean_option_text(output[0]['generated_text'])
        except:
            return f"An alternative concept in {topic}"

    def _clean_option_text(self, text: str) -> str:
        """Clean up generated option text"""
        text = text.strip()

        # Remove common prefixes
        prefixes = ['correct:', 'wrong:', 'option:', 'answer:', '-', '*', '1.', '2.', '3.', '4.']
        for prefix in prefixes:
            if text.lower().startswith(prefix.lower()):
                text = text[len(prefix):].strip()

        # Additional cleaning
        if len(text) < 3 or any(word in text.lower() for word in ['generate', 'option', 'answer']):
            return ""

        return text

    def _generate_additional_options(self, question: str, topic: str, num_needed: int) -> List[str]:
        """Generate additional options if needed"""
        options = []
        prompt = f"""
Generate a plausible but incorrect answer for this question:
{question}
Requirements:
- Must be related to {topic}
- Must be clearly wrong but believable
- Keep it concise"""

        for _ in range(num_needed):
            try:
                output = self.generator(
                    prompt,
                    max_length=50,
                    min_length=10,
                    do_sample=True,
                    temperature=0.8
                )

                option = self._clean_option_text(output[0]['generated_text'])
                if option and option not in options:
                    options.append(option)
            except:
                options.append(f"Alternative answer about {topic}")

        return options

    def _generate_fallback_options(self, question: str, topic: str) -> List[str]:
        """Generate basic fallback options if all else fails"""
        return [
            f"The correct answer about {topic}",
            f"A common misconception in {topic}",
            f"An incorrect approach to {topic}",
            f"Another incorrect solution for {topic}"
        ]
