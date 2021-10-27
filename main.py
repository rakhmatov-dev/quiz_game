from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
import data

### OLD VERSION
# question_bank = []
# for question in question_data:
#     question_bank.append(Question(question["text"], question["answer"]))
#
# quiz = QuizBrain(question_bank)
#
# while quiz.still_has_questions():
#     quiz.next_question()
#
# print("You've completed the quiz.")
# print(f"Your final score was: {quiz.score}/{quiz.question_number}.")
###

quiz = QuizBrain()

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the quiz.")
print(f"Your final score was: {quiz.score}/{quiz.question_number}.")