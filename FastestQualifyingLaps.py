import fastf1 as f1
import fastf1.plotting
from fastf1.core import Laps
import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import numpy as np
import os

def main():
    f1.Cache.enable_cache("C:\Windows\Temp")
    Year = 2022
    number_of_races = 22
    Type = "Q"
    for i in range(1, number_of_races+1):
        session = f1.get_session(Year,i, Type)
        session.load()
        drivers = pd.unique(session.laps["Driver"])
        try:
            fastest_laps = [session.laps.pick_driver(drv).pick_fastest(only_by_time = True) for drv in drivers]
        except:
            fastest_laps = [session.laps.pick_driver(drv).pick_fastest() for drv in drivers]
        fastest_laps = Laps(fastest_laps).sort_values(by = "LapTime").reset_index(drop = True)
        fastest_laps = fastest_laps[fastest_laps['Driver'].notna()]
        pole = fastest_laps.pick_fastest()
        fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole['LapTime']
        print(fastest_laps[['Driver','LapTime','LapTimeDelta']])
        team_colors = list()
        for index, lap in fastest_laps.iterlaps():
            color = fastf1.plotting.team_color(lap['Team'])
            team_colors.append(color)

        fig, ax = plt.subplots()
        ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],color= team_colors, edgecolor = 'grey')
        ax.set_yticks(fastest_laps.index)
        ax.set_yticklabels(fastest_laps['Driver'])
        ax.invert_yaxis()
        ax.set_axisbelow(True)
        plt.xlabel("Gap to pole [Seconds]")
        ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
        a = np.array(ax.get_xticks().tolist())/1000000000
        ax.set_xticklabels(a)
        lap_time_string = strftimedelta(pole['LapTime'], '%m:%s.%ms')
        plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n" 
                    f"Fastest lap: {lap_time_string} ({pole['Driver']})");

        newpath = f'{session.event.year}/Qualifying' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        plt.savefig(f'{session.event.year}/Qualifying/{session.event["EventName"]}.jpeg')

if __name__ == '__main__':
    main()