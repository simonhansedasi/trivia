from flask import Flask, render_template, jsonify, request
import requests
import random
import html
import os

app = Flask(__name__)

OPENTDB = 'https://opentdb.com/api.php'
OPENTDB_CATEGORIES = 'https://opentdb.com/api_category.php'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/categories')
def categories():
    resp = requests.get(OPENTDB_CATEGORIES, timeout=5)
    return jsonify(resp.json()['trivia_categories'])

@app.route('/get_question')
def get_question():
    params = {'amount': 1, 'type': 'multiple'}
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    if category:
        params['category'] = category
    if difficulty:
        params['difficulty'] = difficulty

    resp = requests.get(OPENTDB, params=params, timeout=5)
    data = resp.json()

    if data['response_code'] == 5:
        return jsonify({'error': 'rate_limit'}), 429
    if data['response_code'] != 0:
        return jsonify({'error': 'no_results'}), 404

    result = data['results'][0]
    correct = html.unescape(result['correct_answer'])
    all_answers = [html.unescape(a) for a in result['incorrect_answers']] + [correct]
    random.shuffle(all_answers)

    labels = ['A', 'B', 'C', 'D']
    answers = [
        {'choice': labels[i], 'text': a, 'correct': a == correct}
        for i, a in enumerate(all_answers)
    ]

    return jsonify({
        'question': html.unescape(result['question']),
        'category': result['category'],
        'difficulty': result['difficulty'],
        'answers': answers,
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5014))
    app.run(host='0.0.0.0', port=port)
