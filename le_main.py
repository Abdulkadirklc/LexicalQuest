from Lexi_Q import Lexi_Q, score
from termcolor import colored
import os
import colorama
from colorama import Fore, Style
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from MySnakeGame import minigame


def LexicalQuest():
    game = Lexi_Q('word')
    game.game_mode(mode)
    sword = game.which_word_set(f'ordered_{mode}_lettered.txt')  # selects a random word
    final_score = 0

    
    # --------------------------------------- Graph of progression ---------------------------------------#
    def graph_of_progression():
        # Create the main tkinter window
        page = tk.Tk()
        page.title('My LexicalQuest progression!!!')
        page.geometry("600x700")
        # Create a figure and subplot for the plot
        fig = Figure(figsize=(150, 200), dpi=120)
        plot = fig.add_subplot(111)

        # Generate x values for the plot
        x = range(1, game.Max_attempts + 1)
        # Calculate the updated scores for each attempt
        updated_score = []
        index = 0
        for i in range(2, game.Max_attempts + 2):
            try:
                total = score[index]
                updated_score.append(total)
                index = index + i
            except IndexError:
                updated_score.append(0)

        # Set y values for the plot
        y = updated_score

        # Plot the data
        plot.plot(x, y)
        # Customize the y-axis
        step = 5  # change range of y-axis
        min_y = min(y) - (min(y) % step)  # min value of y-axis
        max_y = max(y) + (step - (max(y) % step))  # max value of y-axis
        plot.set_yticks(np.arange(min_y, max_y + 1, step))

        # Set labels and title for the plot
        plot.set_ylabel("Closeness score")
        plot.set_xlabel("Number of Tries")
        plot.set_title("Closeness to the answer", fontsize=14)

        # Creates a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=page)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Starts the tkinter event loop
        page.mainloop()

    # -------------------------------------------------------------------------------------------------- #

    # continues the game loop while we can attempt
    while game.can_attempt:
        try:
            # make guess
            colorama.init()
            guess = input(Fore.LIGHTMAGENTA_EX + "Type your guess: " + Style.RESET_ALL).upper()
            colorama.deinit()

            # Check the length of the word
            if len(guess) != game.Word_length:
                print(colored(f'Word must be {game.Word_length} characters long.', 'black', 'on_yellow'))
                continue

            # You cannot make the same guess
            elif guess in game.attempts:
                print(colored(f'You\'ve already used {guess}, please make another guess.', 'black', 'on_yellow'))
                continue

            # if your guess in provided list
            elif guess in game.Lexi_Q_words:

                # clears the terminal interface to provide a simple visualisation by looking operating system
                os.system('cls' if os.name == 'nt' else 'clear')

                game.attempt(guess)  # calls a function that appends entered word into a list
                game.show_results(game)

            else:
                print(colored(f"Your guess '{guess}' is not in the provided list.", 'red', attrs=['bold', 'underline']))
                continue

            if game.is_solved:
                final_score += int(score[-1])
                print("You've found the word!!")
                print(f'Your score is => {final_score}')
                print(colored(f"""Please wait a few seconds, your graph is preparing...\nDo not forget to click the 
                close button to continue the game !!!\n""", 'blue'))
                graph_of_progression()
                game.meaning(sword)
                # ıf user wants it starts a new game
                while True:
                    try:
                        done = input("Do you want to play again? (Y,N) : ").upper()
                        if done == 'Y':
                            # clears the terminal interface to provide a simple looking by looking operating system
                            os.system('cls' if os.name == 'nt' else 'clear')
                            score.clear()  # clears the score
                            game.remain_letters.clear()  # clears the unused letter list
                            LexicalQuest()
                        elif done == 'N':
                            print(colored(f"Okay, thanks for your time...\n", 'green', attrs=['bold']))
                            exit(-1)  # exit the game loop
                    except Exception as e:
                        raise ("Oops! Wrong input:", e)

            elif game.remaining_attempts >= 1:
                final_score += int(score[-1])
                print("Wrong guess :( Try again...")
                print(f'Your score is => {final_score}\n')

            #################################  GAME OVER  ###################################################

            else:
                final_score += int(score[-1])
                print(colored("Game over...You couldn't pass the Lexical Quest", 'red', 'on_white', attrs=['bold']))
                print(f'Your score is => {final_score}')
                print(colored(f"""Please wait a few seconds, your graph is preparing...\nDo not forget to click the 
                close button to continue the game !!!\n""", 'blue'))
                graph_of_progression()  # shows the graph
                print(colored(f"The secret word was {sword}", 'yellow', 'on_magenta', attrs=['bold']))
                game.meaning(sword)  # asks you whether you want to learn the meaning

                while True:
                    try:
                        done = input("\nDo you want a new chance? (Y,N) : ").upper()
                        if done == 'Y':
                            new_mode = int(mode)
                            print(colored(f"Mini snake-game is initializing...\n", 'green', attrs=['bold']))
                            time.sleep(0.5)
                            minigame.snake_game(new_mode)  # starts mini snake game
                            res = minigame.game_results
                            if True in res:
                                res.clear()
                                score.clear()  # clears the score
                                game.remain_letters.clear()  # clears the unused letter list
                                LexicalQuest()
                        else:
                            print(colored(f"Okay, thanks for your time...\n", 'green', attrs=['bold']))
                            exit(-1)  # exit the game loop
                    except Exception as e:
                        raise ("Oops! Wrong input:", e)

        ############################  Except CASES  ############################

        except KeyboardInterrupt:
            print(colored("Oops! Keyboard interrupt, see you...", 'yellow', 'on_magenta', attrs=['bold']))
            exit(-1)

        except Exception as e:
            print(colored("Oops! Something went wrong:", 'yellow', 'on_magenta', attrs=['bold']), e)
            exit(-1)


###################### Main part ######################

if __name__ == "__main__":
    print(colored("\nWelcome to LexiQ!!!", "magenta"))

    while True:
        try:
            colorama.init()
            # get the mode from user
            mode = input(Fore.CYAN + """Choose a game mode, type:
            '5' for five lettered mode
            '6' for six lettered mode
            '7' for seven lettered mode: """ + Style.RESET_ALL)

            colorama.deinit()
            if mode in ['5', '6', '7']:
                break
            else:
                print("Invalid input. Please enter '5', '6', or '7'.")
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt!!! Terminating the LexiQ...")
            exit(-1)
    LexicalQuest()  # start the game
    pass
