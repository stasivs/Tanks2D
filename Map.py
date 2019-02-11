from Tools import *
from Blocks import *
from random import choice


class Map:
    def __init__(self, board, p1, p2):
        self.board = board
        self.up_blocks = pygame.sprite.Group()  # Группа верхних блоков (для отрисовки)
        self.down_blocks = pygame.sprite.Group()  # Группа нижних блоков (для отрисовки)
        self.entities = pygame.sprite.Group()  # Группа существ
        self.solid_blocks = pygame.sprite.Group()  # Группа твердых блоков (для столкновений)

        self.cell_size = 32
        self.rows = height // self.cell_size
        self.cells = width // self.cell_size

        self.pclass1 = p1
        self.pclass2 = p2
        self.player1 = self.player2 = None
        self.scores_to_zero()

        self.__spawns1, self.__spawns2 = [], []

    def generate_map(self):
        for i in range(self.rows):
            for j in range(self.cells):
                block = get_block_by_id(self.board[j][i])
                if block.Layer == BaseBlock.UP:
                    b = block(i * self.cell_size, j * self.cell_size, self.up_blocks)
                else:
                    b = block(i * self.cell_size, j * self.cell_size, self.down_blocks)
                if b.Solid:
                    self.solid_blocks.add(b)
                if block is FirstPlayerSpawn:
                    self.__spawns1.append((i * self.cell_size, j * self.cell_size))
                if block is SecondPlayerSpawn:
                    self.__spawns2.append((i * self.cell_size, j * self.cell_size))

    def spawn_player1(self):
        self.player1 = self.pclass1(*choice(self.__spawns1), self.entities)

    def spawn_player2(self):
        self.player2 = self.pclass2(*choice(self.__spawns2), self.entities, 3)

    def scores_to_zero(self):
        self.pclass1.Scores = 0
        self.pclass2.Scores = 0

    def draw(self, _screen):
        self.down_blocks.draw(_screen)
        self.entities.draw(_screen)
        self.up_blocks.draw(_screen)

        _screen.blit(*text(str(self.pclass1.Scores), 208, 0, pygame.Color("Green")))
        _screen.blit(*text(str(self.pclass2.Scores), 408, 0, pygame.Color("Red")))

    def update(self):
        self.down_blocks.update()
        self.entities.update(self.solid_blocks, self.entities)
        self.up_blocks.update()

        if self.player1.killed:
            self.spawn_player1()
        if self.player2.killed:
            self.spawn_player2()

    def get_event(self, event):
        if event.type == pygame.USEREVENT and event.player.__class__ is self.pclass1:
            self.pclass1.Scores += event.scores
        if event.type == pygame.USEREVENT and event.player.__class__ is self.pclass2:
            self.pclass2.Scores += event.scores

        for bl in self.down_blocks:
            bl.get_event(event)
        for ent in self.entities:
            ent.get_event(event)
        for bl in self.up_blocks:
            bl.get_event(event)
