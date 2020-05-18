class Face(object):
    """
    Class representing a surface face for a cubie of the Rubik's cube.
    Each cubie has six faces.
    """
    
    def __init__(self, normal_vector):
        """
        Initializes a face of a cubie.
        
        :param normal_vector: 3D unit PVector perpendicular to the face's plane 
        """
        
        self.n = normal_vector
        self.c = color(15)


    def turn(self, angle, axis):
        """
        Handles the placement of the face during a move of the Rubik's cube
        
        :param angle: Angle of the turn in radians
        :param axis: Axis of rotation; 'x', 'y' or 'z'
        """
        
        v = PVector()
        if (axis == 'x'):
            v.y = round(self.n.y * cos(angle) - self.n.z * sin(angle))
            v.z = round(self.n.y * sin(angle) + self.n.z * cos(angle))
            v.x = round(self.n.x)
        elif (axis == 'y'):
            v.x = round(self.n.x * cos(angle) - self.n.z * sin(angle))
            v.z = round(self.n.x * sin(angle) + self.n.z * cos(angle))
            v.y = round(self.n.y)
        elif (axis == 'z'):
            v.x = round(self.n.x * cos(angle) - self.n.y * sin(angle))
            v.y = round(self.n.x * sin(angle) + self.n.y * cos(angle))
            v.z = round(self.n.z)
        self.n = v;
        
        
    def show(self):
        """
        Constructs the visuals of the face
        """
        
        pushMatrix()
        fill(self.c)
        noStroke()
        rectMode(CENTER)
        translate(0.5 * self.n.x, 0.5 * self.n.y, 0.5 * self.n.z)
        rotate(HALF_PI, self.n.y, self.n.x, self.n.z)
        square(0, 0, 1)
        # rect(0, 0, 1, 1, 0.2) # <-- Too slow
        popMatrix()
    
    
    def set_color(self, c):
        """
        Sets the color of the face
        
        :param c: Color
        """
        
        self.c = c
