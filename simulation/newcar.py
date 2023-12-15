# This Code is Heavily Inspired By The YouTuber: Cheesy AI
# Code Changed, Optimized And Commented By: NeuralNine (Florian Dedov)

from car import Car
from racing_line import RacingLine
from circuit import Circuit,Goal

import math
import random
import sys
import os

import neat
import pygame
import cv2

FPS = 60

# MAP2
START_POSITION = [830, 920]
START_POSITION2 = [831, 920]
CIRCUIT = 'map2'
CIRCUIT_EXTENSION = 'png'

# SILVERSTONE
#START_POSITION = [1258, 1054]
#START_POSITION2 = [1175, 998]
#CIRCUIT = 'silverstone.png'

#AFTER COPSE
#START_POSITION = [570, 179]
#START_POSITION2 = [615, 171]

im = cv2.imread(f'{CIRCUIT}.{CIRCUIT_EXTENSION}')
HEIGHT, WIDTH, CHANNEL = im.shape
SP_X = START_POSITION[0]
SP_Y = START_POSITION[1]

#RUSSIA

CAR_SIZE_X = 30
CAR_SIZE_Y = 30

def calculate_angle(point1, point2):
    x = point2[0] - point1[0]
    y = point1[1] - point2[1]

    h = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    cos = x / h
    return math.degrees(math.acos(cos))

ANGLE = calculate_angle(START_POSITION, START_POSITION2)
print(f'Angle: {ANGLE}')

current_generation = 0 # Generation counter

def run_simulation(genomes, config):
    circuit = Circuit(CIRCUIT, CIRCUIT_EXTENSION)
    
    # Empty Collections For Nets and Cars
    nets = []
    cars = []

    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car(CAR_SIZE_X, CAR_SIZE_Y, START_POSITION[0], START_POSITION[1], ANGLE, WIDTH, circuit.goals))

    # Clock Settings
    # Font Settings & Loading Map
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    
    game_map = pygame.image.load(circuit.file).convert() # Convert Speeds Up A Lot
    for goal in circuit.goals:
        pygame.draw.line(game_map, goal.get_color(), goal.p1, goal.p2, goal.width)

    global current_generation
    current_generation += 1
    racing_line = RacingLine(current_generation)

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For Each Car Get The Acton It Takes
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            car.action(choice)

        # Check If Car Is Still Alive
        # Increase Fitness If Yes And Break Loop If Not
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()
            else:
                racing_line.get_data(i, car.racing_data)

        if still_alive == 0:
            racing_line.dump()
            break

        counter += 1
        if counter == FPS * 20: # Stop After About 20 Seconds
            racing_line.dump()
            break

        # Draw Map And All Cars That Are Alive
        screen.blit(game_map, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)

        # Display Info
        text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    
    # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 150 Generations
    population.run(run_simulation, 150)
