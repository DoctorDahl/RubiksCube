add_library('peasycam')
from cubie import Cubie
from move import Move

def setup():
    """
    Handles the setup for the Rubik's Cube.
    Runs once in the beginning.

    Size of the Rubik's can be changed by changing the value of numLayers.

    The cube can be dragged with the mouse, to turn the entire cube.
    Speedcubing notation is used to turn the different faces:
        F - Front
        B - Back
        U - Top
        D - Bottom
        L - Left
        R - Right

    These keys turn the corresponding face clockwise.
    Hold shift at the same time to turn counterclockwise.
    Number keys 1-6 will perform these moves 180 degrees instead.

    Pressing the spacebar will start a scramble sequence, that is then
    done in reverse - ending with the cube back where it started.
    This is just to showcase the functionality.
    """

    global cam, cube, axis, all_moves, current_move, num_layers
    global counter, sequence_started, sequence

    num_layers = 3 # Amount of layers in the Cube
    a = 10 * floor(num_layers / 2) - 5
    b = 10 * floor(num_layers / 2)
    axis = a if (num_layers % 2 == 0) else b # Value used to determine the offset of each layer.
    cube = [0 for i in range(num_layers ** 3)] # List of all the cubies
    all_moves = [] #List of all possible moves

    scramble_length = num_layers * 8 # Length of the showcase scramble
    counter = 0 # Move counter
    sequence = [] # Generated sequence of moves

    current_move = Move(0, 0, 0, 0)
    sequence_started = False

    # size(800, 800, P3D) #Window size and type
    fullScreen(P3D)
    cam = PeasyCam(this, 100 * (num_layers + 1)) #Placement of the camera
    cam.setWheelScale(0.1)
    cam.setMinimumDistance(200)
    cam.setMaximumDistance(1000)

    # Making the cube's cubies
    index = 0
    for x in range(-axis, axis+1, 10):
        for y in range(-axis, axis+1, 10):
            for z in range(-axis, axis+1, 10):
                matrix = PMatrix3D()
                matrix.translate(x/10.0, y/10.0, z/10.0)
                cube[index] = Cubie(matrix)
                cube[index].set_faces(index, num_layers)
                index = index + 1

    # Making a list of all the possible moves
    for i in range(-axis, axis+1, 10):
        if not (i == 0):
            i /= 10.0
            all_moves.append(Move(i, 0, 0, 2))
            all_moves.append(Move(i, 0, 0, 1))
            all_moves.append(Move(i, 0, 0, -1))
            all_moves.append(Move(0, i, 0, 2))
            all_moves.append(Move(0, i, 0, 1))
            all_moves.append(Move(0, i, 0, -1))
            all_moves.append(Move(0, 0, i, 2))
            all_moves.append(Move(0, 0, i, 1))
            all_moves.append(Move(0, 0, i, -1))

    # Adding random moves to the scramble
    for i in range(scramble_length):
        sequence.append(all_moves[int(random(len(all_moves)))])

    # Reversing the scramble, and adding to the list
    i = scramble_length - 1
    while i >= 0:
        move = sequence[i].copy()
        move.reverse()
        sequence.append(move)
        i -= 1


def draw():
    """
    Handles the drawing of the Rubik's Cube.
    Runs continuously.
    """

    global current_move, sequence_started, counter, cam, num_layers

    background(50) # Background color

    # Setting the HUD
    cam.beginHUD()
    
    fill(255)
    textSize(36)
    n = str(num_layers)
    header = n + "x" + n + "x" + n + " Rubik's Cube"
    textAlign(CENTER)
    text(header, width/2, 120)
    
    fill(200)
    v = height - 130
    h = width - 130
    off = 16    
    textSize(12)
    text("Start showcase by pressing the Spacebar", width / 2, height - 50)
    
    textAlign(LEFT)
    text("F - Front", h, v)
    text("B - Back", h, v + off)
    text("U - Top", h, v + 2 * off)
    text("D - Bottom", h, v + 3 * off)
    text("L - Left", h, v + 4 * off)
    text("R - Right", h, v + 5 * off)
    text("+ SHIFT to reverse", h, v + 6 * off)
    text("Num 1-6 to double", h, v + 7 * off)
    
    cam.endHUD()

    rotateX(-0.5)
    rotateY(0.4)
    rotateZ(0.1)
    scale(50)

    current_move.update(turn)

    if (sequence_started):
        if (current_move.finished):
            if (counter < len(sequence)-1):
                counter += 1
                current_move = sequence[counter]
                current_move.start()

    for i in range(len(cube)):
        push()
        if (abs(cube[i].get_x()) > 0 and cube[i].get_x() == current_move.get_x()):
            rotateX(current_move.angle)
        elif (abs(cube[i].get_y()) > 0 and cube[i].get_y() == current_move.get_y()):
            rotateY(-current_move.angle)
        elif (abs(cube[i].get_z()) > 0 and cube[i].get_z() == current_move.get_z()):
            rotateZ(current_move.angle)
        cube[i].show()
        pop()


def turn(index, dir, axis):
    """
    Handles the actual turning of the cube's layers.
    When animation has ended this method is called.
    
    :param dir: Direction of the turn. Clockwise; 1, Counterclockwise: -1, Double: 2
    :param axis: Axis of rotation; 'x', 'y' or 'z'
    """

    for i in range(len(cube)):
        c = cube[i]
        if (axis == 'x'):
            if (c.get_x() == index):
                matrix = PMatrix2D()
                matrix.rotate(dir * HALF_PI)
                matrix.translate(c.get_y(), c.get_z())
                c.update(c.get_x(), round_to_half(matrix.m02), round_to_half(matrix.m12))
                c.turn_faces(dir, axis)
        elif (axis == 'y'):
            if (c.get_y() == index):
                matrix = PMatrix2D()
                matrix.rotate(dir * HALF_PI)
                matrix.translate(c.get_x(), c.get_z())
                c.update(round_to_half(matrix.m02), c.get_y(), round_to_half(matrix.m12))
                c.turn_faces(dir, axis)
        elif (axis == 'z'):
            if (c.get_z() == index):
                matrix = PMatrix2D()
                matrix.rotate(dir*HALF_PI)
                matrix.translate(c.get_x(), c.get_y())
                c.update(round_to_half(matrix.m02), round_to_half(matrix.m12), c.get_z())
                c.turn_faces(dir, axis)


def round_to_half(num):
    """
    Helper function to avoid floating point errors.
    Flooring to the nearest half.
    
    :param num: Float to be floored to nearest half
    """
    return round(num * 2) / 2.0


def keyPressed():
    """
    Handles keypresses, and starts the corresponding move or move-sequence.
    """
    global current_move, sequence, sequence_started
    global counter, cam

    if not (current_move.animating):
        if (key == ' '):
            current_move = sequence[counter]
            current_move.start()
            counter = 0
            sequence_started = True
        elif (key == ENTER):
            cam.reset(1000)
            return
        apply_move(key)


def apply_move(move):
    """
    Handles keyboard input to perform moves on the cube
    (Only supports 3x3x3 cube for now)
    
    :param move: The char represented by keyboard press
    """
    global axis, current_move

    if (move == '1'): # F2
        current_move = Move(0, 0, axis/10.0, 2)
    elif (move == '2'): # B2
        current_move = Move(0, 0, -axis/10.0, 2)
    elif (move == '3'): # R2
        current_move = Move(axis/10.0, 0, 0, 2)
    elif (move == '4'): # L2
        current_move = Move(-axis/10.0, 0, 0, 2)
    elif (move == '5'): # D2
        current_move = Move(0, axis/10.0, 0, 2)
    elif (move == '6'): # U2
        current_move = Move(0, -axis/10.0, 0, 2)
    elif (move == 'f'): # F
        current_move = Move(0, 0, axis/10.0, 1)
    elif (move == 'F'): # F'
        current_move = Move(0, 0, axis/10.0, -1)
    elif (move == 'B'): # B'
        current_move = Move(0, 0, -axis/10.0, 1)
    elif (move == 'b'): # B
        current_move = Move(0, 0, -axis/10.0, -1)
    elif (move == 'D'): # D'
        current_move = Move(0, axis/10.0, 0, 1)
    elif (move == 'd'): # D
        current_move = Move(0, axis/10.0, 0, -1)
    elif (move == 'u'): # U
        current_move = Move(0, -axis/10.0, 0, 1)
    elif (move == 'U'): # U'
        current_move = Move(0, -axis/10.0, 0, -1)
    elif (move == 'L'): # L'
        current_move = Move(-axis/10.0, 0, 0, 1)
    elif (move == 'l'): # L
        current_move = Move(-axis/10.0, 0, 0, -1)
    elif (move == 'r'): # R
        current_move = Move(axis/10.0, 0, 0, 1)
    elif (move == 'R'): # R'
        current_move = Move(axis/10.0, 0, 0, -1)
    else:
        return
    current_move.start()
