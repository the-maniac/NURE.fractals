import turtle
import math


class Rule(object):

    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b


class LSystem(object):

    def __init__(self, sentence, rules) -> None:
        self.sentence = sentence
        self.rules = rules
        self.cnt = 0

    def generation(self):
        s = []
        for k, v in enumerate(list(self.sentence)):
            r = v
            for rule in self.rules:
                a = rule.a
                if a == v:
                    r = rule.b
                    break
            s.append(r)
        self.sentence = ''.join(s)
        self.cnt += 1


class LDrawer(object):
    def __init__(self, iturtle: turtle.Turtle, sentence, length, angel, debug=False):
        self.sentence = sentence
        self.length = length
        self.angel = angel
        self.iturtle = iturtle
        self.debug = debug

    def log(self, message):
        if self.debug:
            print(message)


    def render(self):
        stack = []
        allowed_commands = ["F", "G", "R", "L", "f", "B", '+', '-', ']', '[']
        length = len(self.sentence)
        for n, c in enumerate(self.sentence):
            multiplier = 1
            if n < length - 1 and self.sentence[n + 1] == "@":
                s = []
                i = n + 2
                while i <= length - 1:
                    if self.sentence[i] == '}':
                        multiplier = float(''.join(s))
                        break
                    if self.sentence[i] != '{':
                        s.append(self.sentence[i])
                    i += 1
            if c not in allowed_commands:
                continue
            self.iturtle.pendown()
            self.log(f'Pen down')
            self.log(f'Command: {c}')
            self.log(f'Multiplier: {multiplier}')
            if c in ["F", "G", "R", "L"]:
                self.log(f'Drawing line')
                self.iturtle.forward(self.length * multiplier)
            elif c in ["f", "B"]:
                self.log(f'Pen up')
                self.log(f'Moving forward')
                self.iturtle.penup()  # pen up - not drawing
                self.iturtle.forward(self.length * multiplier)
            elif c == "+":
                self.log(f'Turning right')
                self.iturtle.right(self.angel)
            elif c == "-":
                self.log(f'Turning left')
                self.iturtle.left(self.angel)
            elif c == "[":
                self.log(f'Save state')
                stack.append((turtle.position(), turtle.heading()))
            elif c == "]":
                self.log(f'Pen up')
                self.log(f'Restoring position')
                self.iturtle.penup()
                position, heading = stack.pop()
                self.iturtle.goto(position)
                self.iturtle.setheading(heading)


def init_turtle():
    ninja = turtle.Turtle()
    ninja.speed(0)  # adjust as needed (0 = fastest)
    ninja.setheading(180)  # initial heading
    # ninja.showturtle()
    ninja.hideturtle()
    # ninja.shapesize(5, 5, 12)
    ninja.resizemode('auto')
    return ninja


def init_screen():
    screen = turtle.Screen()  # create graphics window
    screen.setup(600, 600)
    screen.tracer(False)
    screen.setworldcoordinates(-400, -400, 600, 600)
    return screen


if __name__ == "__main__":
    iterations = 4
    line_length = 40
    debug = False

    rules = [
        Rule('F', "F"),
        Rule('X', "X+YF@{2}+"),
        Rule('Y', "-F@{0.5}X-Y")
    ]

    lsys = LSystem('FX', rules)

    for i in range(0, iterations):
        lsys.generation()
        print(lsys.sentence)

    ninja = init_turtle()
    screen = init_screen()

    drawer = LDrawer(ninja, lsys.sentence, line_length, math.degrees(math.pi / 2), debug=debug)
    drawer.render()

    screen.update()
    # screen.tracer(True)
    # screen.exitonclick()
