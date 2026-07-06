from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

print("Loading AI model... Please wait...")

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

print("AI model loaded successfully!")

@app.route("/", methods=["GET", "POST"])
def index():

    summary = ""

    if request.method == "POST":

        text = request.form["text"]

        if len(text) < 50:
            summary = "Please enter at least 50 characters."
        else:

            result = summarizer(
                text,
                max_length=150,
                min_length=40,
                do_sample=False
            )

            summary = result[0]["summary_text"]

    return render_template(
        "index.html",
        summary=summary
    )

if __name__ == "__main__":
    app.run(debug=True)