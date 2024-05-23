#Combine my results with teammate's result(ML-Model-Cleaned.csv)
import pandas as pd

current = pd.read_csv('ML-Model-Cleaned.csv')
add = pd.read_csv('cleaned.csv')
current = current[(add.columns.tolist())]
combined = pd.concat([current, add], axis=0)
combined.to_csv('combined.csv', index=False)

