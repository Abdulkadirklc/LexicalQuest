import random
from termcolor import colored
import webbrowser
import time

score = []          # collect user scores according to guesses


class Lexi_Q:
    Max_attempts = 0
    Word_length = 0
    Lexi_Q_words = []

    def __init__(self, secretword: str):
        # choose a random word using which_word_set => self.secret = random.choice(self.Lexi_Q_words).upper()
        self.result = None
        self.secret: str = secretword
        self.attempts = []  # list of words that we enter

    remain_letters = []

    def show_results(self, lex):
        """ Shows the table that contains entered words until that point with the help of 'colored_result' function"""
        print(colored("╔═" + "══" * lex.Word_length + "══╗", 'cyan'))
        # creates a loop contains all entered words until that time for every guess

        for lexical in lex.attempts:
            self.result = lex.guesscheck(lexical)
            colored_str = self.colored_result(self.result)  # resign color value every letter
            print(colored("║ ", "cyan") + colored_str + colored("  ║", "cyan"))
        for i in range(lex.remaining_attempts):
            print(colored("║ " + " _" * lex.Word_length + "  ║", 'yellow'))
        print(colored("╚═" + "══" * lex.Word_length + "══╝", 'cyan'))
        # I've made a list of letters that are not in the word
        print(colored(f"\nThey are not in the secret word: \n {sorted(list(set(self.remain_letters)))}\n", 'red'))
        pass

    def colored_result(self, result):
        """Converts entered word into colored_word by looking the letters
        one by one and resigning a proper color value to each"""
        colored_word = ""
        tempscore = 0
        for letter in result:
            if letter[1] == True and letter[2] == True:
                color = 'green'
                # calculate score multiplying the variable of remaining attempts
                tempscore += 5 * (self.remaining_attempts + 1)
            elif letter[1] == True and letter[2] == False:
                color = 'yellow'
                # calculate score multiplying the variable of remaining attempts
                tempscore += 1 * (self.remaining_attempts + 1)
            else:
                color = 'white'
                self.remain_letters.append(letter[0])
                # calculate score multiplying the variable of remaining attempts
                tempscore -= 1 * (self.remaining_attempts + 1)

            # I've had to calculate the score in that way because everytime I call this function it starts counting at
            # the first word and adds to total point
            colored_word = colored_word + " " + str(colored(letter[0], color))
        # adds the tempscore to score list
        score.append(tempscore)

        return colored_word

    def game_mode(self, mode):
        """changes the values of Max_attempts and Word_Lenght according to given input mode"""
        if mode == '5':
            self.Max_attempts = 6
            self.Word_length = 5

        if mode == '6':
            self.Max_attempts = 7
            self.Word_length = 6

        if mode == '7':
            self.Max_attempts = 8
            self.Word_length = 7
        self.Lexi_Q_words = self.which_word_set(f'ordered_{mode}_lettered.txt')
        return mode

    def which_word_set(self, letter_constraint="ordered_5_lettered.txt", ):
        """Takes the words of 'ordered_{n}_lettered.txt' folder as input and put it into a list """
        n_lettered_dataset = []
        with open(letter_constraint, 'r') as words:
            for word in words:
                word = word.strip().upper()
                n_lettered_dataset.append(word)
        self.Lexi_Q_words = n_lettered_dataset
        self.secret = random.choice(self.Lexi_Q_words).upper()              # select the secret word
        return self.secret

    def guesscheck(self, guessing: str):
        """Returns a list of letters and the bool value of whether that letter
        in the word and the position of it is correct that are in secretword """
        listofletters = []
        for i in range(len(self.secret)):
            letter = guessing[i]
            in_it = (True if letter in self.secret else False)
            position = (True if letter == self.secret[i] else False)
            listofletters.append((letter, in_it, position))
        return listofletters

    @property
    def is_solved(self):
        """return True if we still can  make a prediction and last 'self.secret' is the secret word"""
        return len(self.attempts) > 0 and self.attempts[-1] == self.secret

    @property
    def remaining_attempts(self) -> int:  # it will give us an int value
        return self.Max_attempts - len(self.attempts)

    @property
    def can_attempt(self):
        """By using two function which are placed on this it gave us a T/F value if we still make a new prediction"""
        return self.remaining_attempts > 0 and not self.is_solved

    def attempt(self, word: str):
        self.attempts.append(word.upper())

    ############################ Show Meaning ############################
    def meaning(self, sword):
        try:
            meaning = input(f"Are you curious about the meaning of {sword}? (Y,N) : ").upper()

            # create a link that will search in your default browser
            search_url = "https://www.merriam-webster.com/dictionary/" + sword

            if meaning.lower() == "y":

                print(colored("\nSearching for \"" + sword + "\" in your browser...", 'green',
                              attrs=['bold', 'underline']))
                time.sleep(1)
                # browse the meaning
                webbrowser.open(search_url)
            elif meaning.lower() == "n":
                print(colored("Okay, search cancelled :) ", 'green', attrs=['bold']))
        except Exception as e:
            print(colored("Oops! Something went wrong:", 'yellow', 'on_magenta', attrs=['bold']), e)
