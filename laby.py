#! /usr/bin/env python3

#   This is "Jankas Labyrinth Spiel"
#   Version 1.3.1
#
#   Copyright (C) 2000-2009  Claus Brunzema <mail@cbrunzema.de>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# configure here ...

words_to_choose_from=["ALFI", "GLAS", "MAMA", "OMI", "UDA", "JANKA",
                      "HALLO", "PAPA", "CLAUS", "OMA", "OPA", "HASE",
                      "INSA", "SINA", "IGEL", "HAUS", "BETT", "RADIO",
                      "UHR", "AUTO", "NASE", "HUT", "MUND", "HUND",
                      "MOND", "SONNE", "BROT", "TURM", "BAUM", "ZAHN",
                      "KRAN", "ZUG" ]
game_width=7
game_height=4

main_window_geometry="760x540"

#-------------------------------------------------------------------------
import tkinter as tk
import random

class Game:
    WALL=1
    CHAR=2
    HOME=3

    wall_prob=0.6

    def __init__(self, _width, _height):
        self.cellcols=_width
        self.cellrows=_height
        self.width=_width*2+1
        self.height=_height*2+1
        self.make_field()

        self.player_col=0
        self.player_row=0
        self.init_wordlist()
        self.current_word=self.words.pop(0)
        self.words.append(self.current_word)
        self.current_char_index=0
        self.player_char=""
        self.make_char()

    def init_wordlist(self):
        buffer = words_to_choose_from[:int(len(words_to_choose_from)/2)]
        queue = words_to_choose_from[int(len(words_to_choose_from)/2):]
        new = []
        for i in range(30*len(words_to_choose_from)):
            pos = random.randint(0, len(buffer)-1)
            new.append(buffer[pos])
            queue.append(buffer[pos])
            del buffer[pos]
            buffer.append(queue.pop(0))
        self.words = new

    def set_view(self, view):
        self.view=view

    def debug_print(self):
        for row in range(self.height):
            for col in range(self.width):
                sys.stdout.write("%d" % self.field[row][col])
            sys.stdout.write("\n")

    def is_vertical(self, row, col):
        return (((col % 2)==0) and ((row % 2)>0))

    def is_horizontal(self, row, col):
        return (((col % 2)>0) and ((row % 2)==0))

    def is_wall_pos(self, row, col):
        return self.is_vertical(row, col) or self.is_horizontal(row, col)

    def is_valid(self, row, col):
        return ((row>=0) and (col>=0) and
                (row<self.height) and (col<self.width))

    def make_field(self):
        self.field=[]
        for row in range(self.height):
            self.field.append([])
            for col in range(self.width):
                self.field[row].append(0)
        for row in range(self.height):
            self.field[row][0]=Game.WALL;
            self.field[row][self.width-1]=Game.WALL

        for col in range(self.width):
            self.field[0][col]=Game.WALL
            self.field[self.height-1][col]=Game.WALL

        row=0
        col=0
        while (row<self.height or col<self.width):
            if ((random.random()<0.5 or col==self.width) and
                row<self.height):
                if self.is_wall_pos(row, 1):
                    self.make_wall_e(row, 1)
                    self.make_wall_w(row, self.width-2)
                row=row+1
            else:
                if self.is_wall_pos(1, col):
                    self.make_wall_s(1, col)
                    self.make_wall_n(self.height-2, col)
                col=col+1

        self.field[1][1]=Game.HOME;

    def make_wall_n(self, row, col):
        if random.random()>Game.wall_prob:
            return
        if not self.is_valid(row, col):
            return
        if self.field[row][col]>0:
            return
        if (self.field[row-1][col-1]==0 and
            self.field[row-1][col+1]==0 and
            self.field[row-2][col]==0):
            self.field[row][col]=Game.WALL
            self.make_wall_w(row-1, col-1)
            self.make_wall_n(row-2, col)
            self.make_wall_e(row-1, col+1)

    def make_wall_s(self, row, col):
        if random.random()>Game.wall_prob:
            return
        if not self.is_valid(row, col):
            return
        if self.field[row][col]>0:
            return
        if (self.field[row+1][col-1]==0 and
            self.field[row+1][col+1]==0 and
            self.field[row+2][col]==0):
            self.field[row][col]=Game.WALL
            self.make_wall_w(row+1, col-1)
            self.make_wall_s(row+2, col)
            self.make_wall_e(row+1, col+1)

    def make_wall_w(self, row, col):
        if random.random()>Game.wall_prob:
            return
        if not self.is_valid(row, col):
            return
        if self.field[row][col]>0:
            return
        if (self.field[row-1][col-1]==0 and
            self.field[row+1][col-1]==0 and
            self.field[row][col-2]==0):
            self.field[row][col]=Game.WALL
            self.make_wall_n(row-1, col-1)
            self.make_wall_w(row, col-2)
            self.make_wall_s(row+1, col-1)

    def make_wall_e(self, row, col):
        if random.random()>Game.wall_prob:
            return
        if not self.is_valid(row, col):
            return
        if self.field[row][col]>0:
            return
        if (self.field[row-1][col+1]==0 and
            self.field[row+1][col+1]==0 and
            self.field[row][col+2]==0):
            self.field[row][col]=Game.WALL
            self.make_wall_n(row-1, col+1)
            self.make_wall_e(row, col+2)
            self.make_wall_s(row+1, col+1)

    def make_char(self):
        row=random.randint(1, self.height-1)
        col=random.randint(1, self.width-1)
        while (((row%2)==0 and (col%2)==0) or
               self.is_wall_pos(row, col) or
               self.field[row][col]!=0):
            row=random.randint(1, self.height-1)
            col=random.randint(1, self.width-1)
        self.field[row][col]=Game.CHAR

    def cell_to_field(self, cell):
        return cell*2+1

    def move_player_n(self):
        if (self.player_row>0 and
            self.field[
                self.cell_to_field(self.player_row)-1][
                    self.cell_to_field(self.player_col)]!=Game.WALL):
            self.player_row=self.player_row-1
            self.view.update_player()
            self.check_collision()

    def move_player_s(self):
        if (self.player_row<self.cellrows-1 and
            self.field[
                self.cell_to_field(self.player_row)+1][
                    self.cell_to_field(self.player_col)]!=Game.WALL):
            self.player_row=self.player_row+1
            self.view.update_player()
            self.check_collision()

    def move_player_w(self):
        if (self.player_col>0 and
            self.field[
                self.cell_to_field(self.player_row)][
                    self.cell_to_field(self.player_col)-1]!=Game.WALL):
            self.player_col=self.player_col-1
            self.view.update_player()
            self.check_collision()

    def move_player_e(self):
        if (self.player_col<self.cellcols-1 and
            self.field[
                self.cell_to_field(self.player_row)][
                    self.cell_to_field(self.player_col)+1]!=Game.WALL):
            self.player_col=self.player_col+1
            self.view.update_player()
            self.check_collision()

    def check_collision(self):
        if (self.player_char=="" and
            self.field[
            self.cell_to_field(self.player_row)][
                self.cell_to_field(self.player_col)]==Game.CHAR):
            self.player_char=self.current_word[self.current_char_index]
            self.field[
                self.cell_to_field(self.player_row)][
                    self.cell_to_field(self.player_col)]=0
            self.view.update()
        if(self.player_char!="" and
            self.field[
            self.cell_to_field(self.player_row)][
                self.cell_to_field(self.player_col)]==Game.HOME):
            self.player_char=""
            self.current_char_index=self.current_char_index+1
            if self.current_char_index>=len(self.current_word):
                self.view.show_word()
                self.current_word=self.words.pop(0)
                self.words.append(self.current_word)
                self.current_char_index=0
                self.make_field()
            self.make_char()
            self.view.update()

class View:
    def __init__(self, main_window, game):
        self.main_window=main_window
        self.game=game
        self.game.set_view(self)

        self.main_window.bind("<Escape>", self.quit_app)
        self.really_quit=0
        self.bind_game_keys()

        frame=tk.Frame(self.main_window, bg="white")

        canvasframe=tk.Frame(frame, bg="white")

        self.store=tk.Canvas(canvasframe, bg="white", border=0, height=30)
        self.store.pack(side=tk.TOP, fill=tk.X, anchor=tk.N)

        self.labyrinth=tk.Canvas(canvasframe, bg="white", border=0)
        self.labyrinth.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        endbutton=tk.Button(frame, text='Ende', command=self.quit_app,
                          bg="white", relief="flat")
        endbutton.pack(side=tk.BOTTOM, fill=tk.X)

        canvasframe.pack(expand=1, fill=tk.BOTH)
        canvasframe.bind("<Configure>", self.configure_handler)
        frame.pack(expand=1, fill=tk.BOTH)

        self.smiley_original_size=tk.PhotoImage(file="smiley.gif")
        self.home_original_size=tk.PhotoImage(file="home.gif")

    def quit_app(self, event=None):
        self.really_quit=1
        self.main_window.quit()

    def bind_game_keys(self):
        self.main_window.bind("<Up>", self.move_player_n)
        self.main_window.bind("<Down>", self.move_player_s)
        self.main_window.bind("<Left>", self.move_player_w)
        self.main_window.bind("<Right>", self.move_player_e)

    def unbind_game_keys(self):
        self.main_window.unbind("<Up>")
        self.main_window.unbind("<Down>")
        self.main_window.unbind("<Left>")
        self.main_window.unbind("<Right>")

    def configure_handler(self, event):
        self.width=event.width
        self.height=event.height
        self.cellwidth=(event.width-2.0)/self.game.cellcols
        self.cellheight=(event.height-4.0)/(self.game.cellrows+1)

        self.smiley=self.smiley_original_size.subsample(
            min(int(
                (self.smiley_original_size.width())/(0.5*self.cellwidth)),
                int(
                (self.smiley_original_size.height())/(0.5*self.cellheight))))
        self.home=self.home_original_size.subsample(
            min(int(
                (self.home_original_size.width())/(0.3*self.cellwidth)),
                int(
                (self.home_original_size.height())/(0.3*self.cellheight))))
        self.store.configure(height=self.cellheight)
        self.update()

    def update(self):
        self.store.delete(tk.ALL)
        self.store.create_text(
            int(self.cellwidth/2),
            int(self.cellheight/2),
            text=self.game.current_word[0:self.game.current_char_index],
            anchor=tk.W,
            font=("Helvetica",
                  -int(self.cellheight*0.8),
                  "bold"))

        self.labyrinth.delete(tk.ALL)
        self.labyrinth.create_rectangle(1,1,
                                        self.width-2, self.height-2,
                                        width=5)

        self.labyrinth.create_image(0, 0, image=self.smiley, tags="player")

        if self.game.player_char!="":
            self.labyrinth.create_text(
                0, 0,
                text=self.game.current_word[self.game.current_char_index],
                font=("Helvetica",
                      -int(self.cellheight*0.4),
                      "bold"),
                tags="player_char")

        for row in range(self.game.height):
            for col in range(self.game.width):
                if (self.game.is_vertical(row, col) and
                    self.game.field[row][col]==Game.WALL):
                    cell_x=int((col+1)/2)
                    cell_y=int(row/2)
                    self.labyrinth.create_line(cell_x*self.cellwidth+1,
                                               cell_y*self.cellheight+1,
                                               cell_x*self.cellwidth+1,
                                               (cell_y+1)*self.cellheight+1,
                                               width=5)
                if (self.game.is_horizontal(row, col) and
                    self.game.field[row][col]==Game.WALL):
                    cell_x=int(col/2)
                    cell_y=int((row+1)/2)
                    self.labyrinth.create_line(cell_x*self.cellwidth+1,
                                               cell_y*self.cellheight+1,
                                               (cell_x+1)*self.cellwidth+1,
                                               cell_y*self.cellheight+1,
                                               width=5)
                if self.game.field[row][col]==Game.CHAR:
                    self.labyrinth.create_text(
                         int(col/2)*self.cellwidth+(self.cellwidth*0.5),
                        int(row/2)*self.cellheight+(self.cellheight*0.5),
                        text=self.game.current_word[
                            self.game.current_char_index],
                        font=("Helvetica",
                              -int(self.cellheight*0.8),
                              "bold"))

                if self.game.field[row][col]==Game.HOME:
                     self.labyrinth.create_image(
                         int(col/2)*self.cellwidth+(self.cellwidth*0.5),
                        int(row/2)*self.cellheight+(self.cellheight*0.5),
                         image=self.home, tags="home")

        self.labyrinth.lift("player")
        self.labyrinth.lift("player_char")
        self.update_player()

    def move_player_n(self, event):
        self.game.move_player_n()

    def move_player_s(self, event):
        self.game.move_player_s()

    def move_player_w(self, event):
        self.game.move_player_w()

    def move_player_e(self, event):
        self.game.move_player_e()

    def update_player(self):
        self.labyrinth.coords(
            "player",
            self.game.player_col*self.cellwidth+self.cellwidth*0.5,
            self.game.player_row*self.cellheight+self.cellheight*0.5)
        self.labyrinth.coords(
            "player_char",
            self.game.player_col*self.cellwidth+self.cellwidth*0.5,
            self.game.player_row*self.cellheight+self.cellheight*0.5)

    def install_show_word_keys(self):
        self.main_window.bind("<Key>", self.quit_show_word)

    def quit_show_word(self, event=None):
        self.main_window.quit()

    def show_word(self):
        self.store.delete(tk.ALL)
        self.labyrinth.delete(tk.ALL)
        self.labyrinth.create_text(
            self.width/2,
            self.height/2,
            anchor=tk.S,
            text=self.game.current_word,
            font=("Helvetica",
                  -int(self.cellheight*2),
                  "bold"))
        self.unbind_game_keys()
        self.main_window.bind("<Key>", lambda event: "break")
        self.main_window.after(1500, self.install_show_word_keys)
        tk.mainloop()
        if self.really_quit:
            self.main_window.quit()
        self.main_window.unbind("<Key>")
        self.bind_game_keys()

#random.seed(1)
main_window=tk.Tk()
main_window.geometry(main_window_geometry)
main_window.title("Jankas Labyrinth Spiel")
game=Game(game_width, game_height)
view=View(main_window, game)
tk.mainloop()
