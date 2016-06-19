__author__ = 'nacho'

import numpy
import copy
from constants import *

class pos():
    def __init__(self,x=None,y=None,maxx=BOARDWIDTH-1,maxy=BOARDHEIGHT-1):
        self.maxx=maxx
        self.maxy=maxy
        if x==None or y==None:
            self.x=numpy.random.randint(0,self.maxx)
            self.y=numpy.random.randint(0,self.maxy)
            pass
        else:
            self.x=x
            self.y=y


    @property
    def row(self):
        return self.y

    @property
    def column(self):
        return self.x



    def tuple(self):
        return(self.x,self.y)

    def set(self,x,y):
        self.x=x
        self.y=y


    def dup_pos(self):
        #a=pos.pos(self.x,self.y,self.maxx,self.maxy)
        a=copy.deepcopy(self)
        return a

    def move_pos(self,dir):
        """
        :param dir:
           812
           7*3
           654
           0:random
        :return:
        """
        # normalizes to an address code
        # watch out this...
        dir=dir%9
        shift={
            1: (-1,0),
            2: (-1,1),
            3: (0,1),
            4: (1,1),
            5: (1,0),
            6: (1,-1),
            7: (0,-1),
            8: (-1,-1),
            0: (numpy.random.randint(-1,2),numpy.random.randint(-1,2)),
        }[dir]

        self.x+=shift[0]
        self.y+=shift[1]
        if self.x<0:
            self.x=self.maxx-1
        elif self.x==self.maxx:
            self.x=0
        if self.y<0:
            self.y=self.maxy-1
        elif self.y==self.maxy:
            self.y=0

    def add(self,x,y):
        self.x+=x
        self.y+=y

    def rand_pos(self):
        return numpy.random.randint(0,self.maxx),numpy.random.randint(0,self.maxy)

