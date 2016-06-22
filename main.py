__author__ = 'nacho'

import wx
import wx.lib.scrolledpanel as scrolled
import numpy.random
import logging
import codecs
import datetime
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
logger.setLevel(logging.DEBUG)


# ToDo: Don't allow resizing of main frame
# ToDo: Finish world when everyone is dead
class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # Controls main loop
        self.GO=False
        self.TERMINATE=False
        self.STEP=False
        # Selected bug
        self.SELECTEDBUG=None

        self.create_world()

        # begin wxGlade: MyFrame1.__init__
        wx.Frame.__init__(self, *args, **kwds)

        self.playpic = wx.Image("./images/play.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.pausepic = wx.Image("./images/pause.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.play_button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./images/play.png", wx.BITMAP_TYPE_ANY))
        self.step_button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./images/step.png", wx.BITMAP_TYPE_ANY))
        self.stop_button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./images/stop.png", wx.BITMAP_TYPE_ANY))
        self.loadbug_button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./images/loadbug.png", wx.BITMAP_TYPE_ANY))
        self.loadworld_button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./images/loadworld.png", wx.BITMAP_TYPE_ANY))
        self.savebug_button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./images/savebug.png", wx.BITMAP_TYPE_ANY))
        self.saveworld_button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./images/saveworld.png", wx.BITMAP_TYPE_ANY))
        self.label_sow=wx.StaticText(self,wx.ID_ANY, "Sow Rate:")
        self.sow_slider=wx.Slider(self,-1,1,0,len(self.W.sowratevalues)-1)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, "Cycle:")
        self.label_cycle = wx.StaticText(self, wx.ID_ANY, "0")
        self.label_2 = wx.StaticText(self, wx.ID_ANY, "Bugs:")
        self.label_bugs = wx.StaticText(self, wx.ID_ANY, "0")

        self.label_3= wx.StaticText(self, wx.ID_ANY, "Bug Id:")
        self.label_4= wx.StaticText(self, wx.ID_ANY, "Age:")
        self.label_5= wx.StaticText(self, wx.ID_ANY, "Energy:")
        self.label_bugid= wx.StaticText(self, wx.ID_ANY, "id")
        self.label_bugage= wx.StaticText(self, wx.ID_ANY, "age")
        self.label_bugenergy= wx.StaticText(self, wx.ID_ANY, "ener")


        self.text_ops=[]
        for i in range(0,4):
            self.text_ops.append(wx.TextCtrl(self, wx.ID_ANY,"xxxxx"))

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
        self.W.add_bug(B,pos.pos(2,1))

    def __set_properties(self):
        # begin wxGlade: MyFrame1.__set_properties
        self.SetTitle("frame_2")
        self.play_button.SetSize(self.play_button.GetBestSize())
        self.play_button.Bind(wx.EVT_BUTTON, self.onPlay)

        self.step_button.SetSize(self.step_button.GetBestSize())
        self.step_button.Bind(wx.EVT_BUTTON, self.onStep)

        self.stop_button.SetSize(self.stop_button.GetBestSize())
        self.stop_button.Bind(wx.EVT_BUTTON, self.onStop)

        self.sow_slider.SetSize(self.sow_slider.GetBestSize())
        self.sow_slider.Bind(wx.EVT_SLIDER,self.onSowUpdate)

        self.loadbug_button.SetSize(self.loadbug_button.GetBestSize())
        self.loadbug_button.Bind(wx.EVT_BUTTON, self.onLoadbug)

        self.loadworld_button.SetSize(self.loadworld_button.GetBestSize())
        self.loadworld_button.Bind(wx.EVT_BUTTON, self.onLoadworld)

        self.saveworld_button.SetSize(self.saveworld_button.GetBestSize())
        self.saveworld_button.Bind(wx.EVT_BUTTON, self.onSaveworld)

        self.savebug_button.SetSize(self.savebug_button.GetBestSize())
        self.savebug_button.Bind(wx.EVT_BUTTON, self.onSavebug)

        for i in range(0,4):
            self.text_ops[i].Enable(False)
        #pButton.Bind(wx.EVT_BUTTON, self.OnCreate)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame1.__do_layout

        # Main container
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        # Container for map and controls
        sizer_4=wx.FlexGridSizer(1,3,0,0)

        # Map and scrollbars
        # ToDo: Make the map and scrollbars a single control
        sizer_map=wx.FlexGridSizer(2,2,0,0)
        panel=wx.Panel(self,size=(MAPWIDTH,MAPHEIGHT))
        self.map = DrawMap(panel, self.W,pos.pos(0,0))
        self.map.Bind(wx.EVT_LEFT_DOWN, self.onClickMap)

        vbar=wx.ScrollBar(self,style=wx.SB_VERTICAL,size=(16,MAPHEIGHT))
        vbar.SetScrollbar(0,TILESHEIGHT,BOARDHEIGHT,TILESHEIGHT)
        vbar.Bind(wx.EVT_SCROLL,self.onScroll)

        hbar=wx.ScrollBar(self,style=wx.SB_HORIZONTAL,size=(MAPWIDTH,16))
        hbar.SetScrollbar(0,TILESWIDTH,BOARDWIDTH,TILESWIDTH)
        hbar.Bind(wx.EVT_SCROLL,self.onScroll)
        sizer_map.Add(self.map,0,0,0)
        sizer_map.Add(vbar,0,0,0)
        sizer_map.Add(hbar,0,0,0)

        # Container for controls
        ##################################
        sizer_5 = wx.BoxSizer(wx.VERTICAL)

        # Adds map
        sizer_4.Add(sizer_map, 1, 0, 0)

        # Play buttons
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(self.play_button, 0, 0, 0)
        sizer_6.Add(self.step_button, 0, 0, 0)
        sizer_6.Add(self.stop_button, 0, 0, 0)

        sizer_7=wx.BoxSizer(wx.VERTICAL)
        #sizer_7.Add(self.label_sow, 1, wx.ALIGN_BOTTOM, 0)
        sizer_7.Add(item=self.label_sow,proportion=0,flag=wx.ALIGN_BOTTOM)
        sizer_7.Add(self.sow_slider,0,0,0)

        # World info
        grid_sizer_1 = wx.FlexGridSizer(2, 2, 0, 0)
        grid_sizer_1.Add(self.label_1, 0, 0, 0)
        grid_sizer_1.Add(self.label_cycle, 0, 0, 0)
        grid_sizer_1.Add(self.label_2, 0, 0, 0)
        grid_sizer_1.Add(self.label_bugs, 0, 0, 0)

        grid_sizer_2=wx.FlexGridSizer(3,2,0,0)
        grid_sizer_2.Add(self.label_3, 0, 0, 0)
        grid_sizer_2.Add(self.label_bugid, 0, 0, 0)
        grid_sizer_2.Add(self.label_4, 0, 0, 0)
        grid_sizer_2.Add(self.label_bugage, 0, 0, 0)
        grid_sizer_2.Add(self.label_5, 0, 0, 0)
        grid_sizer_2.Add(self.label_bugenergy, 0, 0, 0)

        #bug_panel=wx.Panel(self,style=wx.RAISED_BORDER)
        #bug_panel.SetSizerAndFit(grid_sizer_2)
        #bug_panel.SetSizer(grid_sizer_2)

        sizer_ops=wx.BoxSizer(wx.VERTICAL)
        for i in range(0,4):
            sizer_ops.Add(self.text_ops[i])

        # Adds:
        # Buttons
        sizer_5.Add(sizer_6, 1, 0, 0)
        # Sow slider
        sizer_5.Add(sizer_7, 1, 0, 0 )
        # World info
        sizer_5.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        #sizer_5.Add(bug_panel, 1, wx.EXPAND, 0)
        # Bug info
        sizer_5.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        # Bug ops
        sizer_5.Add(sizer_ops,1, 0, 0)



        ##################################
        # Container for file controls
        ##################################
        sizer_filectrls=wx.BoxSizer(wx.VERTICAL)
        sizer_file1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_file1.Add(self.loadbug_button,0,0,0)
        sizer_file1.Add(self.savebug_button,0,0,0)
        sizer_file2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_file2.Add(self.loadworld_button,0,0,0)
        sizer_file2.Add(self.saveworld_button,0,0,0)
        sizer_filectrls.Add(sizer_file1)
        sizer_filectrls.Add(sizer_file2)

        # Adds controls and buginfo sizers
        sizer_4.Add(sizer_5, 1, 0, 0)
        sizer_4.Add(sizer_filectrls,1,0,0)

        sizer_3.Add(sizer_4, 1, 0, 0)
        self.SetSizer(sizer_3)
        sizer_3.Fit(self)
        self.Layout()
        # end wxGlade


    def onSowUpdate(self,event):
        pos=self.sow_slider.GetValue()
        #v=int(self.sowslider.value)
        #print v
        rate=self.W.sowratevalues[pos]
        self.W.sowrate=rate

    def onLoadbug(self,event):
        openFileDialog = wx.FileDialog(self, "Open bug file", "", "",
                                       "Bug files (*.bug)|*.bug", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.SetDirectory('./savebugs')
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        filename = openFileDialog.GetPath()

        B=bug.bug()
        file=open(filename,'rb')
        B.load(file)
        file.close()
        self.W.add_bug(B)

        self.refresh_labels()

    def onLoadworld(self,event):
        openFileDialog = wx.FileDialog(self, "Open world file", "", "",
                                       "World files (*.world)|*.world", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.SetDirectory('./savebugs')
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        filename = openFileDialog.GetPath()

        X=world.world()
        file=open(filename,'rb')
        self.W=X.load(file)

        # Makes the map to use the recently loaded World
        self.map.W=self.W
        file.close()
        self.map.Refresh()
        self.refresh_labels()


    def onSavebug(self,event):
        if self.SELECTEDBUG!=None and self.SELECTEDBUG.id in self.W.bugs:
            bug=self.W.bugs[self.SELECTEDBUG.id]
            fname="savebugs/"+bug.id+".bug"
            f=codecs.open(fname,'wb')
            #data_stringB=pickle.dumps(bug)
            bug.save(f)
            #f.write(data_stringB)
            f.close()
            self.info_msg("Bug "+bug.id+" saved.")
            #win=self.messWindow("Bug "+bug.id+" saved.")
            #self.re.add_widget(win)
            #self.draw_board()

    def onSaveworld(self,event):
        a=datetime.datetime.now()
        name=a.strftime('%Y%m%d%H%M%S')
        fname="savebugs/"+name+".world"
        f=codecs.open(fname,'wb')
        self.W.save(f)
        f.close()
        self.info_msg("World "+name+" saved.")


    def onClickMap(self,event):
        (c,f)=self.map.OnClick(event)
        print str(c)+','+str(f)
        cell=self.W.board.cell(pos.pos(c,f))
        if cell.is_hab():
            self.SELECTEDBUG=cell.hab[0]
            self.refresh_labels()


    def onScroll(self,event):
        desp=event.GetPosition()
        orient=event.GetOrientation()
        (c,f)=self.map.coords.tuple()
        if orient==wx.HORIZONTAL:
            c=desp
        if orient==wx.VERTICAL:
            f=desp
        self.map.coords.set(c,f)
        print str(f)+','+str(c)
        self.map.Refresh()


    def onTimer(self,event):
        if self.GO and not self.TERMINATE:
            self.TERMINATE=self.W.cycle()
            self.map.Refresh()

            self.refresh_labels()

            if self.STEP:
                self.GO=False
                self.STEP=False
        elif self.TERMINATE:
            self.onStop(event)


    def refresh_labels(self):
        self.label_cycle.SetLabel(str(self.W.cycles))
        self.label_bugs.SetLabel(str(len(self.W.bugs)))

        if self.SELECTEDBUG!=None and self.SELECTEDBUG.id in self.W.bugs:
            b=self.SELECTEDBUG
            self.label_bugid.SetLabel(b.id)
            self.label_bugage.SetLabel(str(b.age))
            self.label_bugenergy.SetLabel(str(b.energy()))

            m=len(b.listops.data)
            for i in range(0,m):
                self.text_ops[i].SetValue(b.listops.data[i])
                #self.text_op.SetValue(b.last_executed)

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
        self.Terminate()


    def Terminate(self):
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

            fname="savebugs/oldest-"+oldest.id+".bug"
            f=codecs.open(fname,'wb')
            #data_stringB=pickle.dumps(bug)
            oldest.save(f)
            #f.write(data_stringB)
            f.close()
            text="Bug "+oldest.id+" has been saved as the oldest bug in the run."
            self.info_msg(text)


    def info_msg(parent, message, caption = 'Message'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

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
        #wx.Panel.__init__(self,parent,size=(200,200))

        self.Bind(wx.EVT_PAINT,self.OnDraw)
        self.Bind(wx.EVT_LEFT_DOWN,self.OnClick)
        self.W=world
        self.coords=coords


    def OnClick(self,event):
        (x,y)=(event.X,event.Y)
        if (x<MAPWIDTH) and (y<MAPHEIGHT):
            mx=x/TILESIZE
            my=y/TILESIZE
            mx+=self.coords.x
            my+=self.coords.y
            return (mx,my)
        else:
            return None

    def OnDraw(self,event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK,1.5))

        c1=self.coords.column
        f1=self.coords.row
        f2=f1+TILESHEIGHT
        c2=c1+TILESWIDTH

        if f2>BOARDHEIGHT:
            f2=BOARDHEIGHT
            f1=f2-TILESHEIGHT
        if c2>BOARDWIDTH:
            c2=BOARDWIDTH
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
                # ToDo: Try to accelerate with DrawRectangleList
                dc.DrawRectangle((x-c1)*TILESIZE,(y-f1)*TILESIZE,TILESIZE,TILESIZE)
                #dc.DrawRectangle((y-f1)*TILESIZE,(x-c1)*TILESIZE,TILESIZE,TILESIZE)



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
