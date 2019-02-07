from tkinter import *
import random
import time


class SimpleGame(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Incoming Avoid Getting Hit!")
        self.config(background="red", width=700, height=400, padx=4, pady=4)
        print("Frame:\t" + str(self.keys()))
        self._canvas()

    def _canvas_gameover(self):
        global instructs
        canvas.create_rectangle(0, 0, 700, 400, fill='black')
        canvas.config(background='black')
        canvas.create_text(c_width / 2, c_height / 2, text="Game Over!", font=("comic sans ms", 48, "bold"),
                           fill="white")

        instructs = Label(self, text="Press 'space' key to restart", background="white",
                          font=("comic sans ms", 12, "normal"))
        instructs.pack(side=BOTTOM)
        self.config(background="white")
        canvas.bind_all("<KeyPress-space>", self._restart)

    def _restart(self, event):
        if event.keysym == 'space':
            instructs.destroy()
            canvas.destroy()
            self._canvas()

    def _canvas(self):
        self.config(background="red")

        global canvas, c_height, c_width
        c_height = 400 - 4
        c_width = 700 - 4
        canvas = Canvas(self, background='white', width=c_width, height=c_height)
        print("\nCanvas:\t" + str(canvas.keys()))
        canvas.pack()

        self._character()
        self._barriers()

    def _game_over(self):
        pass

    def _barriers(self):
        global barriers
        barriers = []
        count = 10
        track_mov = 0
        cmp = 690

        ang_ext = 359
        stop_game = False
        while True:
            if stop_game:
                time.sleep(0.8)
                self._canvas_gameover()
                break

            gen_height = c_height * (random.randint(2, 8) / 10)
            push_down = c_height - (gen_height + 5)
            rec_dwn = canvas.create_rectangle(c_width * (count / 10), push_down, c_width * (count / 10) + 10,
                                              push_down + gen_height,
                                              fill='green')

            height_down = (c_height - gen_height) - 50
            rec_up = canvas.create_rectangle(c_width * (count / 10), 5, c_width * (count / 10) + 10,
                                             height_down,
                                             fill='green')

            barriers.append([rec_up, rec_dwn])

            for p in range(0, 90):
                if stop_game:
                    break
                for x, y in barriers:
                    canvas.move(x, -3, 0)
                    canvas.update()
                    canvas.move(y, -3, 0)
                    canvas.update()

                    if self._detect_collide(x, y):
                        canvas.itemconfig(x, fill='red')
                        canvas.itemconfig(y, fill='red')
                        stop_game = True
                        break

                canvas.itemconfig(character, start=ang_ext, extent=(359 - ang_ext * 2), fill="yellow")

                ang_ext += 2
                if ang_ext > 45:
                    ang_ext = 0

                time.sleep(0.023)
                track_mov += 3
                if track_mov > cmp:
                    canvas.delete(barriers[0][0])
                    canvas.delete(barriers[0][1])
                    del (barriers[0])
                    cmp = 280
                    track_mov = 0

    def _detect_collide(self, b1, b2):
        ch_x2 = canvas.bbox(character)[2]
        ch_y1 = canvas.bbox(character)[1]
        ch_y2 = canvas.bbox(character)[3]

        b1_x1 = canvas.bbox(b1)[0]
        b1_y1 = canvas.bbox(b1)[1]
        b1_y2 = canvas.bbox(b1)[3]

        b2_x1 = canvas.bbox(b2)[0]
        b2_y1 = canvas.bbox(b2)[1]
        b2_y2 = canvas.bbox(b2)[3]

        if ch_x2 > b1_x1 - 3 and ch_x2 < b1_x1 + 3:
            if ch_y1 >= b1_y1 and ch_y1 <= b1_y2:
                return True

        if ch_x2 > b2_x1 - 3 and ch_x2 < b2_x1 + 3:
            if ch_y2 >= b2_y1 and ch_y2 <= b2_y2:
                return True
        return False

    def _character(self):
        global character

        c_half_height = c_height / 2
        character = canvas.create_arc(20, c_half_height, 50, c_half_height + 30, start=0, extent=359, fill="red")

        canvas.bind_all("<KeyPress-Up>", self._move_character)
        canvas.bind_all("<KeyPress-Down>", self._move_character)
        canvas.bind_all("<KeyPress-Left>", self._move_character)
        canvas.bind_all("<KeyPress-Right>", self._move_character)

    def _move_character(self, event):
        if event.keysym == 'Up':
            canvas.move(character, 0, -10)
        elif event.keysym == 'Down':
            canvas.move(character, 0, 10)
        elif event.keysym == 'Left':
            canvas.move(character, 0, 0)
        elif event.keysym == 'Right':
            canvas.move(character, 0, 0)


def main():
    tk = SimpleGame()
    return "\nEVENT LOOP\n"


if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()
