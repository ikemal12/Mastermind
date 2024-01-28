import sys 
import os.path
from itertools import product
import random 

# retrieve the arguments passed after the script name from the command line
arguments = sys.argv[1:]

# check that at least the input and output files have been provided
if len(arguments) < 2:
    sys.exit(1)
else:
    input_file = arguments[0]
    output_file = arguments[1]
    computer_file = 'computerGame.txt'

# same filename error
if input_file == output_file:
    sys.exit(3)

# clear the contents of the output file and computerGame file if they exist, otherwise create a new file
if os.path.exists(output_file):
    try:
        with open(output_file, 'w') as f:
            f.write('')
    except Exception as e:
        sys.exit(3)

if os.path.exists(computer_file):
    try:
        with open(computer_file, 'w') as f:
            f.write('')
    except Exception as e:
        sys.exit() 

'''Initialise default values for optional parameters'''
code_length = 5
maximum_guesses = 12    
available_colours = ['red', 'blue', 'yellow', 'green', 'orange']    

# convert any integer command line arguments into integers for checking later
for i in range(len(arguments)):
    if arguments[i].isdigit():
        arguments[i] = int(arguments[i])

optional_args = arguments[2:] 
num_optional_args = len(optional_args)

# assign the optional parameters based on the arguments given, resorting to the default values when they are not provided
if num_optional_args >= 3:
    if type(optional_args[0]) is str:
        available_colours = optional_args[2:]
    elif type(optional_args[1]) is str:
        code_length = optional_args[0]
        available_colours = optional_args[2:]
    else:
        code_length = optional_args[0]
        maximum_guesses = optional_args[1]
        available_colours = optional_args[2:]
elif num_optional_args == 2:
    if type(optional_args[0]) is int and type(optional_args[1]) is str:
        code_length = optional_args[0]
    elif type(optional_args[0]) is str and type(optional_args[1]) is int:
        maximum_guesses = optional_args[1]
    elif type(optional_args[0]) is int and type(optional_args[1]) is int:
        code_length = optional_args[0]
        maximum_guesses = optional_args[1]
elif num_optional_args == 1:
    if type(optional_args[0]) is int:
        code_length = optional_args[0]

# negative or 0 integer arguments revert to default values
if code_length <= 0:
    code_length = 5
if maximum_guesses <= 0:
    maximum_guesses = 12

def write_to_file(file, line):
    '''Write a given line to either computerGame.txt or the output file'''
    try:
        with open(file, 'a') as f:
            line += '\n'
            f.write(line)
    except Exception as e:
        sys.exit(3)

# retrieve the required information for the game from the input file
try:
    with open(input_file, 'r') as f:
        code_line = f.readline()
        # if the code is an empty line, raise an error
        if not code_line.strip():
            write_to_file(output_file, "No or ill-formed code provided")
            sys.exit(4)

        code_line_words = code_line.split()
        code = code_line_words[1:]
        if code_line_words[0] != "code":
            write_to_file(output_file, "No or ill-formed code provided")
            sys.exit(4)

        player_line = f.readline()
        if not player_line.strip():
            write_to_file(output_file, "No or ill-formed player provided")
            sys.exit(5)

        player_line_words = player_line.split()
        game_mode = player_line_words[1] 
        if player_line_words[0] != "player":
            write_to_file(output_file, "No or ill-formed player provided")
            sys.exit(4)

        # getting a list of the guesses if the mode specified is human
        guesses = []
        if game_mode == "human":
            while True:
                guess = f.readline()
                if not guess or guess == '\n':
                    break
                guesses.append(guess)
        print(guesses)
except Exception as e:
    sys.exit(2)

'''Now that the initial arguments have been processed and the necessary information has been extracted 
   from the input file, we can define the functions that are going to be used in the human and 
   computer version of the game'''

def is_valid(code_or_guess):
    '''Checks if the given code/guess is a valid length and contains valid colours'''
    valid_pegs = True
    for peg in code_or_guess:
        if peg not in available_colours:
            valid_pegs = False
            break

    return ((len(code_or_guess) == code_length) and valid_pegs)

def compare_guess(guess, num_guesses):
    '''Constructs feedback for each peg in the guess and writes it to the output file'''
    feedback = ''
    undetermined_pegs = []
    code_pegs = []

    # if a peg is in the right position and right colour, mark it black
    for i in range(code_length):
        if guess[i] == code[i]:
            feedback += 'black '
        else:
            undetermined_pegs.append(guess[i])
            code_pegs.append(code[i])

    # if the remaining pegs appear in the code, mark them as white
    for peg in undetermined_pegs:
        if peg in code_pegs:
            feedback += 'white '
            code_pegs.remove(peg)       

    write_to_file(output_file, f"Guess {num_guesses}: {feedback}")      

def check_guess_limit(guesses, num_guesses):
    '''Checks if the guess limit has been reached and there are still more guesses remaining'''
    if num_guesses == maximum_guesses and len(guesses) > maximum_guesses:
        write_to_file(output_file, "You lost. Please try again.")
        write_to_file(output_file, f"You can only have {maximum_guesses} guesses.")
        sys.exit(0) # ends the game if the guess limit has been reached

def evaluate_guess(secret, guess):
    '''Calculates the number of black and white pegs for a guess'''
    correct_color_position = sum(a == b for a, b in zip(secret, guess))
    common_colors = sum(min(secret.count(c), guess.count(c)) for c in available_colours)
    correct_color_wrong_position = common_colors - correct_color_position
    return correct_color_position, correct_color_wrong_position 

def computer_guess(all_possibilities):
    '''Takes a guess from the remaining possibilities'''
    return random.choice(all_possibilities)

'''Now we have all the functions we need we can create both versions of the game'''

def human_game():
    '''Plays the simulated version of the game based on the guesses provided'''

    if not is_valid(code):
        write_to_file(output_file, "No or ill-formed code provided") 
        sys.exit(4)
    
    num_guesses = 1
    for guess in guesses:
        # if the guess is an empty line, raise an error
        if not guess.strip():
            write_to_file(output_file, f"Guess {num_guesses}: Ill-formed guess provided")

        # check if the guess is valid
        pegs = guess.split()
        if not is_valid(pegs):
            write_to_file(output_file, f"Guess {num_guesses}: Ill-formed guess provided")
            check_guess_limit(guesses, num_guesses)
            num_guesses += 1
            continue 

        compare_guess(pegs, num_guesses) # write the feedback to output

        # if the guess matches the code, write the corresponding message and end the game
        if pegs == code:
            if num_guesses == 1:
                write_to_file(output_file, "You won in 1 guess. Congratulations!")
            else:
                write_to_file(output_file, f"You won in {num_guesses} guesses. Congratulations!")

            if guess != guesses[-1]:
                write_to_file(output_file, "The game was completed. Further lines were ignored.")
            sys.exit(0)    

        check_guess_limit(guesses, num_guesses) 
        num_guesses += 1

    # if all the guesses have been compared and none were correct, end the game
    write_to_file(output_file, "You lost. Please try again.")


def computer_game():
    '''Tries to guess the code using an algorithm'''

    if not is_valid(code):
        write_to_file(output_file, "No or ill-formed code provided")
        sys.exit(4)
    
    with open(computer_file, 'a') as f:
        f.write(code_line)
    write_to_file(computer_file, "player human")

    # construct a list of all possible combinations of pegs
    num_guesses = 1
    all_possibilities = list(product(available_colours, repeat = code_length))
    all_possibilities = [list(pos) for pos in all_possibilities]

    while True:
        # take a guess and write it to the computerGame.txt file
        guess = computer_guess(all_possibilities)
        guess_line = ' '.join(guess)
        write_to_file(computer_file, guess_line)
        
        # construct the feedback for the guess and write it to the output file
        compare_guess(guess, num_guesses) 

        # end the game if the guess is right
        feedback = evaluate_guess(code, guess)
        if feedback[0] == code_length:
            if num_guesses == 1:
                write_to_file(output_file, "You won in 1 guess. Congratulations!")
            else:
                write_to_file(output_file, f"You won in {num_guesses} guesses. Congratulations!")
            sys.exit(0)
            
        # eliminate possibilities that cannot be the code based on the feedback of the guess
        all_possibilities = [pos for pos in all_possibilities if evaluate_guess(pos, guess) == feedback] 

        if num_guesses == maximum_guesses:
            write_to_file(output_file, "You lost. Please try again.")
            write_to_file(output_file, f"You can only have {maximum_guesses} guesses.")
            break 
        
        num_guesses += 1

'''Before we run any version of the game, let's check that the given code and player are valid'''

if not is_valid(code):
    write_to_file(output_file, "No or ill-formed code provided") 
    sys.exit(4)

if game_mode != "human" and game_mode != "computer":
    write_to_file(output_file, "No or ill-formed player provided")
    sys.exit(5)

# main program: playing the game according to the mode specified
if game_mode == "human":
    human_game()
elif game_mode == "computer":
    computer_game()
sys.exit(0)
