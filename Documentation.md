# Quiz Generator Documentation (Part 1/4)

## Project Overview
This project is a Quiz Generator that uses AI to create questions about any computing-related topic. It can:
- Generate multiple-choice questions
- Allow users to take quizzes
- Keep track of quiz history
- Show quiz results

## Getting Started

### 1. Project Setup

First, create your project folder structure:
```
quiz_generator/
│
├── utils/
│   ├── __init__.py
│   ├── question_handler.py
│   ├── result_handler.py
│   └── quiz_history.py
│
├── quiz_generator.py
└── requirements.txt
```

To create this:
1. Create a new folder called `quiz_generator`
2. Inside it, create another folder called `utils`
3. Create all the files shown above (we'll fill them with code later)

### 2. Installing Required Packages

1. Open your terminal/command prompt
2. Navigate to your project folder
3. Install required packages:
```bash
pip install transformers torch
```

This installs:
- `transformers`: The AI library we're using
- `torch`: Required for running the AI model

### 3. Code Organization

Our code is split into several files for better organization:
- `quiz_generator.py`: Main file that runs everything
- `utils/question_handler.py`: Handles creating questions and options
- `utils/result_handler.py`: Handles quiz taking and showing results
- `utils/quiz_history.py`: Manages saving and loading quiz history

### 4. Basic Concepts Used

For beginners, here are the key concepts we're using:
- **Classes**: Templates for creating objects that hold data and functions
- **Methods**: Functions that belong to a class
- **Objects**: Instances of classes
- **Imports**: Ways to use code from other files
- **AI Model**: Pre-trained system that generates questions

# Quiz Generator Documentation (Part 2/4)

## Detailed File Explanations

### 1. quiz_generator.py (Main File)
```python
from transformers import pipeline
from utils.question_handler import QuestionHandler
from utils.result_handler import ResultHandler
from utils.quiz_history import QuizHistory

# Think of this class like a manager that coordinates everything
class QuizGenerator:
    def __init__(self):
        # When we start up, we need to get everything ready
        print("Loading pre-trained model...")  # Let user know we're working
        # This is like loading a smart brain that can make questions
        self.generator = pipeline('text2text-generation', model='facebook/bart-large-cnn')
        # These are like different helpers that do specific jobs
        self.question_handler = QuestionHandler()  # Makes questions
        self.history = QuizHistory()              # Remembers past quizzes
        self.result_handler = ResultHandler()      # Handles answers and scores
        self.current_quiz = None                  # Keeps track of current quiz

    def generate_quiz(self, topic: str, difficulty: str, num_questions: int) -> dict:
        # This is like a recipe for making a quiz
        questions = []  # Empty list to store our questions

        # For each question we want to make:
        for _ in range(num_questions):
            # Tell the AI what kind of question we want
            prompt = f"""Generate a {difficulty} multiple choice question about {topic}.
            Include 4 possible answers, with the correct answer first."""

            # Ask the AI to make a question
            output = self.generator(prompt,
                                  max_length=200,
                                  temperature=0.8)  # Makes questions more creative

            # Create a proper question with options
            question = self.question_handler.create_question(
                output[0]['generated_text'],
                topic,
                difficulty
            )
            questions.append(question)  # Add to our list

        # Package everything into a nice quiz format
        quiz = {
            'topic': topic,
            'difficulty': difficulty,
            'questions': questions,
            'timestamp': self.history.get_timestamp()  # When we made it
        }

        self.current_quiz = quiz  # Remember current quiz
        self.history.add_quiz(quiz)  # Save to history
        return quiz

# This is where our program starts running
def main():
    quiz_gen = QuizGenerator()  # Create our quiz manager

    # Keep running until user wants to quit
    while True:
        # Show menu
        print("\n=== Quiz Generator ===")
        print("1. Generate new quiz")
        print("2. View history")
        print("3. Exit")

        choice = input("\nChoice: ")  # Ask user what they want to do

        if choice == '1':
            # Get quiz details from user
            topic = input("Enter topic (e.g., Python, Cybersecurity): ")
            difficulty = input("Enter difficulty (easy/medium/hard): ").lower()

            # Make sure difficulty is valid
            while difficulty not in ['easy', 'medium', 'hard']:
                print("Invalid difficulty! Please choose easy, medium, or hard.")
                difficulty = input("Enter difficulty: ").lower()

            # Get number of questions
            try:
                num_questions = int(input("How many questions would you like? "))
                if num_questions <= 0:  # Can't have zero or negative questions!
                    raise ValueError
            except ValueError:
                print("Please enter a valid number greater than 0")
                continue

            # Generate and run the quiz
            quiz = quiz_gen.generate_quiz(topic, difficulty, num_questions)
            user_answers = quiz_gen.result_handler.take_quiz(quiz)
            quiz_gen.result_handler.show_results(quiz, user_answers)

        elif choice == '2':
            # Show quiz history
            quizzes = quiz_gen.history.get_all()
            if not quizzes:
                print("No quiz history found!")
            for quiz in quizzes:
                print(f"\nTopic: {quiz['topic']}")
                print(f"Date: {quiz['timestamp']}")
                print(f"Number of questions: {len(quiz['questions'])}")

        elif choice == '3':
            break  # Exit the program

# This is special code that runs our program
if __name__ == "__main__":
    main()
```

### Understanding the Main File:

1. **What it does**:
   - This is like the boss that controls everything
   - It shows the menu and takes user input
   - It creates quizzes using AI
   - It keeps track of everything

2. **Important Parts**:
   - `QuizGenerator` class: Think of this as a machine that makes quizzes
   - `generate_quiz` method: The recipe for making a quiz
   - `main()` function: Where everything starts

3. **How it works**:
   - When you run the program, it shows a menu
   - You can choose to:
     1. Make a new quiz
     2. Look at old quizzes
     3. Exit the program
   - When making a quiz, it asks for:
     - Topic (what you want questions about)
     - Difficulty (how hard you want it)
     - Number of questions

# Quiz Generator Documentation (Part 3/4)

## Utility Files Explanation

### 1. question_handler.py
```python
from typing import List, Dict
import random

class QuestionHandler:
    def __init__(self):
        # We want 4 options for each question (A, B, C, D)
        self.option_count = 4

    def create_question(self, generated_text: str, topic: str, difficulty: str) -> Dict:
        """This is like a recipe for making each question perfect"""
        # First, make the question look nice
        question = self._format_question(generated_text)

        # Create the multiple choice options
        options = self._generate_options_from_text(generated_text, difficulty)

        # The first option is the right answer
        correct_answer = options[0]
        # Mix up the options so the right answer isn't always first
        random.shuffle(options)

        # Package everything into a nice format
        return {
            'question': question,          # The actual question
            'options': options,            # The A,B,C,D choices
            'correct_answer': correct_answer,  # The right answer
            'difficulty': difficulty       # How hard it is
        }

    def _format_question(self, text: str) -> str:
        """Makes the question text look nice"""
        # Clean up any extra spaces
        text = text.strip()
        # Make sure it ends with a question mark
        if not text.endswith('?'):
            text += '?'
        return text

    def _generate_options_from_text(self, text: str, difficulty: str) -> List[str]:
        """Creates the multiple choice options"""
        # Split the AI's response into parts
        parts = text.split('\n')

        # If the AI gave us options, use them
        if len(parts) > 1:
            options = [p.strip() for p in parts[1:] if p.strip()]
            if len(options) >= 4:
                return options[:4]

        # If we need backup options
        options = [
            "Option 1 - Main concept",
            "Option 2 - Related concept",
            "Option 3 - Similar concept",
            "Option 4 - Alternative concept"
        ]

        return options
```

### 2. result_handler.py
```python
class ResultHandler:
    def take_quiz(self, quiz: dict) -> list:
        """This handles when someone is taking the quiz"""
        user_answers = []  # Keep track of their answers
        print("\n=== Quiz Started ===")

        # Go through each question
        for i, q in enumerate(quiz['questions'], 1):
            print(f"\nQuestion {i}:")
            print(q['question'])  # Show the question

            # Show each option (A, B, C, D)
            for j, option in enumerate(q['options']):
                print(f"{chr(65+j)}. {option}")  # chr(65) is 'A', 66 is 'B', etc.

            # Keep asking until they give a valid answer
            while True:
                answer = input("\nYour answer (A/B/C/D): ").upper()
                if answer in ['A', 'B', 'C', 'D']:
                    user_answers.append(answer)
                    break
                print("Please enter A, B, C, or D")

        return user_answers

    def show_results(self, quiz: dict, user_answers: list):
        """Shows how well they did on the quiz"""
        print("\n=== Quiz Results ===")
        correct_count = 0  # Keep track of right answers

        # Go through each question and answer
        for i, (question, user_answer) in enumerate(zip(quiz['questions'], user_answers), 1):
            print(f"\nQuestion {i}:")

            # Find which letter was the correct answer
            correct_letter = self.get_correct_option_letter(question)

            # Show the question and all options again
            print(question['question'])
            for j, option in enumerate(question['options']):
                letter = chr(65+j)  # Convert number to letter (A, B, C, D)
                if letter == user_answer:
                    # Show if their answer was right or wrong
                    mark = "✓" if letter == correct_letter else "✗"
                    print(f"{letter}. {option} {mark}")
                else:
                    print(f"{letter}. {option}")

            # Tell them if they got it right
            if user_answer == correct_letter:
                correct_count += 1
                print("Correct! ✓")
            else:
                print(f"Incorrect ✗ (Correct answer: {correct_letter})")

        # Show final score as a percentage
        print(f"\nFinal Score: {correct_count}/{len(user_answers)} "
              f"({(correct_count/len(user_answers)*100):.1f}%)")

    def get_correct_option_letter(self, question: dict) -> str:
        """Finds which letter (A,B,C,D) is the right answer"""
        correct_answer = question['correct_answer']
        for i, option in enumerate(question['options']):
            if option == correct_answer:
                return chr(65 + i)  # Convert number to letter
        return "?"
```

### 3. quiz_history.py
```python
import json
from datetime import datetime

class QuizHistory:
    def __init__(self, filename: str = 'quiz_history.json'):
        # Where we'll save the quiz history
        self.filename = filename
        # Load any existing history
        self.history = self.load_history()

    def add_quiz(self, quiz: dict):
        """Save a new quiz to history"""
        self.history.append(quiz)
        self.save_history()

    def get_all(self) -> list:
        """Get all previous quizzes"""
        return self.history

    def get_timestamp(self) -> str:
        """Get current time and date"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_history(self):
        """Save all quizzes to a file"""
        with open(self.filename, 'w') as f:
            json.dump(self.history, f, indent=4)

    def load_history(self) -> list:
        """Load saved quizzes from file"""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []  # If no history exists yet, start empty
```

### Understanding the Utility Files:

1. **question_handler.py**:
   - Think of this as the question creator
   - It takes the AI's text and makes it into a proper question
   - Creates 4 options for each question
   - Makes sure everything is formatted nicely

2. **result_handler.py**:
   - This is like a teacher giving a test
   - Shows questions one by one
   - Takes your answers
   - Grades your answers and shows your score
   - Shows which answers were right or wrong

3. **quiz_history.py**:
   - This is like a diary that remembers all quizzes
   - Saves quizzes to a file so they're not lost
   - Can show you old quizzes you've taken
   - Adds date and time to each quiz


# Quiz Generator Documentation (Part 4/4)

## How Everything Works Together

### 1. The Big Picture
```mermaid
quiz_generator.py (Main File)
    │
    ├── Uses AI Model
    │   └── Generates raw questions
    │
    ├── question_handler.py
    │   └── Creates proper questions with options
    │
    ├── result_handler.py
    │   └── Handles quiz taking and scoring
    │
    └── quiz_history.py
        └── Saves and loads quizzes
```

Let's use a restaurant analogy to understand how these files work together:

1. **quiz_generator.py** is like the Restaurant Manager
   - Takes customer orders (user input for topic/difficulty)
   - Coordinates between kitchen and servers
   - Makes sure everything runs smoothly

2. **AI Model** is like the Head Chef
   - Creates the raw content (questions)
   - Uses its "training" to make relevant questions
   - Sends raw output to be processed

3. **question_handler.py** is like the Sous Chef
   - Takes raw questions from AI
   - Makes them look nice
   - Adds multiple choice options
   - Makes sure everything is properly formatted

4. **result_handler.py** is like the Server
   - Presents questions to user
   - Takes their answers
   - Shows results
   - Gives feedback

5. **quiz_history.py** is like the Record Keeper
   - Writes down all quizzes
   - Keeps track of when they happened
   - Can show past quizzes when asked

### 2. How Data Flows Through the Program

```python
# Step 1: User Input
topic = "Python Programming"
difficulty = "medium"
num_questions = 3

# Step 2: Main Generator Creates Quiz
quiz_gen = QuizGenerator()
# Uses AI to generate raw questions
raw_question = AI_model.generate("Make a question about Python...")

# Step 3: Question Handler Formats It
question_handler.create_question(raw_question)
# Adds multiple choice options
# Makes it look nice

# Step 4: Result Handler Shows Quiz
result_handler.take_quiz(quiz)
# Shows questions one by one
# Takes user answers

# Step 5: Shows Results
result_handler.show_results(quiz, answers)
# Shows score and correct answers

# Step 6: History Saves Everything
quiz_history.add_quiz(quiz)
# Saves to file for later
```

### 3. The AI Part Explained Simply

Imagine the AI like a super-smart student who:
1. Has read lots of books about computing
2. Knows how to make questions
3. Can understand different topics

```python
# This is how we talk to the AI
self.generator = pipeline('text2text-generation', model='facebook/bart-large-cnn')

# When we want a question, we ask like this:
prompt = f"Generate a {difficulty} question about {topic}"
question = self.generator(prompt)
```

The AI:
- Takes our request (prompt)
- Thinks about what it knows about the topic
- Creates a question
- Sends it back to us

### 4. Code Structure and Flow

When you run the program:

1. **First**:
```python
python quiz_generator.py
```

2. **Program Starts**:
```python
if __name__ == "__main__":
    main()  # This starts everything
```

3. **Main Menu Shows**:
```
=== Quiz Generator ===
1. Generate new quiz
2. View history
3. Exit
```

4. **When Generating Quiz**:
   - Gets topic, difficulty, number of questions
   - AI creates questions
   - Question Handler formats them
   - Result Handler shows quiz
   - History saves everything

5. **When Viewing History**:
   - Loads saved quizzes
   - Shows dates and scores

### 5. Error Handling

The program handles problems like:
- Invalid inputs
- AI generation failures
- File saving/loading issues

For example:
```python
try:
    num_questions = int(input("How many questions? "))
except ValueError:
    print("Please enter a valid number")
```
