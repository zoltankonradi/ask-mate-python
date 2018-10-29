from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


# KZoli - Lists and orders questions
@app.route("/")
@app.route("/list")
def route_list():
    sorting = request.args.get('select_order') # KZoli - Gets the ordering.
    question_data = data_manager.question_reader(sorting)  # KZoli - Gets a sorted dictionary of data.
    """
    [{'id': 0, 'vote_number': 7, 'title': 'How to make lists in Python?',
      'submission_time': datetime.datetime(2017, 4, 28, 8, 29), comments: [{}, {}]},
     {'id': 1, 'vote_number': 9, 'title': 'Wordpress loading multiple jQuery Versions',
      'submission_time': datetime.datetime(2017, 4, 29, 9, 19)}]
    """
    return render_template("list.html", question_data=question_data)


# KZoli - Add new question
@app.route("/ask-question", methods=["GET", "POST"])
def route_ask_question():
    if request.method == "GET":
        return render_template("ask-question.html")
    else:
        subject = request.form['title']
        text = request.form['text']
        picture_url = request.form['url']
        data_manager.add_question(subject, text, picture_url)
        return redirect(url_for('route_list'))


# KZoli - Gets the appropriate answer(s) for the question. Updates the views too.
@app.route('/question/<question_id>')
def route_question(question_id):
    answer = data_manager.answer_reader(question_id)
    question = data_manager.find_question_for_answer(question_id)
    comment_question = data_manager.question_comment_reader(question_id)
    data_manager.update_views(question_id)
    return render_template('question.html', answer=answer, question=question, comment_question=comment_question)


# KZoli - Add an answer to the specific question.
@app.route('/question/<question_id>', methods=['POST'])
def route_question_add_answer(question_id):
    text = request.form['text']
    image = request.form['response-image']
    data_manager.post_answer(question_id, text, image)
    return redirect(url_for('route_question', question_id=question_id))


# KZoli - Delete an answer.
@app.route("/answer/<int:answer_id>/delete/<question_id>")
def route_delete_answer(answer_id, question_id):
    data_manager.delete_answer(answer_id)
    return redirect(url_for('route_question', question_id=question_id))


# KZoli - Delete a question.
@app.route("/<int:question_id>")
def route_delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('route_list'))


# KZoli - Edit a question.
@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def route_edit_question(question_id):
    if request.method == "GET":
        question = data_manager.find_question_for_answer(question_id)
        action = "update"
        return render_template("ask-question.html", question_id=question_id, action=action, question=question)
    if request.method == "POST":
        subject = request.form['title']
        text = request.form['text']
        data_manager.update_question(question_id, subject, text)
        return redirect(url_for('route_list'))


# KZoli - Vote on a question.
@app.route("/question/<question_id>/<vote>")
def route_question_voting(question_id, vote):
    data_manager.update_votes_question(question_id, vote)
    return redirect(url_for('route_question', question_id=question_id))


# KZoli - Vote on an answer.
@app.route("/question/<question_id>/<vote>/<answer_id>")
def route_answer_voting(question_id, vote, answer_id):
    data_manager.update_votes_answer(vote, answer_id)
    return redirect(url_for('route_question', question_id=question_id))


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_comment_to_question(question_id):
    if request.method == "GET":
        action = "add_comment_question"
        return render_template("ask-question.html", question_id=question_id, action=action)
    if request.method == "POST":
        new_comment = request.form['text']
        data_manager.post_comment(question_id, new_comment, 'question')
        return redirect(url_for('route_question', question_id=question_id))

@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_comment_to_answer(answer_id):
    if request.method == "GET":
        action = "add_comment_answer"
        return render_template("ask-question.html", answer_id=answer_id, action=action)
    if request.method == "POST":
        new_comment = request.form['text']
        data_manager.post_comment(answer_id, new_comment, 'answer')
        return redirect(url_for('route_list'))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
