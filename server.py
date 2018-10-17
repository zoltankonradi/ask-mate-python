from flask import Flask, render_template, request, redirect, url_for
from data_manager import csv_reader, csv_writer
import time

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
    indexes = []
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
    return render_template("question.html", answers_list=indexed_questions, title=title, message=message)


@app.route('/question/<id>', methods=['POST'])
def route_question_add_answer(id):
    with open('sample_data/answer.csv', 'a') as f:
        id_ = len(csv_reader("sample_data/answer.csv").get('id'))
        f.write(f"{id_},{int(time.time())},35,0,\"{request.form['text']}\",\n")
    return redirect(f"/question/{id}")


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )



    """<!--
{% extends "layout.html" %}
{% block title_content %}
<title>Ask Mate|List</title>
{% endblock title_content %}
{% block h1_content %}
<h1>Ask Mate</h1>
{% endblock h1_content %}
{% block body_content %}
<hr>
<a href="/add-question">Ask a question</a>
<h4>
	List of user questions:
</h4>
<p>
	{% if list_of_questions == "" %}
		No questions to be answered!
	{% else %}
		<div class="boxes">
			{% for i in list_of_questions %}
				<div class="item">{{ questions[1:-1] }}</div>
			{% endfor %}
		</div>
	{% endif %}
</p>
{% endblock body_content %}
-->
"""