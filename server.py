from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


# KZoli - Lists and orders questions
@app.route("/")
def route_list():
    limit = True
    sorting = request.args.get('select_order') # KZoli - Gets the ordering.
    question_data = data_manager.question_reader(sorting, limit)  # KZoli - Gets a sorted dictionary of data.
    """
    [{'id': 0, 'vote_number': 7, 'title': 'How to make lists in Python?',
      'submission_time': datetime.datetime(2017, 4, 28, 8, 29), comments: [{}, {}]},
     {'id': 1, 'vote_number': 9, 'title': 'Wordpress loading multiple jQuery Versions',
      'submission_time': datetime.datetime(2017, 4, 29, 9, 19)}]
    """
    return render_template("list.html", question_data=question_data, limit=limit)


@app.route("/list")
def route_list_no_limit():
    limit = False
    sorting = request.args.get('select_order')
    question_data = data_manager.question_reader(sorting, limit)
    return render_template("list.html", question_data=question_data, limit=limit)


@app.route("/search")
def route_search():
    limit = False
    search_mode = True
    search_text = request.args.get('q')
    question_data = data_manager.search(search_text)
    return render_template("list.html", question_data=question_data, search_mode=search_mode, limit=limit)


# KZoli - Add new question
@app.route("/ask-question", methods=["GET", "POST"])
def route_ask_question():
    if request.method == "GET":
        tags = data_manager.read_tags()
        return render_template("ask-question.html", tags=tags)
    else:
        subject = request.form['title']
        text = request.form['text']
        picture_url = request.form['url']
        new_tag = request.form['new_tag']
        # Finds selected tags.
        tag_ids = data_manager.get_list_of_tag_ids()
        selected_tags_list = []
        for tag_id in tag_ids:
            try:
                selected_tags = request.form[str(tag_id)]
                selected_tags_list.append(selected_tags)
            except KeyError:
                continue
        data_manager.add_question(subject, text, picture_url)
        # If new tag not empty, adds it
        if new_tag != '':
            data_manager.add_tag(new_tag)
        data_manager.add_existing_tags_to_new_question(selected_tags_list)
        return redirect(url_for('route_list'))


# KZoli - Gets the appropriate answer(s) for the question. Updates the views too.
@app.route('/question/<question_id>')
def route_question(question_id):
    answer = data_manager.answer_reader(question_id)
    question = data_manager.find_question_for_answer(question_id)
    comment_question = data_manager.question_comment_reader(question_id)
    question_tags = data_manager.get_tags_for_question(question_id)
    data_manager.update_views(question_id)
    return render_template('question.html', answer=answer, question=question, comment_question=comment_question,
                           question_tags=question_tags)


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
        tags = data_manager.read_tags()
        checked_tags = data_manager.get_checked_tags(question_id)
        question = data_manager.find_question_for_answer(question_id)
        action = "update"
        return render_template("ask-question.html", question_id=question_id, action=action, question=question, tags=tags,
                               checked_tags=checked_tags)
    if request.method == "POST":
        subject = request.form['title']
        text = request.form['text']
        new_tag = request.form['new_tag']
        # Finds selected tags.
        tag_ids = data_manager.get_list_of_tag_ids()
        selected_tags_list = []
        for tag_id in tag_ids:
            try:
                selected_tags = request.form[str(tag_id)]
                selected_tags_list.append(selected_tags)
            except KeyError:
                continue
        # If new tag not empty, adds it
        if new_tag != '':
            selected_tags_list.append(data_manager.add_tag_for_existing_question(new_tag, question_id))
        # Compare new tags to old ones.
        data_manager.compare_new_tags_to_old_ones(selected_tags_list, question_id)
        # Updates question data
        data_manager.update_question(question_id, subject, text)
        return redirect(url_for('route_question', question_id=question_id))


# KZoli - Edit an answer.
@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def route_edit_answer(answer_id):
    question_id = data_manager.find_question_id_for_answer_id(answer_id)
    if request.method == "GET":
        answer = data_manager.find_answer_by_answer_id(answer_id)
        action = "edit_answer"
        return render_template("ask-question.html", question_id=question_id, action=action, answer=answer, answer_id=answer_id)
    if request.method == "POST":
        text = request.form['text']
        data_manager.update_answer(text, answer_id)
        return redirect(url_for('route_question', question_id=question_id))


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
        question_id = data_manager.find_question_id_for_answer_id(answer_id)
        return redirect(url_for('route_question', question_id=question_id))


# KZoli - Delete comment.
@app.route("/comments/<int:comment_id>/<int:question_id>/delete")
def route_delete_comment(comment_id, question_id):
    data_manager.delete_question_comment(comment_id)
    return redirect(url_for('route_question', question_id=question_id))


# KZoli - Edit question comment.
@app.route("/comments/<comment_id>/edit/q", methods=['GET', 'POST'])
def route_edit_comment_question(comment_id):
    if request.method == "GET":
        comment = data_manager.find_comment_message_by_comment_id(comment_id)
        action = "edit_comment_q"
        return render_template("ask-question.html", comment_id=comment_id, action=action, comment=comment)
    if request.method == "POST":
        data_manager.increase_edit_counter(comment_id)
        new_comment = request.form['text']
        data_manager.update_question_comment(new_comment, comment_id)
        question_id = data_manager.find_question_id_by_comment_id(comment_id)
        return redirect(url_for('route_question', question_id=question_id))


# KZoli - Edit comment.
@app.route("/comments/<comment_id>/edit/a", methods=['GET', 'POST'])
def route_edit_comment_answer(comment_id):
    if request.method == "GET":
        comment = data_manager.find_comment_message_by_comment_id(comment_id)
        action = "edit_comment_a"
        return render_template("ask-question.html", comment_id=comment_id, action=action, comment=comment)
    if request.method == "POST":
        data_manager.increase_edit_counter(comment_id)
        new_comment = request.form['text']
        data_manager.update_question_comment(new_comment, comment_id)
        question_id = data_manager.find_question_id_by_comment_id_for_edit_answer_comment(comment_id)
        return redirect(url_for('route_question', question_id=question_id))


# KZoli - Delete a tag.
@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_manager.delete_question_tag(question_id, tag_id)
    return redirect(url_for('route_edit_question', question_id=question_id))


# 3 TW WEEK.
@app.route("/login")
def login():
    return render_template("login_register.html", page='login')


@app.route("/register")
def register():
    return render_template("login_register.html", page='register')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
