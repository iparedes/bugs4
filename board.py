__author__ = 'nacho'

import cell

class board:
    def __init__(self,width,height):
        """
        width=x coordinate
        height=y coordinate
        :param width:
        :param height:
        :return:
        """
        self.height=height
        self.width=width
        self.b=[[cell.cell() for x in range(width)] for y in range(height)]
        # b[row][col]


    def cell(self,pos):
        return self.b[pos.row][pos.column]
