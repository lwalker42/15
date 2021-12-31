import parse
import enum

class OPCODE(enum.Enum):
    MOVE_UP = '^'
    MOVE_DOWN = 'v'
    MOVE_LEFT = '<'
    MOVE_RIGHT = '>'

    INPUT = '?'
    OUTPUT = '!'
    OUTPUT_ASCII = 'X'
    
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    ZERO = '0'
    READ = '@'
    WRITE = '='
    SWAP = '~'

    NOOP = '_'

move_commands = [OPCODE.MOVE_UP, OPCODE.MOVE_DOWN, 
                 OPCODE.MOVE_LEFT, OPCODE.MOVE_RIGHT]


class Interpreter:
    def __init__(self, path):
        self.path = path
        self.buffer = ''
        self.w = 0
        self.h = 0
        self.r = 0
        self.c = 0

    #Determine puzzle size and starting position (cell 0)
    def init_position(self):
        self.buffer = ''

        self.w = len(self.puzzle[0])
        self.h = len(self.puzzle)

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


    def move_up(self):
        if self.r == 0: return None
        self.puzzle[self.r][self.c], self.puzzle[self.r - 1][self.c] = \
        self.puzzle[self.r - 1][self.c], self.puzzle[self.r][self.c]
        self.r -= 1
        return self.puzzle[self.r][self.c]

    def move_down(self):
        if self.r == self.h - 1: return None
        self.puzzle[self.r][self.c], self.puzzle[self.r + 1][self.c] = \
        self.puzzle[self.r + 1][self.c], self.puzzle[self.r][self.c]
        self.r += 1
        return self.puzzle[self.r][self.c]

    def move_left(self):
        if self.c == 0: return None
        self.puzzle[self.r][self.c], self.puzzle[self.r][self.c - 1] = \
        self.puzzle[self.r][self.c - 1], self.puzzle[self.r][self.c]
        self.c -= 1
        return self.puzzle[self.r][self.c]

    def move_right(self):
        if self.c == self.w - 1: return None
        self.puzzle[self.r][self.c], self.puzzle[self.r][self.c + 1] = \
        self.puzzle[self.r][self.c + 1], self.puzzle[self.r][self.c]
        self.c += 1
        return self.puzzle[self.r][self.c]

    def move(self, opcode):
        if opcode not in move_commands: return None
        if opcode == OPCODE.MOVE_UP: return self.move_up()
        elif opcode == OPCODE.MOVE_DOWN: return self.move_down()
        elif opcode == OPCODE.MOVE_LEFT: return self.move_left()
        elif opcode == OPCODE.MOVE_RIGHT: return self.move_right()


    def step(self):

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
        #(Also helps avoid infinite loop)
        if m not in move_commands:
            raise CommandError(self.r, self.c, command)


        '''Main command switch/case'''
        
        #Handle double move command 
        if f in move_commands:
            #Special case: doubled move opcode (jump by accumulator value)
            #i.e. '^^', 'vv', '<<', '>>'
            if f == m:
                i = 0
                while i < self.memory[0]:
                    self.move(m)
                    i += 1

            #If/else move
            if self.memory[0]:
                self.move(m)
            else:
                self.move(f)

        #f is a non-move opcode (i.e. function)
        else:
            #Cell that the move swapped with
            cell = self.move(m)

            if f == OPCODE.INPUT:
                while not self.buffer:
                    self.buffer = input()
                
                #If integer, treat it as such
                try:
                    self.memory[0] = int(self.buffer)
                    self.buffer = ''
                except:
                    self.memory[0] = ord(self.buffer[0])
                    self.buffer = self.buffer[1:]

            elif f == OPCODE.OUTPUT:
                print(self.memory[0])
                
            elif f == OPCODE.OUTPUT_ASCII:
                print(chr(self.memory[0]))

            elif f == OPCODE.ZERO:
                self.memory[0] = 0

            #These opcodes require the accumulator cell to have moved
            elif cell is not None:
                if f == OPCODE.ADD:
                    self.memory[0] += self.memory[cell]
                if f == OPCODE.SUBTRACT:
                    self.memory[0] -= self.memory[cell]
                if f == OPCODE.MULTIPLY:
                    self.memory[0] *= self.memory[cell]
                if f == OPCODE.DIVIDE:
                    self.memory[0] /= self.memory[cell]
                if f == OPCODE.READ:
                    self.memory[0] = self.memory[cell]
                if f == OPCODE.WRITE:
                    self.memory[cell] = self.memory[0]
                if f == OPCODE.SWAP:
                    self.memory[0], self.memory[cell] = \
                    self.memory[cell], self.memory[0]
            
            #NOOP
            else:
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
        #Reduces overhead compared to finding 0 cell everytime
        self.init_position()
        self.memory = [i for i in range(self.w*self.h)]

        try:
            while True:
                self.step()

                if (self.r, self.c) == (self.h - 1, self.w -1):
                    if self.check_puzzle():
                        print("Program terminated")
                        return

        except CommandError as e:
            print(e.message)
            return



class CommandError(Exception):
    def __init__(self, r, c, command):
        self.message = "Command Error at (" + str(r) +", " + str(c) + "): '" + command + "'"
        super().__init__(self.message)
        self.__suppress_context__ = True
        
        

