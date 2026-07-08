# ==========================================================
# SummarAI AI Engine
# ==========================================================

import re


# ==========================================================
# Clean Text
# ==========================================================

def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()



# ==========================================================
# Split Sentences
# ==========================================================

def split_sentences(text):

    sentences = re.split(

        r'(?<=[.!?])\s+',

        text

    )

    return sentences



# ==========================================================
# Word Frequency
# ==========================================================

def word_frequency(words):

    frequency = {}


    for word in words:

        word = word.lower()


        if len(word) > 3:

            frequency[word] = frequency.get(word,0)+1


    return frequency



# ==========================================================
# Summarize Text
# ==========================================================

def summarize_text(text, sentence_count=3):


    if not text:

        return "No text provided"



    text = clean_text(text)


    sentences = split_sentences(text)



    if len(sentences) <= sentence_count:

        return text



    words=[]


    for sentence in sentences:

        words.extend(
            sentence.split()
        )



    frequency = word_frequency(words)



    scores={}



    for sentence in sentences:


        score=0


        for word in sentence.split():


            clean_word = re.sub(

                r"[^a-zA-Z]",

                "",

                word.lower()

            )


            score += frequency.get(

                clean_word,

                0

            )



        scores[sentence]=score




    ranked = sorted(

        scores,

        key=scores.get,

        reverse=True

    )



    selected = ranked[:sentence_count]



    summary=[]



    for sentence in sentences:

        if sentence in selected:

            summary.append(sentence)



    return " ".join(summary)



# ==========================================================
# Text Details
# ==========================================================

def get_text_details(text):


    return {

        "words":
        len(text.split()),


        "characters":
        len(text),


        "sentences":
        len(split_sentences(text))

    }



# ==========================================================
# Test
# ==========================================================

if __name__=="__main__":


    sample="""

    Artificial intelligence is growing fast.

    AI helps people solve problems.

    Machine learning is a part of AI.

    """


    print(
        summarize_text(sample)
    )
    import re
from collections import Counter


def clean_text(text):
    """Remove extra spaces and line breaks."""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_sentences(text):
    """Split text into sentences."""

    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [s for s in sentences if s.strip()]


def tokenize(text):
    """Convert text into words."""

    words = re.findall(r"[A-Za-z']+", text.lower())

    return words


def summarize_text(text, max_sentences=3):
    """
    Simple frequency-based summarizer.
    """

    text = clean_text(text)

    if not text:
        return "Please enter some text."

    sentences = split_sentences(text)

    if len(sentences) <= max_sentences:
        return text

    words = tokenize(text)

    frequency = Counter(words)

    scores = {}

    for sentence in sentences:

        sentence_words = tokenize(sentence)

        score = 0

        for word in sentence_words:

            score += frequency[word]

        scores[sentence] = score

    best = sorted(
        scores,
        key=scores.get,
        reverse=True
    )[:max_sentences]

    summary = []

    for sentence in sentences:

        if sentence in best:

            summary.append(sentence)

    return " ".join(summary)


def get_text_details(text):

    text = clean_text(text)

    words = len(tokenize(text))

    characters = len(text)

    sentences = len(split_sentences(text))

    reading_time = max(1, round(words / 200))

    return {
        "words": words,
        "characters": characters,
        "sentences": sentences,
        "reading_time": reading_time
    }


if __name__ == "__main__":

    sample = """
    Artificial Intelligence is transforming the world.
    It helps automate repetitive tasks.
    Machine learning is a branch of AI.
    AI is widely used in healthcare, education and finance.
    It improves productivity and decision making.
    """

    print("Summary:\n")

    print(summarize_text(sample))

    print("\nDetails:\n")

    print(get_text_details(sample))