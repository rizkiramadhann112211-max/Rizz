from flask import Flask, request, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target = request.form.get('target', '').strip()
        threads = request.form.get('threads', '5').strip()
        if not target:
            return render_template('index.html', error='Masukkan nomor target, Yang Mulia!')
        
        # Perbaikan: jalankan main_engine.py dengan input melalui stdin
        input_data = f"{target}\n{threads}\n"
        try:
            result = subprocess.run(
                ['python', 'main_engine.py'],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=60
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = '⏰ Proses terlalu lama, coba kurangi thread.'
        except Exception as e:
            output = f'❌ Error: {str(e)}'
        return render_template('index.html', output=output)
    return render_template('index.html')

app = app