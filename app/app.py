from flask import Flask, render_template
import json

app = Flask(__name__)

# Load JSON data
with open('documents/NARA_files.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

@app.route('/')
def index():
    # Extract transcripts from the JSON data
    transcripts = data.get('digitalObjects')
    print(data.get('digitalObjects')[0])
    return render_template('index.html', transcripts=transcripts)

if __name__ == '__main__':
    app.run(debug=True)
