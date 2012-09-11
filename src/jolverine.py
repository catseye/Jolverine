# Reference interpreter for Jolverine 1.0
# Sept 12, 2012, Chris Pressey, Cat's Eye Technologies
# This program is in the public domain -- see the file UNLICENSE.

import sys

class Program(object):
    def __init__(self, program, debug=False):
        self.wheel = [
            'left',
            'right',
            'rot',
            'adddx',
            'adddy',
            'input',
            'output',
        ]
        self.index = 0
        self.head = 0
        self.tape = {}
        self.playfield = {}
        self.insertpos = 'bottom'
        self._debug = debug
        y = 0
        self.maxx = 0
        for line in file:
            line = line.rstrip('\r\n')
            x = 0
            while x < len(line):
                self.playfield[(x, y)] = line[x]
                x += 1
            if x > self.maxx:
                self.maxx = x
            y += 1
        self.maxy = y
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 0

    ### helpers ###
    
    def limit(self, x):
        if x == 2:
            return -1
        if x == -2:
            return 1
        return x

    ### instructions ###
    
    def left(self):
        self.head -= 1

    def right(self):
        self.head += 1

    def rot(self):
        val = self.tape.get(self.head, 0)
        val += 1
        val = self.limit(val)
        self.tape[self.head] = val

    def adddx(self):
        self.dx += self.tape.get(self.head, 0)
        self.dx = self.limit(self.dx)

    def adddy(self):
        self.dy += self.tape.get(self.head, 0)
        self.dy = self.limit(self.dy)

    def input(self):
        c = sys.stdin.read(1)
        if c == '0':
            pass
        elif c == '1':
            self.rot()
        elif c in (' ', '\n', '\r', '\t'):
            pass
        else:
            raise ValueError("Illegal binary input character '%s'" % c)

    def output(self):
        val = self.tape.get(self.head, 0)
        if val == 1:
            c = sys.stdout.write('1')
            sys.stdout.flush()
        elif val == 0:
            c = sys.stdout.write('0')
            sys.stdout.flush()
        else:
            raise ValueError("Illegal binary output value '%d'" % val)

    ### execution ###

    def cycle(self):
        self.index += 1
        self.index %= len(self.wheel)

    def execute(self):
        name = self.wheel[self.index]
        self.debug("*                    EXECUTING %s @ (%d,%d)" % (name, self.x, self.y))
        command = getattr(self, name)
        command()
        self.wheel.pop(self.index)
        if self.insertpos == 'bottom':
            self.wheel.insert(0, name)
            self.insertpos = 'top'
        else:
            self.wheel.append(name)
            self.insertpos = 'bottom'

    def run(self):
        while True:
            instr = self.playfield.get((self.x, self.y), ' ')
            if instr == '*':
                self.execute()
            self.cycle()
            self.x += self.dx
            self.y += self.dy
            self.dump()
            if (self.x < 0 or self.y < 0 or
                self.x > self.maxx or self.y > self.maxy):
                break

    ### debugging ###
    
    def dump(self):
        if not self._debug:
            return
        print "------------"
        print "x=%d,y=%d,dx=%d,dy=%d" % (self.x, self.y, self.dx, self.dy)
        print "head: %d cell: %d" % (self.head, self.tape.get(self.head, 0))
        print "Next reinsert: %s" % self.insertpos
        print "Wheel:"
        print "------------"
        i = 0
        for x in self.wheel:
            arrow = "   "
            if i == self.index:
                arrow = "-->"
            print "%s %d. %s" % (arrow, i, x)
            i += 1
        print "------------"


    def debug(self, msg):
        if self._debug:
            print msg

if __name__ == '__main__':
    debug = False
    fnai = 1
    if sys.argv[1] == '-d':
        debug = True
        fnai = 2
    with open(sys.argv[fnai]) as file:
        p = Program(file, debug=debug)
    p.dump()
    p.run()
