from face import Face


class Cubie(object):
    """
    Class representing one of the small sub-divisions of the Rubik's cube.
    A standard 3x3x3 Rubik's cube has 27 of these.
    """
    
    def __init__(self, matrix):
        """
        Initializes a cubie
        
        :param matrix: PMatrix3D placing the cubie in 3D-space
        """
        
        self.matrix = matrix
        self.faces = [0 for i in range(6)]
     
           
    def set_faces(self, index, num_layers):
        """
        Populates the six faces of the cubie with Face-objects,
        and assigns the correct color to these.

        :param index: ID number of the cubie
        :param numLayers: Number of layers in the cube
        """
        
        self.faces[0] = Face(PVector(0,0,1))
        self.faces[1] = Face(PVector(0,0,-1))
        self.faces[2] = Face(PVector(0,1,0))
        self.faces[3] = Face(PVector(0,-1,0))
        self.faces[4] = Face(PVector(1,0,0))
        self.faces[5] = Face(PVector(-1,0,0))
        
        if (index % num_layers == num_layers -1):
            self.faces[0].set_color("#FFFFFF") # White
        
        if (index % num_layers == 0):
            self.faces[1].set_color("#FFD500") # Yellow
            
        if (index % (num_layers ** 2) >= (num_layers * (num_layers - 1))):
            self.faces[2].set_color("#FF5900") # Orange
        
        if (index % (num_layers ** 2) < num_layers):
            self.faces[3].set_color("#B90000") # Red
        
        if (index >= num_layers ** 2 * (num_layers - 1)):
            self.faces[4].set_color("#009B48") # Green
        
        if (index < num_layers ** 2):
            self.faces[5].set_color("#0045AD") # Blue
    
    
    def turn_faces(self, dir, axis):
        """
        Handles the turning of the cubies faces, when a move is made
        
        :param dir: Direction of the turn. Clockwise; 1, Counterclockwise: -1, Double: 2
        :param axis: Axis of rotation; 'x', 'y' or 'z'
        """
        
        angle = dir * HALF_PI
        for f in self.faces:
            f.turn(angle, axis)
    
    
    def update(self, x, y, z):
        """
        Updates the cubies placement in 3D space after a move
        
        :param x: The cubie's new x-coordinate
        :param y: The cubie's new y-coordinate
        :param z: The cubie's new z-coordinate
        """
        
        self.matrix.reset()
        self.matrix.translate(x, y, z)
    
    
    def show(self):
        """
        Defines the look of the cubie, and shows it's faces
        """
        
        noFill()
        stroke(0)
        strokeWeight(0.15)
        pushMatrix()
        applyMatrix(self.matrix)
        box(1)
        for f in self.faces:
            f.show()
        popMatrix()
    
    
    def get_x(self):
        return self.matrix.m03
    
    
    def get_y(self):
        return self.matrix.m13
    
    
    def get_z(self):
        return self.matrix.m23
