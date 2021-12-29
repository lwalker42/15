class Parser:

    def __init__(self, path):
        self.path = path
        self.line_num = 0

    class ParserError(Exception):
        def __init__(self, parser, message):
            super().__init__("line " + str(parser.line_num) + ": " + message)
            self.__suppress_context__ = True

    def raise_parse_error(self, message):
        raise self.ParserError(self, message)


    def open(self, *args):
        self.line_num = 0
        self.file = open(self.path, *args)

    def close(self):
        self.file.close()

    def readline(self):
        self.line_num += 1
        return self.file.readline()


    def parse(self):
        puzzle = []
        commands = []

        self.open('r')

        #Read puzzle
        while True:
            line = self.readline().strip()
            #empty line read
            if not line:
                #if the puzzle is defined, this must be the line break after it
                if puzzle: break
                #otherwise, it's padding at the top
                else: continue


            try:
                toks = list(map(lambda tok: int(tok.strip()), line.split(',')))
            except ValueError:
                self.raise_parse_error("Invalid puzzle label")

            if puzzle and len(puzzle[0]) != len(toks):
                self.raise_parse_error("Puzzle must be rectangular")
            puzzle.append(toks)

        #Check puzzle is the set [0, n-1]
        flat = [ele for row in puzzle for ele in row]
        flat.sort()
        for i in range(len(flat)):
            if i != flat[i]:
                self.raise_parse_error("Puzzle must contain a consecutive set of digits "
                                       "starting at 0")

        #Read commands
        while True:
            line = self.readline().strip()
            #End of file; anything after 
            if not line: break

            toks = list(map(lambda tok: tok.strip(), line.split(',')))

            if len(puzzle[0]) != len(toks):
                self.raise_parse_error("Command array must be the same size as the puzzle")
            commands.append(toks)
        
        if len(puzzle) != len(commands):
            self.raise_parse_error("Command array must be the same size as the puzzle")

        return (puzzle, commands)



