from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from io import BytesIO
import os

from raffle_core import read_participants, read_exclusions, run_raffle

MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret')
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            prizes_str = request.form.get('prizes', '').strip()
            seed = request.form.get('seed', '').strip() or None

            if not prizes_str.isdigit() or int(prizes_str) <= 0:
                flash('Please enter a valid positive integer for number of prizes.', 'error')
                return redirect(url_for('index'))
            prizes = int(prizes_str)

            participants_file = request.files.get('participants')
            if not participants_file or participants_file.filename == '':
                flash('Please upload the participants CSV.', 'error')
                return redirect(url_for('index'))

            exclude_file = request.files.get('exclude')

            try:
                totals = read_participants(participants_file.stream)
                if exclude_file and exclude_file.filename:
                    excluded = read_exclusions(exclude_file.stream)
                    for x in excluded:
                        totals.pop(x, None)

                results = run_raffle(totals, prizes, seed)
                return render_template('results.html', results=results)
            except Exception as e:
                flash(f'Error: {e}', 'error')
                return redirect(url_for('index'))

        return render_template('index.html')

    return app

app = create_app()
