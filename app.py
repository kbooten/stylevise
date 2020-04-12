from flask import Flask
from flask import render_template,jsonify,request
import os
app = Flask(__name__)

from Judge import Judge
judge = Judge()

@app.route('/')
def main_page():
    return render_template('webgame.html')


@app.route('/evaluate', methods=['POST'])
def get_input():
	content = request.get_json()
	input_sentence = content['currentSentence']
	level = content['currentLevel']
	old_sentences = content["oldSentences"]
	returnValues = judge.input_and_test_new_sent(input_sentence,level,old_sentences)
	return jsonify(returnValues)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)