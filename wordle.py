#./bin/python3

from os.path import abspath, join
from random import randint
from collections import Counter
try:
    from termcolor import colored
    COLOR = True
except:
    global colored
    def colored(x, *_, **__):
        return x
    COLOR = False

# Words from https://people.sc.fsu.edu/~jburkardt/datasets/words

global ABSPATH
ABSPATH = abspath(".")
def _count_gen(reader):
    b = reader(1 << 20) # 1 MB at a time
    while b:
        yield b
        b = reader(1 << 20)

def random_line(file):
    line = next(file)
    for index, _line in enumerate(file, 2):
        if not randint(0, index):
            line = _line
    return str(line)

class Wordle_Game:

    def __init__(self, wordspath):
        with open(wordspath, 'rb') as wordslist:
            self._word = random_line(wordslist)[2:-2].upper()
        self.length = len(self._word)
        self.attempts = 0
        self._counter = Counter(self._word)
        self.won = False

    def __len__(self):
        return self.attempts

    def _validate(self, word):
        """Validation code, returns bulls (correct) and cows (wrong place)"""
        bull, cow = 0, self._counter & Counter(word)
        res = [None] * len(word)
        cows = [" "] * len(word)
        for idx, (x,y) in enumerate(zip(self._word, word)):
            if x==y: # Bull
                cow[x] -= 1
                bull += 1
                res[idx] = colored(x, 'green', attrs=['reverse'])

        for idx, x in enumerate(word):
            if res[idx] == None:
                if cow[x] > 0:
                    cow[x] -= 1
                    if COLOR:
                        res[idx] = colored(x, 'yellow')
                        cows[idx] = "*"
                    else:
                        res[idx] = "*"
                        cows[idx] = x
                else:
                    res[idx] = '*'
        return ''.join(res), ''.join(cows), bull, len(cow)

    def guess(self, word):
        if self.won:
            return
        word, cows, bull, cow = self._validate(word)
        self.attempts += 1
        if bull == self.length:
            self.won = True
        return word, cows, bull, cow

def wordle(words="passwords.txt"):
    wordspath = join(ABSPATH, words)
    try:
        while True:
            game = Wordle_Game(wordspath)
            print("WORD:\n[", "*" * game.length, "]") 
            while not game.won:
                inp = input("> ").upper()
                if len(inp) != game.length:
                    print("  ERR: WRONG LENGTH")
                    continue
                word, cow, b,c = game.guess(inp)
                print(f"\r> {word} : {len(game)}")
                if not COLOR and c != 0:
                    print(f"> {cow} Misplaced")
            else:
                print("  Victory! ")
    except EOFError:
        print(f"> Word was:\n> {game._word}") 

if __name__ == "__main__":
    wordle()
