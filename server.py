from flask import Flask, render_template, request, redirect, url_for
from data_manager import csv_reader, add_answer, generate_answer_id, get_submission_time, add_question
from data_manager import generate_question_id, update_view_number_question, delete_answer, update_answer_csv
from connection import increase_view_number
import time

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def route_list():
    questions = csv_reader('sample_data/question.csv')
    # QUESTIONS: id, submission_time, view_number, vote_number, title, message, image
    # ANSWERS: id, submission_time, vote_number, question_id, message, image
    questions = sort_questions(questions, request.args.get('select_order'))
    return render_template("list.html", questions=zip(questions[0], questions[1], questions[2], questions[3]))


def sort_questions(questions, order):
    if order is None:
        converted_times = []
        for times in questions.get("submission_time"):
            converted_times.append(time.ctime(int(times)))
        return [questions.get('id'), questions.get("title"), converted_times, questions.get("vote_number")]
    sorted_questions = []
    for i in range(len(questions.get("id"))):
        sorted_questions.append([questions.get("id")[i],
                                 questions.get("title")[i],
                                 questions.get("submission_time")[i],
                                 questions.get("vote_number")[i]])
    if order == "asc":
        sorted_questions.sort(key=lambda k: int(k[2]))
    elif order == "desc":
        sorted_questions.sort(key=lambda k: int(k[2]), reverse=True)
    ids, titles, submission_time, vote_number = [], [], [], []
    for elem in sorted_questions:
        ids.append(elem[0])
        titles.append(elem[1])
        submission_time.append(elem[2])
        vote_number.append(elem[3])
    converted_times = []
    for times in submission_time:
        converted_times.append(time.ctime(int(times)))
    return [ids, titles, converted_times, vote_number]


@app.route("/ask-question", methods=["GET", "POST"])
def route_ask_question():
    if request.method == "GET":
        return render_template("ask-question.html")
    else:
        id = generate_question_id(csv_reader("sample_data/question.csv"))
        submission_time = get_submission_time()
        title = request.form["title"]
        message = request.form["text"]
        image = request.form["url"]
        add_question("sample_data/question.csv", id, submission_time, 0, 0, title, message, image)
        return redirect("/list")


@app.route("/question/<id>")
def route_question(id):
    answers = csv_reader('sample_data/answer.csv')
    questions = csv_reader('sample_data/question.csv')
    title = questions.get('title')[int(id)]
    message = questions.get('message')[int(id)]
    current_view_number = questions["view_number"][int(id)]
    questions["view_number"][int(id)] = increase_view_number(int(current_view_number))
    update_view_number_question("sample_data/question.csv", questions)
    updated_number_of_views = questions["view_number"][int(id)]
    vote_number = questions.get('vote_number')[int(id)]
    image = questions.get("image")[int(id)]
    answers_vote_number = answers.get('vote_number')[int(id)]
    start_at = -1
    indexes = [] # this doesn't get the indexes of the answers related to the question, but their place in the answer.csv file
    while True:
        try:
            location = answers.get('question_id').index(id, start_at + 1)
        except ValueError:
            break
        else:
            indexes.append(location)
            start_at = location
    indexed_questions = []
    for i in indexes:
        indexed_questions.append(answers.get('message')[i])
    actual_indexes=[]
    actual_answers=[]
    actual_vote_number=[]
    with open("sample_data/answer.csv", 'r') as f:
        content=f.readlines()
        for i in range(len(content)):
            content[i]=content[i].split(',')
        for i in range(len(content)-1, 0, -1):
            for j in range(len(indexed_questions)):
                if ((indexed_questions[j] == content[i][4][1:-1]) or (indexed_questions[j] == content[i][4]))\
                     and (id == content[i][3]):
                    actual_indexes.append(content[i][0])
                    actual_answers.append(indexed_questions.pop(j))
                    actual_vote_number.append(content[i][2])
                    break
    return render_template("question.html", answers_list=zip(indexed_questions, actual_indexes), title=title, message=message, id=id, views=updated_number_of_views, vote_number=vote_number, image=image)
    actual_indexes.reverse()
    actual_answers.reverse()
    actual_vote_number.reverse()
    return render_template("question.html", answers_list=zip(actual_answers, actual_indexes, actual_vote_number),
                           title=title, message=message, id=id, vote_number=vote_number, views=updated_number_of_views,
                           answers_vote_number=answers_vote_number)


@app.route('/question/<id>', methods=['POST'])
def route_question_add_answer(id):
    answer_id = generate_answer_id(csv_reader("sample_data/answer.csv"))
    submission_time=get_submission_time()
    add_answer("sample_data/answer.csv", answer_id, submission_time, 0, id, request.form['text'], "")
    return redirect(f"/question/{id}")


@app.route("/answer/<answer_id>/delete/<id_>")
def route_delete_answer(answer_id, id_):
    delete_answer(answer_id)
    return redirect(url_for('route_question', id=id_))


@app.route("/question/<id>/<vote>")
def route_question_voting(id, vote):
    questions = csv_reader('sample_data/question.csv')
    vote_number = questions.get('vote_number')[int(id)]
    answers = csv_reader('sample_data/answer.csv')
    answers_vote_number = answers.get('vote_number')[int(id)]
    if vote == "vote-up":
        vote_number = int(vote_number) + 1
    elif vote == "vote-down":
        vote_number = int(vote_number) - 1
    elif vote == "answer-vote-up":
        answers_vote_number = int(answers_vote_number) + 1
    elif vote == "answer-vote-down":
        answers_vote_number = int(answers_vote_number) - 1
    questions["vote_number"][int(id)] = vote_number
    update_view_number_question("sample_data/question.csv", questions)
    answers["vote_number"][int(id)] = answers_vote_number
    update_answer_csv("sample_data/answer.csv", answers)
    return redirect(f"/question/{id}")


@app.route("/question/<id>/edit", methods=["GET", "POST"])
def route_edit_question(id):
    questions = csv_reader('sample_data/question.csv')
    id = int(id)
    if request.method == "GET":
        action = "update"
        return render_template("ask-question.html", id=id, action=action, data=questions)
    if request.method == "POST":
        questions["title"][int(id)] = request.form["title"]
        questions["message"][int(id)] = request.form["text"]
        update_view_number_question("sample_data/question.csv", questions)
        update_view_number_question("sample_data/question.csv", questions)
        return redirect("/list")


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
