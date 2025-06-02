import fastf1 as f1
import numpy as np
import pandas as pd
import os
import pprint as pprint
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

laps_FP2 = laps_data.get('FP2')
if laps_FP2 is None:
    print(f"❌ FP2 data unavailable")

laps_FP3 = laps_data.get('FP3')
if laps_FP3 is None:
    print(f"❌ FP3 data unavailable")

# ---------------------------------- Average lap time for each compound ------------------------------------ #

# Function to calculate the avg time
def avg_lap_time(lap_df, driver, compound): 
    laps_driver = lap_df.pick_drivers([driver])
    compound_laps = laps_driver[(laps_driver['Compound'] == compound) & (laps_driver['IsAccurate'] == True)]

    if compound_laps.empty:
        return None
    else:
        return compound_laps['LapTime'].mean().total_seconds()

# Storing data in dictionary for FP1
if laps_FP1 is not None:
    compounds = laps_FP1['Compound'].unique()
    avg_time_by_compound_FP1 = {}

    for compound in compounds:
        avg_time_driver = {}
        for drv in laps_FP1['Driver'].unique():
            avg_time = avg_lap_time(laps_FP1, drv, compound)
            avg_time_driver[drv] = avg_time
        avg_time_by_compound_FP1[compound] = avg_time_driver

# Storing data in dictionary for FP2
if laps_FP2 is not None:
    compounds = laps_FP2['Compound'].unique()
    avg_time_by_compound_FP2 = {}
    for compound in compounds:
        avg_time_driver = {}
        for drv in laps_FP2['Driver'].unique():
            avg_time = avg_lap_time(laps_FP2, drv, compound)
            avg_time_driver[drv] = avg_time
        avg_time_by_compound_FP2[compound] = avg_time_driver

# Storing data in dictionary for FP3
if laps_FP3 is not None:
    compounds = laps_FP3['Compound'].unique()
    avg_time_by_compound_FP3 = {}
    for compound in compounds:
        avg_time_driver = {}
        for drv in laps_FP3['Driver'].unique():
            avg_time = avg_lap_time(laps_FP3, drv, compound)
            avg_time_driver[drv] = avg_time
        avg_time_by_compound_FP3[compound] = avg_time_driver

# ---------------------------------- Average Degradation for each compound ------------------------------------ #

#Function to calculate the avg degradation 
def avg_degradation(laps_df, driver, compound):
    driver_laps = laps_df.pick_drivers([driver])
    compound_laps = driver_laps[(driver_laps['Compound'] == compound) 
                                & (driver_laps['IsAccurate'] == True)
                                & (driver_laps['PitInTime'].isna()) 
                                & (driver_laps['LapTime'].notna())]
    if compound_laps.empty:
        return None
    degradation = []
    stints = compound_laps.groupby('Stint')
    for _, stint in stints:
        laps_in_stint = stint.sort_values('LapNumber')
        if len(laps_in_stint) < 3:
            continue
        first_lap = laps_in_stint['LapTime'].iloc[0].total_seconds()
        last_lap = laps_in_stint['LapTime'].iloc[-1].total_seconds()
        degr = (last_lap - first_lap) / (len(stint) - 1)
        if degr < 0 or degr > 2:
            continue
        degradation.append(degr)
    if degradation:
        return np.mean(degradation)
    else:
        return None

# Storing data in dictionary for FP1
if laps_FP1 is not None:
    compounds = laps_FP1['Compound'].unique()
    avg_degradation_by_compound_FP1 = {}
    for compound in compounds:
        avg_degradation_driver = {}
        for drv in laps_FP1['Driver'].unique():
            avg_deg = avg_degradation(laps_FP1, drv, compound)
            avg_degradation_driver[drv] = float(avg_deg) if avg_deg is not None else None
        avg_degradation_by_compound_FP1[compound] = avg_degradation_driver

# Storing data in dictionary for FP2
if laps_FP2 is not None:
    compounds = laps_FP2['Compound'].unique()
    avg_degradation_by_compound_FP2 = {}
    for compound in compounds:
        avg_degradation_driver = {}
        for drv in laps_FP2['Driver'].unique():
            avg_deg = avg_degradation(laps_FP2, drv, compound)
            avg_degradation_driver[drv] = float(avg_deg) if avg_deg is not None else None
        avg_degradation_by_compound_FP2[compound] = avg_degradation_driver

# Storing data in dictionary for FP3
if laps_FP3 is not None:
    compounds = laps_FP3['Compound'].unique()
    avg_degradation_by_compound_FP3 = {}
    for compound in compounds:
        avg_degradation_driver = {}
        for drv in laps_FP3['Driver'].unique():
            avg_deg = avg_degradation(laps_FP3, drv, compound)
            avg_degradation_driver[drv] = float(avg_deg) if avg_deg is not None else None
        avg_degradation_by_compound_FP3[compound] = avg_degradation_driver
pprint.pprint(avg_degradation_by_compound_FP3)