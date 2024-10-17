##test

import sys
import os
from pynput import keyboard

#editing
#------ under line 0
#🯰🯱 🯲 🯳 🯴 🯵 🯶 🯷 🯸 🯹
#merge both Sheet.add_box's
#ctrl+lrud

def color(text,color):
    return("\x1b[38;2;{};{};{}m".format(*color)+f"{text}\x1b[0m")

class Sheet:

    def __init__(self, filename, sep=";"):

        with open(filename,"r") as file:
            self.content=file.read().replace("\ufeff","").split("\n")

        self.heigth=len(self.content)
        self.sep=sep

        self.content=[line.split(self.sep) for line in self.content]
        self.width=max([len(line) for line in self.content])

        for i in range(self.heigth):
            while len(self.content[i])<self.width:
                self.content[i].append("")

        self.num_color=(0,255,255);
        self.line_color=(225,0,225)
        self.cursor_color=(120,10,65)
        self.background=(70,0,40)

        self.cursor=[0,0]
        self.display_cursor=0;

        self.text=""

    def format(self,i):

        if i in "0123456789":
            return(color(i, self.num_color))

        if i in "│|─‾_🭶🭻┬┴┘└┐┌":
            return(color(i, self.line_color))

        return(i)

    def add_box_bottom(text, y):

        width=len("".join(text[0]))
        text.append(["" for i in range(width)])
        prev_line="".join(text[y])

        for x in range(1,width-1):
            if prev_line[x]=="│":
                text[y+1][x]="┴"
                continue
            text[y+1][x]+="─"
        text[y+1][x+1]="┘"
        text[y+1][0]="└"

    def add_box_top(text):

        width=len("".join(text[0]))
        text.insert(0,["" for i in range(width)])
        next_line="".join(text[1])

        for x in range(1,width-1):
            if next_line[x]=="│":
                text[0][x]="┬"
                continue
            text[0][x]+="─"
        text[0][x+1]="┐"
        text[0][0]="┌"

    def update(self):

        text=[["" for i in range(self.width+1)] for i in range(self.heigth)]

        for y in range(self.heigth):
            text[y][0]+=f"│ {y:<3} "
            for x in range(0,self.width):

                text[y][x+1]+="│ "
                text[y][x+1]+=f"{self.content[y][x]:<20}"[:20]+" "
            text[y][-1]+="│"

        self.line_width=len("".join(text[0]))

        Sheet.add_box_bottom(text, y)
        Sheet.add_box_top(text)

        for y in range(self.heigth):
            for x in range(self.width+1):
            
                background=""

                if text[y+1][x] not in "│|─‾_🭶🭻┬┴┘└┐┌":

                    if x==self.cursor[0] and y==self.cursor[1]:
                        background="\x1b[48;2;{};{};{}m".format(*self.cursor_color)
                    elif not y%2:
                        background="\x1b[48;2;{};{};{}m".format(*self.background)

                text[y+1][x]="".join([background+self.format(line) for line in text[y+1][x]])
            text[y+1][-1]+="\x1b[0m"

        text=["".join(line) for line in text]

        text[0]=color(text[0], self.line_color)
        text[-1]=color(text[-1], self.line_color)

        self.text=text

    def display(self):

        self.update()

        tsize=os.get_terminal_size()

        start=self.display_cursor
        end=self.display_cursor+tsize[1]

        sys.stdout.write("\x1b[H"+"\n".join(
        [self.text[i]+" "*(tsize[0]-self.line_width)
            for i in range(start,end)])+f"\x1b[{tsize[1]};{tsize[0]-6}H")

def on_press(key):

    aqua.cursor[0]+=((key==keyboard.Key.right)-(key==keyboard.Key.left))
    aqua.cursor[1]+=((key==keyboard.Key.down)-(key==keyboard.Key.up))

    aqua.cursor[0]=min(max(aqua.cursor[0],0),aqua.width)
    aqua.cursor[1]=min(max(aqua.cursor[1],0),aqua.heigth-1)

    tsize=os.get_terminal_size()

    while aqua.cursor[1]+1>=aqua.display_cursor+tsize[1]:
        aqua.display_cursor+=1
    while aqua.cursor[1]<aqua.display_cursor-1:
        aqua.display_cursor-=1

    if aqua.display_cursor==1:
        aqua.display_cursor=0

    if aqua.display_cursor==0 and aqua.cursor[1]+1>=tsize[1]:
        aqua.display_cursor=2

    if aqua.cursor[1]==aqua.heigth-1:
        aqua.display_cursor=aqua.heigth-tsize[1]+2

#    aqua.update()
    aqua.display()

listener=keyboard.Listener(on_press=on_press,
                           on_release=lambda key: None)
listener.start()

if __name__=='__main__':


    print("\x1b[A")
    print("\x1b[?1049h\x1b[H")
    #print(22,end="")

    aqua=Sheet("laderdesder.csv")
    aqua.display()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\x1b[?1049l")
