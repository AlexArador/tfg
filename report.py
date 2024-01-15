import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

from circuit import Circuit

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
    
def get_driver_pic(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        obj = soup.find(class_='infobox')

        if obj:
            first_image = obj.find('img')
            if first_image:
                return first_image['src']
            else:
                print(f'No image found within the object for URL {url}')
        else:
            print(f'No object found with the provided class for URL {url}')
    else:
        print(f'Error processing the request to the provided URL: {url}')

def export_drivers():
    BASE_PATH = 'data'
    FILE_NAME = 'drivers.csv'
    df = pd.read_csv(os.path.join(BASE_PATH, 'raw', FILE_NAME))
    
    drivers_list = list(set(pd.read_csv(os.path.join('data', 'circuits', 'times.csv'))['driverId'].tolist()))
    df = df[df['driverId'].isin(drivers_list)]

    df['name'] = df.apply(lambda x: x['forename'] + ' ' + x['surname'], axis=1)
    df['picture'] = df['url'].apply(lambda x: get_driver_pic(x))

    df = df[['driverId', 'code', 'number', 'name', 'picture']]

    df.to_csv(os.path.join(BASE_PATH, FILE_NAME), index=False, header=True)

    print(df.head())
    
def export_races():
    BASE_PATH = 'data'
    FILE_NAME = 'races.csv'
    
    df = pd.read_csv(os.path.join(BASE_PATH, 'raw', FILE_NAME))
    df = df[['raceId', 'circuitId', 'date']]
    
    df.to_csv(os.path.join(BASE_PATH, FILE_NAME), header=True, index=False)

#generate_report()
Circuit.get_laptimes()
Circuit.get_circuits()
export_drivers()
export_races()