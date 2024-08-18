import random
# To install colorama, run the following command in your VS Code terminal:
# python3 -m pip install colorama
from colorama import Fore, Back, Style, init
import string
init(autoreset=True) #Ends color formatting after each print statement

from wordle_secret_words import get_secret_words
from valid_wordle_guesses import get_valid_wordle_guesses



global valid_words
valid_words = get_valid_wordle_guesses()
def get_feedback(guess: str, secret_word: str) -> str:
    '''Generates a feedback string based on comparing a 5-letter guess with the secret word. 
       The feedback string uses the following schema: 
        - Correct letter, correct spot: uppercase letter ('A'-'Z')
        - Correct letter, wrong spot: lowercase letter ('a'-'z')
        - Letter not in the word: '-'

        Args:
            guess (str): The guessed word
            secret_word (str): The secret word

        Returns:
            str: Feedback string, based on comparing guess with the secret word
    
        Examples
        >>> get_feedback("lever", "EATEN")
        "-e-E-"
            
        >>> get_feedback("LEVER", "LOWER")
                "L--ER"
            
        >>> get_feedback("MOMMY", "MADAM")
                "M-m--"
            
        >>> get_feedback("ARGUE", "MOTTO")
                "-----"

    
    '''
    ### BEGIN SOLUTION

    guess = guess.upper()
    if len(guess) < 5:
        return "-----"
    freq = [0]*26
    for c in secret_word:
        freq[ord(c)-ord('A')] += 1
    feedback = ""
    valid = set()
    for i in range(len(secret_word)):
        if guess[i] == secret_word[i]:
            if freq[ord(guess[i])-ord('A')] <= 0:
                feedback = feedback.replace(guess[i].lower(), "-")
            # valid.add(guess[i])
            # feedback += Back.GREEN + guess[i]
            feedback += guess[i].upper()
            freq[ord(guess[i])-ord('A')] -= 1
            # for word in valid_guesses.copy():
            #     if word[i] != guess[i] or guess[i] not in word:
            #         valid_guesses.remove(word)
        elif freq[ord(guess[i])-ord('A')] > 0:
            # valid.add(guess[i])
            # feedback += Back.YELLOW + guess[i]
            feedback += guess[i].lower()
            freq[ord(guess[i])-ord('A')] -= 1
            # for word in valid_guesses.copy():
            #     if word[i] == guess[i] or guess[i] not in word:
            #         valid_guesses.remove(word)
        else:
            # feedback += Back.BLACK + guess[i]
            feedback += "-"
            # for word in valid_guesses.copy():
            #     if guess[i] == word[i] or (guess[i] in word and guess[i] not in valid):
            #         valid_guesses.remove(word)


    return feedback

    ### END SOLUTION 

def letterFreq(possible_words):
    """Finds frequencies of letters in each position"""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet = alphabet.upper()
    arr = {}
    for c in alphabet:
        freq = [0, 0, 0, 0, 0]
        for i in range(0, 5):
            for w in possible_words:
                if w[i] == c:
                    freq[i] += 1
        arr.update({c: freq})
    return arr

def score_words(valid_guesses, freq):
    words = {}
    max_freq = [0, 0, 0, 0, 0]
    
    for c in freq:
        for i in range(0, 5):
            if max_freq[i] < freq[c][i]:
                max_freq[i] = freq[c][i]
    for w in valid_guesses:
        score = 1
        for i in range(0,5):
            c = w[i]
            
            score += 1 + (freq[c][i] - max_freq[i]) ** 2
        words.update({w: score})
    return words

def bestWord(valid_guesses, frequencies):
    """Finds the best word"""
    max_score = 1000000000000000000     # start with a ridiculous score
    best_word = "words"     # start with a random word
    scores = score_words(valid_guesses, frequencies)
    for w in valid_guesses:
        if scores[w] < max_score:
            max_score = scores[w]
            best_word = w
    return best_word


def get_AI_guess(guesses: list[str], feedback: list[str], secret_words: set[str], valid_guesses: set[str]) -> str:
    '''Analyzes feedback from previous guesses/feedback (if any) to make a new guess
        
        Args:
         guesses (list): A list of string guesses, which could be empty
         feedback (list): A list of feedback strings, which could be empty
         secret_words (set): A set of potential secret words
         valid_guesses (set): A set of valid AI guesses
        
        Returns:
         str: a valid guess that is exactly 5 uppercase letters
    '''
    ### BEGIN SOLUTION
    # for i in range(len(guesses)):
    #     if (len(guesses[i]) < 5):
    #         continue
    #     guess = guesses[i].upper()
    #     freq = [0]*26
    #     valid = set()
    #     feedback = ""
    #     valid_guesses = get_valid_wordle_guesses()
    #     for c in secret_words[i]:
    #         freq[ord(c)-ord('A')] += 1
    #     for j in range(len(secret_words[i])):
    #         if guess[i][j] == secret_words[i][j]:
    #             if freq[ord(guess[i][j])-ord('A')] <= 0:
    #                 feedback = feedback.replace(guess[i][j].lower(), "-")
    #             valid.add(guess[i][j])
    #             # feedback += Back.GREEN + guess[i]
    #             feedback += guess[i][j].upper()
    #             freq[ord(guess[i][j])-ord('A')] -= 1
    #             for word in valid_guesses.copy():
    #                 if word[i][j] != guess[i][j] or guess[i][j] not in word:
    #                     valid_guesses.remove(word)
    #         elif freq[ord(guess[i][j])-ord('A')] > 0:
    #             valid.add(guess[i][j])
    #             # feedback += Back.YELLOW + guess[i]
    #             feedback += guess[i][j].lower()
    #             freq[ord(guess[i][j])-ord('A')] -= 1
    #             for word in valid_guesses.copy():
    #                 if word[i][j] == guess[i][j] or guess[i][j] not in word:
    #                     valid_guesses.remove(word)
    #         else:
    #             # feedback += Back.BLACK + guess[i]
    #             feedback += "-"
    #             for word in valid_guesses.copy():
    #                 if guess[i][j] == word[i][j] or (guess[i][j] in word and guess[i][j] not in valid):
    #                     valid_guesses.remove(word)
    
    if len(guesses) < 1:
        return bestWord(valid_guesses, letterFreq(valid_guesses))
    feedback = feedback[-1]
    guess = guesses[-1]
    new_set = set()
    for i, letter in enumerate(feedback):
        if letter.isupper():
            valid_guesses = set([word for word in valid_guesses if word[i] == guess[i].upper()])
            # for word in valid_guesses.copy():
            #     if word[i] != guess[i].upper() or guess[i].upper() not in word:
            #         new_set.add(word)
            #         # print(len(valid_guesses))
        elif letter.islower():
            # for word in valid_guesses.copy():
            #     if word[i] == guess[i].upper() or guess[i].upper() not in word:
            #         new_set.add(word)
            #         #print(len(valid_guesses))
            valid_guesses = set([word for word in valid_guesses if word[i] != guess[i].upper() and guess[i].upper() in word])
        else:
            valid_guesses = set([word for word in valid_guesses if word[i] != guess[i].upper() and (guess[i].upper() not in word or guess[i].upper() in feedback)])
            # for word in valid_guesses.copy():
            #     if guess[i].upper() == word[i] or (guess[i].upper() in word and guess[i].upper() not in feedback):
            #         new_set.add(word)
    # for i in range(len(feedback)):
    #     if len(guesses[i]) < 5:
    #         continue
    #     for j in range(len(feedback[i])):
    #         if feedback[i][j].isupper():
    #             for word in valid_guesses.copy():
    #                 if word[j] != guesses[i][j].upper() or guesses[i][j].upper() not in word:
    #                     valid_guesses.remove(word)
    #                     # print(len(valid_guesses))
    #         elif feedback[i][j].islower():
    #             for word in valid_guesses.copy():
    #                 if word[j] == guesses[i][j].upper() or guesses[i][j].upper() not in word:
    #                     valid_guesses.remove(word)
    #                     #print(len(valid_guesses))
    #         else:
    #             for word in valid_guesses.copy():
    #                 if guesses[i][j].upper() == word[j] or (guesses[i][j].upper() in word and guesses[i][j].upper() not in feedback[i]):
    #                     valid_guesses.remove(word)
    # valid_guesses = valid_guesses.difference(new_set)
    return bestWord(valid_guesses, letterFreq(valid_guesses))

    ### END SOLUTION 

def is_valid(guess, target):
    if len(guess) != len(target):
        return False
    return True

if __name__ == "__main__":
    # TODO: Write your own code to call your functions here
    final_feedback = ""
    guesses = []
    feedbacks = []
    for i in range(1, 8):
        final_feedback += Back.WHITE + " "
        if not i % 7:
            final_feedback += Back.RESET + "\n"

    # valid_guesses = get_valid_wordle_guesses()
    target = random.choice(list(get_secret_words()))
    target = "HUMUS"
    n = 0
    found = False
    printable = set(string.printable)
    print(target)
    while n < 6 and not found:
        guess = input("Enter word to guess: ")
        feedback = get_feedback(guess, target)
        feedbacks.append(feedback)
        guesses.append(guess)
        if guess.lower() == "h":
            print("The best word to move forward with is: " + get_AI_guess(guesses, feedbacks, [str(target)], valid_words))
            continue

        if not is_valid(guess, target):
            print("Invalid guess, try again")
            continue

        
        

        n+=1
        # final_feedback += Back.WHITE + " " + Back.WHITE + feedback + Back.WHITE + " " + Back.RESET + "\n"
        # final_feedback += Back.WHITE + " "*7 + Back.RESET + '\n'
        

        # if ''.join(''.join(filter(lambda x: x in printable, feedback)).split('[42m')[1:]) == target:
        #     found = True
        if feedback == target:
            found = True
        
        # print(final_feedback)
        print(feedback)



    if found:
        print("Congrats, you won!")
    else:
        print(f"Awww, you didn't win, but better luck next time! The word was: {target}")
        

