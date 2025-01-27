from typing import List, Dict
import random
from transformers import T5ForConditionalGeneration, T5Tokenizer

class QuestionHandler:
    def __init__(self):
        print("Initializing question handler...")
        self.model_name = "t5-base"
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
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
            # Create a more specific prompt for generating options
            option_prompt = f"""
            Question: {question}
            Task: Generate 4 distinct answer options for this {difficulty} level question about {topic}.
            Requirements:
            - First option must be the correct answer
            - Other options must be plausible but incorrect
            - Each option must be unique and related to {topic}
            """

            # Generate options
            inputs = self.tokenizer.encode(option_prompt, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model.generate(
                inputs,
                max_length=200,
                min_length=20,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1
            )

            generated_options = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Process and clean options
            options = []
            for line in generated_options.split('\n'):
                line = line.strip()
                # Remove any numbering or bullet points
                line = line.lstrip('1234567890.-)*> ')
                if line and len(line) > 5 and line not in options:
                    options.append(line)

            # If we got enough unique options, use them
            if len(options) >= 4:
                return options[:4]

            # If we need more options, generate additional ones
            while len(options) < 4:
                additional_prompt = f"Generate another plausible but incorrect answer for: {question}"
                inputs = self.tokenizer.encode(additional_prompt, return_tensors="pt")
                outputs = self.model.generate(
                    inputs,
                    max_length=50,
                    min_length=10,
                    do_sample=True,
                    temperature=0.8
                )
                new_option = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                if new_option not in options:
                    options.append(new_option)

            return options

        except Exception as e:
            print(f"Error generating options: {e}")
            # Generate generic but topic-relevant options as last resort
            return [
                f"The most appropriate answer for this {topic} question",
                f"A related but incorrect approach in {topic}",
                f"Another possible but incorrect solution in {topic}",
                f"A common misconception about this aspect of {topic}"
            ]
