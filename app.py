from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    """Start a new game"""
    session['target_number'] = random.randint(1, 100)
    session['guesses'] = 0
    session['game_over'] = False
    session['messages'] = []
    return jsonify({
        'status': 'success',
        'message': 'New game started! Guess a number between 1 and 100.'
    })

@app.route('/guess', methods=['POST'])
def make_guess():
    """Process a guess"""
    if 'target_number' not in session:
        return jsonify({
            'status': 'error',
            'message': 'No active game. Please start a new game.'
        })
    
    try:
        guess = int(request.json.get('guess'))
    except (ValueError, TypeError):
        return jsonify({
            'status': 'error',
            'message': 'Please enter a valid number.'
        })
    
    if session.get('game_over'):
        return jsonify({
            'status': 'error',
            'message': 'Game is over. Please start a new game.'
        })
    
    target = session['target_number']
    session['guesses'] += 1
    guesses = session['guesses']
    
    if guess == target:
        session['game_over'] = True
        return jsonify({
            'status': 'success',
            'message': f'🎉 Congratulations! You guessed the number {target} correctly in {guesses} attempt{"s" if guesses != 1 else ""}!',
            'game_over': True,
            'guesses': guesses,
            'target': target
        })
    elif guess > target:
        return jsonify({
            'status': 'hint',
            'message': f'Too high! Try a lower number. (Attempt {guesses})',
            'game_over': False,
            'guesses': guesses
        })
    else:
        return jsonify({
            'status': 'hint',
            'message': f'Too low! Try a higher number. (Attempt {guesses})',
            'game_over': False,
            'guesses': guesses
        })

@app.route('/game_status', methods=['GET'])
def game_status():
    """Get current game status"""
    return jsonify({
        'has_game': 'target_number' in session,
        'game_over': session.get('game_over', False),
        'guesses': session.get('guesses', 0)
    })

if __name__ == '__main__':
    app.run(debug=True)
