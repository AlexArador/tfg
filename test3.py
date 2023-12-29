import neat
import os

# Configuración del modelo
config_path = 'config.txt'
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

# Directorio para guardar checkpoints
checkpoint_dir = 'models'

# Crear un población y un Checkpointer
p = neat.Population(config)
checkpointer = neat.Checkpointer()

# Bucle de evolución
for generation in range(100):  # Por ejemplo, realiza 100 generaciones
    # Ejecutar una generación de la evolución
    genomes = p.run(lambda genomes, generation: None, 1)

    # Guardar el estado de la evolución en un archivo de checkpoint
    checkpointer.save_checkpoint(checkpoint_dir, genomes, config, generation)

# Finalizar la evolución
p.stop()

# Nota: Puedes usar checkpointer.restore_checkpoint() para cargar el estado desde un checkpoint si es necesario.
