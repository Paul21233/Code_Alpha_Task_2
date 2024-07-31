# Hangman game
from listOfWords import guess_words
import random

wrong_guess = {
    0: ("   ",
        "   ",
        "   "),
    1: (" o ",
        "   ",
        "   ",),
    2: (" o ",
        " | ",
        "   "),
    3: (" o ",
        "/| ",
        "   "),
    4: (" o ",
        "/|\\",
        "   "),
    5: (" o ",
        "/|\\",
        "/  "),
    6: (" o ",
        "/|\\",
        "/ \\")
}


# function to display hangman
def display_hangman(wrongGuess):
    print("----------------")
    for i in wrong_guess[wrongGuess]:
        print(i)
    print("----------------")


# function to display the hints
def display_hint(hint):
    print(" ".join(hint))


# function to display answer
def show_answer(ans):
    print(" ".join(ans))


# main logic function
def main():
    answer = random.choice(guess_words)
    incorrect = 0
    hint = ["_"] * len(answer)
    guessed_word = set()
    is_running = True

    while is_running:
        display_hangman(incorrect)
        display_hint(hint)
        guess = input("Enter a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input")
            continue

        if guess in guessed_word:
            print(f"{guess} already guessed")
            continue

        guessed_word.add(guess)

        if guess in answer:
            for i in range(len(answer)):
                if answer[i] == guess:
                    hint[i] = guess
        else:
            incorrect += 1

        if "_" not in hint:
            display_hangman(incorrect)
            show_answer(answer)
            print("HURRAH!!! YOU WIN!")
            is_running = False
        elif incorrect >= len(wrong_guess) - 1:
            display_hangman(incorrect)
            show_answer(answer)
            print("(╥_╥) YOU LOSE!")
            is_running = False


if __name__ == "__main__":
    main()
