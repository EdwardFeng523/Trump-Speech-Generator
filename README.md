# Trump-Speech-Generator

## About

This is a trumpified chat bot built by a high order bidirectional markov model. It is well tuned such that given a word, it is going to give back a sentence containing the word sounds like what Trump has said.

## Getting started

### Installing

```
git clone https://github.com/EdwardFeng523/Trump-Speech-Generator.git
cd Trump-Speech-Generator
pip install -r requirements.txt
```

### Running locally

```
python app.py
```
Then terminal will notify you that the app is running on your local server. The server should run at `http://localhost:8080`

## REST API

Currently this speech generator is available on Heroku as a REST API.

```
Endpoint: http://trumpifier1.herokuapp.com/sentence/<word>
Sample request:  http://trumpifier1.herokuapp.com/sentence/love
Sample output: {"sentence":"I love the Tea Party and you can call it anything that you want ."}
```
Note that because Heroku turns the server off when no request is directed to the server for certain amount of time, it might take a while for you to get response the first time you use it (since the server is being restarted).
