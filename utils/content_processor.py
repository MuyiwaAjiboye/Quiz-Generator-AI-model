import random
from collections import defaultdict
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import re

class ContentProcessor:
    def __init__(self):
        print("Initializing Content Processor...")
        # Download required NLTK data (only needed once)
        try:
            # Download necessary NLTK components
            nltk.download('punkt')     # For tokenization
            nltk.download('averaged_perceptron_tagger')  # For POS tagging
            nltk.download('stopwords')  # For removing common words
        except Exception as e:
            print(f"Warning: NLTK download failed: {e}")

        # Initialize NLP tools and patterns
        self.stop_words = set(stopwords.words('english'))
        self.content = {}

        # Patterns for different types of content
        self.patterns = {
            'definition': r'(?:is|are|refers to|means|defines)',
            'example': r'(?:example|such as|like|instance)',
            'process': r'(?:steps|procedure|process|method)',
            'comparison': r'(?:compared to|versus|whereas|while)',
            'characteristic': r'(?:features|properties|attributes)'
        }

        self.load_content()

    def load_content(self):
        """Load content from content_database.py"""
        from content_database import COMPUTING_CONTENT
        self.content = COMPUTING_CONTENT

    def _process_text(self, text: str) -> dict:
        """
        Process text using NLP techniques
        Returns a dictionary containing:
        - sentences: List of individual sentences
        - words: List of important words (excluding stop words)
        - pos_tags: List of (word, POS tag) pairs
        - key_terms: Set of important terms
        """
        try:
            # Split text into sentences
            sentences = sent_tokenize(text)

            # Process each sentence
            all_words = []
            all_pos_tags = []
            key_terms = set()

            for sentence in sentences:
                # Tokenize words
                words = word_tokenize(sentence)

                # Remove stop words and punctuation
                words = [word for word in words
                        if word.lower() not in self.stop_words
                        and word.isalnum()]

                # Get POS tags
                pos_tags = pos_tag(words)

                # Collect important terms based on POS tags
                for word, tag in pos_tags:
                    if tag.startswith(('NN', 'VB', 'JJ')):  # Nouns, Verbs, Adjectives
                        key_terms.add(word)

                all_words.extend(words)
                all_pos_tags.extend(pos_tags)

            return {
                'sentences': sentences,
                'words': all_words,
                'pos_tags': all_pos_tags,
                'key_terms': key_terms
            }
        except Exception as e:
            print(f"Error processing text: {e}")
            return {
                'sentences': [text],
                'words': text.split(),
                'pos_tags': [],
                'key_terms': set()
            }

    def create_question(self, section: str) -> dict:
        """Generate a question from the given section using NLP analysis"""
        try:
            # Process the text
            processed = self._process_text(section)

            # Determine the content type
            content_type = self._identify_content_type(section, processed)

            # Get main concepts
            main_concept = self._get_main_concept(processed)

            # Generate question
            question = self._generate_question(main_concept, content_type)

            # Generate options
            wrong_options = self._generate_wrong_options(main_concept, content_type, processed)

            # Combine and shuffle options
            options = [section] + wrong_options
            random.shuffle(options)

            return {
                'question': question,
                'options': options,
                'correct_answer': section
            }
        except Exception as e:
            print(f"Error creating question: {e}")
            return None

    def _identify_content_type(self, text: str, processed: dict) -> str:
        """
        Identify the type of content using patterns and POS analysis
        Returns: 'definition', 'example', 'process', 'comparison', or 'general'
        """
        text_lower = text.lower()

        # Check each pattern
        for content_type, pattern in self.patterns.items():
            if re.search(pattern, text_lower):
                return content_type

        # If no pattern matches, analyze POS tags
        pos_sequence = [tag for _, tag in processed['pos_tags']]

        if 'VBZ' in pos_sequence and pos_sequence.count('NN') > 2:
            return 'definition'
        elif pos_sequence.count('VB') > 2:
            return 'process'

        return 'general'

    def _get_main_concept(self, processed: dict) -> str:
        """Extract the main concept from processed text"""
        # First try to find proper nouns
        proper_nouns = [word for word, tag in processed['pos_tags']
                       if tag == 'NNP']
        if proper_nouns:
            return proper_nouns[0]

        # Then try regular nouns
        nouns = [word for word, tag in processed['pos_tags']
                if tag.startswith('NN')]
        if nouns:
            return nouns[0]

        # Fallback to first key term
        if processed['key_terms']:
            return list(processed['key_terms'])[0]

        # Last resort: first word
        return processed['words'][0] if processed['words'] else "this concept"

    def _generate_question(self, concept: str, content_type: str) -> str:
        """Generate an appropriate question based on content type"""
        templates = {
            'definition': [
                f"Which of the following best describes {concept}?",
                f"What is the correct definition of {concept}?",
                f"How would you define {concept}?"
            ],
            'example': [
                f"Which is a correct example of {concept}?",
                f"What demonstrates the use of {concept}?",
                f"How is {concept} typically used?"
            ],
            'process': [
                f"What is the correct process involving {concept}?",
                f"How does {concept} work?",
                f"What are the steps in {concept}?"
            ],
            'comparison': [
                f"How does {concept} compare to other approaches?",
                f"What distinguishes {concept} from alternatives?",
                f"What is unique about {concept}?"
            ],
            'general': [
                f"Which statement about {concept} is correct?",
                f"What is true about {concept}?",
                f"Which of the following correctly describes {concept}?"
            ]
        }

        return random.choice(templates.get(content_type, templates['general']))

    def _generate_wrong_options(self, concept: str, content_type: str, processed: dict) -> list:
        """Generate wrong options based on content type and analysis"""
        wrong_options = []

        # Get some key terms for variation
        key_terms = list(processed['key_terms'])

        templates = {
            'definition': [
                f"{concept} is a different concept that involves {random.choice(key_terms) if key_terms else 'different processes'}.",
                f"{concept} refers to an unrelated technology in software development.",
                f"This is an incorrect interpretation of {concept}."
            ],
            'example': [
                f"This example incorrectly applies {concept}.",
                f"This is a common misconception about using {concept}.",
                f"This represents an invalid use case for {concept}."
            ],
            'process': [
                f"This process is not how {concept} actually works.",
                f"These steps would lead to incorrect implementation of {concept}.",
                f"This is an outdated approach to {concept}."
            ],
            'comparison': [
                f"This comparison misrepresents the features of {concept}.",
                f"This incorrectly contrasts {concept} with other methods.",
                f"This comparison is based on outdated information about {concept}."
            ],
            'general': [
                f"This statement contains incorrect information about {concept}.",
                f"This is a common misunderstanding about {concept}.",
                f"This represents an incorrect view of {concept}."
            ]
        }

        # Get templates for the content type or use general templates
        option_templates = templates.get(content_type, templates['general'])
        wrong_options.extend(option_templates)

        return wrong_options[:3]  # Return exactly 3 wrong options

    def get_content_sections(self, topic: str) -> list:
        """Split content into meaningful sections"""
        content = self.content.get(topic.lower())
        if not content:
            return []

        # Split into sections
        sections = []
        current_section = []

        for line in content.split('\n'):
            line = line.strip()
            if not line:
                if current_section:
                    sections.append(' '.join(current_section))
                    current_section = []
            elif line.endswith(':'):
                if current_section:
                    sections.append(' '.join(current_section))
                current_section = [line]
            elif line.startswith('-'):
                sections.append(line[1:].strip())
            else:
                current_section.append(line)

        if current_section:
            sections.append(' '.join(current_section))

        # Filter out very short sections
        return [s for s in sections if len(s.split()) > 5]

    def get_available_topics(self) -> list:
        """Get list of available topics"""
        return list(self.content.keys())
