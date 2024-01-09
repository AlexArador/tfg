from car import Car
from racing_data import RacingLine
from circuit import Circuit

import sys
import neat
import pygame
import pickle
import os

class Simulation:
    def __init__(self, circuit: Circuit, generation: int, genomes, cars, nets, config, model_n, current_generation: int = 0, fps: int = 60, time_limit: int = 5) -> None:
        pygame.init()
        self.circuit = circuit
        self.generation = generation
        self.racing_line = RacingLine(os.path.join('models', f'model_{str(model_n)}', 'racing_data'), self.generation)
        self.genomes = genomes
        self.config = config
        self.fps = fps
        self.time_limit = time_limit

        self.tick_limit = self.fps * self.time_limit

        print(f'Tick limit: {self.tick_limit}')

        self.single_genome = not type(self.genomes) is list

        self.clock = pygame.time.Clock()
        self.generation_font = pygame.font.SysFont('Arial', 30)
        self.alive_font = pygame.font.SysFont('Arial', 20)

        self.screen = pygame.display.set_mode((self.circuit.get_image_size()), pygame.RESIZABLE)
        self.game_map = pygame.image.load(self.circuit.file).convert()
        self.circuit_prop = self.circuit.get_prop()
        self.circuit_start_position = self.circuit.start_position
        for g in self.circuit.goals:
            g.draw_goal(self.game_map)

        self.cars = cars
        self.nets = nets
        self.current_generation = current_generation
        self.current_time = 0
        self.start_time = 0

    def main_loop(self):
        self.start_time = pygame.time.get_ticks() / 1000
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            still_alive = self.car_loop()
            if still_alive == 0:
                self.racing_line.dump()
                self.start_time = pygame.time.get_ticks()
                break

            # Draw Map And All Cars That Are Alive
            self.screen.blit(self.game_map, (0, 0))
            for car in self.cars:
                if car.is_alive():
                    car.draw(self.screen)

            # Display Info
            text = self.generation_font.render(f'Generation: {str(self.current_generation)}', True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (900, 450)
            self.screen.blit(text, text_rect)

            text = self.alive_font.render(f'Still Alive: {str(still_alive)}', True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (900, 490)
            self.screen.blit(text, text_rect)

            self.current_time = pygame.time.get_ticks() / 1000
            text = self.alive_font.render(f"Tiempo: {RacingLine.convert_time(self.current_time - self.start_time)}", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (900, 1000)
            self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(self.fps)

    def car_loop(self):
        still_alive = 0
        for i, car in enumerate(self.cars):
            if car.is_alive():
                if car.last_time_crossed < self.tick_limit:
                    output = self.nets[i].activate(car.get_data())
                    #print(output)
                    choice = output.index(max(output))
                    still_alive += 1
                    car.update(self.game_map, choice)
                    if not self.single_genome:
                        self.genomes[i][1].fitness += car.get_reward()
                else:
                    car.alive = False
            else:
                car.alive = False
                car.set_time(self.current_time - self.start_time)
                self.racing_line.get_data(i, car.racing_data)

        return still_alive

class Model:
    CONFIG_PATH = 'config.txt'
    CHECKPOINT_PREFIX = 'checkpoint-gen-'
    MODEL_PATH = 'models'

    #def __init__(self, circuits: list[Circuit], change_every, current_generation: int = 0, model_path = 'models', config_path: str = 'config.txt', checkpoint_prefix: str = 'checkpoint-gen-') -> None:
    def __init__(self, circuit: Circuit, current_generation: int = 0, model_path = 'models', config_path: str = 'config.txt', checkpoint_prefix: str = 'checkpoint-gen-') -> None:
        #self.circuits = circuits
        self.circuit = circuit
        self.current_generation = current_generation
        #self.current_circuit = 0
        #self.generation_stint = 0

        #self.change_every = change_every

        self.MODEL_PATH = model_path
        self.CONFIG_PATH = config_path
        self.CHECKPOINT_PREFIX = checkpoint_prefix
        
        #self.circuit = self.circuits[0]
        
        self.prop = self.circuit.get_prop()
        self.circuit_w, self.circuit_h = self.circuit.get_image_size()
        self.circuit_l = self.circuit._get_length()
        self.circuit_c = self.circuit._get_chord()
        self.sp_0 = self.circuit.start_position[0]
        self.sp_1 = self.circuit.start_position[1]

        self.model_n = 0

    def update_circuit(self):
        self.circuit = self.circuits[self.current_circuit]

        self.prop = self.circuit.get_prop()
        self.circuit_w, self.circuit_h = self.circuit.get_image_size()
        self.circuit_l = self.circuit._get_length()
        self.circuit_c = self.circuit._get_chord()
        self.sp_0 = self.circuit.start_position[0]
        self.sp_1 = self.circuit.start_position[1]

    def change_circuit(self):
        if self.current_circuit == len(self.circuits) - 1:
            self.current_circuit = 0
        else:
            self.current_circuit += 1
            
        self.update_circuit()

    def run(self, genomes, config):
        nets = []
        cars = []
        
        #if self.generation_stint == self.change_every:
        #    self.generation_stint = 0
        #    self.change_circuit()
        #else:
        #    self.generation_stint += 1

        simulation = Simulation(self.circuit, self.current_generation, genomes, cars, nets, config, self.model_n)

        if type(genomes) is list:
            for i, g in genomes:
                net = neat.nn.FeedForwardNetwork.create(g, config)
                nets.append(net)
                g.fitness = 0

                cars.append(Car(self.sp_0, self.sp_1, self.circuit.start_angle, self.circuit_w, self.circuit.goals, self.prop, self.circuit, self.circuit_l, self.circuit_c))
        else:
            net = neat.nn.FeedForwardNetwork.create(genomes, config)
            nets.append(net)
            cars.append(Car(self.sp_0, self.sp_1, self.circuit.start_angle, self.circuit_w, self.circuit.goals, self.prop, self.circuit, self.circuit_l, self.circuit_c))
            
        print(f'Number of cars: {len(cars)}')

        self.current_generation += 1
        simulation.current_generation = self.current_generation
        simulation.cars = cars
        simulation.nets = nets
        simulation.genomes = genomes

        simulation.main_loop()
        
    def validate_execution(self, execution, model_n, load_checkpoint):
        if execution not in ['new', 'restore', 'deploy']:
            print(f'Provided _execution_ value is not valid: {execution}')
            return False

        if execution in ['restore', 'deploy']:
            if len(os.listdir(self.MODEL_PATH)) < model_n:
                print(f'Provided model does not exist. Last model is: {model_n}')
                return False
            else:
                model_path = os.path.join(self.MODEL_PATH, f'model_{str(model_n)}')
                if execution == 'deploy':
                    if not os.path.exists(os.path.join(model_path, 'genome.pkl')):
                        print(f'Selected model ({model_n}) did not end the training')
                        return False
                if execution == 'restore':
                    if os.path.exists(model_path):
                        if not os.path.exists(os.path.join(model_path, f'{self.CHECKPOINT_PREFIX}{str(load_checkpoint)}')):
                            print(f'Selected checkpoint ({load_checkpoint}) to load does not exist')
                            checkpoints = os.listdir(model_path)
                            load_checkpoint = max([int(x.replace(self.CHECKPOINT_PREFIX, '')) for x in checkpoints if self.CHECKPOINT_PREFIX in x])
                            print(f'New selected load checkpoint: {load_checkpoint}')
                            self.current_generation = load_checkpoint
                    else:
                        print(f'Selected model ({model_n}) does not exist')
                        return False
                    
        return True
        

    def execute(self, execution: str, model_n: int = 1, load_checkpoint: int = None, generations: int = 150, checkpoint: int = 10):
        self.validate_execution(execution, model_n, load_checkpoint)

        config = neat.config.Config(neat.DefaultGenome,
                                    neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation,
                                    self.CONFIG_PATH)

        if execution in ['new', 'restore']:
            if execution == 'new':
                model_n = len(os.listdir(self.MODEL_PATH)) + 1

            folder_name = f'model_{str(model_n)}'
            model_folder = os.path.join(self.MODEL_PATH, folder_name)
            checkpointer = neat.Checkpointer(checkpoint, filename_prefix=os.path.join(model_folder, self.CHECKPOINT_PREFIX))
            stats = neat.StatisticsReporter()

            if execution == 'new':
                os.mkdir(model_folder)
                population = neat.Population(config)
            elif execution == 'restore':
                checkpoint_path = os.path.join(model_folder, f'{self.CHECKPOINT_PREFIX}{load_checkpoint}')
                population = checkpointer.restore_checkpoint(checkpoint_path)
                generations -= checkpoint

            self.model_n = model_n

            population.add_reporter(neat.StdOutReporter(True))
            population.add_reporter(stats)
            population.add_reporter(checkpointer)

            population.run(self.run, generations)

            with open(os.path.join(model_folder, 'genome.pkl'), 'wb') as genome_file:
                pickle.dump(stats.best_genome(), genome_file)
        elif execution == 'deploy':
            folder_name = f'model_{str(model_n)}'
            genome_file = os.path.join(self.MODEL_PATH, folder_name, 'genome.pkl')

            # Cargar el genoma desde el archivo
            with open(genome_file, 'rb') as f:
                genome = pickle.load(f)

            self.run(genome, config)

if __name__ == "__main__":
    generations = 30 # PARAMETRIZE
    checkpoint = 5 # PARAMETRIZE
    model_n = 31 # PARAMETRIZE
    load_checkpoint = 58 # PARAMETRIZE

    execution = 'new' # PARAMETRIZE
    #execution = 'restore' # PARAMETRIZE
    #execution = 'deploy' # PARAMETRIZE
    
    change_every = 2
    
    circuits = [
        Circuit('silverstone', 'png'),
        Circuit('albert_park', 'png')
    ]

    m = Model(circuits[0], 0)
    m.execute(execution, model_n, load_checkpoint, generations, checkpoint)
