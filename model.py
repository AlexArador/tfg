# This Code is Heavily Inspired By The YouTuber: Cheesy AI
# Code Changed, Optimized And Commented By: NeuralNine (Florian Dedov)

from car import Car
from racing_data import RacingLine
from circuit import Circuit

import sys
import neat
import pygame
import pickle
import os

FPS = 60

CIRCUIT = 'silverstone'
CIRCUIT_EXTENSION = 'png'

circuit = Circuit(CIRCUIT, CIRCUIT_EXTENSION)
circuit_chord = circuit.chord
print(f'La cuerda del circuito es de {circuit_chord} píxeles')
circuit_w, circuit_h = circuit.get_image_size()
print(f'Las dimensiones de la imagen del circuito son {circuit_w}x{circuit_h}')
print(f'La proporción de la imagen con la realidad del circuito es: {circuit.get_prop()}')

CAR_SIZE_X = 60
CAR_SIZE_Y = 30

current_generation = 0 # Generation counter

MODEL_PATH = 'models'
model_n = len(os.listdir(MODEL_PATH)) + 1
folder_name = f'model_{str(model_n)}'

def run_simulation(genomes, config):
    global circuit
    global folder_name
    global current_generation

    # Empty Collections For Nets and Cars
    nets = []
    cars = []
    
    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((circuit_w, circuit_h), pygame.RESIZABLE)
    
    # Clock Settings
    # Font Settings & Loading Map
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    
    game_map = pygame.image.load(circuit.file).convert() # Convert Speeds Up A Lot
    for goal in circuit.goals:
        goal.draw_goal(game_map)

    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car(circuit.start_position[0], circuit.start_position[1], circuit.start_angle, circuit_w, circuit.goals, circuit.get_prop()))

    current_generation += 1
    racing_line = RacingLine(current_generation)

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # Check If Car Is Still Alive
        # Increase Fitness If Yes And Break Loop If Not
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                # Get The Acton It Takes
                output = nets[i].activate(car.get_data())
                choice = output.index(max(output))
                still_alive += 1
                car.update(game_map, choice)
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

    if current_generation % 10 == 0:
        file = os.path.join(MODEL_PATH, folder_name, f'model_gen{current_generation}.pkl')
        with open(file, 'wb') as config_file:
            print(f'Saving model of generation {current_generation} in')
            pickle.dump(config, config_file)

        #with open('neat_genome.pkl', 'wb') as genome_file:
            #pickle.dump(genome, genome_file)

if __name__ == "__main__":
    execution = 'new' # PARAMETRIZE
    #execution = 'apply' # PARAMETRIZE

    generation = 10 # PARAMETRIZE

    model_folder = os.path.join(MODEL_PATH, folder_name)

    if execution == 'new':
        os.mkdir(model_folder)

    # Load Config
    CONFIG_PATH = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                CONFIG_PATH)

    if execution == 'new':
        # Create Population And Add Reporters
        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)

        # Run Simulation For A Maximum of 150 Generations
        population.run(run_simulation, 150)
        
        print(population.best_genome)
    elif execution == 'apply':
        model_file = os.path.join(model_folder, f'neeat_config_gen{generation}.pkl')
        with open(model_file, 'rb') as f:
            genome = pickle.load(f)

        # Crear una red neuronal a partir del genoma
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        # Aquí puedes utilizar la red neuronal (net) para hacer predicciones, realizar tareas, etc.
        # Por ejemplo:
        inputs = [1.0, 0.5, 0.2]  # Ejemplo de entrada
        outputs = net.activate(inputs)
        print("Salida de la red neuronal:", outputs)
