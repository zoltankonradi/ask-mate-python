from flask import Flask, render_template, request, redirect, url_for
from data_manager import csv_reader, add_answer, generate_answer_id, get_submission_time, delete_answer

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def route_list():
    questions = csv_reader('sample_data/question.csv')
    # QUESTIONS: id, submission_time, view_number, vote_number, title, message, image
    # ANSWERS: id, submission_time, vote_number, question_id, message, image
    questions = sort_questions(questions, request.args.get('select_order'))
    return render_template("list.html", questions=zip(questions[0], questions[1], questions[2]))


def sort_questions(questions, order):
    if order is None:
        return [questions.get('id'), questions.get("title"), questions.get("submission_time")]
    sorted_questions = []
    for i in range(len(questions.get("id"))):
        sorted_questions.append([questions.get("id")[i],
                                 questions.get("title")[i],
                                 questions.get("submission_time")[i]])
    if order == "asc":
        sorted_questions.sort(key=lambda k: int(k[2]))
    elif order == "desc":
        sorted_questions.sort(key=lambda k: int(k[2]), reverse=True)
    ids, titles, submission_time = [], [], []
    for elem in sorted_questions:
        ids.append(elem[0])
        titles.append(elem[1])
        submission_time.append(elem[2])
    return [ids, titles, submission_time]


@app.route("/ask-question")
def route_ask_question():
    return render_template("ask-question.html")


@app.route("/question/<id>")
def route_question(id):
    answers = csv_reader('sample_data/answer.csv')
    questions = csv_reader('sample_data/question.csv')
    title = questions.get('title')[int(id)]
    message = questions.get('message')[int(id)]
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
    with open("sample_data/answer.csv", 'r') as f:
        content=f.readlines()
        for line in content:
            for question in indexed_questions:
                if question in line:
                    actual_indexes.append(line[0])
                    break
    return render_template("question.html", answers_list=zip(indexed_questions, actual_indexes), title=title, message=message, id=id)


@app.route('/question/<id>', methods=['POST'])
def route_question_add_answer(id):
    answer_id = generate_answer_id(csv_reader("sample_data/answer.csv"))
    submission_time=get_submission_time()
    add_answer("sample_data/answer.csv", answer_id, submission_time, 0, id, request.form['text'], "")
    return redirect(f"/question/{id}")


@app.route("/answer/<answer_id>/delete")
def route_delete_answer(answer_id):
    delete_answer(answer_id)
    return redirect(url_for('route_list'))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
