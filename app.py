from flask import Flask, render_template, request, redirect
import random

app = Flask(__name__)

# WORDS + HINTS
words = {
    "apple": "A fruit",
    "banana": "Yellow fruit",
    "juice": "A drink",
    "mango": "King of fruits",
    "movie": "Cinema",
    "beautiful": "Pretty",
    "television": "Watching device"
}

# START GAME
def start_game():

    global word, hint, display, chances, guessed

    word = random.choice(list(words.keys()))
    hint = words[word]

    display = ["_"] * len(word)

    chances = 6

    guessed = []


start_game()


@app.route("/", methods=["GET", "POST"])
def home():

    global word, hint, display, chances, guessed

    message = ""

    # HANGMAN STAGES
    stages = [

"""
  -----
  |   |
  |   O
  |  /|\\
  |  / \\
__|__
""",

"""
  -----
  |   |
  |   O
  |  /|\\
  |  /
__|__
""",

"""
  -----
  |   |
  |   O
  |  /|\\
  |
__|__
""",

"""
  -----
  |   |
  |   O
  |   |
  |
__|__
""",

"""
  -----
  |   |
  |   O
  |
  |
__|__
""",

"""
  -----
  |   |
  |
  |
  |
__|__
""",

"""
     
     
     
     
     
"""
]

    if request.method == "POST":

        # GET INPUT
        guess = request.form["guess"].lower()

        # ALREADY GUESSED
        if guess in guessed:

            message = "Already Guessed!"

        else:

            guessed.append(guess)

            # CORRECT LETTER
            if guess in word:

                message = "Correct!"

                for i in range(len(word)):

                    if word[i] == guess:

                        display[i] = guess

            # WRONG LETTER
            else:

                message = "Wrong!"

                chances -= 1

    # WIN
    if "_" not in display:

        message = "🎉 You Won!"

    # LOSE
    if chances <= 0:

        message = f"💀 Game Over! Word was '{word}'"

    # HANGMAN
    hangman = stages[max(0, chances)]

    return render_template(
        "index.html",
        display=" ".join(display),
        chances=chances,
        guessed=", ".join(guessed),
        message=message,
        hint=hint,
        hangman=hangman
    )


# RESET GAME
@app.route("/reset")
def reset():

    start_game()

    return redirect("/")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)