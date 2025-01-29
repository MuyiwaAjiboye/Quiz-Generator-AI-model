import streamlit as st
from utils.content_processor import ContentProcessor
from utils.result_handler import ResultHandler
import random

class QuizGenerator:
    def __init__(self):
        self.content_processor = ContentProcessor()
        self.result_handler = ResultHandler()
        self.current_quiz = None

    def generate_quiz(self, topic: str, num_questions: int):
        """Generate a quiz for the given topic"""
        sections = self.content_processor.get_content_sections(topic)

        if not sections:
            return None, f"Topic not found. Available topics: {', '.join(self.content_processor.get_available_topics())}"

        questions = []
        try:
            for _ in range(min(num_questions, len(sections))):
                section = random.choice(sections)
                sections.remove(section)  # Avoid duplicate questions

                question_dict = self.content_processor.create_question(section)
                if question_dict:
                    questions.append(question_dict)

            self.current_quiz = questions
            return questions, None

        except Exception as e:
            return None, f"Error generating quiz: {e}"

# Streamlit UI
def main():
    st.title("Quiz Generator")
    st.write("Generate quizzes from available topics with ease.")

    # Instantiate QuizGenerator
    quiz_gen = QuizGenerator()

    # Sidebar for topic selection
    st.sidebar.header("Quiz Options")
    available_topics = quiz_gen.content_processor.get_available_topics()
    topic = st.sidebar.selectbox("Select a topic", options=available_topics)
    num_questions = st.sidebar.number_input("Number of questions", min_value=1, step=1, value=5)

    # Generate Quiz Button
    if st.sidebar.button("Generate Quiz"):
        st.write(f"### Generating quiz for topic: {topic}")
        quiz, error = quiz_gen.generate_quiz(topic, num_questions)

        if error:
            st.error(error)
        else:
            for i, q in enumerate(quiz, start=1):
                st.write(f"**Q{i}:** {q['question']}")
                st.write(f"_Options:_ {', '.join(q['options'])}")
                if st.button(f"Show Answer for Q{i}", key=f"answer_{i}"):
                    st.write(f"**Answer:** {q['answer']}")

if __name__ == "__main__":
    main()