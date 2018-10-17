from flask import Flask, render_template, request, redirect, url_for
from data_manager import csv_reader

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def route_list():
    questions = csv_reader('sample_data/question.csv')
    # QUESTIONS: id, submission_time, view_number, vote_number, title, message, image
    # ANSWERS: id, submission_time, vote_number, question_id, message, image
    return render_template("list.html", questions=zip(questions.get('id'), questions.get('title')))


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