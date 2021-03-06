class Screen:

    blankChar = "."

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.buffer = [[self.blankChar for i in range(0, self.x)] for j in range(0, self.y)]

    def wipeScreen(self):
        """
        resets the screen to be blank (made up of "blankChar"s)
        """
        self.buffer = [[self.blankChar for i in range(0, self.x)] for j in range(0, self.y)]

    def print(self):
        """
        print the screen to the console. If you want the screen updated without waiting for user input, you need to call something like wait(100) and SpicyGame.print()
        :return:
        """
        for line in self.buffer:
            for char in line:
                print(char + "  ", end='')
            print()
        self.wipeScreen()
