import fastf1 as f1
import numpy as np
import pandas as pd

cache = '/Users/arthavpatel/Desktop/race_outcome_prediction/f1_cache'
os.makedirs(cache, exist_ok=True)
f1.Cache.enable_cache(cache)