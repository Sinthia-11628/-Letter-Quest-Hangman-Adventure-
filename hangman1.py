import tkinter as tk
import random
import requests
from tkinter import messagebox

# Hangman drawings
HANGMAN_PICS = [
    """
       ------
       |    |
            |
            |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
            |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
       |    |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\   |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\   |
      /     |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\   |
      / \   |
            |
    =========
    """
]

#  random word from Cambridge Dictionary API
def get_random_word():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word")
        if response.status_code == 200:
            word = response.json()[0]

            dict_response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            if dict_response.status_code == 200:
                data = dict_response.json()
                meaning = data[0]['meanings'][0]['definitions'][0]['definition']
                example = data[0]['meanings'][0]['definitions'][0].get('example', 'No example available.')
                synonyms = data[0]['meanings'][0].get('synonyms', [])
                antonyms = data[0]['meanings'][0].get('antonyms', [])
                return word, meaning, example, synonyms, antonyms
    except Exception as e:
        print("Error fetching word:", e)
    except:
        return "apple", "A round fruit with red or green skin.", "She ate a juicy apple.", ["fruit"], []

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Funny Hangman: Save the Stickman!")
        self.root.geometry("800x500")
        self.root.config(bg="#f0f4f8")

        

        # Layout frames
        self.right_frame = tk.Frame(root, bg="#f0f4f8")
        self.right_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.left_frame = tk.Frame(root, bg="#f0f4f8")
        self.left_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Hangman drawing
        self.hangman_label = tk.Label(self.right_frame, text=HANGMAN_PICS[0], font=("Courier", 14), bg="#f0f4f8")
        self.hangman_label.pack()

        # Word Display
        self.word_label = tk.Label(self.left_frame, font=("Poppins", 22, "bold"), bg="#f0f4f8")
        self.word_label.pack(pady=10)

        # Chances left label
        self.chances_label = tk.Label(self.left_frame, font=("Poppins", 16), fg="red", bg="#f0f4f8")
        self.chances_label.pack(pady=5)

        # Guessing buttons
        self.guess_button_frame = tk.Frame(self.left_frame, bg="#f0f4f8")
        self.guess_button_frame.pack()

        self.buttons = {}
        row = 0
        col = 0
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            self.buttons[letter] = tk.Button(
                self.guess_button_frame, text=letter.upper(), width=4, height=2,
                command=lambda letter=letter: self.guess(letter),
                font=("Poppins", 12), bg="#4CAF50", fg="white"
            )
            self.buttons[letter].grid(row=row, column=col, padx=3, pady=3)
            col += 1
            if col > 7:
                col = 0
                row += 1

        # Reset Button
        self.reset_button = tk.Button(self.left_frame, text="Reset Game", width=15, height=2,
                                      font=("Poppins", 12), command=self.reset_game, bg="#FF9800", fg="white")
        self.reset_button.pack(pady=10)

        self.reset_game()

        self.update_ui()

    def display_word(self):
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

    def guess(self, letter):
        if letter in self.guessed_letters:
            return
        
        self.guessed_letters.append(letter)
        
        if letter not in self.word:
            self.chances -= 1
        
        self.update_ui()
        self.check_game_status()

    def update_ui(self):
        self.word_label.config(text=self.display_word())
        self.chances_label.config(text=f"Chances left: {self.chances}")
        self.hangman_label.config(text=HANGMAN_PICS[len(HANGMAN_PICS) - 1 - self.chances])

    def check_game_status(self):
        if self.chances == 0:
            messagebox.showerror("Game Over", f"You lost! The word was: {self.word.upper()}\nMeaning: {self.meaning}\nExample: {self.example}")
            self.disable_buttons()
        elif all(letter in self.guessed_letters for letter in self.word):
            messagebox.showinfo("You Won!", "Congrats! You saved the stickman!")
            self.disable_buttons()

    def disable_buttons(self):
        for button in self.buttons.values():
            button.config(state=tk.DISABLED)

    def reset_game(self):
        self.word, self.meaning, self.example, self.synonyms, self.antonyms = get_random_word()
        self.guessed_letters = []
        self.chances = len(HANGMAN_PICS) - 1
        self.update_ui()
        for button in self.buttons.values():
            button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()