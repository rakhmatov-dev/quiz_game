import data
import random


class QuizBrain:

    # TODO 1. Using a session token of Trivia DB API | DONE
    # TODO 2. Question category (any category) | DONE
    # TODO 3. Question type (type=boolean = True/False, type=multiple = Multiple Choice, any type) | DONE
    # TODO 4. Quiz difficulty (easy, medium, hard) | DONE

    QUIZ_SIZE = 5

    def __init__(self):
        # OLD VERSION
        # self.question_number = 0
        # self.questions_list = questions_list
        #

        self.category_id = data.select_a_category()
        self.question_type = data.select_a_question_type()
        self.quiz_difficulty = data.select_a_quiz_difficulty()
        self.auth_token = data.retrieve_token()
        self.questions_list = data.get_question_list(self)
        self.question_number = 0
        self.score = 0
        # print(self.questions_list)

    def still_has_questions(self):
        return self.question_number < len(self.questions_list)

    def next_question(self):
        current_question = self.questions_list[self.question_number]
        self.question_number += 1
        print("\n")
        if current_question.type == "multiple":
            print(f"Q.{self.question_number}: {current_question.text}")
            random.shuffle(current_question.answers)
            print(f"A: {current_question.answers[0]}")
            print(f"B: {current_question.answers[1]}")
            print(f"C: {current_question.answers[2]}")
            print(f"D: {current_question.answers[3]}")
            user_letter = input("Choose your answer: ")
            if user_letter.upper() == 'A':
                user_answer = current_question.answers[0]
            elif user_letter.upper() == 'B':
                user_answer = current_question.answers[1]
            elif user_letter.upper() == 'C':
                user_answer = current_question.answers[2]
            else:
                user_answer = current_question.answers[3]
            self.check_answer(user_answer, current_question.correct_answer)

        else:
            user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False)?: ")
            self.check_answer(user_answer, current_question.correct_answer)

    def check_answer(self, user_answer, correct_answer):
        if user_answer.lower() == correct_answer.lower():
            print("You got it right!")
            self.score += 1
        else:
            print("That's wrong.")
            print(f"The correct answer was {correct_answer}.")
        print(f"Your current score is: {self.score}/{self.question_number}.\n")
