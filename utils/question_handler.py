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
            For the question: {question}
            Generate four answer choices where only one is correct.
            Format:
            Correct: [The correct answer]
            Wrong1: [A plausible but incorrect answer]
            Wrong2: [Another plausible but incorrect answer]
            Wrong3: [Another plausible but incorrect answer]
            """

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

            # Extract options, looking for the format we specified
            options = []
            for line in generated_options.split('\n'):
                line = line.strip()
                if line.startswith(('Correct:', 'Wrong1:', 'Wrong2:', 'Wrong3:')):
                    option = line.split(':', 1)[1].strip()
                    if option and len(option) > 1:
                        options.append(option)

            if len(options) >= 4:
                return options[:4]

            # If we don't get proper options, generate them one by one
            return self._generate_fallback_options(question, topic)

        except Exception as e:
            print(f"Error generating options: {e}")
            return self._generate_fallback_options(question, topic)

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
