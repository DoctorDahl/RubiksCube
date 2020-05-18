class Move(object):
    """
    Class representing the visual action of a move on a Rubik's cube.
    """
    
    def __init__(self, x, y, z, dir):
        """
        Initializes a move of a Rubik's cube
        Only one of x, y and z can be non-zero.
        
        :param x: Layer in x-axis affected
        :param y: Layer in y-axis affected
        :param z: Layer in z-axis affected
        :param dir: Direction of the turn. Clockwise; 1, Counterclockwise: -1, Double: 2
        """
        
        self.x = x
        self.y = y
        self.z = z
        self.dir = dir
        self.angle = 0
        self.speed = 0.15 # Animation speed
        self.animating = False
        self.finished = False
    
    
    def copy(self):
        """
        Returns a copy of the move 
        """
        
        return Move(self.x, self.y, self.z, self.dir)
    
    
    def reverse(self):
        """
        Reverses the direction of the move
        """
        
        if (self.dir != 2):
            self.dir = self.dir * -1
    
    
    def start(self):
        """
        Sets the flags for the move to start animating
        """
        
        self.animating = True
        self.finished = False
        self.angle = 0
    
    
    def update(self, turn):
        """
        Handles the animation of a move performed on the Rubik's Cube
        Once the full move has been animated, the actual turn is performed.
        
        :param turn: turn-function from RubiksCube.pyde
        """
        
        if (self.animating):
            if (self.dir == 2):
                self.angle += self.dir * self.speed * 0.5
                if (abs(self.angle) > PI):
                    self.angle = 0
                    self.animating = False
                    self.finished = True
                    if (abs(self.x) > 0):
                        turn(self.x, self.dir, 'x')
                    elif (abs(self.y) > 0):
                        turn(self.y, self.dir, 'y')
                    elif (abs(self.z) > 0):
                        turn(self.z, self.dir, 'z')
            else:
                self.angle += self.dir * self.speed
                if (abs(self.angle) > HALF_PI):
                    self.angle = 0
                    self.animating = False
                    self.finished = True
                    if (abs(self.x) > 0):
                        turn(self.x, self.dir, 'x')
                    elif (abs(self.y) > 0):
                        turn(self.y, self.dir, 'y')
                    elif (abs(self.z) > 0):
                        turn(self.z, self.dir, 'z')

    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_z(self):
        return self.z
