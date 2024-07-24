from flask import Flask, render_template, request, session, redirect, url_for
import requests
import logging

app=Flask(__name__)
app.secret_key='first_project'

API_URL="https://random-word-api.herokuapp.com/word?number=1"

def get_word():
    response=requests.get(API_URL)
    logging.debug(f"Request: {response.request.url}")
    logging.debug(f"Status Code: {response.status_code}")
    logging.debug(f"Response Text: {response.text}")
    if(response.status_code == 200):
        return response.json()[0].upper()
    return None

@app.route('/')
def index():
    if 'word' not in session:
        session['word']=get_word()
        session['guessct']=[]
        session['miss']=0
        session['msg']=''
    word_disp=''.join(l if l in session['guessct'] else '_' for l in session['word'])
    return render_template('index.html', word_disp=word_disp, guesses=session['guessct'], misses=session['miss'],  message=session.get('msg', ''))

@app.route('/reset')
def reset():
    session.pop('word', None)
    session.pop('guessct', None)
    session.pop('miss', None)
    session.pop('msg', None)
    return redirect(url_for('index'))

@app.route('/guess',  methods=['POST'])
def guess():
    guess=request.form['guess'].upper()
    if guess not in session['guessct']:
        session['guessct'].append(guess)
        if guess in session['word']:
            session['msg']=f"Good Guess! '{guess}' is in the word!"
        else:
            session['miss']+=1
            session['msg']=f"Sorry! '{guess}' is not in the word!"
    else:
        session['msg']=f"You already guessed '{guess}'"
    return redirect(url_for('index'))



if __name__  == '__main__':
    app.run(debug=True)