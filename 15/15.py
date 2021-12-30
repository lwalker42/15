import parse
import enum

class OPCODE(enum):
    MOVE_UP = '^'
    MOVE_DOWN = 'v'
    MOVE_LEFT = '<'
    MOVE_RIGHT = '>'

    INPUT = '?'
    OUTPUT = '!'
    
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    ZERO = '0'
    READ = '='
    WRITE = '#'

    NOOP = '_'


    

class Interpreter:
    def __init__(self, path):
        self.path = path
        self.w = 0
        self.h = 0

    #Find the current position (0 cell)
    def find_start(self):
        r, c = -1, -1
        for i in range(len(self.h)):
            for j in range(len(self.w)):
                if not self.puzzle[i][j]:
                    r, c = i, j
                    break
            if r != -1: break
        return r, c

    #Check if puzzle is solved
    def check_puzzle(self):
        flat = [ele for row in self.puzzle for ele in row]
        for i in range(len(flat)):
            if flat[i] != (i + 1) % len(flat):
                return False
        return True


    def run(self):
        #Handle parsing
        try:
            parser = parse.Parser(self.path)
            self.puzzle, self.commands = parser.parse()
            print(self.puzzle, self.commands)
        except parse.ParseError as e:
            print(e.message)
            quit()
        except FileNotFoundError:
            print("No file found: '" + self.path + "'")
            quit()


        #Initialize memory model and other stuff
        self.w = len(self.puzzle[0])
        self.h = len(self.puzzle)
        #Reduces overhead compared to finding 0 cell everytime
        r, c = self.find_start()
        self.memory = [i for i in range(self.w*self.h)]






        
        

