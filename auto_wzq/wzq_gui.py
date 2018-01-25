import numpy as np

from tkinter import *
from functools import partial
from wzq import WZQ

class GUI_WZQ:
    def __init__(self,h,w):
        self.master = Tk()
        self.master.title('mini_wzq')
        self.master.resizable(width=False, height=False)
        self.wzq = WZQ(h,w)
        self.h = h
        self.w = w

        self.player = 1
        self.player_text = {1:'●',2:'〇'}
        self.player_head = {1:'黑',2:'白'}

        self.headarea = self.create_headarea()
        self.gamearea = self.create_gamearea(h,w)
        self.headarea.pack()
        self.gamearea.pack()
        self.master.mainloop()

    def reset(self):
        pass

    def flash(self,i,j):
        if self.wzq.win:
            return
        if self.wzq.play_1_round((i,j),self.player):
            exec("self.e%d_%d['text']='%s'"%(i,j,self.player_text[self.player]))
            if self.player==1:
                self.player = 2
            elif self.player==2:
                self.player = 1
            if self.wzq.win:
                self.headlabel['text'] = 'win:'+self.player_head[self.wzq.win]
            else:
                self.headlabel['text'] = 'next:'+self.player_head[self.player]
                if self.player==2:
                    point = self.wzq.robot_1(self.player).tolist()
                    self.flash(*point)

    def create_headarea(self):
        head = Frame(self.master)
        self.headlabel = headarea = Label(head,text='next:'+self.player_head[self.player])
        resetbot = Button(head,text='reset',font=('黑体',9),relief='groove',command=self.reset)
        headarea.pack(side=LEFT)
        resetbot.pack(side=RIGHT)
        return head

    def create_gamearea(self,h,w):
        gamearea = Frame(self.master)
        for i in range(h):
            for j in range(w):
                exec("self.e%d_%d = Button(gamearea,text='  ',font=('黑体',7),width=1,relief='groove',command=partial(self.flash,%d,%d))"%(i,j,i,j))
                exec("self.e%d_%d.grid(row=i,column=j,sticky=W+E+N+S)"%(i,j))
        return gamearea


if __name__ == "__main__":
    v = GUI_WZQ(19,19)


        
