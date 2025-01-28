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
            option_prompt = f"""
            Question: {question}
            Generate four concise answer options.
            - First option must be the correct answer
            - Other options must be plausible but incorrect
            - Each option should be brief and clear
            - No explanations or prefixes
            """

            inputs = self.tokenizer.encode(option_prompt, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model.generate(
                inputs,
                max_length=100,
                min_length=10,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1
            )

            options = []
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Clean and extract options
            for line in generated_text.split('\n'):
                clean_option = self._clean_option_text(line)
                if clean_option and clean_option not in options:
                    options.append(clean_option)

            # Ensure we have exactly 4 options
            while len(options) < 4:
                fallback = self._generate_fallback_option(question, topic)
                if fallback and fallback not in options:
                    options.append(fallback)

            return options[:4]

        except Exception as e:
            print(f"Error generating options: {e}")
            return self._generate_fallback_options(question, topic)

    def _clean_option_text(self, text: str) -> str:
        """Clean up generated option text"""
        # Remove prefixes and clean up
        text = text.strip()
        prefixes = ['option:', 'answer:', 'correct:', 'incorrect:', '-', '*', '1.', '2.', '3.', '4.']
        for prefix in prefixes:
            if text.lower().startswith(prefix.lower()):
                text = text[len(prefix):].strip()

        # Remove if too short or contains unwanted patterns
        if len(text) < 3 or 'generate' in text.lower() or 'option' in text.lower():
            return ""

        return text

    def _generate_fallback_option(self, question: str, topic: str) -> str:
        """Generate a single fallback option"""
        try:
            prompt = f"Generate a brief, incorrect answer for: {question}"
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            outputs = self.model.generate(
                inputs,
                max_length=50,
                min_length=5,
                do_sample=True,
                temperature=0.8
            )
            return self._clean_option_text(self.tokenizer.decode(outputs[0], skip_special_tokens=True))
        except:
            return f"Alternative answer about {topic}"

    def _generate_fallback_options(self, question: str, topic: str) -> List[str]:
        """Generate options one by one if the batch generation fails"""
        options = []
        prompts = [
            f"What is the correct answer to: {question}",
            f"Generate an incorrect but plausible answer to: {question}",
            f"Generate another incorrect but plausible answer to: {question}",
            f"Generate one more incorrect but plausible answer to: {question}"
        ]

        for prompt in prompts:
            try:
                inputs = self.tokenizer.encode(prompt, return_tensors="pt")
                outputs = self.model.generate(
                    inputs,
                    max_length=50,
                    min_length=10,
                    do_sample=True,
                    temperature=0.8
                )
                option = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
                if option and option not in options:
                    options.append(option)
            except:
                options.append(f"Option {len(options) + 1} for {topic}")

        return options[:4]
