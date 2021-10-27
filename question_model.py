class Question:

    # OLD VERSION
    # def __init__(self, text, answer):
    #     self.text = text
    #     self.answer = answer
    #

    def __init__(self, category, text, correct_answer, q_type, difficulty, answers):
        self.category = category
        self.text = text
        self.correct_answer = correct_answer
        self.type = q_type
        self.difficulty = difficulty
        self.answers = answers



