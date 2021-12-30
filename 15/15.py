import parse

class Interpreter:
    def __init__(self, path):
        self.path = path
        self.parser = parse.Parser(path)

    def interpret(self):
        try:
            puzzle, commands = self.parser.parse()
            print(puzzle, commands)
        except parse.ParseError as e:
            print(e.message)
            pass
        except FileNotFoundError:
            print("No file found: '" + self.path + "'")
