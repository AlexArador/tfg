from car import Car
from racing_data import RacingLine
from circuit import Circuit

import sys
import neat
import pygame
import pickle
import os

FPS = 60
TIME_LIMIT = 10 # SECONDS

TICK_LIMIT = FPS * TIME_LIMIT

CIRCUIT = 'silverstone'
CIRCUIT_EXTENSION = 'png'

circuit = Circuit(CIRCUIT, CIRCUIT_EXTENSION)
circuit_chord = circuit.chord
print(f'La longitud del circuito es de {circuit.length}')
print(f'La cuerda del circuito es de {circuit_chord} píxeles')
circuit_w, circuit_h = circuit.get_image_size()
print(f'Las dimensiones de la imagen del circuito son {circuit_w}x{circuit_h}')
print(f'La proporción de la imagen con la realidad del circuito es: {circuit.get_prop()}')

current_generation = 0 # Generation counter

MODEL_PATH = 'models'

class Simulation:

    def __init__(self, circuit: Circuit, generation: int, genomes, cars, nets, config) -> None:
        pygame.init()
        self.circuit = circuit
        self.generation = generation
        self.racing_line = RacingLine(self.generation)
        self.genomes = genomes
        self.config = config

        self.single_genome = not type(self.genomes) is list

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

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            still_alive = self.car_loop()
            if still_alive == 0:
                self.racing_line.dump()
                break
            else:
                ltc = [c.last_time_crossed for c in self.cars if c.is_alive()]
                if len(ltc) == 0 or min(ltc) >= TICK_LIMIT:
                    print(ltc)
                    self.racing_line.dump()
                    break

            # Draw Map And All Cars That Are Alive
            self.screen.blit(self.game_map, (0, 0))
            for car in self.cars:
                if car.is_alive():
                    car.draw(self.screen)

            # Display Info
            text = self.generation_font.render(f'Generation: {str(current_generation)}', True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (900, 450)
            self.screen.blit(text, text_rect)

            text = self.alive_font.render(f'Still Alive: {str(still_alive)}', True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (900, 490)
            self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

    def car_loop(self):
        still_alive = 0
        for i, car in enumerate(self.cars):
            if car.is_alive():
                # Get The Acton It Takes
                output = self.nets[i].activate(car.get_data())
                choice = output.index(max(output))
                still_alive += 1
                car.update(self.game_map, choice)
                if not self.single_genome:
                    self.genomes[i][1].fitness += car.get_reward()
            else:
                self.racing_line.get_data(i, car.racing_data)

        return still_alive

def run(genomes, config):
    global circuit
    global current_generation

    nets = []
    cars = []

    simulation = Simulation(circuit, current_generation, genomes, cars, nets, config)

    sp_0 = circuit.start_position[0]
    sp_1 = circuit.start_position[1]
    prop = circuit.get_prop()

    if type(genomes) is list:
        for i, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0

            cars.append(Car(sp_0, sp_1, circuit.start_angle, circuit_w, circuit.goals, prop))
    else:
        net = neat.nn.FeedForwardNetwork.create(genomes, config)
        nets.append(net)
        cars.append(Car(sp_0, sp_1, circuit.start_angle, circuit_w, circuit.goals, prop))

    current_generation += 1
    simulation.cars = cars
    simulation.nets = nets
    simulation.genomes = genomes

    simulation.main_loop()

def execute(execution: str, config_path: str, checkpoint_prefix: str, model_n: int = 1, load_checkpoint: int = None, generations: int = 150, checkpoint: int = 10):
    global current_generation
    
    if execution not in ['new', 'restore', 'deploy']:
        print(f'Provided _execution_ value is not valid: {execution}')
        return

    if execution in ['restore', 'deploy']:
        if len(os.listdir(MODEL_PATH)) < model_n:
            print(f'Provided model does not exist. Last model is: {model_n}')
            return
        else:
            if execution == 'deploy':
                if not os.path.exists(os.path.join(MODEL_PATH, f'model_{str(model_n)}', 'genome.pkl')):
                    print(f'Selected model did not end the training')
                    return
            if execution == 'restore':
                if os.path.exists(os.path.join(MODEL_PATH, f'model_{str(model_n)}')):
                    if not os.path.exists(os.path.join(MODEL_PATH, f'model_path{str(model_n)}', checkpoint_prefix, str(load_checkpoint))):
                        print(f'Selected checkpoint ({load_checkpoint}) to load does not exist')
                        checkpoints = os.listdir(os.path.join(MODEL_PATH, f'model_{str(model_n)}'))
                        load_checkpoint = max([int(x.replace(checkpoint_prefix, '')) for x in checkpoints if checkpoint_prefix in x])
                        print(f'New selected load checkpoint: {load_checkpoint}')
                        current_generation = load_checkpoint
                else:
                    print(f'Selected model does not exist')
                    return

    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    if execution in ['new', 'restore']:
        if execution == 'new':
            model_n = len(os.listdir(MODEL_PATH)) + 1
        elif execution == 'restore':
            model_n = 1 # PARAMETRIZE
            checkpoint = 9 # PARAMETRIZE

        folder_name = f'model_{str(model_n)}'
        model_folder = os.path.join(MODEL_PATH, folder_name)

        checkpointer = neat.Checkpointer(checkpoint, filename_prefix=os.path.join(model_folder, checkpoint_prefix))
        stats = neat.StatisticsReporter()

        if execution == 'new':
            os.mkdir(model_folder)
            population = neat.Population(config)
        elif execution == 'restore':
            checkpoint_path = os.path.join(model_folder, f'{CHECKPOINT_PREFIX}{checkpoint}')
            population = checkpointer.restore_checkpoint(checkpoint_path)
            generations -= checkpoint

        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(stats)
        population.add_reporter(checkpointer)

        population.run(run, generations)

        with open(os.path.join(model_folder, 'genome.pkl'), 'wb') as genome_file:
            pickle.dump(stats.best_genome(), genome_file)
    elif execution == 'deploy':
        folder_name = f'model_{str(model_n)}'
        genome_file = os.path.join(MODEL_PATH, folder_name, 'genome.pkl')

        # Cargar el genoma desde el archivo
        with open(genome_file, 'rb') as f:
            genome = pickle.load(f)

        run(genome, config)

if __name__ == "__main__":
    CONFIG_PATH = 'config.txt'
    CHECKPOINT_PREFIX = 'checkpoint-gen-'

    generations = 100 # PARAMETRIZE
    checkpoint = 5 # PARAMETRIZE
    model_n = 21 # PARAMETRIZE
    load_checkpoint = 99 # PARAMETRIZE

    execution = 'new' # PARAMETRIZE
    execution = 'restore' # PARAMETRIZE
    execution = 'deploy' # PARAMETRIZE

    execute(execution, CONFIG_PATH, CHECKPOINT_PREFIX, model_n, load_checkpoint, generations, checkpoint)
