import pyxel


WINDOW_WIDTH = 150
WINDOW_HEIGHT = 150

WINDOW_BACKGROUND_COLOR = 1
FIELD_COLOR = 11
TAC_COLOR = 11
TIC_COLOR = 11


class Field:
    def __init__(self, step=1):
        # NOTE: 1 - X; 0 - O
        self.field = [None for i in range(9)]
        self.__step = step

    def step(self):
        if self.__step == 1:
            self.__step = 0
            return 1
        self.__step = 1
        return 0

    def game_end(self):
        if None not in self.field:
            return True
        return False
    
    def game_win(self):
        if self.field[0] == self.field[1] == self.field[2] != None or \
           self.field[3] == self.field[4] == self.field[5] != None or \
           self.field[6] == self.field[7] == self.field[8] != None or \
           self.field[0] == self.field[3] == self.field[6] != None or \
           self.field[1] == self.field[4] == self.field[7] != None or \
           self.field[2] == self.field[5] == self.field[8] != None or \
           self.field[0] == self.field[4] == self.field[8] != None or \
           self.field[2] == self.field[4] == self.field[6] != None:
               return True
        return False
    

class Draw:
    def __init__(self, field=Field()):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)
        pyxel.mouse(True)
        
        self.to_draw = []
        self.field = field

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(WINDOW_BACKGROUND_COLOR)

        self.draw_text_name_of_game()
        self.draw_field(FIELD_COLOR)

        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.spawn_figure()
        self.draw_figures()

        if self.field.game_win():
            self.game_end_text()
            self.game_end_win_text()
            self.game_restart_text(79)
            self.game_restart()
        if self.field.game_end():
            self.game_end_text()
            self.game_restart_text(72)
            self.game_restart()
    
    def draw_text_name_of_game(self):
        pyxel.text(53, 7, "Tic-Tac-Toe", pyxel.frame_count // 3 % 16)

    def draw_field(self, color):
        pyxel.line(56, 18, 56, 132, color)
        pyxel.line(94, 18, 94, 132, color)
        pyxel.line(18, 56, 132, 56, color)
        pyxel.line(18, 94, 132, 94, color)

    def draw_tac(self, x, y, color):
        # tac - X
        pyxel.line(x + 8, y + 8, x + 30, y + 30, color)
        pyxel.line(x + 30, y + 8, x + 8, y + 30, color)

    def draw_tic(self, x, y, color):
        # tic - O
        pyxel.circb(x + 19, y + 19, 15, color)

    def draw_figures(self):
        if len(self.to_draw) == 0:
            return
        for figure in self.to_draw:
            if figure[0] == "tac":
                self.draw_tac(figure[1], figure[2], TAC_COLOR)
                continue
            self.draw_tic(figure[1], figure[2], TIC_COLOR)

    def spawn_figure(self):
        square = self.define_square(pyxel.mouse_x, pyxel.mouse_y)
        if square != None:
            field_num, x, y = square
            if self.field.field[field_num] != None:
                return

            self.field.field[field_num] = self.field.step()
            if self.field.field[field_num] == 1:
                self.to_draw.append(["tac", x, y])
                return
            self.to_draw.append(["tic", x, y])

    def define_square(self, x, y, x_begin=18, y_begin=18, x_move=38, y_move=38):
        x_pos, y_pos = x_begin, y_begin
        for sq in range(9):
            if (sq % 3 == 0) and (sq != 0):
                x_pos = x_begin
                y_pos += y_move
            if (x > x_pos and x < x_pos + x_move) and (y > y_pos and y < y_pos + y_move):
                return sq, x_pos, y_pos
            x_pos += x_move
        return None

    def game_end_text(self):
        pyxel.text(58, 60, "Game END", pyxel.frame_count // 3 % 16)

    def game_end_win_text(self):
        winner = self.to_draw[-1][0]
        if winner == "tac":
            winner = "X"
            color = TAC_COLOR
        if winner == "tic":
            winner = "0"
            color = TIC_COLOR
        pyxel.text(60, 67, f"{winner} - win", color)

    def game_restart_text(self, y, x=39):
        pyxel.text(x, y, "press R to resturt", pyxel.frame_count // 3 % 16)

    def game_restart(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.field.field = [None for i in range(9)]
            self.to_draw = []


if __name__ == "__main__":
    Draw()
