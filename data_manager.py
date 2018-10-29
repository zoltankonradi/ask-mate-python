import connection
import util


# KZoli - Reads in the questions, and sorts it.
@connection.connection_handler
def question_reader(cursor, order):
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
                        SELECT id, vote_number, title, submission_time, view_number FROM question ORDER BY vote_number DESC;
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
    return answer_data


# KZoli - Finds the question for the answers to be displayed. Or just simply find a question.
@connection.connection_handler
def find_question_for_answer(cursor, question_id):
    cursor.execute("""
                    SELECT id, submission_time, vote_number, title, message, view_number FROM question 
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
                    DELETE FROM answer WHERE id = %(id)s;
                   """,
                   {'id': answer_id})


# KZoli - Delete a question.
@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM answer WHERE question_id = %(id)s;
                   """,
                   {'id': question_id})
    cursor.execute("""
                    DELETE FROM question WHERE id = %(id)s;
                   """,
                   {'id': question_id})


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