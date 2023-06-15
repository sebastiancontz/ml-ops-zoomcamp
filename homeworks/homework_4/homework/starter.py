#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import numpy as np
import sys

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

year = int(sys.argv[1])
month = int(sys.argv[2])

input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
output_file = f'./outputs/preds_yellow_tripdata_{year:04d}-{month:02d}.parquet'

df = read_data(input_file)
dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

print("preds std:", np.round(np.std(y_pred), 2))
print("preds mean:", np.round(np.mean(y_pred), 2))

df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
df["predicted_duration"] = y_pred
df_result = df[["ride_id", "predicted_duration"]].copy()

df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)

