# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:14:25 2011

@author: Jboeye

#version 4 visual of presence matrix and perceptual ranges.
"""


#import random
import numpy as np
from math import *                    
import Tkinter as tk
import copy as cp

class Visual:
    def __init__(self,max_xy,visual_zoom):
        self.zoom = visual_zoom
        self.root = tk.Tk()
        self.offset = 50   
        self.max_xy = max_xy
        self.squares = np.empty((self.max_xy, self.max_xy),dtype=object)
        self.canvas = tk.Canvas(self.root, 
                                width=2*self.offset+max_xy*self.zoom, 
                                height=2*self.offset+max_xy*self.zoom)
        self.canvas.pack()
        #self.canvas.config(background = 'white')
        self.canvas.create_line(0,0,max_xy,0,fill='black',width=2)
        self.canvas.create_line(self.offset,
                                self.offset,
                                self.offset+max_xy*self.zoom,
                                self.offset,
                                fill='black',width=2)
        self.canvas.create_line(self.offset,
                                self.offset+max_xy*self.zoom,
                                self.offset+max_xy*self.zoom,
                                self.offset+max_xy*self.zoom,
                                fill='black',width=2)         
        self.canvas.create_line(self.offset,
                                self.offset,
                                self.offset,
                                self.offset+max_xy*self.zoom,
                                fill='black',width=2)        
        self.canvas.create_line(self.offset+max_xy*self.zoom,
                                self.offset,
                                self.offset+max_xy*self.zoom,
                                self.offset+max_xy*self.zoom,
                                fill='black',width=2) 
        self.initialize_squares()
                                
    def initialize_squares(self):
        '''creates squares (drawing object)'''
        for x in xrange(self.max_xy):
            for y in xrange(self.max_xy):
                self.squares[x, y] = self.canvas.create_rectangle(self.offset+self.zoom * x,
                                                     self.offset+self.zoom * y, 
                                                     self.offset+self.zoom * x + self.zoom,
                                                     self.offset+self.zoom * y + self.zoom,
                                                     outline = 'black', 
                                                     fill = 'yellow')         
    def reset_squares(self):
        for x in xrange(self.max_xy):
            for y in xrange(self.max_xy):
                self.canvas.itemconfigure(self.squares[x, y],fill=('yellow')) 
                                
    def color_square(self, color, x, y):
        '''Changes the color of the square'''   
        self.canvas.itemconfigure(self.squares[x%self.max_xy, y%self.max_xy],fill=color)                                
        
    def create_shark(self,x,y,radius):
        return self.canvas.create_oval(self.offset+self.zoom*(x-radius),
                                       self.offset+self.zoom*(y-radius),
                                       self.offset+self.zoom*(x+radius),
                                       self.offset+self.zoom*(y+radius), 
                                       outline='black',
                                       fill='blue')
    def create_fish(self,x,y,speed,max_speed):
        color = (speed)/float(max_speed)
        if color < 0:
            color = 0
        elif color > 1:
            color = 1        
        green = int(255 * color) 
        red =  255 - green      
        blue = 0
        rgb = red, green, blue     
        hex_code = '#%02x%02x%02x' % rgb        
        return self.canvas.create_rectangle(self.offset+self.zoom*(x-2/float(self.zoom)),
                                            self.offset+self.zoom*(y-2/float(self.zoom)), 
                                            self.offset+self.zoom*(x+2/float(self.zoom)), 
                                            self.offset+self.zoom*(y+2/float(self.zoom)), 
                                            outline=str(hex_code),
                                            fill=str(hex_code))   
                                            
    def move(self,drawing,dx,dy):
        self.canvas.move(drawing,self.zoom*dx,self.zoom*dy)
        
    def delete(self,drawing):
        self.canvas.delete(drawing)
    
    def update(self):
        self.canvas.update()
                           
                           
        
class Fish:     
    def __init__(self, angle, x, y, pers_maxspeed, drawing):   #blueprint of beetle
        self.angle = angle             
        self.x = x
        self.y = y
        self.pers_maxspeed = pers_maxspeed                  #create individual maxspeed
        self.drawing=drawing    
        self.dx = 0
        self.dy = 0        

    def move_random(self,max_xy):
        speed=np.random.uniform(0,self.pers_maxspeed)
        self.angle += np.random.uniform(-pi/8,pi/8)
        self.dx = speed * cos(self.angle)
        self.dy = speed * sin(self.angle)
        self.adjust_movement(max_xy)    
        if (max_xy<self.x<0) or (max_xy<self.y<0):
            print self.x,self.y
        
    def adjust_movement(self,max_xy):
        if (self.x+self.dx>=max_xy):
            self.dx -= max_xy
        elif (self.x+self.dx<0):
            self.dx += max_xy
        if (self.y+self.dy>=max_xy):
            self.dy -= max_xy
        elif (self.y+self.dy<0):
            self.dy += max_xy
        self.x += self.dx
        self.y += self.dy             
        
    def check_if_eaten(self,shark_x,shark_y,shark_radius):
        eaten = False
        if ((self.x-shark_x)**2+(self.y-shark_y)**2) < ((shark_radius)**2):
            eaten = True
        return eaten
        
    def aggregate(self,max_density_patch_coords,max_xy): 
        target_x = max_density_patch_coords[0]      
        target_y = max_density_patch_coords[1]          
        speed=self.pers_maxspeed*0.75
        self.angle=(np.random.uniform(-pi/8,pi/8) 
                    + acos(fabs(self.x-target_x)
                    /(sqrt((self.x-target_x)**2
                    +(self.y-target_y)**2))))
        if (self.x-target_x<0) and (self.y-target_y>0): # prey to the lower right
            self.angle-=pi/2;                 # -90°
        elif (self.x-target_x>0) and (self.y-target_y>0): # prey to the lower left 
            self.angle+=pi;                   # +180°
        elif (self.x-target_x>0) and (self.y-target_y<0): # trap to the upper left
           self.angle+=pi/2;                  # +90°  
        self.dx = speed * cos(self.angle)
        self.dy = speed * sin(self.angle)
        self.adjust_movement(max_xy)   
    
    def flee(self,shark_x,shark_y,max_xy):
        speed=self.pers_maxspeed 
        #adjust movement for torus
        if (self.x-shark_x)>(max_xy-10): #fish near right edge, predator near left edge
            shark_x += max_xy
        elif (self.x-shark_x)<-(max_xy-10):#fish near left edge, predator near right edge
            shark_x -= max_xy
        if (self.y-shark_y)>(max_xy-10): #fish near upper edge, predator near bottom edge
            shark_y += max_xy
        elif (self.y-shark_y)<-(max_xy-10):#fish near bottom edge, predator near upper edge
            shark_y -= max_xy            
        self.angle=(np.random.uniform(-pi/4,pi/4) + 
                    acos(fabs(self.x-shark_x)/
                    (sqrt((self.x-shark_x)**2
                    +(self.y-shark_y)**2)))) 
        if (self.x-shark_x<0) and (self.y-shark_y>0): # trap to the lower right
            self.angle+=pi/2;                 # +90°
        elif (self.x-shark_x<0) and (self.y-shark_y<0): # trap to the upper right 
            self.angle+=pi;                   # +180°
        elif (self.x-shark_x>0) and (self.y-shark_y<0): # trap to the upper left
            self.angle-=pi/2;                 # -90°
        self.dx = speed * cos(self.angle)
        self.dy = speed * sin(self.angle) 
        self.adjust_movement(max_xy) 
                    

class Shark:    
    def __init__(self,
                 angle,
                 x,y, 
                 radius, 
                 shark_perceptual_range, 
                 shark_max_speed,
                 drawing):
        self.radius=radius
        self.perceptual_range=shark_perceptual_range
        if self.radius<0.5:
            self.radius=0.5
        self.pers_maxspeed = 2/float(self.radius)
        self.angle =angle
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.drawing = drawing
        self.satisfaction = 10

    def move_random(self,max_xy):
        if self.satisfaction>15:
            speed=np.random.uniform(0,self.pers_maxspeed/5.)
        else:
            speed=np.random.uniform(0,self.pers_maxspeed/1.5)
        self.angle += np.random.uniform(-pi/10,pi/10)
        self.dx = speed * cos(self.angle)
        self.dy = speed * sin(self.angle)
        self.adjust_movement(max_xy)        
        
    def move_directional(self,target,max_xy):     
        speed=self.pers_maxspeed
        #adjust movement for torus
        if (self.x-target.x)>(self.perceptual_range+5): #prey near left edge, predator near right edge
            target.x += max_xy
        elif (self.x-target.x)<-(self.perceptual_range+5):#prey near right edge, predator near left edge
            target.x -= max_xy
        if (self.y-target.y)>(self.perceptual_range+5): #prey near bottom edge, predator near upper edge
            target.y += max_xy
        elif (self.y-target.y)<-(self.perceptual_range+5):#prey near upper edge, predator near bottom edge
            target.y -= max_xy            
        #determine angle
        self.angle=(np.random.uniform(-pi/4,pi/4) 
                    + acos(fabs(self.x-target.x)
                    /(sqrt((self.x-target.x)**2
                    +(self.y-target.y)**2))))
        #adjust angle to three alternative directions
        if (self.x-target.x<0) and (self.y-target.y>0): # prey to the lower right
            self.angle-=pi/2;                 # -90°
        elif (self.x-target.x>0) and (self.y-target.y>0): # prey to the lower left 
            self.angle+=pi;                   # +180°
        elif (self.x-target.x>0) and (self.y-target.y<0): # trap to the upper left
           self.angle+=pi/2;                  # +90°  
        self.dx = speed * cos(self.angle)
        self.dy = speed * sin(self.angle)
        self.adjust_movement(max_xy)

    def adjust_movement(self,max_xy):
        if (self.x+self.dx>=max_xy):
            self.dx -= max_xy
        elif (self.x+self.dx<0):
            self.dx += max_xy
        if (self.y+self.dy>=max_xy):
            self.dy -= max_xy
        elif (self.y+self.dy<0):
            self.dy += max_xy
        self.x += self.dx
        self.y += self.dy        
              

#PREPARATIONS & INITIALIZATIONS        
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
        self.visual_zoom=visual_zoom
        self.visual = Visual(self.max_xy,self.visual_zoom)
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
        for i in range (startsharkpop):             #Initialize traps
            angle = np.random.uniform(0,2*pi)
            x = np.random.uniform(shark_kill_range,self.max_xy-shark_kill_range)
            y = np.random.uniform(shark_kill_range,self.max_xy-shark_kill_range)
            drawing = self.visual.create_shark(x,y,shark_kill_range)
            self.sharks.append(Shark(angle,
                                     x, y,
                                     shark_kill_range,
                                     shark_perceptual_range,
                                     shark_max_speed,
                                     drawing))
            
    def init_fishes(self,startfishpop, max_speed):    
        for k in range (startfishpop):      #initialize beetles
            angle = np.random.uniform(0,2*pi)             
            x = np.random.uniform(0,self.max_xy)
            y = np.random.uniform(0,self.max_xy)
            pers_maxspeed = np.random.uniform(0.1,max_speed) 
            drawing = self.visual.create_fish(x,y,pers_maxspeed,max_speed)                 
            self.fishes.append(Fish(angle,x,y,pers_maxspeed,drawing))    


    def time_step(self):
        self.visual.reset_squares()
        fish_presence = [[[] for x in xrange(self.max_xy)] for y in xrange(self.max_xy)]
        for index,fish in enumerate(self.fishes):
            fish_presence[int(fish.x)][int(fish.y)].append(index)
            
        
        for shark in self.sharks:
            target_index_list = []
            if shark.satisfaction>0:
                shark.satisfaction-=1
            if shark.satisfaction>15:
                shark.move_random(self.max_xy)
                self.visual.canvas.itemconfigure(shark.drawing,fill='blue')                 
            else:      
                self.visual.canvas.itemconfigure(shark.drawing,fill='red') 
                for x in xrange(int(floor(shark.x-shark.perceptual_range)),
                                int(ceil(shark.x+shark.perceptual_range+1))):
                    for y in xrange(int(floor(shark.y-shark.perceptual_range)),
                            int(ceil(shark.y+shark.perceptual_range+1))):
                                if (x-shark.x)**2 + (y-shark.y)**2<(shark.perceptual_range)**2:
                                    target_index_list.extend(fish_presence[x%self.max_xy][y%self.max_xy])              
                if len(target_index_list) == 0:
                    shark.move_random(self.max_xy)
                else:
                    target = cp.copy(self.fishes[target_index_list[np.random.randint(len(target_index_list))]])
                    shark.move_directional(target,self.max_xy)
            self.visual.move(shark.drawing,shark.dx,shark.dy) 
                               
        shark_near = np.zeros([self.max_xy,self.max_xy], dtype = bool)
        for shark in self.sharks:
            for x in xrange(int(floor(shark.x-self.fish_perceptual_range)),
                            int(ceil(shark.x+self.fish_perceptual_range+1))):
                for y in xrange(int(floor(shark.y-self.fish_perceptual_range)),
                        int(ceil(shark.y+self.fish_perceptual_range+1))):
                        if (x-shark.x)**2 + (y-shark.y)**2<(shark.perceptual_range+1)**2:  
                            shark_near[x%self.max_xy][y%self.max_xy] = True
                            self.visual.color_square('brown',x,y)                            
                        elif (x-shark.x)**2 + (y-shark.y)**2<(self.fish_perceptual_range+1)**2:
                            shark_near[x%self.max_xy][y%self.max_xy] = True
                            self.visual.color_square('orange',x,y)

        fish_presence = [[[] for x in xrange(self.max_xy)] for y in xrange(self.max_xy)]
        for index,fish in enumerate(self.fishes):
            fish_presence[int(fish.x)][int(fish.y)].append(index)
            self.visual.color_square('purple',fish.x,fish.y)

                        
        old_fishpop = self.fishes[:]
        del self.fishes[:]
        for fish in old_fishpop:
            if not(shark_near[int(fish.x),int(fish.y)]):
                if len(fish_presence[int(fish.x)][int(fish.y)])>self.fish_school_density:
                    fish.move_random(self.max_xy)                   
                else:         
                    max_density = 0                      
                    for x in xrange(int(floor(fish.x - self.fish_perceptual_range)),
                                    int(ceil(fish.x+self.fish_perceptual_range+1))):
                        for y in xrange(int(floor(fish.y-self.fish_perceptual_range)),
                                int(ceil(fish.y+self.fish_perceptual_range+1))):
                           if (x!=int(fish.x)) and (y!=int(fish.y)):
                               if len(fish_presence[x%self.max_xy][y%self.max_xy])>max_density:
                                   max_density = len(fish_presence[x%self.max_xy][x%self.max_xy])
                                   max_density_patch_coords = (x,y)                                
                    if max_density == 0:
                        fish.move_random(self.max_xy)
                    else:
                        fish.aggregate(max_density_patch_coords,self.max_xy)
                self.fishes.append(fish)
                self.visual.move(fish.drawing,fish.dx,fish.dy)
            else:
                for shark in self.sharks:
                    eaten = False
                    if fish.check_if_eaten(shark.x,shark.y,shark.radius):
                        if shark.satisfaction < 100:
                            shark.satisfaction+=20
                            eaten = True
                            self.visual.delete(fish.drawing)
                            break
                if not(eaten):
                    fish.flee(shark.x,shark.y,self.max_xy)
                    self.fishes.append(fish)       
                    self.visual.move(fish.drawing,fish.dx,fish.dy)         
             
        self.visual.update()
    def get_average_fish_speed(self):
        speed_sum=0
        average = 0
        if len(self.fishes)>0:
            for fish in self.fishes:
                speed_sum+=fish.pers_maxspeed
            average = speed_sum/float(len(self.fishes))
        return average
            
#MAINLOOP
class Simulation:
    def __init__(self,
                 max_time,
                 max_xy,               #Landscape boundaries
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
                                   max_xy,  #Landscape boundaries
                                   fish_max_speed,
                                   shark_max_speed,
                                   fish_perceptual_range,
                                   shark_perceptual_range,
                                   shark_kill_range,
                                   fish_school_density,
                                   visual_zoom)                              
        
        self.run(max_time)
    def run(self,max_time):
        for t in xrange(max_time):
            self.all_animals.time_step()
            if t%100 ==0:
                avr_fish_speed=self.all_animals.get_average_fish_speed()
                print t, len(self.all_animals.fishes), round(avr_fish_speed,4), self.all_animals.sharks[0].satisfaction

if __name__ == '__main__':                
    simulation=Simulation(max_time = 500000,
                          max_xy=25,                                                #Landscape boundaries
                          fish_max_speed=1,
                          shark_max_speed=1,
                          start_fish_pop=2000,
                          start_shark_pop=1,
                          fish_perceptual_range = 6,
                          shark_perceptual_range = 4,
                          shark_kill_range = 2,
                          fish_school_density = 5,
                          visual_zoom = 30)

    root.simulation() #halts screen after simulation???

