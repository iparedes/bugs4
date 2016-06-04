__author__ = 'nacho'

import wx
import wx.lib.scrolledpanel as scrolled
import numpy.random
import logging
from constants import *
from operator import attrgetter

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

import world
import bug
import pos

WIDTH=180
HEIGHT=380

logger = logging.getLogger('bugs')
hdlr=logging.FileHandler('./bugs.log')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)




# ToDo: Don't allow resizing
# ToDo: Finish world when everyone is dead
class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # Controls main loop
        self.GO=False
        self.TERMINATE=False
        self.STEP=False


        self.create_world()

        # begin wxGlade: MyFrame1.__init__
        wx.Frame.__init__(self, *args, **kwds)

        self.playpic = wx.Image("./images/play.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.pausepic = wx.Image("./images/pause.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.play_button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./images/play.png", wx.BITMAP_TYPE_ANY))
        self.step_button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./images/step.png", wx.BITMAP_TYPE_ANY))
        self.stop_button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./images/stop.png", wx.BITMAP_TYPE_ANY))
        self.label_1 = wx.StaticText(self, wx.ID_ANY, "Cycle:")
        self.label_cycle = wx.StaticText(self, wx.ID_ANY, "0")
        self.label_2 = wx.StaticText(self, wx.ID_ANY, "Bugs:")
        self.label_bugs = wx.StaticText(self, wx.ID_ANY, "0")

        self.IDTIMER=100
        self.timer=wx.Timer(self,self.IDTIMER)
        self.Bind(wx.EVT_TIMER,self.onTimer,id=self.IDTIMER)

        self.timer.Start(100)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def create_world(self):
        l=self.preload('./prog')
        B=bug.bug()
        B.compile(l)
        self.W=world.world()
        self.W.add_bug(B,pos.pos(10,20))

    def __set_properties(self):
        # begin wxGlade: MyFrame1.__set_properties
        self.SetTitle("frame_2")
        self.play_button.SetSize(self.play_button.GetBestSize())
        self.play_button.Bind(wx.EVT_BUTTON, self.onPlay)

        self.step_button.SetSize(self.step_button.GetBestSize())
        self.step_button.Bind(wx.EVT_BUTTON, self.onStep)

        self.stop_button.SetSize(self.stop_button.GetBestSize())
        self.stop_button.Bind(wx.EVT_BUTTON, self.onStop)

        #pButton.Bind(wx.EVT_BUTTON, self.OnCreate)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame1.__do_layout
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        #sizer_4 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_4=wx.FlexGridSizer(1,2,0,0)

        sizer_map=wx.FlexGridSizer(2,2,0,0)
        panel=wx.Panel(self,size=(MAPWIDTH,MAPHEIGHT))
        self.map = DrawMap(panel, self.W,(0,0))

        vbar=wx.ScrollBar(self,style=wx.SB_VERTICAL,size=(16,MAPHEIGHT))
        vbar.SetScrollbar(0,TILESHEIGHT,BOARDSIZE,TILESHEIGHT)
        vbar.Bind(wx.EVT_SCROLL,self.onScroll)

        hbar=wx.ScrollBar(self,style=wx.SB_HORIZONTAL,size=(MAPWIDTH,16))
        hbar.SetScrollbar(0,TILESWIDTH,BOARDSIZE,TILESWIDTH)
        hbar.Bind(wx.EVT_SCROLL,self.onScroll)
        sizer_map.Add(self.map,0,0,0)
        sizer_map.Add(vbar,0,0,0)
        sizer_map.Add(hbar,0,0,0)



        # There are probably better ways to set the size than hardputting the width of the scrollbars (16)
        #spanel=scrolled.ScrolledPanel(self,-1,size=(MAPWIDTH+16,MAPHEIGHT+16))
        #spanel.SetScrollbars(TILESIZE,TILESIZE,BOARDSIZE-TILESWIDTH,BOARDSIZE-TILESHEIGHT)
        #spanel.Bind(wx.EVT_SCROLLWIN, self.onScroll)


        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(2, 2, 0, 0)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_4.Add(sizer_map, 1, 0, 0)

        sizer_6.Add(self.play_button, 0, 0, 0)
        sizer_6.Add(self.step_button, 0, 0, 0)
        sizer_6.Add(self.stop_button, 0, 0, 0)
        sizer_5.Add(sizer_6, 1, 0, 0)
        grid_sizer_1.Add(self.label_1, 0, 0, 0)
        grid_sizer_1.Add(self.label_cycle, 0, 0, 0)
        grid_sizer_1.Add(self.label_2, 0, 0, 0)
        grid_sizer_1.Add(self.label_bugs, 0, 0, 0)
        sizer_5.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_5, 1, 0, 0)
        sizer_3.Add(sizer_4, 1, 0, 0)
        self.SetSizer(sizer_3)
        sizer_3.Fit(self)
        self.Layout()
        # end wxGlade

    def onScroll(self,event):
        desp=event.GetPosition()
        orient=event.GetOrientation()
        (f,c)=self.map.coords
        if orient==wx.HORIZONTAL:
            c=desp
        if orient==wx.VERTICAL:
            f=desp
        self.map.coords=(f,c)
        print str(f)+','+str(c)
        self.map.Refresh()


    def onTimer(self,event):
        if self.GO and not self.TERMINATE:
            self.GO=self.W.cycle()
            self.map.Refresh()
            self.label_cycle.SetLabel(str(self.W.cycles))
            self.label_bugs.SetLabel(str(len(self.W.bugs)))
            if self.STEP:
                self.GO=False
                self.STEP=False


    def onStep(self,event):
        self.STEP=True
        self.GO=False
        self.onPlay(event)

    def onPlay(self,event):
        self.GO=not self.GO
        if not self.GO or self.STEP:
            self.play_button.SetBitmap(self.playpic)
        else:
            self.play_button.SetBitmap(self.pausepic)


    def onStop(self,event):
        self.TERMINATE=True
        self.timer.Stop()

        L=self.W.graveyard
        M=[x for x in self.W.bugs.values()]
        N=L+M
        totpop=len(N)
        print "The world ended at "+str(self.W.cycles)+" cycles."
        print "A total of "+str(totpop)+" bugs lived during this time."
        if totpop>0:
            oldest=max(L+M,key=attrgetter('age'))
            print "Oldest bug:"
            print "Id: "+oldest.id
            print "Age: "+str(oldest.age)
            print "Maxpop: "+str(self.W.maxpop)
            l=oldest.decompile()
            print l



    def preload(self,fich):
        L=[]
        with open(fich,'r') as f:
            for line in f:
                for word in line.split():
                    L.append(word)
        return L

# end of class MyFrame1

# class MyScrolledPanel(scrolled.ScrolledPanel):
#     def __init__(self, parent,size):
#         scrolled.ScrolledPanel.__init__(self, parent, -1,size=size)
#
#         vbox=wx.BoxSizer(wx.VERTICAL)
#         self.SetScrollbars(20,20,200,200)
#         self.SetSizer(vbox)
#         self.SetupScrolling()
#         self.SetAutoLayout(1)
#         self.FitInside()


class DrawMap(wx.Panel):

    def __init__(self,parent,world,coords):
        wx.Panel.__init__(self,parent,size=(MAPWIDTH,MAPHEIGHT))
        #wx.Panel.__init__(self,parent,size=(BOARDSIZE*TILESIZE,BOARDSIZE*TILESIZE))
        #scrolled.ScrolledPanel.__init__(self,parent,-1,size=(MAPWIDTH+20,MAPHEIGHT+20))
        #MyScrolledPanel.__init__(self,parent,size=(MAPWIDTH+20,MAPHEIGHT+20))

        self.Bind(wx.EVT_PAINT,self.OnDraw)
        self.W=world
        self.coords=coords



    def OnDraw(self,event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK,1.5))


        c1=self.coords[0]
        f1=self.coords[1]
        f2=f1+TILESHEIGHT
        c2=c1+TILESWIDTH

        if f2>=BOARDSIZE:
            f2=BOARDSIZE
            f1=f2-TILESHEIGHT
        if c2>=BOARDSIZE:
            c2=BOARDSIZE
            c1=c2-TILESHEIGHT

        for y in range(f1,f2):
            for x in range(c1,c2):
                a=self.W.board.cell(pos.pos(x,y))
                if a.is_hab():
                    b=a.hab[0]
                    d=b.diet()
                    if d==HERB:
                        color=HERBCOLOR
                    elif d==CARN:
                        color=CARNCOLOR
                    else:
                        color=OMNICOLOR
                elif a.has_food(CARN):
                    color=RED
                elif a.has_food(HERB):
                    color=GREEN
                else:
                    color=BROWN
                dc.SetBrush(wx.Brush(color, wx.SOLID))
                dc.DrawRectangle((y-f1)*TILESIZE,(x-c1)*TILESIZE,TILESIZE,TILESIZE)



# class DrawMap(MyScrolledPanel):
#     def __init__(self,parent,world,coords):
#         #wx.Panel.__init__(self,parent,size=(MAPWIDTH,MAPHEIGHT))
#         MyScrolledPanel.__init__(self,parent,size=(MAPWIDTH+20,MAPHEIGHT+20))
#         self.Bind(wx.EVT_PAINT,self.OnDraw)
#         self.W=world
#         self.coords=coords
#
#
#     def OnDraw(self,event=None):
#         dc = wx.PaintDC(self)
#         dc.Clear()
#         dc.SetPen(wx.Pen(wx.BLACK,1.5))
#
#
#         f1=self.coords[0]
#         c1=self.coords[1]
#         f2=f1+TILESHEIGHT
#         c2=c1+TILESWIDTH
#
#         if f2>=BOARDSIZE:
#             f2=BOARDSIZE
#             f1=f2-TILESHEIGHT
#         if c2>=BOARDSIZE:
#             c2=BOARDSIZE
#             c1=c2-TILESHEIGHT
#
#         for y in range(f1,f2):
#             for x in range(c1,c2):
#                 a=self.W.board.cell(pos.pos(x,y))
#                 if a.is_hab():
#                     b=a.hab[0]
#                     d=b.diet()
#                     if d==HERB:
#                         color=HERBCOLOR
#                     elif d==CARN:
#                         color=CARNCOLOR
#                     else:
#                         color=OMNICOLOR
#                 elif a.has_food(CARN):
#                     color=RED
#                 elif a.has_food(HERB):
#                     color=GREEN
#                 else:
#                     color=BROWN
#                 dc.SetBrush(wx.Brush(color, wx.SOLID))
#                 dc.DrawRectangle((y-f1)*TILESIZE,(x-c1)*TILESIZE,TILESIZE,TILESIZE)




if __name__ == '__main__':
    aplication = wx.App()
    window = MainFrame(parent=None)
    #window=DrawMap(parent=None)
    window.Show()
    aplication.MainLoop()
