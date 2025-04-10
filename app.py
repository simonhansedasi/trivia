from flask import Flask, render_template, request, redirect, url_for, jsonify
import trivia as tr
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 


# Initialize questions and numbers globally for easy access
qs, ns = tr.open_questions()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    
    
    # Randomly select a question to serve
    next_question = random.choice(ns)
    question_data = next(q for q in qs if q['number'] == next_question)

    # Return question and answer choices as JSON
    # return question_data
    return jsonify(question_data)

@app.route('/reveal_answer', methods=['POST'])
def reveal_answer():
    question_number = request.json.get('question_number')
    question = next(q for q in qs if q['number'] == question_number)
    correct_answer = None

    # Find the correct answer
    for i, answer in enumerate(question['answers']):
        if answer['correct']:
            correct_answer = 'ABC'[i]

    # Return the correct answer as JSON
    return jsonify({"correct_answer": correct_answer})


if __name__ == "__main__":
    app.run(port = 5005)
