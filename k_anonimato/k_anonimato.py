import numpy as np
import pandas as pd

df = pd.read_csv('salario.csv')
df.head().groupby("pais").mean()
