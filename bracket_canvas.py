
import math, numpy
import sys

# (y, x) !!! (i, j) !!! (row, column)

class BracketCanvas:
    canvas = []
    names = []
    positions = []
    n = 2
    k = 1
    playa_size = (3, k+2)
    connection_size = (0, 5)
    nround = 1
    margin = 2
    width = 1
    height = 1
    start_indices = []
    transpose = False

    side_wall_char = '|'
    horizontal_wall_char = '-'
    connection_cable = '-|'
    connection_string = '-->'


    def __init__(self, names, positions, transpose=False):
        self.names = names
        self.positions = positions
        self.transpose = transpose

        # change characters if transposed
        if transpose:
            self.side_wall_char = '-'
            self.horizontal_wall_char = '|'
            self.connection_cable = '|-'
            self.connection_string = '||v'

        # max len of name
        self.k = 1
        for name in names:
            if len(name) > self.k:
                self.k = len(name)
        playa_size = (3, self.k+2)

        # width, height
        self.n = len(names)
        self.nround = int(math.ceil(math.log(self.n, 2)))
        self.height = self.n * (self.playa_size[0] + 1) + self.margin
        self.width = (self.nround + 1) * playa_size[1] + self.nround * self.connection_size[1] + self.k + 1
        self.canvas = [[' ' for j in range(self.width)] for i in range(self.height)]

        # start index of each round
        self.start_indices = [0]
        for r in range(1, self.nround+1):
            self.start_indices.append(self.start_indices[r-1] + int(self.n/(2**(r-1))))

    def d(self, pos, char):
        self.canvas[pos[0]][pos[1]] = char

    def dr(self, pos, char):
        self.canvas[pos[0]][pos[1]] = char
        return (pos[0], pos[1]+1)

    def dd(self, pos, char):
        self.canvas[pos[0]][pos[1]] = char
        return (pos[0]+1, pos[1])

    def draw_str(self, pos, string):
        for c in string:
            pos = self.dr(pos, c)
        return pos

    def draw_rep(self, pos, char, times):
        for i in range(times):
            pos = self.dr(pos, char)
        return pos

    def draw_playa(self, pos, name):

        cursor = pos
        cursor = self.dr(cursor, self.side_wall_char)
        cursor = self.draw_rep(cursor, self.horizontal_wall_char, self.k)
        cursor = self.dr(cursor, self.side_wall_char)

        cursor = (pos[0]+1, pos[1])
        cursor = self.dr(cursor, self.side_wall_char)
        cursor = self.draw_str(cursor, name)
        cursor = self.draw_rep(cursor, ' ', self.k - len(name))
        cursor = self.dr(cursor, self.side_wall_char)

        cursor = (pos[0]+2, pos[1])
        cursor = self.dr(cursor, self.side_wall_char)
        cursor = self.draw_rep(cursor, self.horizontal_wall_char, self.k)
        cursor = self.dr(cursor, self.side_wall_char)

        cursor = (cursor[0]+self.margin, pos[1])
        return cursor, (pos[0]+1, pos[1]+self.k+2)

    def draw_connection(self, pos1, pos2):
        up = pos1
        down = pos2
        if pos1[0] > pos2[0]:
            up = pos2
            down = pos1

        cursor = self.dr(up, self.connection_cable[0])
        while cursor[0] <= down[0]:
            cursor = self.dd(cursor, self.connection_cable[1])
        cursor = self.draw_rep(down, self.connection_cable[0], cursor[1] - down[1])

        out = self.draw_str((up[0] + int((down[0] - up[0]) / 2), cursor[1]+1), self.connection_string)

        return (out[0]-1, out[1])


    def draw_the_whole_sh(self):

        # clear
        for i in range(self.height):
            for j in range(self.width):
                self.canvas[i][j] = ' '
        # draw
        pos = 0
        nplace = self.n
        leftover = None
        cursor = (self.margin, self.margin)
        next_pos = []
        for r in range(self.nround): # FIXME

            # playas
            conns = []
            for p in range(nplace):
                name_to_draw = ''
                if pos in self.positions:
                    name_to_draw = self.names[self.positions.index(pos)]

                if len(next_pos) == 0:
                    cursor, conn = self.draw_playa(cursor, name_to_draw)
                else:
                    cursor, conn = self.draw_playa(next_pos[p], name_to_draw)
                conns.append(conn)
                pos += 1

            # connections
            if leftover != None:
                conns.append(leftover)
                leftover = None

            next_pos = []
            for i in range(int(len(conns)/2)):
                next_pos.append(self.draw_connection(conns[2*i], conns[2*i+1]))
            if len(conns) % 2 == 1: # odd
                leftover = conns[len(conns)-1]

            nplace = len(next_pos)

        if pos in self.positions:
            self.draw_str((next_pos[0][0]+1, next_pos[0][1]+1), self.names[self.positions.index(pos)])

        self.present()

    def present(self):
        if self.transpose:
            for j in range(self.width):
                for i in range(self.height):
                    sys.stdout.write( '%s' % self.canvas[i][j] )
                sys.stdout.write('\n')
        else:
            for i in range(self.height):
                for j in range(self.width):
                    sys.stdout.write( '%s' % self.canvas[i][j] )
                sys.stdout.write('\n')

    def winner_pos(self, winner_prev_pos):
        r = -1
        while r < len(self.start_indices) and self.start_indices[r+1] <= winner_prev_pos:
            r += 1

        return self.start_indices[r+1] + (winner_prev_pos - self.start_indices[r]) / 2


if __name__ == '__main__':
    
    # test
    names = ['adwaadw','bdddd','caaa','dawddawdaw']*10
    positions = range(len(names))
    positions[0] = 50

    #names = ['A', 'a', 'a']
    #positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]

    c = BracketCanvas(names, positions, True)
    c.draw_the_whole_sh()


