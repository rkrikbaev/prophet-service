#!/usr/bin/python3

import os

r, w = os.pipe()

with os.fdopen(r, "rb") as rf:
   content = rf.readline()

   print(content)

str=b'{ "metadata": {"point": "shym-2", "type": "prophet","settings": {"growth": "linear","changepoint_prior_scale": 30,"seasonality_prior_scale": 35,"interval_width": 0.98, "daily_seasonality": false,"weekly_seasonality": false,"yearly_seasonality": false,"seasonality": [{"name": "hour","period": 0.0417,"fourier_order": 5}]}},"history": [[1626159114000, 46.46659429239697, 33.865], [1626162714000, 50.38077545566983, 33.135], [1626166314000, 49.786295583493974, 33.0]], "future": [[1626321114000, 19.27],[1626321115000, 19.27],[1626321116000, 66.1]]}\n'

with os.fdopen(w, "wb") as wf:
   t = wf.write(str,"utf-8")

   print(t)

"""
import json

JSON = '''{
    "metadata": {
        "containerId": "16354ed4eeaa5eb42169c153b731a56eea09dc450476ef101c57090fcb3afe7d",
        "point": "shym-2",
        "start_time": "2021-10-20 10:38:37.518264",
        "finish_time": "2021-10-20 10:39:22.661520"
    },
    "prediction": [
        26.440550333303296,
        27.934360447781003,
        21.55088396636851
    ]
}'''
JSON = JSON.replace("\n", "") + "\n"
data = os.read(3, 10000)
os.write(4, bytes(JSON, "utf-8"))

#print(JSON)
#obj = json.loads(JSON)
#print(obj)
"""