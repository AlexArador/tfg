import pickle
import neat

# Supongamos que 'config' es tu configuración NEAT y 'genome' es tu modelo NEAT
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation, 'config-feedforward')
genome = neat.DefaultGenome(1)  # Ejemplo, debes tener tu propio genoma

# Guardar configuración y modelo
with open('neat_config.pkl', 'wb') as config_file, open('neat_genome.pkl', 'wb') as genome_file:
    pickle.dump(config, config_file)
    pickle.dump(genome, genome_file)


import pickle
import neat

# Cargar configuración y modelo
with open('neat_config.pkl', 'rb') as config_file, open('neat_genome.pkl', 'rb') as genome_file:
    loaded_config = pickle.load(config_file)
    loaded_genome = pickle.load(genome_file)

# Crear el modelo NEAT
neat_model = neat.nn.FeedForwardNetwork.create(loaded_genome, loaded_config)
