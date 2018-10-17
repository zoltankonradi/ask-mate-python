import csv


def csv_reader(filename):
    with open(filename) as csvfile:
        csv_file = csv.reader(csvfile, delimiter=',')
        if filename == 'sample_data/question.csv':
            return question_reader(csv_file)
        else:
            return answer_reader(csv_file)


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


# def get_table_from_file(file_name):
#     with open(file_name, "r") as file:
#         lines = file.readlines()
#     table = [element.replace("\n", "").split(",") for element in lines]
#     return table
#
#
# def write_table_to_file(file_name, table, method):
#     with open(file_name, method) as file:
#         for record in table:
#             row = ';'.join(record)
#             file.write(row + "\n")
