from flask import Flask, jsonify
import speech_generator

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_sentence(word):
    return "welcome to the trumpifier server"

@app.route('/sentence/<word>', methods=['GET'])
def get_sentence(word):
    print ("got word", word)
    return jsonify({'sentence': speech_generator.run(word, 1)})


if __name__ == '__main__':
    app.run(debug=True)
