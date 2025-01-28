import random

class ContentProcessor:
    def __init__(self):
        print("Initializing Content Processor...")
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
        """Generate a question from a content section"""
        try:
            # Create question from section
            question = self._create_question(section)
            correct_answer = section
            wrong_options = self._generate_wrong_options(section)

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

    def _create_question(self, section: str) -> str:
        """Create a question based on the content"""
        # Get the main concept (first few words)
        main_concept = ' '.join(section.split()[:3])

        # Question templates
        templates = [
            f"Which of the following best describes {main_concept}?",
            f"What is the correct explanation of {main_concept}?",
            f"Which statement accurately describes {main_concept}?",
            f"What is the proper definition of {main_concept}?"
        ]

        return random.choice(templates)

    def _generate_wrong_options(self, correct_answer: str) -> list:
        """Generate plausible but incorrect options"""
        # Get the main concept
        main_concept = ' '.join(correct_answer.split()[:3])

        wrong_options = [
            f"{main_concept} is a tool used primarily for system optimization and debugging.",
            f"{main_concept} is an advanced feature used only in enterprise-level applications.",
            f"{main_concept} is a deprecated concept that has been replaced by newer alternatives."
        ]

        return wrong_options

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
