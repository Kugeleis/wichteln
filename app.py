"""
This module contains the Flask application for the Secret Santa web interface.
"""

from flask import Flask, render_template, request, redirect, url_for
from src.wichteln.main import SecretSanta

app = Flask(__name__)
game = SecretSanta()

@app.route('/')
def index():
    """
    Renders the main page.
    """
    return render_template('index.html', participants=game.participants)

@app.route('/add', methods=['POST'])
def add_participant():
    """
    Adds a participant to the game.
    """
    name = request.form.get('name')
    if name:
        game.add_participant(name)
    return redirect(url_for('index'))

@app.route('/assign')
def assign():
    """
    Assigns Secret Santas and redirects to the results page.
    """
    game.assign_santas()
    return redirect(url_for('results'))

@app.route('/results')
def results():
    """
    Renders the results page.
    """
    return render_template('results.html', assignments=game.assignments)

@app.route('/reset', methods=['POST'])
def reset():
    """
    Resets the game and redirects to the main page.
    """
    game.reset()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)