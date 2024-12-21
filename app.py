from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'smash_secret'

@app.route('/')
def home():
    session.clear()
    return render_template('home.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/start', methods=['POST'])
def start():
    session['total_distance'] = random.randint(10, 15)
    session['time_elapsed'] = 0
    session['mph'] = 0
    session['position'] = 1
    session['game_over'] = False
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        if session.get('game_over', False):
            return redirect(url_for('home'))

        move = int(request.form.get('move', 0))
        if move < 1 or move > 8:
            error = "Invalid move. Enter a number between 1 and 8."
            return render_template('game.html', error=error, **session)

        # Update game state
        mph = session['mph']
        if move == 1:
            mph = mph * 3 + 20 + random.randint(1, 10)
        elif move == 2:
            mph = mph * 3 // 2 + 7 + random.randint(1, 6)
        elif move == 3:
            mph = mph * 7 // 8 - 6 + random.randint(1, 4)
        elif move == 4:
            mph = mph * 4 // 7 - 26 + random.randint(1, 8)
        elif move in (5, 6, 7, 8):
            mph = mph * 9 // 10 * (0.7 + random.random() * 0.6)
        mph = max(0, mph)

        # Check for collision
        if random.randint(1, 100) < 10:  # 10% chance
            session['game_over'] = True
            return render_template('game.html', smash=True, **session)

        session['mph'] = mph
        session['time_elapsed'] += 1
        session['total_distance'] -= mph // 120

        if session['total_distance'] <= 0:
            session['game_over'] = True
            return render_template('game.html', finish=True, **session)

        session['position'] = random.randint(1, 7)

    return render_template('game.html', **session)

if __name__ == '__main__':
    app.run(debug=True)