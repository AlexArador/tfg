import pandas as pd


df = pd.DataFrame([
    [1,1],
    [1,2],
    [1,3],
    [1,4]
    ], columns=['generation', 'car'])

print(df[['generation', 'car']])


print()