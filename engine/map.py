import csv
from typing import List

import pygame
from pygame import Vector2 as vec2

class Map:
    def __init__(self, path: str, surface: pygame.surface.Surface, size: float) -> None:
        self.path = path
        self.surface = surface
        self.map_rect_width = size
        self.map_tile_image = pygame.Surface((self.map_rect_width, self.map_rect_width))
        self.map_tile_image.fill((100, 100, 100))

        self.data = []
        self.light_pos = []
        with open(path, "r") as f:
            reader = csv.reader(f)
            for line in reader:
                self.data.append(line)

        self.start_game_rect = None
        self.end_game_rect = None

        self.map_rects: List[pygame.Rect] = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == '2':
                    self.player_pos = self.map_rect_width * vec2(j, i)
                    self.offset = - self.player_pos + 0.5 * vec2(self.surface.get_size()) - 0.5 * vec2(self.map_rect_width, self.map_rect_width)
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == '3':
                    self.light_pos.append(vec2(
                        j * self.map_rect_width + self.offset.x,
                        i * self.map_rect_width + self.offset.y
                    ))
                if self.data[i][j] == '8':
                    self.start_game_rect = pygame.Rect(
                        self.map_rect_width * vec2(j , i) + self.offset,
                        self.map_rect_width * vec2(1, 1)
                    )
                if self.data[i][j] == '9':
                    self.end_game_rect = pygame.Rect(
                        self.map_rect_width * vec2(j , i) + self.offset,
                        self.map_rect_width * vec2(1, 1)
                    )
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == '1':
                    self.map_rects.append( pygame.Rect((
                        j * self.map_rect_width + self.offset.x,
                        i * self.map_rect_width + self.offset.y,
                        self.map_rect_width,
                        self.map_rect_width
                        )))

        if self.start_game_rect and self.end_game_rect:
            self.map_rects.append(self.start_game_rect)
            self.map_rects.append(self.end_game_rect)

        self.nearby_rects = []

        self.start_game_enabled = False
        self.end_game_enabled = False

    def draw(self, scroll, player_pos: vec2): 
        self.nearby_rects.clear()
        for rect in self.map_rects:
            distance = (player_pos - vec2(rect.center)).magnitude_squared()
            if distance <= (self.surface.get_width() ** 2):
                self.nearby_rects.append(rect)
                self.surface.blit(self.map_tile_image, rect.move(-scroll))
        if self.start_game_rect and self.end_game_rect:
            pygame.draw.rect(self.surface, (255, 0, 0), self.start_game_rect.move(-scroll))
            pygame.draw.rect(self.surface, (255, 0, 0), self.end_game_rect.move(-scroll))
