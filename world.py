__author__ = 'nacho'



import random
import logging
import pickle
import numpy.random
from constants import *

logger=logging.getLogger('bugs')

import pos
import bug
import hab
import board

# ToDo fix the difference between cycles and bug age (in a world with only one bug,
# the bug dies 2 cycles younger than the world
class world:
    def __init__(self):
        #self.habs={}
        self.bugs={}
        self.cycles=0
        self.bugcount=0
        self.maxpop=0
        self.board=board.board(BOARDSIZE,BOARDSIZE)
        self.deaths=[] # Ident of bugs dead during the cycle
        self.newborns=[] # Newborns during the cycle
        self.graveyard=[] # Dead bugs

        # Per thousand of cells growing food per cycle
        self.sowratevalues=[0.0001,0.001,0.01,0.1,1,2,5,10,50,100]
        self.sowrate=self.sowratevalues[SOWRATE]

# ToDo look for hab use
    def add_bug(self,b,posi=None):
        # d=b.diet()
        # if d==HERB:
        #     h.color=HERBCOLOR
        # elif d==CARN:
        #     h.color=CARNCOLOR
        # else:
        #     h.color=OMNICOLOR
        self.bugcount+=1
        ident=hex(self.bugcount)[2:]
        b.id=ident
        #b.board=self.board
        if not b.board:
            b.board.append(self.board)

        if posi==None:
            # Generates a random pos
            p=pos.pos()
        else:
            p=posi

        b.pos=p
        #self.habs.append(h)
        # Addes the bug to the list of living bugs
        self.bugs[ident]=b

        self.board.cell(p).set_hab(b)
        logger.info('Added bug '+ident)


    # def rand_pos(self):
    #     return numpy.random.randint(0,BOARDSIZE),numpy.random.randint(0,BOARDSIZE)

    # def new_pos(self,pos,dir):
    #     """
    #
    #     :param pos:
    #     :param dir:
    #        812
    #        7*3
    #        654
    #        0:random
    #     :return:
    #     """
    #     # normalizes to an address code
    #     # watch out this...
    #     dir=dir%9
    #     shift={
    #         1: (-1,0),
    #         2: (-1,1),
    #         3: (0,1),
    #         4: (1,1),
    #         5: (1,0),
    #         6: (1,-1),
    #         7: (0,-1),
    #         8: (-1,-1),
    #         0: (random.randint(-1,1),random.randint(-1,1)),
    #     }[dir]
    #
    #     a=pos[0]+shift[0]
    #     b=pos[1]+shift[1]
    #     if a<0:
    #         a=BOARDSIZE-1
    #     elif a==BOARDSIZE:
    #         a=0
    #     if b<0:
    #         b=BOARDSIZE-1
    #     elif b==BOARDSIZE:
    #         b=0
    #
    #     return (a,b)


    def step(self,b):
        """
        Steps a bug. Performs interactions between bug and world
        :param hab:
        :return:
        """
        # get current bug
        #b=hab.bug
        #b.age+=1
        logger.info('Running bug '+b.id+' ('+str(b.energy())+')')
        ret=b.step()
        for k in ret.keys():
            if k==RETDEAD:
                l=ret[RETDEAD]
                for id in l:
                    logger.info('Dead bug '+id+' at age '+str(b.age))
                    #bug=self.bugs[id]
                    self.deaths.append(id)
            elif k==RETOFFS:
                l=ret[RETOFFS]
                for bug in l:
                    bug.mutate(MUTRATE,STDDEV)
                    self.newborns.append(bug)

        # Process ret

        # pos=b.pos
        # cell=self.board.cell(pos)
        # ident=b.id
        # diet=b.diet()


        # ToDo: SHR
        # # This actions are lead by the world, when to be realistic should be part of the behaviour of the bug, but...
        # if b.dead():
        #     logger.info('Dead bug '+ident+' at age '+str(b.age))
        #     self.deaths.append(ident)
        #     cell.del_hab(ident)
        # elif b.mature():
        #     # offspring
        #     logger.info('Offspringing '+ident)
        #     l=b.offspring()
        #     for i in l:
        #         self.mutate(i)
        #         self.newborns.append(i)
        #         #self.add_hab(i)
        # else:
        #     if cell.has_food(diet):
        #         logger.info('Feeding '+ident)
        #         f=cell.consume_food(diet)
        #         b.feed(f)
        #
        #     # tests if the bug asks for an action
        #     c=b.readcomm()
        #     op=bug.OPS[c]
        #     if op=='MOV':
        #         # Moves the bug in the direction pointed by the head of the stack
        #         v=b.pop()
        #         logger.info('MOV '+str(v)+' '+ident)
        #         # WATCH HERE
        #         newpos=self.new_pos(pos,v)
        #         #if not self.board.cell(newpos).is_hab():
        #         hab.pos=newpos
        #         self.board.cell(pos).del_hab(ident)
        #         self.board.cell(newpos).set_hab(ident)
        #     elif op=='MOVA':
        #         # Moves the bug away from the direction pointed by the head of the stack
        #         logger.info('MOVA '+ident)
        #         v=b.pop()
        #         # WATCH HERE
        #         v+=4
        #         if v>8:
        #             v-=8
        #         newpos=self.new_pos(pos,v)
        #         #if not self.board.cell(newpos).is_hab():
        #         hab.pos=newpos
        #         self.board.cell(pos).del_hab(ident)
        #         self.board.cell(newpos).set_hab(ident)
        #     elif op=='SRFD':
        #         # Searches for food. Pushes the direction into the stack
        #         logger.info('SRFD '+ident)
        #         # ToDo: bug sets initial position
        #         for i in range(1,9):
        #             newpos=self.new_pos(pos,i)
        #             c=self.board.cell((newpos))
        #             if c.has_food(diet):
        #                 b.push(i)
        #                 break
        #         b.push(0)
        #     elif op=='SRBG':
        #         # Searches a near bug. Pushes the direction into the stack
        #         logger.info('SRBG '+ident)
        #         # ToDo: bug sets initial position
        #         for i in range(1,9):
        #             newpos=self.new_pos(pos,i)
        #             c=self.board.cell((newpos))
        #             if c.is_hab():
        #                 b.push(i)
        #                 break
        #         b.push(0)
        #     elif op=='ATK':
        #         # Attacks the other bug. (Only if one on one)
        #         l=list(cell.hab)
        #         if len(l)==2:
        #             l.remove(ident)
        #             b2=self.habs[l[0]].bug
        #             logger.info(ident+' ATK '+b2.id)
        #             e1=b.energy()
        #             e2=b2.energy()
        #             if e1>=e2:
        #                 logger.info(ident+' wins')
        #                 # Wins the attacking bug
        #                 #self.deaths.append(b2.id)
        #                 #cell.del_hab(b2.id)
        #                 b2.kill()
        #                 cell.grow_food(CARN,e2)
        #             else:
        #                 # Wins the defending bug
        #                 logger.info(ident+' losses and dies')
        #                 #self.deaths.append(ident)
        #                 #cell.del_hab(ident)
        #                 b.kill()
        #                 cell.grow_food(CARN,e1)
        #     elif op=='SHR':
        #         # Shares energy with the bugs in the same location
        #         l=list(cell.hab)
        #         neighbors=len(l)-1
        #         logger.info(ident+' SHR')
        #         if neighbors>0:
        #             logger.info(ident+' shares its energy')
        #             # There are neighbors
        #             e=b.energy()
        #             e=e*b.sharing_quote()
        #             b.feed(-e)
        #             # Shares the energy to be transfer among all the neighbors
        #             e=e/l
        #             l.remove(ident)
        #             for ident in l:
        #                 b2=self.habs[ident].bug
        #                 b2.feed(e)
        #     else:
        #         b.step()



    def cycle(self):
        self.cycles+=1
        logger.debug("Start processing "+str(len(self.deaths))+" deaths")
        for i in self.deaths:
            b=self.bugs.pop(i,None)
            self.graveyard.append(b)
        self.deaths=[]
        logger.debug("End processing deaths")
        logger.debug("Start processing "+str(len(self.newborns))+" newborns")
        for i in self.newborns:
            self.add_bug(i)
        self.newborns=[]
        logger.debug("End processing newborns")
        pop=len(self.bugs)
        if pop>self.maxpop:
            self.maxpop=pop
        if pop==0:
            logger.info('The end of the world')
            return False
        logger.info('New cycle '+str(self.cycles)+'. '+str(len(self.bugs))+' bugs.')
        for k,h in self.bugs.iteritems():
            self.step(h)

        self.sow()
        return True

    def sow(self):
        logger.info('Sowing...')
        m=BOARDSIZE*BOARDSIZE*self.sowrate/1000
        logger.debug('Start sowing '+str(m)+' cells')
        for i in range(0,int(m)):
            #x=numpy.random.randint(0,BOARDSIZE/5)*5
            x=numpy.random.randint(0,BOARDSIZE)
            y=numpy.random.randint(0,BOARDSIZE)

            self.board.cell(pos.pos(x,y)).grow_food()
        logger.debug('End sowing')

    # ToDo include configurable MUTRATE
    def mutate(self,bug):
        # size=bug.size()
        # average=size*MUTRATE/100
        # stdev=average*STDDEV/100
        # tomut=abs(numpy.random.normal(average,stdev+1))
        # listmut=numpy.random.randint(0,size,size=int(tomut))
        #bug.mutate(listmut)
        bug.mutate(MUTRATE,STDDEV)


    def dump(self,file):
        for k,b in self.habs.iteritems():
            a=b.bug.dump()
            file.write(a)

    def save(self,file):
        """
        Saves the state of the world in the file
        :param file:
        :return:
        """
        pickle.dump(self,file)

    def load(self,file):
        """
        Loads the state of the world from file
        :param file:
        :return: an object with the world
        """
        a=pickle.load(file)
        return a




