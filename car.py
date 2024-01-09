import math
import pygame

import numpy as np

from racing_data import DataPoint
from circuit import Goal, Circuit

BORDER_COLOR = (255, 255, 255) # Color To Crash on Hit
CAR_SPRITE = 'car.png'

class Car: 

    mass = 700 # kg
    power = 350000 # w
    width = 10 # m
    length = 10 # m
    max_steering = 450 # degrees

    acceleration = 0
    top_speed = 35

    def __init__(self, sp_x, sp_y, angle, width, goals: list[Goal], prop, circuit: Circuit, length, chord, fps=60) -> None:
        self.prop = prop
        self.size_x = self.length * self.prop
        self.size_y = self.width * self.prop
        self.corners = [0, 0, 0, 0]

        self.width = width

        self.sprite = pygame.image.load(CAR_SPRITE).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.size_x, self.size_y))
        self.rotated_sprite = self.sprite

        self.position = [sp_x, sp_y]
        self.angle = angle
        self.speed = 0

        self.speed_set = False # Flag For Default Speed Later on

        self.center = [self.position[0] + self.size_x / 2, self.position[1] + self.size_y / 2] # Calculate Center

        self.radars = [] # List For Sensors / Radars
        self.drawing_radars = [] # Radars To Be Drawn

        self.alive = True # Boolean To Check If Car is Crashed

        self.distance = 0 # Distance Driven
        self.time = None # Time Passed

        self.length_m = length
        self.length_px = chord

        self.conversion_rate = self._conversion_rate()
        self.circuit = circuit

        self.racing_data = []
        self.goals = goals
        self.active_goal = [x for x in goals if x.is_active()][0]
        self.active_goal_index = 0
        self.car_rect = self.sprite.get_rect()
        self.n_goals = len(self.goals)
        self.goals_crossed = 0
        self.last_time_crossed = 0
        self.position_ref = 0
        self.fps = fps
        
        self.d = self.distance_to_next_goal()

    def action(self, choice):
        if choice == 0: # Steer Left
            self.angle += 15
        elif choice == 1: # Steer Right
            self.angle -= 15
        elif choice == 2: # Slow Down
            new_speed = self.get_speed_diff()
            self.speed = self.speed - new_speed if self.speed - new_speed > 0 else 1
            #self.speed = self.speed - 4 if self.speed - 4 > 0 else 1
        elif choice == 3: # Speed Up
            new_speed = self.get_speed_diff()
            self.speed += new_speed
            #self.speed += 1

    def set_time(self, time):
        if self.time is None:
            self.time = time

    def _conversion_rate(self):
        return self.length_m / self.length_px

    def get_speed_diff(self):
        return self.power / (self.mass * self.speed * self.fps * 1000) * self.conversion_rate

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position) # Draw Sprite
        self.draw_radar(screen) #OPTIONAL FOR SENSORS

    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def activate_next(self):
        if self.active_goal_index == self.n_goals - 1:
            self.active_goal_index = 0
        else:
            self.active_goal_index += 1

        for i,g in enumerate(self.goals):
            g.switch_to(i == self.active_goal_index)

        self.active_goal = [x for x in self.goals if x.is_active()][0]

    def _track_center(self):
        r0 = self.radars[0][1]
        r1 = self.radars[-1][1]
        return 1 - abs(r0 - r1) / abs(r0 + r1) if r0 + r1 > 0 else 0

    def has_crossed(self):
        has_crossed = any(self.car_rect.clipline(self.active_goal.get_line()))
        if has_crossed:
            self.activate_next()
        return has_crossed

    def move(self):
        # Get Rotated Sprite And Move Into The Right X-Direction
        # Don't Let The Car Go Closer Than 20px To The Edge
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], self.width - 120)
        self.car_rect.x = self.position[0]

        # Increase Distance and Time
        self.distance += self.speed

        # Same For Y-Position
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], self.width - 120)
        self.car_rect.y = self.position[1]

        # Calculate New Center
        self.center = [int(self.position[0]) + self.size_x / 2, int(self.position[1]) + self.size_y / 2]

        # Calculate Four Corners
        # Length Is Half The Side
        length = 0.5 * self.size_x
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]
    
    def update(self, game_map, choice):
        if not self.speed_set:
            self.speed = 1
            self.speed_set = True

        self.action(choice)
        self.move()
        has_crossed = self.has_crossed()
        if has_crossed:
            self.goals_crossed += 1
            self.last_time_crossed = 0
            print('CAR HAS CROSSED')
        else:
            #print('CAR HAS NOT CROSSED')
            self.last_time_crossed += 1
            #print(f'LTC: {self.last_time_crossed}')

        dp = DataPoint(self.position[0], self.position[1], self.speed, self.angle, choice)
        self.racing_data.append(dp)

        # Check Collisions And Clear Radars
        self.check_collision(game_map)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

        self.position_ref += self._track_center()

    def get_data(self):
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = radar[1]

        #return_values.append(self.speed)
        #return_values.append(self.angle)
        #return_values.append(self._track_center())
        return return_values

    def is_alive(self):
        return self.alive
    
    def distance_to_next_goal(self):
        p1 = np.array(self.active_goal.p1)
        p2 = np.array(self.active_goal.p2)
        p3 = np.array(self.center)
        
        return np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)

    def get_reward(self):
        #t_m = 1 if self.time is None else self.time
        #c_min = self.circuit.get_best_time(True)
        #c_max = self.circuit.get_best_time(False)
        #g_c = self.goals_crossed
        #g_t = self.n_goals
        #d = self.position_ref
        
        #d = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
        d = self.distance_to_next_goal()
        reward = 1 if d < self.d else -1
        self.d = d
        
        return reward

        #return g_c / g_t * (1 - abs(c_min - t_m * g_t / (g_c + 1)) / (c_max - c_min)) * d
        #return self.time * (self.goals_crossed / self.n_goals + self.position_ref)
        #return self.distance * self.goals_crossed / self.n_goals
        #return self.goals_crossed / self.n_goals * 100

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center

        return rotated_image
