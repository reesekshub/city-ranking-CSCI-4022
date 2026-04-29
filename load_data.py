import pandas as pd
import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt

def load_comparison_data(time_diff_dir):
    csv_files = sorted(Path(time_diff_dir).glob('*.csv'))
    rows = {}
    for csv_file in csv_files:
        city = csv_file.stem[:csv_file.stem.find('_delta')-3]
        city_df = pd.read_csv(csv_file)
        key_col = city_df.columns[0]

        # flatten the city_df so each city becomes a row and each origin->destination pair becomes a column
        series = city_df.set_index(key_col).stack()
        series.index = [f"{row}->{col}" for row, col in series.index]
        rows[city] = pd.to_numeric(series)

    df = pd.DataFrame.from_dict(rows, orient='index')
    df.index.name = 'city'
    if 'home->home' in df.columns:
        df.drop(columns=['home->home'], inplace=True)
    return df