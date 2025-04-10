import re
import random
import zipfile
import os
import json
from tqdm import tqdm



def open_questions():

    print('loading...')
    root = '/home/simonhans/coding/trivia/data/'
    file = os.path.join(root, 'archive.zip')
    extracted = os.path.join(root, 'extracted')


    if not os.path.exists(extracted):
        os.makedirs(extracted)

    if not os.path.isfile(os.path.join(extracted, 'DB.json')):
        with zipfile.ZipFile(file) as zip_ref:
            zip_ref.extractall(os.path.join(root, 'extracted'))
    elif os.path.isfile(os.path.join(extracted, 'DB.json')):
        print('data extracted,,,')


    db = os.path.join(extracted, 'DB.json')

    with open(db, 'r') as file:
        data = json.load(file)



    print('loading questions...')
    ticker = 0
    questions = []
    for i in tqdm(data):
        ticker += 1
        # print(i)
        number = ticker
        question = i['question']

        q = {}

        q['number'] = ticker
        q['question'] = i['question']

        q['answers'] = i['answers']
        questions.append(q)


    url_pattern = re.compile(r'https?://[^\s]+')

    print('organizing questions...')

    questions = [question for question in questions if not any(url_pattern.search(answer['text']) for answer in question['answers'])]
    for index, item in enumerate(questions, start = 1):
        item['number'] = index



    numbers = [q['number'] for q in questions]
    
    return questions, numbers




def select_question(questions, numbers):

    n = random.choice(numbers) 
    print(questions[n]['question'])



    correct = None
    for l in range(3):
        choice = questions[n]['answers'][l]['choice']
        text =  questions[n]['answers'][l]['text']
        if questions[n]['answers'][l]['correct'] == True:
            if l == 0:
                correct = 'A'
            elif l == 1:
                correct = 'B'
            elif l == 2:
                correct = 'C'
        print(f'{choice}: {text}')
    print('')
    while True:
        selection = input('What is your final answer? A, B, or C? ').upper()

        if selection not in ['A', 'B', 'C']:
            print('')
            print('Please select a valid answer: A, B, or C')
        else:
            break  # Exit loop if input is valid

    # Check if the selected answer is correct
    if selection == correct:
        print("Correct! You're so smart!")
        print('')
    else:
        print("Incorrect!")
        print(f'Correct answer is {correct}')
        print('')