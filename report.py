import os
import pandas as pd

def generate_report():
    BASE_PATH = 'models'
    OUTPUT_PATH = os.path.join('data', 'models')

    MODEL_PREFIX = 'model_'
    GENERATION_PREFIX = 'gen'
    GENERATION_SUFFIX = '.csv'

    models = [[x.replace(MODEL_PREFIX, ''), x, os.path.join(BASE_PATH, x)] for x in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, x))]

    df_models = pd.DataFrame(models, columns=['key', 'model', 'path'])

    generations = []
    for i,row in df_models.iterrows():
        model_path = row['path']
        model_id = row['key']

        generation_path = os.path.join(model_path, 'racing_data')

        generations.extend([[model_id, x.replace(GENERATION_PREFIX, '').replace(GENERATION_SUFFIX, ''), x, os.path.join(generation_path, x)] for x in os.listdir(generation_path)])

    df_generations = pd.DataFrame(generations, columns=['model', 'generation', 'key', 'path'])

    df_models.to_csv(os.path.join(OUTPUT_PATH, 'models.csv'), index=False, header=True)
    df_generations.to_csv(os.path.join(OUTPUT_PATH, 'generations.csv'), index=False, header=True)

generate_report()