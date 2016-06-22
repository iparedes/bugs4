__author__ = 'nacho'


class shiftlist:
    def __init__(self,long):
        self.maxsize=long
        self.data=[]
        self._maxed=False


    def add(self,val):
        if not self._maxed:
            self.data.append(val)
            if len(self.data)==self.maxsize:
                self._maxed=True
        else:
            del self.data[0]
            self.data.append(val)