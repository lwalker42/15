import parse
import enum

class OPCODE(enum.Enum):
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

move_commands = [OPCODE.MOVE_UP, OPCODE.MOVE_DOWN, 
                 OPCODE.MOVE_LEFT, OPCODE.MOVE_RIGHT]


class Interpreter:
    def __init__(self, path):
        self.path = path
        self.w = 0
        self.h = 0
        self.r = 0
        self.c = 0

    #Find the current position (0 cell)
    def find_start(self):
        self.r, self.c = -1, -1
        for i in range(self.h):
            for j in range(self.w):
                if not self.puzzle[i][j]:
                    self.r, self.c = i, j
                    break
            if self.r != -1: break
        return self.r, self.c

    #Check if puzzle is solved
    def check_puzzle(self):
        flat = [ele for row in self.puzzle for ele in row]
        for i in range(len(flat)):
            if flat[i] != (i + 1) % len(flat):
                return False
        return True


    def step(self, r = -1, c = -1):
        if r == -1 or c == -1:
            r, c = self.find_start()

        # Isolate Move and Function out of each command
        command = self.commands[self.r][self.c]
        try:
            m = OPCODE(command[0])
            try:
                f = OPCODE(command[1])
            except IndexError:
                f = OPCODE.NOOP
        except IndexError:
            m = OPCODE.NOOP
            f = OPCODE.NOOP
        #Each command must begin with a move
        if m not in move_commands:
            raise CommandError(self.r, self.c, command)

        
        if m == OPCODE.MOVE_UP:
            pass

        


    def run(self):
        #Handle parsing
        try:
            parser = parse.Parser(self.path)
            self.puzzle, self.commands = parser.parse()
            #print(self.puzzle, self.commands)
        except parse.ParseError as e:
            print(e.message)
            return
        except FileNotFoundError:
            print("No file found: '" + self.path + "'")
            return

        #Initialize memory model and other stuff
        self.w = len(self.puzzle[0])
        self.h = len(self.puzzle)
        #Reduces overhead compared to finding 0 cell everytime
        self.find_start()
        self.memory = [i for i in range(self.w*self.h)]

        try:
            self.step()
        except CommandError as e:
            print(e.message)
            return



class CommandError(Exception):
    def __init__(self, r, c, command):
        self.message = "Command Error at (" + str(r) +", " + str(c) + "): '" + command + "'"
        super().__init__(self.message)
        self.__suppress_context__ = True
        
        

