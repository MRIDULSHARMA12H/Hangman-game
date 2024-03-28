import tkinter as tk
from tkinter import messagebox
import random

# Define color configurations for dark theme
dark_theme = {
    "bg": "black",
    "fg": "white",
    "button_bg": "black",
    "button_fg": "gold"
}

# Define color configurations for light theme
light_theme = {
    "bg": "white",
    "fg": "black",
    "button_bg": "white",
    "button_fg": "blue"
}

current_theme = dark_theme  # Default theme

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
    'dhoni': "This player is referred to as 'captain Cool'.",
    'virat': "This player is often called the 'King of Cricket'.",
    'sachin': "This player is considered the 'Legend of Cricket'.",
    'warner': "Ultimate sledger in test series.",
    'gayle': "Universal boss.",
    'dravid': "Current Indian cricket coach.",
    'williamson': "All-time leading run-scorer for New Zealand."
}

class HangmanGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Game")
        self.geometry("1210x450")  # Modified window size
        self.configure(bg=current_theme["bg"])
        self.score = 0  # Initialize score

        self.teamLabel = tk.Label(self, text="MASTER BLASTER", font=('times new roman', 30), bg=current_theme["bg"], fg=current_theme["fg"])
        self.teamLabel.pack(pady=20)

        self.questionFrame = tk.Frame(self, bg=current_theme["bg"])
        self.questionFrame.pack()

        self.hintLabel = tk.Label(self.questionFrame, text='', font=('Arial', 16), bg=current_theme["bg"], fg=current_theme["fg"])
        self.hintLabel.pack(side=tk.LEFT)

        # Add change question button
        self.change_question_button = tk.Button(self.questionFrame, text="Change Question", font=('Arial', 12), bg=current_theme["button_bg"], fg=current_theme["button_fg"], command=self.change_question)
        self.change_question_button.pack(side=tk.RIGHT)

        self.hangmanLabel = tk.Label(self, text=HANGMAN_PICS[0], font=('Courier', 12), bg=current_theme["bg"], fg=current_theme["fg"])
        self.hangmanLabel.pack(pady=20)

        self.wordLabel = tk.Label(self, text='', font=('Arial', 24), bg=current_theme["bg"], fg=current_theme["fg"])
        self.wordLabel.pack()

        self.missedLabel = tk.Label(self, text='', font=('Arial', 16), bg=current_theme["bg"], fg=current_theme["fg"])
        self.missedLabel.pack()

        self.guessEntry = tk.Entry(self, font=('Arial', 14))
        self.guessEntry.pack(pady=10)

        self.letterFrame = tk.Frame(self, bg=current_theme["bg"])
        self.letterFrame.pack()

        self.letterButtons = []
        for char in 'abcdefghijklmnopqrstuvwxyz':
            button = tk.Button(self.letterFrame, text=char, font=('Arial', 12), bg=current_theme["button_bg"], fg=current_theme["button_fg"], command=lambda c=char: self.guessLetter(c))
            button.pack(side=tk.LEFT, padx=3)
            self.letterButtons.append(button)

        self.scoreLabel = tk.Label(self, text="Score: 0", font=('Arial', 16), bg=current_theme["bg"], fg=current_theme["fg"])
        self.scoreLabel.pack()  # Pack the score label
        
        # Add theme change buttons
        self.theme_button = tk.Button(self, text="Dark Theme", font=('Arial', 12), bg=current_theme["button_bg"], fg=current_theme["button_fg"], command=self.toggle_theme)
        self.theme_button.pack(pady=10)

        self.newGame()

    def toggle_theme(self):
        global current_theme
        if current_theme == dark_theme:
            current_theme = light_theme
            self.theme_button.config(text="Dark Theme", bg=current_theme["button_bg"], fg=current_theme["button_fg"])
        else:
            current_theme = dark_theme
            self.theme_button.config(text="Light Theme", bg=current_theme["button_bg"], fg=current_theme["button_fg"])
        self.configure(bg=current_theme["bg"])
        self.teamLabel.config(bg=current_theme["bg"], fg=current_theme["fg"])
        self.hintLabel.config(bg=current_theme["bg"], fg=current_theme["fg"])
        self.hangmanLabel.config(bg=current_theme["bg"], fg=current_theme["fg"])
        self.wordLabel.config(bg=current_theme["bg"], fg=current_theme["fg"])
        self.missedLabel.config(bg=current_theme["bg"], fg=current_theme["fg"])
        self.guessEntry.config(bg=current_theme["bg"], fg=current_theme["fg"])
        self.letterFrame.config(bg=current_theme["bg"])
        self.scoreLabel.config(bg=current_theme["bg"], fg=current_theme["fg"])
        for button in self.letterButtons:
            button.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])

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
            self.score += 10  # Increment score by 10 for each correct guess
            self.scoreLabel.config(text=f"Score: {self.score}")  # Update score label
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

    def change_question(self):
        self.newGame()

if __name__ == "__main__":
    app = HangmanGame()
    app.mainloop()
