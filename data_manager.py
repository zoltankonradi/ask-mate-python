import connection
import util


# KZoli - Reads in the questions, and sorts it.
@connection.connection_handler
def question_reader(cursor, order, limit):
    if limit is True:
        if order == 'DESC_BY_TIME':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY submission_time DESC LIMIT 5;
                           """)
        elif order == 'ASC_BY_TIME':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY submission_time ASC LIMIT 5;
                           """)
        elif order == 'ASC_BY_VOTES':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY vote_number ASC LIMIT 5;
                           """)
        elif order == 'DESC_BY_VOTES':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY vote_number DESC LIMIT 5;
                           """)
        elif order == 'ASC_BY_VIEWS':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY view_number ASC LIMIT 5;
                           """)
        elif order == 'DESC_BY_VIEWS':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY view_number DESC LIMIT 5;
                           """)
        else:
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY submission_time DESC LIMIT 5;
                           """)
    else:
        if order == 'DESC_BY_TIME':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY submission_time DESC;
                           """)
        elif order == 'ASC_BY_TIME':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY submission_time ASC;
                           """)
        elif order == 'ASC_BY_VOTES':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY vote_number ASC;
                           """)
        elif order == 'DESC_BY_VOTES':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY vote_number DESC;
                           """)
        elif order == 'ASC_BY_VIEWS':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY view_number ASC;
                           """)
        elif order == 'DESC_BY_VIEWS':
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY view_number DESC;
                           """)
        else:
            cursor.execute("""
                            SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY submission_time DESC;
                           """)
    question_data = cursor.fetchall()
    return question_data


# KZoli - Add new question.
@connection.connection_handler
def add_question(cursor, subject, text, picture_url):
    time = util.generate_time()
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
                          VALUES (%(sub_time)s, %(views)s, %(votes)s, %(subject)s, %(text)s, %(image)s);""",
                   {'sub_time': time, 'views': 0, 'votes': 0, 'subject': subject,
                    'text': text, 'image': picture_url})


# KZoli - Lists all the answers.
@connection.connection_handler
def answer_reader(cursor, question_id):
    cursor.execute("""
                    SELECT id, submission_time, vote_number, question_id, message, image FROM answer 
                    WHERE question_id = %(q_id)s ORDER BY submission_time ASC;
                   """, {'q_id': int(question_id)})
    answer_data = cursor.fetchall()
    data = answer_comment_reader(answer_data)
    return data


@connection.connection_handler
def answer_comment_reader(cursor, answer_data):
    for row_of_answer in answer_data:
        cursor.execute("""
                        SELECT * FROM comment 
                        WHERE answer_id = %(a_id)s ORDER BY submission_time DESC;
                       """, {'a_id': int(row_of_answer.get('id'))})
        row_of_answer['comments'] = cursor.fetchall()
    return answer_data


# KZoli - Finds the question for the answers to be displayed. Or just simply find a question.
@connection.connection_handler
def find_question_for_answer(cursor, question_id):
    cursor.execute("""
                    SELECT id, submission_time, vote_number, title, message, view_number, image FROM question 
                    WHERE id = %(q_id)s;
                   """, {'q_id': int(question_id)})
    question_data = cursor.fetchall()
    return question_data


# KZoli - Post an answer.
@connection.connection_handler
def post_answer(cursor, question_id, text, image):
    time = util.generate_time()
    cursor.execute("""INSERT INTO answer (submission_time, vote_number, question_id, message, image) 
                      VALUES (%(sub_time)s, %(votes)s, %(q_id)s, %(text)s, %(image_url)s);""",
                   {'sub_time': time, 'votes': 0, 'q_id': question_id, 'text': text, 'image_url': image})


# KZoli - Delete an answer.
@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM comment WHERE question_id = %(id)s;
                   """,
                   {'id': answer_id})
    cursor.execute("""
                    DELETE FROM comment WHERE answer_id = %(id)s;
                   """,
                   {'id': answer_id})
    cursor.execute("""
                    DELETE FROM answer WHERE id = %(id)s;
                   """,
                   {'id': answer_id})


# KZoli - Delete a question.
@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM comment WHERE question_id = %(id)s;
                   """,
                   {'id': question_id})
    ids_list = find_answers_id_for_question_id(question_id)
    for i in ids_list:
        cursor.execute("""
                        DELETE FROM comment WHERE answer_id = %(id)s;
                       """,
                       {'id': i})
    cursor.execute("""
                    DELETE FROM answer WHERE question_id = %(id)s;
                   """,
                   {'id': question_id})
    cursor.execute("""
                    DELETE FROM question_tag WHERE question_id = %(id)s;
                   """,
                   {'id': question_id})
    cursor.execute("""
                    DELETE FROM question WHERE id = %(id)s;
                   """,
                   {'id': question_id})


@connection.connection_handler
def find_answers_id_for_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT id FROM answer 
                    WHERE question_id = %(a_id)s;
                   """, {'a_id': int(question_id)})
    ids = cursor.fetchall()
    ids_list = []
    for i in ids:
        ids_list.append(i.get('id'))
    return ids_list


# KZoli - Update a question.
@connection.connection_handler
def update_question(cursor, question_id, subject, text):
    cursor.execute("""
                    UPDATE question SET message = %(message)s, title = %(title)s
                    WHERE id = %(id)s;""",
                   {'message': text, 'title': subject, 'id': question_id})


# KZoli - Update votes on a question.
@connection.connection_handler
def update_votes_question(cursor, question_id, vote):
    if vote == 'vote-up':
        cursor.execute("""
                        UPDATE question SET vote_number = vote_number + 1 WHERE id = %(id)s;""",
                       {'id': int(question_id)})
    else:
        cursor.execute("""
                        UPDATE question SET vote_number = vote_number - 1 WHERE id = %(id)s;""",
                       {'id': int(question_id)})


# KZoli - Update votes on an answer.
@connection.connection_handler
def update_votes_answer(cursor, vote, answer_id):
    if vote == 'vote-up':
        cursor.execute("""
                        UPDATE answer SET vote_number = vote_number + 1 WHERE id = %(id)s;""",
                       {'id': int(answer_id)})
    else:
        cursor.execute("""
                        UPDATE answer SET vote_number = vote_number - 1 WHERE id = %(id)s;""",
                       {'id': int(answer_id)})


# KZoli - View counter.
@connection.connection_handler
def update_views(cursor, question_id):
    cursor.execute("""
                    UPDATE question SET view_number = view_number + 1 WHERE id = %(id)s;""",
                   {'id': int(question_id)})


# KZoli - Posts a commment.
@connection.connection_handler
def post_comment(cursor, comment_id, comment, comment_type):
    submission_time = util.generate_time()
    if comment_type == 'question':
        cursor.execute("""INSERT INTO comment (submission_time, question_id, message, edited_count) 
                          VALUES (%(sub_time)s, %(q_id)s, %(text)s, %(edit)s);""",
                       {'sub_time': submission_time, 'q_id': comment_id, 'text': comment, 'edit': 0})
    else:
        cursor.execute("""INSERT INTO comment (submission_time, answer_id, message, edited_count) 
                          VALUES (%(sub_time)s, %(q_id)s, %(text)s, %(edit)s);""",
                       {'sub_time': submission_time, 'q_id': comment_id, 'text': comment, 'edit': 0})


# KZoli - Reads comments for questions.
@connection.connection_handler
def question_comment_reader(cursor, question_id):
    cursor.execute("""
                    SELECT id, question_id, submission_time, message, edited_count FROM comment 
                    WHERE question_id = %(q_id)s ORDER BY submission_time DESC;
                   """, {'q_id': int(question_id)})
    comment = cursor.fetchall()
    return comment


# KZoli - Delete a question comment.
@connection.connection_handler
def delete_question_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment WHERE id = %(id)s;
                   """,
                   {'id': comment_id})


# KZoli - Finds a question_id for an answer_id. Extends add_comment_to_answer function.
@connection.connection_handler
def find_question_id_for_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer WHERE id = %(a_id)s;
                   """, {'a_id': answer_id})
    question_id = cursor.fetchall()
    q_id = 0
    for id_of_question in question_id:
        q_id = id_of_question.get('question_id')
    return q_id


# KZoli - Finds an answer by an answer_id.
@connection.connection_handler
def find_answer_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT message FROM answer WHERE id = %(a_id)s;
                   """, {'a_id': answer_id})
    answer = cursor.fetchall()
    return answer


# KZoli - Update an answer.
@connection.connection_handler
def update_answer(cursor, text, answer_id):
    cursor.execute("""
                    UPDATE answer SET message = %(message)s WHERE id = %(a_id)s;""",
                   {'message': text, 'a_id': answer_id})


# KZoli - Find comment message by comment_id.
@connection.connection_handler
def find_comment_message_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT message FROM comment WHERE id = %(c_id)s;
                   """, {'c_id': comment_id})
    comment_message = cursor.fetchall()
    return comment_message


# KZoli - Update comment.
@connection.connection_handler
def update_question_comment(cursor, new_comment, comment_id):
    cursor.execute("""
                    UPDATE comment SET message = %(message)s WHERE id = %(c_id)s;""",
                   {'message': new_comment, 'c_id': comment_id})


# KZoli - Find question_id by comment_id.
@connection.connection_handler
def find_question_id_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT question_id FROM comment WHERE id = %(c_id)s;
                   """, {'c_id': comment_id})
    question_id = cursor.fetchall()
    q_id = 0
    for id_of_question in question_id:
        q_id = id_of_question.get('question_id')
    return q_id


# KZoli - Find question_id by comment_id for edit answer comment.
@connection.connection_handler
def find_question_id_by_comment_id_for_edit_answer_comment(cursor, comment_id):
    cursor.execute("""
                    SELECT answer_id FROM comment WHERE id = %(c_id)s;
                   """, {'c_id': comment_id})
    answer_id = cursor.fetchall()
    a_id = 0
    for id_of_answer in answer_id:
        a_id = id_of_answer.get('answer_id')
    q_id = find_question_id_from_answer_id(a_id)
    return q_id


# KZoli - Find question_id by answer_id.
@connection.connection_handler
def find_question_id_from_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer WHERE id = %(a_id)s;
                   """, {'a_id': answer_id})
    question_id = cursor.fetchall()
    q_id = 0
    for id_of_question in question_id:
        q_id = id_of_question.get('question_id')
    return q_id


# KZoli - Update edit counter for comments.
@connection.connection_handler
def increase_edit_counter(cursor, comment_id):
    cursor.execute("""
                    UPDATE comment SET edited_count = edited_count + 1 WHERE id = %(id)s;""",
                   {'id': int(comment_id)})


@connection.connection_handler
def search(cursor, search_text):
    search_text = '%' + search_text + '%'
    cursor.execute("""
                    SELECT id, vote_number, title, submission_time, view_number FROM question
                    WHERE LOWER(title) LIKE %(text)s OR message LIKE %(text)s;
                   """, {'text': search_text})
    search_result = cursor.fetchall()
    return search_result


@connection.connection_handler
def read_tags(cursor):
    cursor.execute("""
                    SELECT * FROM tag
                    """)
    tags = cursor.fetchall()
    return tags


@connection.connection_handler
def add_tag(cursor, new_tag):
    cursor.execute("""
                    SELECT name FROM tag WHERE name = %(tag)s;
                    """, {'tag': new_tag})
    tag_check = cursor.fetchall()
    if tag_check != []:
        return
    cursor.execute("""
                    SELECT id FROM question ORDER BY submission_time DESC LIMIT 1;
                    """)
    newest_question_id = cursor.fetchall()
    newest_question_id = newest_question_id[0].get('id')
    cursor.execute("""
                  INSERT INTO tag (name) VALUES (%(tag)s);
                  """, {'tag': new_tag})
    cursor.execute("""
                    SELECT id FROM tag ORDER BY id DESC LIMIT 1;
                    """)
    newest_tag_id = cursor.fetchall()
    newest_tag_id = newest_tag_id[0].get('id')
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id) VALUES (%(q_id)s, %(t_id)s);
                    """, {'q_id': newest_question_id, 't_id': newest_tag_id})


@connection.connection_handler
def get_list_of_tag_ids(cursor):
    cursor.execute("""
                    SELECT id FROM tag;
                    """)
    ids = cursor.fetchall()
    id_list = []
    for i in ids:
        id_list.append(i.get('id'))
    return id_list


@connection.connection_handler
def add_existing_tags_to_new_question(cursor, existing_tags):
    cursor.execute("""
                    SELECT id FROM question ORDER BY submission_time DESC LIMIT 1;
                    """)
    question_id = cursor. fetchall()[0].get('id')
    for existing_tag in existing_tags:
        cursor.execute("""
                        INSERT INTO question_tag (question_id, tag_id) VALUES (%(q_id)s, %(t_id)s);
                        """, {'q_id': question_id, 't_id': int(existing_tag)})


@connection.connection_handler
def get_tags_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT tag_id FROM question_tag WHERE question_id = %(q_id)s;
                    """, {'q_id': question_id})
    tag_ids = cursor.fetchall()
    tag_names = []
    for tag_id in tag_ids:
        cursor.execute("""
                        SELECT name FROM tag WHERE id = %(t_id)s;
                        """, {'t_id': tag_id.get('tag_id')})
        tag_name = cursor.fetchall()
        tag_names.append(tag_name[0].get('name'))
    return tag_names

@connection.connection_handler
def get_checked_tags(cursor, question_id):
    cursor.execute("""
                    SELECT tag_id FROM question_tag WHERE question_id = %(q_id)s;
                    """, {'q_id': question_id})
    tag_ids = cursor.fetchall()
    tag_list = []
    for i in tag_ids:
        tag_list.append(i.get('tag_id'))
    return tag_list


@connection.connection_handler
def compare_new_tags_to_old_ones(cursor, new_tags_for_question, question_id):
    cursor.execute("""
                    SELECT tag_id FROM question_tag WHERE question_id = %(q_id)s;
                    """, {'q_id': question_id})
    old_tags_for_question = cursor.fetchall()
    for i in range(len(old_tags_for_question)):
        old_tags_for_question[i] = old_tags_for_question[i].get('tag_id')
    print(old_tags_for_question)
    for i in range(len(new_tags_for_question)):
        new_tags_for_question[i] = int(new_tags_for_question[i])
    print(new_tags_for_question)
    for i in range(len(old_tags_for_question)):
        old_tags_for_question[i] = int(old_tags_for_question[i])
    print(old_tags_for_question)
    for old_tag in old_tags_for_question:
        if old_tag not in new_tags_for_question:
            cursor.execute("""
                            DELETE FROM question_tag WHERE question_id = %(id)s AND tag_id = %(old_tag)s;
                           """,
                           {'id': question_id, 'old_tag': old_tag})
    for new_tag in new_tags_for_question:
        if new_tag not in old_tags_for_question:
            cursor.execute("""
                          INSERT INTO question_tag (question_id, tag_id) VALUES (%(q_id)s, %(t_id)s);
                          """, {'q_id': question_id, 't_id': new_tag})


@connection.connection_handler
def add_tag_for_existing_question(cursor, new_tag, question_id):
    cursor.execute("""
                    SELECT name FROM tag WHERE name = %(tag)s;
                    """, {'tag': new_tag})
    tag_check = cursor.fetchall()
    if tag_check != []:
        return
    cursor.execute("""
                  INSERT INTO tag (name) VALUES (%(tag)s);
                  """, {'tag': new_tag})
    cursor.execute("""
                    SELECT id FROM tag ORDER BY id DESC LIMIT 1;
                    """)
    newest_tag_id = cursor.fetchall()
    newest_tag_id = newest_tag_id[0].get('id')
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id) VALUES (%(q_id)s, %(t_id)s);
                    """, {'q_id': int(question_id), 't_id': newest_tag_id})
    return newest_tag_id


@connection.connection_handler
def delete_question_tag(cursor, question_id, tag_id):
    cursor.execute("""
                    DELETE FROM question_tag WHERE tag_id = %(t_id)s;
                   """,
                   {'t_id': int(tag_id)})
    cursor.execute("""
                    DELETE FROM tag WHERE id = %(id)s;
                   """,
                   {'id': int(tag_id)})
