import streamlit as st
from utils.content_processor import ContentProcessor
from utils.result_handler import ResultHandler
import random
from datetime import datetime
import os
import json


class QuizGenerator:
    def __init__(self):
        if 'quiz_generator_initialized' not in st.session_state:
            with st.spinner('Initializing Quiz Generator...'):
                self.content_processor = ContentProcessor()
                self.result_handler = ResultHandler()
                st.session_state.quiz_generator_initialized = True

    def generate_quiz(self, topic: str, num_questions: int):
        """Generate a quiz for the given topic"""
        sections = self.content_processor.get_content_sections(topic)
        if not sections:
            st.error(f"Topic not found. Please select a valid topic from the dropdown.")
            return None

        questions = []
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(min(num_questions, len(sections))):
                status_text.text(f"Generating question {i + 1}/{num_questions}")
                progress_bar.progress((i + 1) / num_questions)

                section = random.choice(sections)
                sections.remove(section)  # Avoid duplicate questions
                question_dict = self.content_processor.create_question(section)
                if question_dict:
                    questions.append(question_dict)

            progress_bar.empty()
            status_text.empty()
            return questions

        except Exception as e:
            st.error(f"Error generating quiz: {e}")
            return None


def initialize_session_state():
    if 'quiz_gen' not in st.session_state:
        st.session_state.quiz_gen = QuizGenerator()
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = None
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False


def reset_quiz():
    st.session_state.current_quiz = None
    st.session_state.user_answers = {}
    st.session_state.quiz_submitted = False


def save_quiz_result(quiz, user_answers):
    results_dir = "quiz_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(results_dir, f"quiz_result_{timestamp}.json")

    result_data = {
        "timestamp": timestamp,
        "questions": [],
        "user_answers": user_answers
    }

    for q in quiz:
        question_data = {
            "question": q['question'],
            "options": q['options'],
            "correct_answer": q['correct_answer']
        }
        result_data["questions"].append(question_data)

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=4, ensure_ascii=False)
        st.success(f"Quiz results saved to: {filename}")
    except Exception as e:
        st.error(f"Error saving quiz results: {e}")


def main():
    st.set_page_config(page_title="Quiz Generator", page_icon="📚", layout="wide")
    st.title("📚 Interactive Quiz Generator")

    initialize_session_state()

    # Main quiz interface
    st.header("Generate a New Quiz")

    with st.form("quiz_parameters", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            available_topics = st.session_state.quiz_gen.content_processor.get_available_topics()
            topic = st.selectbox(
                "Select Topic",
                options=available_topics,
                key="topic_selector"
            ).lower()

        with col2:
            num_questions = st.number_input("Number of Questions",
                                          min_value=1,
                                          max_value=10,
                                          value=3)

        generate_button = st.form_submit_button("Generate Quiz")

    if generate_button and topic:
        reset_quiz()
        st.session_state.current_quiz = st.session_state.quiz_gen.generate_quiz(topic, num_questions)

    # Display quiz if it exists
    if st.session_state.current_quiz:
        st.header("Take the Quiz")

        for i, question in enumerate(st.session_state.current_quiz):
            st.subheader(f"Question {i + 1}")
            st.write(question['question'])

            # Format options with letters (A, B, C, D)
            options = question['options']
            if options:
                selected_answer = st.radio(
                    "Select your answer:",
                    range(len(options)),
                    format_func=lambda x: f"{chr(65 + x)}. {options[x]}",
                    key=f"question_{i}",
                    index=None
                )

                if selected_answer is not None:
                    st.session_state.user_answers[i] = options[selected_answer]

            st.markdown("---")

        # Show submit button only if all questions are answered
        all_answered = len(st.session_state.user_answers) == len(st.session_state.current_quiz)

        if all_answered:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Submit Quiz", key="submit_quiz"):
                    st.session_state.quiz_submitted = True
            with col2:
                if st.button("Clear Answers", key="clear_answers"):
                    st.session_state.user_answers = {}
                    st.rerun()

        # Show results after submission
        if st.session_state.quiz_submitted:
            st.header("Quiz Results")
            correct_count = 0

            for i, question in enumerate(st.session_state.current_quiz):
                user_answer = st.session_state.user_answers.get(i)
                correct_answer = question['correct_answer']
                is_correct = user_answer == correct_answer
                correct_count += 1 if is_correct else 0

                st.subheader(f"Question {i + 1}")
                st.write(question['question'])

                if is_correct:
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Incorrect")
                    st.write(f"Your answer: {user_answer}")
                    st.write(f"Correct answer: {correct_answer}")

                st.markdown("---")

            score_percentage = (correct_count / len(st.session_state.current_quiz)) * 100
            st.header(f"Final Score: {score_percentage:.1f}%")
            st.progress(score_percentage / 100)

            # Save results
            save_quiz_result(st.session_state.current_quiz, st.session_state.user_answers)

            if st.button("Start New Quiz"):
                reset_quiz()
                st.rerun()


if __name__ == "__main__":
    main()