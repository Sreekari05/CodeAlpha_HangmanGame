from flask import Flask, render_template, request, redirect
import random

app = Flask(__name__)

# Words and hints
words = {
    "apple": "A fruit",
    "banana": "Yellow fruit",
    "juice": "A drink",
    "extraordinary": "Something amazing",
    "name": "Your identity",
    "mango": "King of fruits",
    "beautiful": "Pretty",
    "enjoy": "Have fun",
    "movie": "Cinema",
    "television": "Watching device"
}

# Start game
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

    global word, display, chances, guessed

    message = ""

    # Hangman stages
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

        # Stop guessing after game ends
        if chances > 0 and "_" in display:

            guess = request.form["guess"].lower()

            # Repeated guess
            if guess in guessed:
                message = "Already guessed!"

            else:

                guessed.append(guess)

                # Correct guess
                if guess in word:

                    message = "Correct!"

                    for i in range(len(word)):
                        if word[i] == guess:
                            display[i] = guess

                # Wrong guess
                else:
                    message = "Wrong!"
                    chances -= 1

    # Win condition
    if "_" not in display:
        message = "🎉 You Won!"

    # Lose condition
    elif chances <= 0:
        message = f"💀 Game Over! Word was '{word}'"

    # Hangman display
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


@app.route("/reset")
def reset():
    start_game()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)