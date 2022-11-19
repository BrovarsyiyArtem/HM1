# Problem Set 2, hangman.py
# Name: Artem Brovarskyi
# Collaborators:-
# Time spent: 3 days

# Hangman Game
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    set_secret_word = set(secret_word)
    if set_secret_word.difference(letters_guessed) == set():
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    resault = ['_']*len(secret_word)
    for k in letters_guessed:
        for i in range(len(secret_word)):
            if secret_word[i] == k:
                resault.pop(i)
                resault.insert(i, k)

    return resault


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = string.ascii_lowercase
    for i in letters_guessed:
        available_letters = available_letters.replace(i, '')
    return available_letters


def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with .

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    """
    warning = 3
    guesses = 6
    print("Welcome to the game Hangman! \nI am thinking of a word that is", len(
        secret_word), "letters long. \nYou have ", warning, 'warnings left \n', '-' * 20,)
    letters_guessed = set()
    while guesses > 0:
        repit = False
        word_try = get_guessed_word(secret_word, letters_guessed)
        print('You have', guesses, 'guesses left. \nAvailable letters: ',
              get_available_letters(letters_guessed))
        letter_input = input('Please guess a letter:').lower()
        if letter_input.isalpha():
            if letter_input in ['a', 'e', 'i', 'o', 'u']:
                fine = 2
            else:
                fine = 1
            if letter_input in letters_guessed:
                repit = True
            letters_guessed.add(letter_input)
        else:
            if warning > 0:
                guesses += 1
                warning -= 1
                print('Oops! That is not a valid letter. You have',
                      warning, 'warnings left:')
            else:
                print(
                    'Oops!That is not a valid letter. You have mised 1 guesse. Now you have', guesses, 'guesses')
        if is_word_guessed(secret_word, letters_guessed):
            goal_set = set(secret_word)
            goal = 0
            for j in goal_set:
                goal += 1
            print(
                "Congratulations, you won!!! Your total score for this game is:", goal*guesses)
            break
        else:
            if word_try != get_guessed_word(secret_word,
                                            letters_guessed) and repit != 'True':
                print('Good guess', *get_guessed_word(secret_word,
                      letters_guessed), '\n', '-' * 20)
            elif repit:
                print("Oops! You've already guessed that letter ", '\n', '-' * 20)
                warning -= 1
                if warning > 0:
                    print('You have', warning, 'warnings left')
                elif warning < 0:
                    guesses -= fine
            else:
                print('Oops, That letter is not in my word:', *
                      get_guessed_word(secret_word, letters_guessed), '\n', '-' * 20)
                guesses -= fine
    else:
        print('Sorry, you lose. The word was', secret_word)


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_index = 0
    other_word_index = 0
    my_word = my_word.replace(' ', '')
    check_set = set(my_word.replace('_', ''))
    if len(my_word) == len(other_word):
        while my_word_index < len(my_word):
            if my_word[my_word_index] != '_':
                if my_word[my_word_index] == other_word[other_word_index]:
                    check_set.add(my_word[my_word_index])
                else:
                    return False
            else:
                if other_word[other_word_index] in check_set:
                    return False
            my_word_index += 1
            other_word_index += 1
        return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    my_word_resault = ''
    for i in my_word:
        my_word_resault += i
    match_count = 0
    for i in wordlist:
        if match_with_gaps(my_word_resault, i):
            match_count += 1
            print(i, end=" ")
    if match_count == 0:
        print('No matches found')


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 

    Follows the other limitations detailed in the problem write-up.
    '''
    warning = 3
    guesses = 6
    print("Welcome to the game Hangman! \nI am thinking of a word that is", len(
        secret_word), "letters long. \nYou have ", warning, 'warnings left \n', '-' * 20,)
    letters_guessed = set()
    while guesses > 0:
        repit = False
        word = get_guessed_word(secret_word, letters_guessed)
        print('You have', guesses, 'guesses left. \nAvailable letters: ',
              get_available_letters(letters_guessed))
        letter_input = input('Please guess a letter: ')
        if letter_input == "*":
            print('Possible word matches are: ', end='')
            show_possible_matches(word)
            print('\n', '-' * 20)
        elif letter_input.isalpha():
            letter_input = letter_input.lower()
            if letter_input in ['a', 'e', 'i', 'o', 'u']:
                fine = 2
            else:
                fine = 1
            if letter_input in letters_guessed:
                repit = True
            letters_guessed.add(letter_input)
        else:
            if warning > 0:
                guesses += 1
                warning -= 1
                print('Oops! That is not a valid letter. You have',
                      warning, 'warnings left:')
            else:
                print(
                    'Oops!That is not a valid letter. You have mised 1 guesse. Now you have', guesses, 'guesses')
        if is_word_guessed(secret_word, letters_guessed):
            goal_set = set(secret_word)
            goal = 0
            for j in goal_set:
                goal += 1
            print(
                "Congratulations, you won!!! Your total score for this game is:", goal*guesses)
            break
        elif letter_input != '*':
            if word != get_guessed_word(secret_word, letters_guessed) and repit != 'True':
                print('Good guess', *get_guessed_word(secret_word,
                      letters_guessed), '\n', '-' * 20)
            elif repit:
                print("Oops! You've already guessed that letter ", '\n', '-' * 20)
                warning -= 1
                if warning > 0:
                    print('You have', warning, 'warnings left')
                elif warning < 0:
                    guesses -= fine
            else:
                print('Oops, That letter is not in my word:', *
                      get_guessed_word(secret_word, letters_guessed), '\n', '-' * 20)
                guesses -= fine
    else:
        print('Sorry, you lose. The word was', secret_word)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.
if __name__ == "__main__":
    #secret_word = choose_word(wordlist)
    # hangman(secret_word)
    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
