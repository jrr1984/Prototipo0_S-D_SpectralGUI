import pandas as pd

# Reading out just the data lines and storing into a pandas dataframe should work with this:
df = pd.read_csv('xy_positions_FULL50micron.csv', skiprows=231)
df.to_csv('xy_positions_FULL50micron.csv', index=False)



