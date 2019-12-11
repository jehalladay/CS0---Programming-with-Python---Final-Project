"""
Assignment - Final project: Hangman
James Halladay
CS0-Beginners programming with python
Date: 11/1/19


********************************************************************************************************
Steps:
Step 1. Import Tkinter tools, random, OS, and Sys
Step 2. Set up Clear Screen Function
    Step 3.1: Create init function
    Step 3.2: Create function to calculate number of tries remaining
    Step 3.3: Create current word function to spawn a word for the game
    Step 3.4: Create hidden word function to display current progress of word starting with a series of _ and spaces
    Step 3.5: Create word checker function that takes in the current word and a guess and returns a new partial word and miss count
    Step 3.6: Create function to return the current stages of ASCII art for the console scoreboard
    Step 3.7: Create str function to print current game values in console
Step 3. Create Game object using classes
Step 4. Create Tkinter window for GUI interface
    Step 4.1: Create init function, bringing data from Game object
    Step 4.2: Create keyboard function
    Step 4.3: Create keyboard return function which gets called every time a button is activated
    Step 4.4: Create image function to render hangman picture and update it
    Step 4.5: Create a packing function to place all objects on the grid and update grid
Step 5. Create a console scoreboard so that the game can be played with or without GUI
Step 6. Create main function
Step 7. Create GUI test function
Step 8. Create Functional test function
Step 9. Create Unit test function
Step 10. Create Test handler for tests
Step 11. Create function to run main or tests depending on the initial parameters
Step 12. Check to make sure program isnt being called before running function created in Step 11
********************************************************************************************************
sources for the hangman pictures:
https://en.wikipedia.org/wiki/File:Hangman-0.png
https://en.wikipedia.org/wiki/File:Hangman-1.png
https://en.wikipedia.org/wiki/File:Hangman-2.png
https://en.wikipedia.org/wiki/File:Hangman-3.png
https://en.wikipedia.org/wiki/File:Hangman-4.png
https://en.wikipedia.org/wiki/File:Hangman-5.png
https://en.wikipedia.org/wiki/File:Hangman-6.png"""


# Step 1. Import Tkinter tools, Python Imaging Library tools, and the built-ins OS and Sys
#           Only imports the functions needed to execute the program

from sys import argv
from os import name, system
from tkinter import Tk, Frame, Label, Button, PhotoImage, IntVar
from random import randint

# Step 2. Set up Clear Screen Function

def clearScreen():
    """Clears Screen takes no argument, returns no values"""
    if name == 'nt':
        system('cls')
    else:
        system('clear')


#A continue function for the main function

def continue_function() -> bool:
    """function controls loops for the console
    always returns true for yes and false for no"""
    y = input('Would you like to continue" [y|n] ' )
    if y == 'y' or y == 'Y' or y == 'Yes' or y == "yes" or y == "YES":
        return True
    else:
        return False


# Step 3. Create Game object using classes

class game(object):
    """Class defines an object that contains all progress made from the game"""


    # Step 3.1: Create init function

    def __init__(self, x=0, y=0, w='_ _ _ _ _ _ _ '):
        '''keys define starting values for the game, used in tests
        assumes word has seven digits, will resize based on word generated'''
        self.word = self.current_word()
        self.partial_word = self.hidden_word(self.word)
        self.score = x
        self.miss = y
        self.totalloss = 0
        self.totalwin = 0
        self.tries = self.Misses()
        self.player_name = 'Player Name'

    # Step 3.2: Create function to calculate number of tries remaining

    def Misses(self) -> int:
        """Returns number of tries remaining in current game"""
        if self.miss < 6:
            x = 6 - self.miss
        else:
            x = 0
        return x


    # Step 3.3: Create current word function to spawn a word for the game

    def current_word(self, file='words.txt') -> str:
        '''Opens words.txt and picks a random word to use for the game
        can take a string as a parameter in order to designate a different file
        returns a one word string'''
        assert type(file) == str
        file = open(file, 'r')
        lines = file.read()
        file.close()
        lines = lines.upper().split()
        if len(lines) > 1:
            file, word = randint(1, len(lines)-1), ""
            word = word.join(lines[file])
        else:
            word = ""
            word = word.join(lines)
        assert type(word) == str
        return word


    # Step 3.4: Create hidden word function to display current progress of word starting with a series of _ and spaces

    def hidden_word(self, word: str) -> str:
        """Function takes a string as an input
        Creates a string of underscores and dashes that is double the length of the word given
        Returns new string"""
        assert type(word) == str
        w = "_ "*len(word)
        assert type(w) == str
        return w


    # Step 3.5: Create word checker function that takes in the current word and a guess and returns a new partial word and miss count

    def word_checker(self, word: str, partial_word: str, guess: str, misses: int) -> (str, int):
        """Function checks if guess is in word
        If it is it inserts all occurences of it into the partial word being shown
        Function takes a word, the current partial word, and a guess"""
        assert(type(word)) == str
        assert(type(partial_word)) == str
        assert(type(guess)) == str
        assert(len(guess)) == 1
        assert(type(misses)) == int
        new_partial_word = partial_word
        if misses < 6:
            if guess in word:
                for a in range(0, len(word)):
                    if word[a] == guess:
                        new_partial_word = new_partial_word[:a*2] + guess + new_partial_word[(a*2)+1:]
            else:
                misses += 1

        assert(type(new_partial_word)) == str
        return (new_partial_word, misses)


    def guess_filter(self, x: str) -> bool:
        if len(x) == 1:
            try:
                x = str(x)
                x = x.upper()
                self.word_checker(self.word, self.partial_word, x, self.miss)
                return True
            except:
                return False
        else:
            return False

    # Step 3.6: Create function to return the current stages of ASCII art for the console scoreboard

    def hangman(self, x: int) -> str:
        """Function returns the current stage of the hangman game based on the section desired
        x=1: Head
        x=2: Torso
        x=3: Legs"""
        if x == 1:
            if self.miss >= 1:
                return 'O'
            else:
                return ' '
        elif x == 2:
            if self.miss == 2:
                return ' | '
            elif self.miss == 3:
                return '/| '
            elif self.miss >= 4:
                return '/|\\'
            else:
                return '   '
        elif x == 3:
            if self.miss == 5:
                return '/  '
            elif self.miss >= 6:
                return '/ \\'
            else:
                return '   '
        else:
            return ' '


    # Step 3.7: Create new game function to restart the game

    def new_game(self, x=0, y=0,):
        """Function resets the game and spawns new word"""
        self.win_calc()
        self.word = self.current_word()
        self.partial_word = self.hidden_word(self.word)
        self.score = x
        self.miss = y
        self.tries = self.Misses()


    # Step 3.8: Create Win calculator function to run when the player initiates a new game

    def win_calc(self):
        """Function checks the current partial word with the solution
        if the strings match increment totalwin
        if the strings do not match increment totalloss"""
        answer = ""
        for c in self.word.upper():
            answer += c
            answer +=" "
        print("answer = ", answer)
        print("current = ", self.partial_word)
        if answer == self.partial_word:
            self.totalwin += 1
        else:
            self.totalloss += 1

    # Step 3.9: Create str function to print scoreboard in console

    def __str__(self):
        '''Creates a scoreboard that prints to the console for testing and to satisfy the ASCII hangman display requirement'''
        y = """
    __________________________________________________________________
    | Word: \t\t %s  |/\t\t|\t     |
    | Misses: \t\t %s \t \t |  \t\t%s\t     |
    | Guesses left: \t %s \t \t |             %s\t     |
    | Wins: \t\t %s \t \t |             %s\t     |
    | Losses: \t\t %s \t \t |  \t\t\t     |
    | \t \t \t \t\t |  \t\t\t     |
    | \t \t \t\t \t |     \t\t \t     |
    | \t \t \t \t\t |     \t\t \t     |
    ******************************************************************
    """ % (self.partial_word, self.miss, self.hangman(1), (6-self.miss), self.hangman(2), self.totalwin, self.hangman(3), self.totalloss)
        return y







# Step 4. Create Tkinter window for GUI interface

class window(Tk):
    """Creates a window to display current progress in the game and return values given to the game object in order to progress
    the game.
    Creates a keyboard with extra buttons to show game stats, close the window, and start a new game
    Finds the current stage of the game and displays the appropriate PNG file in the window"""

    # Step 4.1: Create init function, bringing data from Game object

    def __init__(self, game_obj: 'expects game class object'):
        assert(type(game_obj)) == game
        Tk.__init__(self)
        self.title('Hangman')
        
        self.geometry("1000x600+250+100")
        self.head = Label(text='Hello World!')
        self.game = game_obj
        self.word_label = Label(self, text="  " + self.game.partial_word + '  ', font=('Concolas 24 bold'))

        self.try_label = Label(self, text="Guesses left:")
        self.wins_label = Label(self, text="Wins:")
        self.losses_label = Label(self, text="Losses:")

        self.labeltext = IntVar()
        self.labeltext.set(self.game.Misses())
        self.missNum = Label(self, textvariable=self.labeltext)

        self.wintext = IntVar()
        self.wintext.set(self.game.totalwin)
        self.winNum = Label(self, textvariable=self.wintext)

        self.losstext = IntVar()
        self.losstext.set(self.game.totalloss)
        self.lossNum = Label(self, textvariable=self.losstext)

        self.keyboard_function()
        self.hangman_stage(0)
        self.package_update(0)


    # Step 4.2: Create Hint keyboard function

    def hint_function(self):
        """Function for the a button that returns the next letter while counting the hint as a missed guess"""
        self.game.miss += 1
        self.labeltext.set(self.game.miss)
        for c in self.game.word.upper():
            if c in self.game.partial_word:
                pass
            else:
                x = c
                self.keyboard_return(x)
                break
        
        self.package_update(1)
        print(self.game.miss)


    # Step 4.3: Create new game keyboard function

    def new_game_button(self):
        """Function for the new game button to reset the game values and spawn a new word"""
        self.game.new_game()
        self.package_update(0) #Run both to set up initial conditions and reset all the previously triggered conditions
        self.package_update(1)


    # Step 4.4: Create keyboard function

    def keyboard_function(self):
        """Function spawns all of the buttons for the GUI keyboard"""
        self.close_button = Button(self, text="Close", command=self.quit, activebackground='red', activeforeground='light blue', font=("Helvetica 18"), width=4)
        self.close_button.grid(row=4, column=12)
        self.new_button = Button(self, text="New Game", command=lambda n=0: self.new_game_button(), activebackground='red', activeforeground='light blue', font=("Helvetica 18"))
        self.new_button.grid(row=4, column=3, columnspan=2)
        self.miss_button = Button(self, text="Hint", command=self.hint_function, font=("Helvetica 18"), width=4)        
        self.miss_button.grid(column=3, row=3)                
        keyboard = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
        n=0
        for i in keyboard:
            Button(self, text=i, command=lambda d=i: self.keyboard_return(d), font=("Helvetica 18"), width=4).grid(row=2+n//10, column=3+n%10)
            n += 1
            if n == 10:
                n +=1
            elif n == 20:
                n +=2


    # Step 4.3: Create keyboard return function which gets called every time a button is activated

    def keyboard_return(self, x: str):
        """Function takes button presses and progresses the game"""
        assert(type(x)) == str
        if self.game.miss < 6:
            self.game.partial_word, self.game.miss = self.game.word_checker(self.game.word, self.game.partial_word, x, self.game.miss)
        self.package_update(1) # 2 Times because it doesnt work otherwise, probably due to timing
        self.package_update(1)
        print(self.game)


    # Step 4.4: Create image function to render hangman picture and update it

    def hangman_stage(self, stage: int) -> 'Mutates imgLabel with Photoimage object':
        """function takes an integer between 0 and 6 and displays the corresponding stage in the GUI"""
        assert(type(stage)) == int
        photos = [PhotoImage(file='hangman-0.png'), PhotoImage(file='hangman-1.png'), PhotoImage(file='hangman-2.png'), PhotoImage(file='hangman-3.png'), PhotoImage(file='hangman-4.png'), PhotoImage(file='hangman-5.png'), PhotoImage(file='hangman-6.png')]
        self.imgLabel = Label(image=photos[stage])
        self.imgLabel.image = photos[stage]     # Python's garbage collector won't keep the images unless I create an object specific variable to hold it
        self.imgLabel.images = photos
        self.imgLabel.grid(row=0, column=0, columnspan=3, padx=10, pady=40)


    # Step 4.5: Create a packing function to place all objects on the grid and update grid

    def package_update(self, update: int):
        """function places all objects on a grid to display
        the param update takes two arguments
        0 - initial placement
        1 - update placement

        function places certain items on the grid every time it is ran
        items that only need to be placed once are only executed if update = 0
        otherwise items that only need to be placed during certain stages
        or items that change throughout the game are placed if update = 1"""

        self.word_label = Label(self, text="  " + self.game.partial_word + "  ", font=('Concolas 24 bold'))
        self.word_label.grid(row=0, column=3, columnspan=6, padx=10)
        self.labeltext.set(self.game.Misses())
        self.wintext.set(self.game.totalwin)
        self.losstext.set(self.game.totalloss)
        self.missNum.grid(column=1, row=2)
        self.winNum.grid(column=1, row=3)
        self.lossNum.grid(column=1, row=4)

        if update == 0:
            self.loss_label = Label(self, text='                         ', font=('Concolas 24 bold'))
            self.loss_label.grid(row=1, column=3, columnspan=6, padx=10)
            self.head.grid(column=0, row=1)
            self.try_label.grid(column=0, row=2)
            self.losses_label.grid(column=0, row=4)
            self.wins_label.grid(column=0, row=3)
        else: 
            if self.game.miss < 6:
                self.hangman_stage(self.game.miss)
                self.loss_label = Label(self, text='                      ', font=('Concolas 24 bold'))
                self.loss_label.grid(row=1, column=3, columnspan=6, padx=10)
            else:
                self.hangman_stage(6)
                self.loss_label = Label(self, text='Y O U  L O S T', font=('Concolas 24 bold'))
                self.loss_label.grid(row=1, column=3, columnspan=6, padx=10)
        return







# Step 6. Create main function

def main(test=0):
    """Function to control the programs flow of control"""
    first = game()
    x = False
    if test == 0:
        print('Hangman')
        print()
        first.player_name = input('Please enter a User Name: \t')
        print("Hello %s, Welcome to Hangman." % first.player_name)
        print('The objective is to save the prisoner before he gets executed')
        print('To save the prisoner, complete the unknown word and uncover evidence that will prove his case')
        x = continue_function()
    while x:
        print("Spawning GUI please check hotbar")
        w = window(first)
        w.mainloop()
        break
    return True
            






# Step 7. Create GUI test function

def testgui1(on=True):
    """Function tests gui, on = true for testing the gui"""
    if on:
        print('Testing Gui: Uses the custom window class and tkinter ')
        second = game()
        y = window(second)
        y.mainloop()


# Step 8. Create Functional test function

def functional_test():
    """Function tests the entire program"""
    assert main('test value') == True
    return True


# Step 9. Create Unit test function

def unit_test(Set: int) -> True: #if all tests pass
    """tests for individual functions, only tests the set of tests that is specifically called
    provides print statements that inform the user of which tests fail or pass"""
    assert(type(Set)) == int
    if Set == 1:
        print('Testing set %s: the current_word function of the class game' % Set)
        test1 = game()
        assert(len(test1.current_word())) == 7
        assert(len(test1.current_word('testword1.txt'))) == 5
        assert(len(test1.current_word('testword2.txt'))) == 7
        assert(test1.current_word('testword1.txt')) == 'CHINA'
        assert(test1.current_word('testword2.txt')) == 'FINLAND'
    elif Set == 2:
        print('Testing set %s: the hidden_word function of the class game' % Set)
        test1 = game()
        assert(test1.hidden_word('China')) == "_ _ _ _ _ "
        assert(test1.hidden_word('Russia')) == "_ _ _ _ _ _ "
        assert(test1.hidden_word('India')) == "_ _ _ _ _ "
        assert(test1.hidden_word('America')) == "_ _ _ _ _ _ _ "
        assert(len(test1.hidden_word('China'))) == 10
        assert(len(test1.hidden_word('Russia'))) == 12
        assert(len(test1.hidden_word('India'))) == 10
        assert(len(test1.hidden_word('America'))) == 14
    elif Set == 3:
        print('Testing set %s: the word_checker function of the class game' % Set)
        test1 = game()
        assert(test1.word_checker("CHINA", "_ H _ _ _ ", "C", 0)) == ("C H _ _ _ ", 0)
        assert(test1.word_checker("CHINA", "_ H _ _ _ ", "B", 0)) == ("_ H _ _ _ ", 1)
        assert(test1.word_checker("CAADA", "_ _ _ _ _ ", "A", 0)) == ("_ A A _ A ", 0)
    return True


# Step 10. Create Test handler for tests

def try_test(value=(0,)):
    """function runs test functions and handles the raised errors"""
    assert(type(value)) == tuple
    for i in value:
        if i == 0:
            try:
                assert functional_test() == True                    #this was for testing the functions, I set up the tests before creating the functions
                print('Functional test passes')
            except AssertionError:
                print('Funtional test failed')                      #If the functional test fails, the test goes on to the unit tests of individual functions
        else:
            try: 
                assert unit_test(i) == True                         #The parameter of unit_test being one means that it tests the first set of asserts in the unit test function, or only the asserts that test the cia_detector function
                print("Unit test on set %s passes" % i)
            except AssertionError:
                print('Unit test on set %s failed' % i)


# Step 11. Create function to run main or tests depending on the initial parameters

def start_main():
    """Function runs tests if test is given as a second parameter for executing the program"""
    if len(argv) >= 2 and argv[1] == "test":
        try_test((0,1,2,3))
        testgui1(on=True)
    else:
        clearScreen()
        main(0)




# Step 12. Check to make sure program isnt being called before running function created in Step 11

if __name__ == "__main__":
    start_main()