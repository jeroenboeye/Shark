# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:14:25 2011

@author: Jboeye

#version 4 visual of presence matrix and perceptual ranges. Optimizing torus behaviour
#version 5 optimize speed, less visuals.
#version 6 further optimization, omit extra loop over sharks to update presence.
# delete unnecessary fish presence loop, optimize aggregation behaviour by
# calculation the angle in which to aggregate for each cell on the grid
#rather than each individual.
"""

import tkinter as tk
import numpy as np
import math
import copy

class Visual:
    def __init__(self, max_xy, visual_zoom):
        self.zoom = visual_zoom
        self.root = tk.Tk()
        self.offset = 2 * visual_zoom
        self.max_xy = max_xy
        self.canvas = tk.Canvas(self.root,
                                width=2 * self.offset + max_xy * self.zoom,
                                height=2 * self.offset + max_xy * self.zoom)
        self.canvas.pack()
        # self.canvas.config(background = 'white')
        self.canvas.create_line(0, 0, max_xy, 0, fill='black', width=2)
        self.canvas.create_line(self.offset,
                                self.offset,
                                self.offset + max_xy * self.zoom,
                                self.offset,
                                fill='black', width=2)
        self.canvas.create_line(self.offset,
                                self.offset + max_xy * self.zoom,
                                self.offset + max_xy * self.zoom,
                                self.offset + max_xy * self.zoom,
                                fill='black', width=2)
        self.canvas.create_line(self.offset,
                                self.offset,
                                self.offset,
                                self.offset + max_xy * self.zoom,
                                fill='black', width=2)
        self.canvas.create_line(self.offset + max_xy * self.zoom,
                                self.offset,
                                self.offset + max_xy * self.zoom,
                                self.offset + max_xy * self.zoom,
                                fill='black', width=2)

    def create_shark(self, x, y, radius):
        return self.canvas.create_oval(self.offset + self.zoom * (x - radius),
                                       self.offset + self.zoom * (y - radius),
                                       self.offset + self.zoom * (x + radius),
                                       self.offset + self.zoom * (y + radius),
                                       outline='black',
                                       fill='blue')

    def create_fish(self, x, y, speed, max_speed):
        color = (speed) / float(max_speed)
        if color < 0:
            color = 0
        elif color > 1:
            color = 1
        green = int(255 * color)
        red = 255 - green
        blue = 0
        rgb = red, green, blue
        hex_code = '#%02x%02x%02x' % rgb
        return self.canvas.create_rectangle(self.offset + self.zoom * (x - 2 / float(self.zoom)),
                                            self.offset + self.zoom * (y - 2 / float(self.zoom)),
                                            self.offset + self.zoom * (x + 2 / float(self.zoom)),
                                            self.offset + self.zoom * (y + 2 / float(self.zoom)),
                                            outline=str(hex_code),
                                            fill=str(hex_code))

    def move(self, drawing, dx, dy):
        self.canvas.move(drawing, self.zoom * dx, self.zoom * dy)

    def delete(self, drawing):
        self.canvas.delete(drawing)

    def update(self):
        self.canvas.update()


class Fish:
    def __init__(self, angle, x, y, pers_maxspeed, drawing):  # blueprint of beetle
        self.angle = angle
        self.x = x
        self.y = y
        self.pers_maxspeed = pers_maxspeed  # create individual maxspeed
        self.drawing = drawing
        self.dx = 0
        self.dy = 0

    def move_random(self, max_xy):
        speed = np.random.uniform(0, self.pers_maxspeed)
        self.angle += np.random.uniform(-math.pi / 8, math.pi / 8)
        self.dx = speed * math.cos(self.angle)
        self.dy = speed * math.sin(self.angle)
        self.adjust_movement(max_xy)
        if (max_xy < self.x < 0) or (max_xy < self.y < 0):
            print(self.x, self.y)

    def adjust_movement(self, max_xy):
        if (self.x + self.dx >= max_xy):
            self.dx -= max_xy
        elif (self.x + self.dx < 0):
            self.dx += max_xy
        if (self.y + self.dy >= max_xy):
            self.dy -= max_xy
        elif (self.y + self.dy < 0):
            self.dy += max_xy
        self.x += self.dx
        self.y += self.dy

    def check_if_eaten(self, shark_x, shark_y, shark_radius):
        eaten = False
        if ((self.x - shark_x) ** 2 + (self.y - shark_y) ** 2) < ((shark_radius) ** 2):
            eaten = True
        return eaten

    def aggregate(self, direction, max_xy):
        speed = self.pers_maxspeed * 0.75
        self.angle = (direction + np.random.uniform(-math.pi / 8, math.pi / 8))
        self.dx = speed * math.cos(self.angle)
        self.dy = speed * math.sin(self.angle)
        self.adjust_movement(max_xy)

    def flee(self, shark_x, shark_y, max_xy):
        speed = self.pers_maxspeed
        # adjust movement for torus
        if (self.x - shark_x) > (max_xy - 10):  # fish near right edge, predator near left edge
            shark_x += max_xy
        elif (self.x - shark_x) < -(max_xy - 10):  # fish near left edge, predator near right edge
            shark_x -= max_xy
        if (self.y - shark_y) > (max_xy - 10):  # fish near upper edge, predator near bottom edge
            shark_y += max_xy
        elif (self.y - shark_y) < -(max_xy - 10):  # fish near bottom edge, predator near upper edge
            shark_y -= max_xy
        self.angle = (np.random.uniform(-math.pi / 4, math.pi / 4) +
                      math.acos(math.fabs(self.x - shark_x) /
                           (math.sqrt((self.x - shark_x) ** 2
                                 + (self.y - shark_y) ** 2))))
        if (self.x - shark_x < 0) and (self.y - shark_y > 0):  # trap to the lower right
            self.angle += math.pi / 2  # +90°
        elif (self.x - shark_x < 0) and (self.y - shark_y < 0):  # trap to the upper right
            self.angle += math.pi  # +180°
        elif (self.x - shark_x > 0) and (self.y - shark_y < 0):  # trap to the upper left
            self.angle -= math.pi / 2  # -90°
        self.dx = speed * math.cos(self.angle)
        self.dy = speed * math.sin(self.angle)
        self.adjust_movement(max_xy)


class Shark:
    def __init__(self,
                 angle,
                 x, y,
                 radius,
                 shark_perceptual_range,
                 shark_max_speed,
                 drawing):
        self.radius = radius
        self.perceptual_range = shark_perceptual_range
        if self.radius < 0.5:
            self.radius = 0.5
        self.pers_maxspeed = 1
        self.angle = angle
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.drawing = drawing
        self.satisfaction = 10

    def move_random(self, max_xy):
        if self.satisfaction > 150:
            speed = np.random.uniform(0, self.pers_maxspeed / 5.)
        else:
            speed = np.random.uniform(0, self.pers_maxspeed / 1.5)
        self.angle += np.random.uniform(-math.pi / 10, math.pi / 10)
        self.dx = speed * math.cos(self.angle)
        self.dy = speed * math.sin(self.angle)
        self.adjust_movement(max_xy)

    def move_directional(self, target, max_xy):
        speed = self.pers_maxspeed
        # adjust movement for torus
        if (self.x - target.x) > (self.perceptual_range + 5):  # prey near left edge, predator near right edge
            target.x += max_xy
        elif (self.x - target.x) < -(self.perceptual_range + 5):  # prey near right edge, predator near left edge
            target.x -= max_xy
        if (self.y - target.y) > (self.perceptual_range + 5):  # prey near bottom edge, predator near upper edge
            target.y += max_xy
        elif (self.y - target.y) < -(self.perceptual_range + 5):  # prey near upper edge, predator near bottom edge
            target.y -= max_xy
            # determine angle
        self.angle = (np.random.uniform(-math.pi / 4, math.pi / 4)
                      + math.acos(math.fabs(self.x - target.x)
                             / (math.sqrt((self.x - target.x) ** 2
                                     + (self.y - target.y) ** 2))))
        # adjust angle to three alternative directions
        if (self.x - target.x < 0) and (self.y - target.y > 0):  # prey to the lower right
            self.angle -= math.pi / 2  # -90°
        elif (self.x - target.x > 0) and (self.y - target.y > 0):  # prey to the lower left
            self.angle += math.pi  # +180°
        elif (self.x - target.x > 0) and (self.y - target.y < 0):  # trap to the upper left
            self.angle += math.pi / 2  # +90°
        self.dx = speed * math.cos(self.angle)
        self.dy = speed * math.sin(self.angle)
        self.adjust_movement(max_xy)

    def adjust_movement(self, max_xy):
        if (self.x + self.dx >= max_xy):
            self.dx -= max_xy
        elif (self.x + self.dx < 0):
            self.dx += max_xy
        if (self.y + self.dy >= max_xy):
            self.dy -= max_xy
        elif (self.y + self.dy < 0):
            self.dy += max_xy
        self.x += self.dx
        self.y += self.dy

        # PREPARATIONS & INITIALIZATIONS


class Animals:
    def __init__(self,
                 startsharkpop,
                 startfishpop,
                 max_xy,
                 fish_max_speed,
                 shark_max_speed,
                 fish_perceptual_range,
                 shark_perceptual_range,
                 shark_kill_range,
                 fish_school_density,
                 visual_zoom):
        self.max_xy = max_xy
        self.fishes = []
        self.sharks = []
        self.visual_zoom = visual_zoom
        self.visual = Visual(self.max_xy, self.visual_zoom)
        self.fish_perceptual_range = fish_perceptual_range
        self.init_sharks(startsharkpop,
                         shark_kill_range,
                         shark_perceptual_range,
                         shark_max_speed)
        self.init_fishes(startfishpop, fish_max_speed)
        self.fish_school_density = fish_school_density

    def init_sharks(self,
                    startsharkpop,
                    shark_kill_range,
                    shark_perceptual_range,
                    shark_max_speed):
        for i in range(startsharkpop):  # Initialize traps
            angle = np.random.uniform(0, 2 * math.pi)
            x = np.random.uniform(shark_kill_range, self.max_xy - shark_kill_range)
            y = np.random.uniform(shark_kill_range, self.max_xy - shark_kill_range)
            drawing = self.visual.create_shark(x, y, shark_kill_range)
            self.sharks.append(Shark(angle,
                                     x, y,
                                     shark_kill_range,
                                     shark_perceptual_range,
                                     shark_max_speed,
                                     drawing))

    def init_fishes(self, startfishpop, max_speed):
        for k in range(startfishpop):  # initialize beetles
            angle = np.random.uniform(0, 2 * math.pi)
            x = np.random.uniform(0, self.max_xy)
            y = np.random.uniform(0, self.max_xy)
            pers_maxspeed = np.random.uniform(0.1, max_speed)
            drawing = self.visual.create_fish(x, y, pers_maxspeed, max_speed)
            self.fishes.append(Fish(angle, x, y, pers_maxspeed, drawing))

    def shark_movement(self, fish_presence):
        shark_presence = np.zeros([self.max_xy, self.max_xy], dtype=bool)
        for shark in self.sharks:
            target_index_list = []
            if shark.satisfaction > 0:
                shark.satisfaction -= 1
            if shark.satisfaction > 150:
                shark.move_random(self.max_xy)
                self.visual.canvas.itemconfigure(shark.drawing, fill='blue')
            else:
                self.visual.canvas.itemconfigure(shark.drawing, fill='red')
                for x in range(int(math.floor(shark.x - shark.perceptual_range)),
                               int(math.ceil(shark.x + shark.perceptual_range + 1))):
                    for y in range(int(math.floor(shark.y - shark.perceptual_range)),
                                   int(math.ceil(shark.y + shark.perceptual_range + 1))):
                        if (x - shark.x) ** 2 + (y - shark.y) ** 2 < (shark.perceptual_range) ** 2:
                            target_index_list.extend(fish_presence[x % self.max_xy][y % self.max_xy])
                if len(target_index_list) == 0:
                    shark.move_random(self.max_xy)
                else:
                    target = copy.copy(self.fishes[target_index_list[np.random.randint(len(target_index_list))]])
                    shark.move_directional(target, self.max_xy)
            # update presence matrix
            for x in range(int(math.floor(shark.x - self.fish_perceptual_range)),
                           int(math.ceil(shark.x + self.fish_perceptual_range + 1))):
                for y in range(int(math.floor(shark.y - self.fish_perceptual_range)),
                               int(math.ceil(shark.y + self.fish_perceptual_range + 1))):
                    if (x - shark.x) ** 2 + (y - shark.y) ** 2 < (shark.perceptual_range + 1) ** 2:
                        shark_presence[x % self.max_xy][y % self.max_xy] = True
                    elif (x - shark.x) ** 2 + (y - shark.y) ** 2 < (self.fish_perceptual_range + 1) ** 2:
                        shark_presence[x % self.max_xy][y % self.max_xy] = True
            self.visual.move(shark.drawing, shark.dx, shark.dy)
        return shark_presence

    def get_direction_matrix(self, shark_presence, fish_presence):
        self.aggregation_direction = np.zeros([self.max_xy, self.max_xy], dtype=float)
        self.random_walk_matrix = np.zeros([self.max_xy, self.max_xy], dtype=bool)
        for x in range(self.max_xy):
            for y in range(self.max_xy):
                if not (shark_presence[x, y]):
                    if (self.fish_school_density > len(fish_presence[x][y]) > 0):
                        max_density = 0
                        for sx in range(int(math.floor(x - self.fish_perceptual_range)),
                                        int(math.ceil(x + self.fish_perceptual_range + 1))):
                            for sy in range(int(math.floor(y - self.fish_perceptual_range)),
                                            int(math.ceil(y + self.fish_perceptual_range + 1))):
                                if (sx != x) and (sy != y):
                                    if len(fish_presence[sx % self.max_xy][sy % self.max_xy]) > max_density:
                                        max_density = len(fish_presence[sx % self.max_xy][sy % self.max_xy])
                                        max_density_patch_coords = (sx, sy)
                        if max_density == 0:
                            self.random_walk_matrix[x, y] = True
                        else:
                            direction = (math.acos(math.fabs(x - max_density_patch_coords[0])
                                              / (math.sqrt((x - max_density_patch_coords[0]) ** 2
                                                      + (y - max_density_patch_coords[1]) ** 2))))
                            if (x - max_density_patch_coords[0] < 0) and (
                                    y - max_density_patch_coords[1] > 0):  # prey to the lower right
                                direction -= math.pi / 2  # -90°
                            elif (x - max_density_patch_coords[0] > 0) and (
                                    y - max_density_patch_coords[1] > 0):  # prey to the lower left
                                direction += math.pi  # +180°
                            elif (x - max_density_patch_coords[0] > 0) and (
                                    y - max_density_patch_coords[1] < 0):  # trap to the upper left
                                direction += math.pi / 2
                            self.aggregation_direction[x, y] = direction
                    else:
                        self.random_walk_matrix[x, y] = True

    def fish_movement(self, shark_presence, fish_presence):
        self.get_direction_matrix(shark_presence, fish_presence)
        old_fishpop = self.fishes[:]
        del self.fishes[:]
        for fish in old_fishpop:
            if not (shark_presence[int(fish.x), int(fish.y)]):
                if self.random_walk_matrix[int(fish.x), int(fish.y)] == True:
                    fish.move_random(self.max_xy)
                else:
                    fish.aggregate(self.aggregation_direction[int(fish.x), int(fish.y)], self.max_xy)
                self.fishes.append(fish)
                self.visual.move(fish.drawing, fish.dx, fish.dy)
            else:
                for shark in self.sharks:
                    eaten = False
                    if fish.check_if_eaten(shark.x, shark.y, shark.radius):
                        if shark.satisfaction < 250:
                            shark.satisfaction += 20
                            eaten = True
                            self.visual.delete(fish.drawing)
                            break
                if not (eaten):
                    fish.flee(shark.x, shark.y, self.max_xy)
                    self.fishes.append(fish)
                    self.visual.move(fish.drawing, fish.dx, fish.dy)

    def time_step(self):
        # make a 2D array of the landscape with a list for each cell,
        # this list will be filled with indexes of the local prey
        fish_presence = [[[] for x in range(self.max_xy)] for y in range(self.max_xy)]
        for index, fish in enumerate(self.fishes):
            fish_presence[int(fish.x)][int(fish.y)].append(index)
        shark_presence = self.shark_movement(fish_presence)
        self.fish_movement(shark_presence, fish_presence)
        self.visual.update()

    def get_average_fish_speed(self):
        speed_sum = 0
        average = 0
        if len(self.fishes) > 0:
            for fish in self.fishes:
                speed_sum += fish.pers_maxspeed
            average = speed_sum / float(len(self.fishes))
        return average


# MAINLOOP
class Simulation:
    def __init__(self,
                 max_time,
                 max_xy,  # Landscape boundaries
                 fish_max_speed,
                 shark_max_speed,
                 start_fish_pop,
                 start_shark_pop,
                 fish_perceptual_range,
                 shark_perceptual_range,
                 shark_kill_range,
                 fish_school_density,
                 visual_zoom):

        self.all_animals = Animals(start_shark_pop,
                                   start_fish_pop,
                                   max_xy,  # Landscape boundaries
                                   fish_max_speed,
                                   shark_max_speed,
                                   fish_perceptual_range,
                                   shark_perceptual_range,
                                   shark_kill_range,
                                   fish_school_density,
                                   visual_zoom)

        self.run(max_time)

    def run(self, max_time):
        for t in range(max_time):
            self.all_animals.time_step()
            if t % 100 == 0:
                avr_fish_speed = self.all_animals.get_average_fish_speed()
                print(t, len(self.all_animals.fishes), round(avr_fish_speed, 4))


if __name__ == '__main__':
    simulation = Simulation(max_time=500000,
                            max_xy=20,  # Landscape boundaries
                            fish_max_speed=1,
                            shark_max_speed=1,
                            start_fish_pop=4000,
                            start_shark_pop=1,
                            fish_perceptual_range=4,
                            shark_perceptual_range=3,
                            shark_kill_range=1,
                            fish_school_density=5,
                            visual_zoom=20)

    root.simulation()  # halts screen after simulation???
