import os
import csv
# import random
import datetime


def _match_score(my_answer, mentor_answer):
    """Calculate Score."""
    matches = 0
    my_ans = [x.lower() for x in my_answer]
    ment_ans = [x.lower() for x in mentor_answer[0]]
    for (a, b) in zip(my_ans, ment_ans):
        if a == b:
            matches += 1
    return matches


def dummy_match(my_answer):
    return 1


def get_mentor_match(my_answer, mentors):
    best_score = 0
    best_mentor = mentors[0][1]
    # if no match to any mentors, randomly select one
    for k in mentors:
        # for each mentor, find score
        score = _match_score(my_answer, mentors[0])
        if score > best_score:
            best_score = score
            best_mentor = k[1]
    return best_mentor


def load_mentor_answers(filename):
    answers = []
    f = "sciencerunaway/static/" + filename
    with open(f, 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|', dialect=csv.excel_tab)
        for index, row in enumerate(spamreader):
            if index == 0:
                continue
            answers.append([row[1:], row[0]])
    return answers


def load_mentor_profiles(filename, backupfile, csv_file=True):

    mentors = {}
    mentors_questions = []
    f = "sciencerunaway/static/" + filename
    with open(f, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for index, row in enumerate(spamreader):
            if index == 0:
                mentors_questions = row
                continue
            try:
                mentors[row[0]] = row[1:]
            except:
                pass
    return mentors, mentors_questions


def _load_questions(filename):
    questions = {}
    f = open("sciencerunaway/static/" + filename)
    lines = f.read().split("\r")
    for line in lines[1:]:
        row = line.split(',')
        questions[row[0]] = row[1:]
    return questions


def load_questions(filename):
    questions = []
    f = "sciencerunaway/static/" + filename
    with open(f, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for index, row in enumerate(spamreader):
            if index == 0:
                continue
            questions.append(row)
    return questions


def load_mentor_names(filename):
    links = {}
    # links_rev = {}
    f = open("sciencerunaway/static/" + filename)

    f = "sciencerunaway/static/" + filename
    with open(f, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for index, row in enumerate(spamreader):
            if index == 0:
                continue

            links[row[0]] = row[1]
            # links_rev[row[1]] = row[0]

    return links

    lines = f.read().split("\r")
    for line in lines[1:]:
        row = line.split(',')


def write_log_file(file, line):
    if not os.path.exists(file):
        open(file, 'w').close()

    with open(file, "a") as myfile:
        myfile.write(str(datetime.datetime.today()) + "\t" + line + "\n")

def add_answer_to_db(answer, db = 'file'):
    TBL_NAME = 'responses'
    timestamp = datetime.today()
    sql_cmd = "INSERT " + ','.join(answer) + " INTO " + responses + ";"
    sql_cmd += "COMMIT;"
    #create new cursor
    if db == 'file':
        pass
        # print (answer)
    elif db == 'mysql':
    #execute ecommand
        msg = cur.execute(sql_cmd)
        return msg

def main(answers, logfile = "database.log", mentor_files = "mentor_profiles.csv"):
    #given answers, return page to go to and 
    #also store answer

    #
    msg = add_answer_to_db(answers)
    mentors = load_mentor_answers(mentor_files)
    match = get_mentor_match(answers, mentors)
    return match

