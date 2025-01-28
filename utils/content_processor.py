from content_database import COMPUTING_CONTENT, TRAINING_DATA
import random

class ContentProcessor:
    def __init__(self):
        self.content = COMPUTING_CONTENT
        self.training_data = TRAINING_DATA

    def get_content(self, topic: str) -> str:
        """Get content for a specific topic"""
        topic = topic.lower()
        if topic in self.content:
            # Split content into manageable sections
            sections = [s.strip() for s in self.content[topic].split('\n')
                       if len(s.strip()) > 50]  # Only sections with substantial content
            return '\n'.join(sections)
        return None

    def get_training_data(self, topic: str) -> list:
        """Get training data for topic"""
        topic = topic.lower()
        if topic in self.training_data:
            return self.training_data[topic]
        return []

    def get_available_topics(self) -> list:
        """Get list of available topics"""
        return list(self.content.keys())

    def get_section_by_difficulty(self, topic: str, difficulty: str) -> str:
        """Get content section based on difficulty"""
        content = self.get_content(topic)
        if not content:
            return None

        sections = content.split('\n\n')  # Split by double newline to get major sections

        # Filter sections by approximate difficulty
        if difficulty == 'easy':
            # Get introductory sections
            suitable_sections = [s for s in sections if len(s.split()) < 100]
        elif difficulty == 'medium':
            # Get middle sections
            suitable_sections = [s for s in sections if 100 <= len(s.split()) <= 200]
        else:  # hard
            # Get more detailed sections
            suitable_sections = [s for s in sections if len(s.split()) > 200]

        return random.choice(suitable_sections) if suitable_sections else random.choice(sections)

    def get_context_for_question(self, topic: str, question_type: str) -> str:
        """Get relevant context for generating specific types of questions"""
        content = self.get_content(topic)
        if not content:
            return None

        sections = [s.strip() for s in content.split('\n') if len(s.strip()) > 50]

        # Select appropriate sections based on question type
        if question_type == 'definition':
            # Look for sections with 'is' or 'are'
            suitable_sections = [s for s in sections if ' is ' in s.lower() or ' are ' in s.lower()]
        elif question_type == 'comparison':
            # Look for sections with comparing words
            compare_words = ['versus', 'vs', 'compared to', 'while', 'whereas']
            suitable_sections = [s for s in sections
                               if any(word in s.lower() for word in compare_words)]
        elif question_type == 'application':
            # Look for sections with practical examples
            practical_words = ['example', 'application', 'use case', 'practice']
            suitable_sections = [s for s in sections
                               if any(word in s.lower() for word in practical_words)]
        else:
            suitable_sections = sections

        return random.choice(suitable_sections) if suitable_sections else random.choice(sections)

    def extract_key_concepts(self, text: str) -> list:
        """Extract key concepts from text for generating distractors"""
        # Split text into sentences
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]

        # Extract key phrases (simplified version)
        key_concepts = []
        for sentence in sentences:
            # Look for definitions or key points
            if (' is ' in sentence or ' are ' in sentence or
                ' refers to ' in sentence or ' means ' in sentence):
                key_concepts.append(sentence)

        return key_concepts

    def get_related_concepts(self, topic: str, concept: str) -> list:
        """Get related concepts for generating plausible wrong answers"""
        content = self.get_content(topic)
        if not content:
            return []

        # Split into sentences and find related ones
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
        related = []

        # Simple similarity check (can be improved with NLP techniques)
        concept_words = set(concept.lower().split())
        for sentence in sentences:
            sentence_words = set(sentence.lower().split())
            # If there's some word overlap but not too much
            common_words = concept_words.intersection(sentence_words)
            if common_words and len(common_words) < len(concept_words):
                related.append(sentence)

        return related[:3]  # Return top 3 related concepts
