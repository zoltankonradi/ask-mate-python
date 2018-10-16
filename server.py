from flask import Flask, render_template, request, redirect, url_for
from data_manager import get_table_from_file

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def route_list():
    questions = get_table_from_file('sample_data/question.csv')
    list_of_questions = []
    list_of_ids = []
    for element in range(len(questions)):
        list_of_questions.append(questions[element][4])
        list_of_ids.append(questions[element][0])
    print(list_of_ids)
    return render_template("list.html", questions=zip(list_of_ids[1:], list_of_questions[1:]))


@app.route("/ask-question")
def route_ask_question():
    return render_template("ask-question.html")


@app.route("/question/<id>")
def route_question(id):
    answers = get_table_from_file('sample_data/answer.csv')
    answers_list = []
    for question_id_in_answers in answers:
        if question_id_in_answers[3] == id:
            answers_list.append(question_id_in_answers[4][1:-1])
    # reads questions
    questions = get_table_from_file('sample_data/question.csv')
    title = ''
    message = ''
    for id_in_question in questions:
        print(id_in_question)
        print(id)
        if id_in_question[0] == id:
            title = id_in_question[4][1:-1]
            message = id_in_question[-1]
    return render_template("question.html", answers_list=answers_list, title=title, message=message)


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