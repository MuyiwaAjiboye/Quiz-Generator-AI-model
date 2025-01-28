from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import random

class ContentProcessor:
    def __init__(self):
        print("Initializing Content Processor with T5 model...")
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')
        self.model = T5ForConditionalGeneration.from_pretrained('t5-base')
        self.content = {}
        self.load_content()

    def load_content(self):
        """Load content from content_database.py"""
        from content_database import COMPUTING_CONTENT
        self.content = COMPUTING_CONTENT

    def get_content(self, topic: str) -> str:
        """Get content for a specific topic"""
        return self.content.get(topic.lower(), None)

    def get_available_topics(self) -> list:
        """Get list of available topics"""
        return list(self.content.keys())

    def generate_question_from_section(self, section: str) -> dict:
        """Generate a question from a content section using T5"""
        try:
            # Generate question
            question = self._generate_question(section)
            if not question:
                return None

            # Generate correct answer (using a different prompt)
            correct_answer = self._generate_answer(question, section)
            if not correct_answer:
                return None

            # Generate wrong options
            wrong_options = self._generate_wrong_options(section, correct_answer)

            # Combine all options
            options = [correct_answer] + wrong_options
            random.shuffle(options)

            return {
                'question': question,
                'options': options,
                'correct_answer': correct_answer
            }
        except Exception as e:
            print(f"Error in question generation: {e}")
            return None

    def _generate_question(self, text: str) -> str:
        """Generate a question using T5"""
        try:
            input_text = f"generate question: {text}"
            input_ids = self.tokenizer.encode(
                input_text,
                return_tensors='pt',
                max_length=512,
                truncation=True
            )

            outputs = self.model.generate(
                input_ids,
                max_length=64,
                min_length=20,
                 do_sample=True,
                num_beams=5,
                no_repeat_ngram_size=2,

                temperature=0.7,
                top_p=0.95
            )

            question = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            question = self._clean_question(question)
            return question
        except Exception as e:
            print(f"Error generating question: {e}")
            return None

    def _generate_answer(self, question: str, context: str) -> str:
        """Generate correct answer using T5"""
        try:
            input_text = f"answer: {question} context: {context}"
            input_ids = self.tokenizer.encode(
                input_text,
                return_tensors='pt',
                max_length=512,
                truncation=True
            )

            outputs = self.model.generate(
                input_ids,
                max_length=128,
                min_length=20,
                do_sample=True,
                num_beams=4,
                temperature=0.7,
                top_p=0.9
            )

            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return answer.strip()
        except Exception as e:
            print(f"Error generating answer: {e}")
            return None

    def _generate_wrong_options(self, context: str, correct_answer: str, num_options=3) -> list:
        """Generate wrong options using T5"""
        try:
            wrong_options = []
            input_prompts = [
                f"generate incorrect but plausible answer: {context}",
                f"generate different explanation: {context}",
                f"generate alternative answer: {context}"
            ]

            for prompt in input_prompts:
                input_ids = self.tokenizer.encode(
                    prompt,
                    return_tensors='pt',
                    max_length=512,
                    truncation=True
                )

                outputs = self.model.generate(
                    input_ids,
                    max_length=64,
                    min_length=10,
                    do_sample=True,
                    num_beams=4,
                    temperature=0.8,
                    top_p=0.9,
                    no_repeat_ngram_size=2
                )

                wrong_option = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                if wrong_option and wrong_option != correct_answer and wrong_option not in wrong_options:
                    wrong_options.append(wrong_option.strip())

            # If we didn't generate enough wrong options, add some generic ones
            while len(wrong_options) < num_options:
                fallback = f"Alternative explanation {len(wrong_options) + 1} for {context.split()[0]}"
                if fallback not in wrong_options:
                    wrong_options.append(fallback)

            return wrong_options[:num_options]
        except Exception as e:
            print(f"Error generating wrong options: {e}")
            return [f"Alternative explanation {i+1}" for i in range(num_options)]

    def _clean_question(self, question: str) -> str:
        """Clean up the generated question"""
        question = question.strip()

        # Remove common prefixes
        prefixes = ['question:', 'q:', 'generate question:', 'ask:', 'answer:']
        for prefix in prefixes:
            if question.lower().startswith(prefix):
                question = question[len(prefix):].strip()

        # Ensure question ends with question mark
        if not question.endswith('?'):
            question += '?'

        return question

    def get_content_sections(self, topic: str) -> list:
        """Split content into meaningful sections"""
        content = self.get_content(topic)
        if not content:
            return []

        # Split content into sections
        sections = []
        current_section = []

        for line in content.split('\n'):
            line = line.strip()
            if line:
                if line.endswith(':'):  # New section header
                    if current_section:
                        sections.append(' '.join(current_section))
                    current_section = [line]
                elif line.startswith('-'):  # List item
                    if current_section:
                        sections.append(' '.join(current_section))
                    current_section = [line[1:].strip()]
                else:
                    current_section.append(line)

        # Add the last section
        if current_section:
            sections.append(' '.join(current_section))

        # Filter out very short sections and clean them
        return [s.strip() for s in sections if len(s.strip()) > 50]
