import markovify
import twilio.twiml
from flask import Flask, request, redirect


app = Flask(__name__)

@app.route("/message", methods=['GET', 'POST'])
def message():
    resp = twilio.twiml.Response()
    resp.message(model.make_short_sentence(100))
    return str(resp)

if __name__ == "__main__":
    with open("tweets.csv") as f:
        text = f.read()

    model = markovify.Text(text)
    app.run(debug=True)

