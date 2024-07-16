from flask import Flask, render_template
import json

app = Flask(__name__)

# Load JSON data
with open('documents/NARA_files.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
with open('logs/transcripts.json', 'r', encoding='utf-8') as file:
    data2 = json.load(file)


@app.route('/')
def index():
    # Extract transcripts from the JSON data
    transcripts = data.get('digitalObjects')
    print(data.get('digitalObjects')[0])
    return render_template('index.html', transcripts=transcripts)

@app.route('/transcript')
def transcripts():
    # Extract transcripts from the JSON data
    transcripts = data2.get('transcripts')
    return render_template('transcript.html', transcripts=transcripts)

@app.route('/transcript/<id>')
def transcript(id):
    # Extract transcripts from the JSON data
    transcripts = data2.get('transcripts')
    valid = []

    for transcript in transcripts:
        if transcript.get('filename') == id:
            valid.append(transcript)
    
    return render_template('transcript.html', transcripts=valid)


if __name__ == '__main__':
    app.run(debug=True)
