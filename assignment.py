import tkinter as tk
from tkinter import messagebox
import random

HANGMAN_PICS = ['''
    +---+
         |
         |
         |
        ===''', '''
    +---+
    O   |
        |
        |
       ===''', '''
    +---+
    O   |
    |   |
        |
       ===''', '''
    +---+
    O   |
   /|   |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
   /    |
       ===''', '''
    +---+
    O   |
   /|\  |
   / \  |
       ===''']

cricketers = {
    'rohit': "In India, this player is known as 'Hitman'.",
    'dhoni': "This player is referred to as 'Mr. Cool'.",
    'virat': "This player is often called the 'King of Cricket'.",
    'sachin': "This player is considered the 'Legend of Cricket'.",
    'warner': "Ultimate sledger in test series.",
    'gayle': "Universal boss.",
    'dravid': "Current Indian cricket coach.",
    'williamson': "All-time leading run-scorer for New Zealand."
}

class HangmanGame(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Hangman Game")
        self.geometry("1260x450")  # Modified window size
        self.configure(bg="black")

        self.mridulLabel = tk.Label(self, text="mridul", font=('Allegro', 24), bg="black", fg="white")
        self.mridulLabel.pack(pady=20)

        self.hintLabel = tk.Label(self, text='', font=('Arial', 16), bg="black", fg="white")
        self.hintLabel.pack()

        self.hangmanLabel = tk.Label(self, text=HANGMAN_PICS[0], font=('Courier', 12), bg="black", fg="white")
        self.hangmanLabel.pack(pady=20)

        self.wordLabel = tk.Label(self, text='', font=('Arial', 24), bg="black", fg="white")
        self.wordLabel.pack()

        self.missedLabel = tk.Label(self, text='', font=('Arial', 16), bg="black", fg="white")
        self.missedLabel.pack()

        self.guessEntry = tk.Entry(self, font=('Arial', 14))
        self.guessEntry.pack(pady=10)

        self.letterFrame = tk.Frame(self, bg="black")
        self.letterFrame.pack()

        self.letterButtons = []
        for char in 'abcdefghijklmnopqrstuvwxyz':
            button = tk.Button(self.letterFrame, text=char, font=('Arial', 12), bg="black", fg="black", command=lambda c=char: self.guessLetter(c))  # Modified font color to black
            button.pack(side=tk.LEFT, padx=3)
            self.letterButtons.append(button)

        self.newGame()

    def newGame(self):
        self.current_cricketer = random.choice(list(cricketers.keys()))
        self.secretWord = self.current_cricketer
        self.hintLabel.config(text=cricketers[self.current_cricketer])
        self.wordLabel.config(text=' '.join(['_' for _ in self.secretWord]))
        self.missedLetters = ''
        self.correctLetters = ''
        self.gameIsDone = False
        self.currentHangmanPicIndex = 0
        self.hangmanLabel.config(text=HANGMAN_PICS[self.currentHangmanPicIndex])
        for button in self.letterButtons:
            button.config(state=tk.NORMAL)

    def displayBoard(self):
        if self.gameIsDone:
            return
        self.missedLabel.config(text="Missed Letters: " + self.missedLetters)
        word_with_blanks = ''
        for letter in self.secretWord:
            if letter in self.correctLetters:
                word_with_blanks += letter + ' '
            else:
                word_with_blanks += '_ '
        self.wordLabel.config(text=word_with_blanks)

    def guessLetter(self, guess):
        if guess in self.missedLetters or guess in self.correctLetters:
            messagebox.showwarning("Already Guessed", "You have already guessed that letter. Choose again.")
            return
        if guess in self.secretWord:
            self.correctLetters += guess
            if all(letter in self.correctLetters for letter in self.secretWord):
                messagebox.showinfo("Congratulations!", f"You guessed it! The secret word is '{self.secretWord}'. You win!")
                self.newGame()
        else:
            self.missedLetters += guess
            self.currentHangmanPicIndex += 1
            if self.currentHangmanPicIndex == len(HANGMAN_PICS) - 1:
                messagebox.showinfo("Game Over", f"You have run out of guesses!\nThe word was '{self.secretWord}'.")
                self.newGame()
        self.displayBoard()
        self.hangmanLabel.config(text=HANGMAN_PICS[self.currentHangmanPicIndex])
        self.updateLetterButtons()

    def updateLetterButtons(self):
        for button in self.letterButtons:
            if button["text"] in self.correctLetters or button["text"] in self.missedLetters:
                button.config(state=tk.DISABLED)

if '_name_' == "_main_":
    app = HangmanGame()
    app.mainloop()