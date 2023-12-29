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

class Simulation:

    def __init__(self, circuit: Circuit, generation: int, genomes, cars, nets, config) -> None:
        pygame.init()
        self.circuit = circuit
        self.generation = generation
        self.racing_line = RacingLine(self.generation)
        self.genomes = genomes
        self.config = config

        self.clock = pygame.time.Clock()
        self.generation_font = pygame.font.SysFont('Arial', 30)
        self.alive_font = pygame.font.SysFont('Arial', 20)

        self.screen = pygame.display.set_mode((self.circuit.get_image_size()), pygame.RESIZABLE)
        self.game_map = pygame.image.load(self.circuit.file).convert()
        self.circuit_prop = self.circuit.get_prop()
        self.circuit_start_position = self.circuit.start_position
        for g in circuit.goals:
            g.draw_goal(self.game_map)

        self.cars = cars
        self.nets = nets
        self.counter = 0

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            still_alive = self.car_loop()
            if still_alive == 0:
                self.racing_line.dump()
                break
            
            self.counter += 1
            if self.counter == FPS * 20: # Stop After About 20 Seconds
                self.racing_line.dump()

            # Draw Map And All Cars That Are Alive
            self.screen.blit(self.game_map, (0, 0))
            for car in self.cars:
                if car.is_alive():
                    car.draw(self.screen)

            # Display Info
            text = self.generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (900, 450)
            self.screen.blit(text, text_rect)

            text = self.alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (900, 490)
            self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

        self.dump_model()

    def car_loop(self):
        still_alive = 0
        for i, car in enumerate(self.cars):
            if car.is_alive():
                # Get The Acton It Takes
                output = self.nets[i].activate(car.get_data())
                choice = output.index(max(output))
                still_alive += 1
                car.update(self.game_map, choice)
                self.genomes[i][1].fitness += car.get_reward()
            else:
                self.racing_line.get_data(i, car.racing_data)
        
        return still_alive
    
    def dump_model(self):
        global MODEL_PATH
        global folder_name

        if self.generation % 10 == 0:
            file = os.path.join(MODEL_PATH, folder_name, f'model_gen{self.generation}.pkl')
            with open(file, 'wb') as config_file:
                print(f'Saving model of generation {self.generation} in')
                pickle.dump(self.config, config_file)

            config_file.close()

    #def load_model(self, path, file):
        #with open(os.path.join(path, file), 'wb') as genome_file:
            #loaded_config = pickle.load(genome, genome_file)

        #genome_file.close()
        #return loaded_config

def run_simulation(genomes, config):
    global circuit
    global folder_name
    global current_generation
    
    nets = []
    cars = []
    
    simulation = Simulation(circuit, current_generation, genomes, cars, nets, config)
    
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car(circuit.start_position[0], circuit.start_position[1], circuit.start_angle, circuit_w, circuit.goals, circuit.get_prop()))

    current_generation += 1
    
    simulation.cars = cars
    simulation.nets = nets
    simulation.genomes = genomes

    simulation.main_loop()
    
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
        
        print('BEST GENOME:')
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
