import fastf1 as f1
import numpy as np
import pandas as pd
import os

cache = '/Users/arthavpatel/Desktop/race_outcome_prediction/f1_cache'
os.makedirs(cache, exist_ok=True)
f1.Cache.enable_cache(cache)

# ---------------------------------- Loading the Grand Prix ------------------------------------ #

grand_prix_name = 'Spanish Grand Prix'
year = 2025
practice_sessions = ['FP1', 'FP2', 'FP3']
laps_data = {}

for session_name in practice_sessions:
    try:
        session = f1.get_session(year, grand_prix_name, session_name)
        session.load()
        laps_data[session_name] = session.laps
    except Exception as e:
        print(f"❌ {session_name} is unavailable: {e}")

laps_FP1 = laps_data.get('FP1')
if laps_FP1 is None:
    print(f"❌ FP1 data unavailable")


