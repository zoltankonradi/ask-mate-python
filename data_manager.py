import csv, time
import urllib

def answer_reader(csv_file):
    dictionary = {}
    for row in csv_file:
        if 'id' in dictionary:
            dictionary['id'].append(row[0])
        else:
            dictionary.update({'id': []})
        if 'submission_time' in dictionary:
            dictionary['submission_time'].append(row[1])
        else:
            dictionary.update({'submission_time': []})
        if 'vote_number' in dictionary:
            dictionary['vote_number'].append(row[2])
        else:
            dictionary.update({'vote_number': []})
        if 'question_id' in dictionary:
            dictionary['question_id'].append(row[3])
        else:
            dictionary.update({'question_id': []})
        if 'message' in dictionary:
            dictionary['message'].append(row[4])
        else:
            dictionary.update({'message': []})
        if 'image' in dictionary:
            dictionary['image'].append(row[5])
        else:
            dictionary.update({'image': []})
    return dictionary


def question_reader(csv_file):
    dictionary = {}
    for row in csv_file:
        if 'id' in dictionary:
            dictionary['id'].append(row[0])
        else:
            dictionary.update({'id': []})
        if 'submission_time' in dictionary:
            dictionary['submission_time'].append(row[1])
        else:
            dictionary.update({'submission_time': []})
        if 'view_number' in dictionary:
            dictionary['view_number'].append(row[2])
        else:
            dictionary.update({'view_number': []})
        if 'vote_number' in dictionary:
            dictionary['vote_number'].append(row[3])
        else:
            dictionary.update({'vote_number': []})
        if 'title' in dictionary:
            dictionary['title'].append(row[4])
        else:
            dictionary.update({'title': []})
        if 'message' in dictionary:
            dictionary['message'].append(row[5])
        else:
            dictionary.update({'message': []})
        if 'image' in dictionary:
            dictionary['image'].append(row[6])
        else:
            dictionary.update({'image': []})
    return dictionary


def csv_reader(filename):
    with open(filename) as csvfile:
        csv_file = csv.reader(csvfile, delimiter=',')
        if filename == 'sample_data/question.csv':
            return question_reader(csv_file)
        else:
            return answer_reader(csv_file)


def add_question(filename, id, submission_time, view_number, vote_number, title, message, image):
    new_data = [id, submission_time, view_number, vote_number, title, message, image]
    with open(filename, "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_data)


def add_answer(filename, id, submission_time, vote_number, question_id, message, image):
    new_data =[id, submission_time, vote_number, question_id, message, image]
    with open(filename, "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_data)


def delete_answer(answer_id):
    with open("sample_data/answer.csv", 'r+') as csvfile:
        file_content=csvfile.readlines()
    for i in range(len(file_content)):
        file_content[i]=file_content[i].split(',')
    for i in range(len(file_content)):
        if file_content[i][0] == answer_id:
            del file_content[i]
            break
    for i in range(len(file_content)):
        file_content[i]=','.join(file_content[i])
    with open("sample_data/answer.csv", "w") as csvfile:
        csvfile.writelines(file_content)
    return


def update_view_number_question(filename, data):
    with open (filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        first_row = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
        writer.writerow(first_row)
        for entry in range(len(data["id"])):
            row = [data["id"][entry],
                   data["submission_time"][entry],
                   data["view_number"][entry],
                   data["vote_number"][entry],
                   data["title"][entry],
                   data["message"][entry],
                   data["image"][entry]]
            writer.writerow(row)


def update_answer_csv(filename, data):
    with open (filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        first_row = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
        writer.writerow(first_row)
        for entry in range(len(data["id"])):
            row = [data["id"][entry],
                   data["submission_time"][entry],
                   data["vote_number"][entry],
                   data["question_id"][entry],
                   data["message"][entry],
                   data["image"][entry]]
            writer.writerow(row)


def generate_question_id(data):
    id = len(data["id"])
    return id


def generate_answer_id(data):
    id = int(data["id"][-1]) + 1
    return id


def get_submission_time():
    return int(time.time())

