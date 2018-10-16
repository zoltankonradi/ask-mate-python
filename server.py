from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def route_list():
    return render_template("list.html")


@app.route("/ask-question")
def route_ask_question():
    return render_template("ask-question.html")



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
	{% if list_of_contents == "" %}
		No questions to be answered!
	{% else %}
		<div class="boxes">
			{% for question in dict %}
				<div class="item">{{ question }}</div>
			{% endfor %}
		</div>
	{% endif %}
</p>
{% endblock body_content %}
-->
"""