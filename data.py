import requests
from requests.exceptions import HTTPError
from prettytable import PrettyTable
from question_model import Question

TRIVIA_URL = "https://opentdb.com"

# OLD VERSION
# question_data = [
#     {"text": "A slug's blood is green.", "answer": "True"},
#     {"text": "The loudest animal is the African Elephant.", "answer": "False"},
#     {"text": "Approximately one quarter of human bones are in the feet.", "answer": "True"},
#     {"text": "The total surface area of a human lungs is the size of a football pitch.", "answer": "True"},
#     {"text": "In West Virginia, USA, if you accidentally hit an animal with your car, you are free to take it "
#              "home to eat.", "answer": "True"},
#     {"text": "In London, UK, if you happen to die in the House of Parliament, "
#              "you are entitled to a state funeral.", "answer": "False"},
#     {"text": "It is illegal to pee in the Ocean in Portugal.", "answer": "True"},
#     {"text": "You can lead a cow down stairs but not up stairs.", "answer": "False"},
#     {"text": "Google was originally called 'Backrub'.", "answer": "True"},
#     {"text": "Buzz Aldrin's mother's maiden name was 'Moon'.", "answer": "True"},
#     {"text": "No piece of square dry paper can be folded in half more than 7 times.", "answer": "False"},
#     {"text": "A few ounces of chocolate can to kill a small dog.", "answer": "True"}
# ]
#


def retrieve_token():
    try:
        response = requests.get(TRIVIA_URL + "/api_token.php?command=request")
        response.raise_for_status()
        json_response = response.json()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}.")
        return ""

    except Exception as err:
        print(f"Other error occurred: {err}.")
        return ""

    # for key, value in json_response.items():
    #     print(f"Key: {key}")
    #     print(f"Value: {value}")

    if json_response["response_code"] == 0:
        return json_response["token"]
    else:
        print(json_response["response_message"])
        return ""


def select_a_category():
    try:
        response = requests.get(TRIVIA_URL + "/api_category.php")
        response.raise_for_status()
        json_response = response.json()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}.")
        return ""

    except Exception as err:
        print(f"Other error occurred: {err}.")
        return ""

    trivia_categories = json_response["trivia_categories"]
    table = PrettyTable()
    table.title = "Category list"
    table.field_names = ["№", "Name"]
    for index in range(0, len(trivia_categories)):
        table.add_row([index + 1, trivia_categories[index]["name"]])
    print(table)
    user_choice = input("Please select a category of questions. Type category № or 'ANY', "
                        "if you want play quiz with questions from different categories: ")
    if user_choice.upper() == 'ANY':
        return 'ANY'
    else:
        try:
            category_id = trivia_categories[int(user_choice) - 1]["id"]
            category_name = trivia_categories[int(user_choice) - 1]['name']
            print(f"You chose {category_name} category. "
                  f"Our database has {get_category_question_count(category_id)} questions in this category.")
            return category_id

        except Exception as err:
            print("Inappropriate category number!")
            return -1


def get_category_question_count(category_id):
    try:
        response = requests.get(TRIVIA_URL + "/api_count.php?category=" + str(category_id))
        response.raise_for_status()
        json_response = response.json()

    except HTTPError as http_err:
        # print(f"HTTP error occurred: {http_err}.")
        return 0

    except Exception as err:
        # print(f"Other error occurred: {err}.")
        return 0

    return json_response["category_question_count"]["total_question_count"]


def select_a_question_type():
    table = PrettyTable()
    table.title = "Question types"
    table.field_names = ["№", "Type"]
    table.add_row(["1", "True|False"])
    table.add_row(["2", "Multiple choice"])
    table.add_row(["3", "Any"])
    print(table)
    user_choice = input("Please select a question type. Enter type №: ")
    if user_choice == '3':
        print("You chose questions from different types.")
        return "ANY"
    elif user_choice == '1':
        print("You chose True|False questions.")
        return "boolean"
    elif user_choice == '2':
        print("You chose multiple choice questions.")
        return "multiple"
    return ""


def select_a_quiz_difficulty():
    table = PrettyTable()
    table.title = "Quiz difficulty"
    table.field_names = ["№", "Difficulty"]
    table.add_row(["1", "Easy"])
    table.add_row(["2", "Medium"])
    table.add_row(["3", "Hard"])
    table.add_row(["4", "Any"])
    print(table)
    user_choice = input("Please select a quiz difficulty. Enter type №: ")
    if user_choice == '4':
        print("You will have questions from different level of difficulty.")
        return "ANY"
    elif user_choice == '1':
        print("You chose EASY quiz.")
        return "easy"
    elif user_choice == '2':
        print("You chose MEDIUM quiz.")
        return "medium"
    elif user_choice == '3':
        print("You chose HARD quiz.")
        return "hard"
    return ""


def get_question_list(quiz):

    request_url = f"/api.php?amount={quiz.QUIZ_SIZE}&token={quiz.auth_token}"

    if quiz.category_id != "ANY":
        request_url += f"&category={str(quiz.category_id)}"

    if quiz.question_type != "ANY":
        request_url += f"&type={quiz.question_type}"

    if quiz.quiz_difficulty != "ANY":
        request_url += f"&difficulty={quiz.quiz_difficulty}"

    try:
        response = requests.get(TRIVIA_URL + request_url)
        response.raise_for_status()
        json_response = response.json()

    except HTTPError as http_err:
        # print(f"HTTP error occurred: {http_err}.")
        return 0

    except Exception as err:
        # print(f"Other error occurred: {err}.")
        return 0

    questions_list = []
    if json_response["response_code"] == 0:
        results = json_response["results"]
        for question in results:
            answers = question["incorrect_answers"]
            answers.append(question["correct_answer"])
            questions_list.append(Question(question["category"], question["question"], question["correct_answer"],
                                           question["type"], question["difficulty"], answers))
    return questions_list
