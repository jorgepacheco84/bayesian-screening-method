import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import seaborn as sns
sns.set()

SMALL_SIZE = 15
MEDIUM_SIZE = 15
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
#plt.rc('figure', titlesize=BIGGER_SIZE)  # fo


def plot():
    statistics = pd.read_csv('output/estimation-VE-ajusted-by-age-each-week.csv', index_col=0)
    week = statistics.index.unique()
    numberOfWeek = week[-1]
    sundayOfWeek = pd.date_range("2021-01-03", periods=numberOfWeek, freq="W")
    sturdayOfWeek = pd.date_range("2021-01-09", periods=numberOfWeek, freq="W")

    sundayOfWeek = pd.to_datetime(sundayOfWeek,  format="%Y-%m-%d").strftime("%d-%m-%y")
    sturdayOfWeek = pd.to_datetime(sturdayOfWeek,  format="%Y-%m-%d").strftime("%d-%m-%y")

    date = []
    for w in week:
        date.append(sundayOfWeek[w-1]+'\n'+sturdayOfWeek[w-1])

    typeOfEfficacity = ['casos', 'uci', 'def']

    dicSE = dict(zip(typeOfEfficacity,['cases','ICU','deaths']))
    fig, ax=plt.subplots(1,3,figsize=(25,10))
    fig.suptitle("Estimation of vaccine efficacy ajusted by age each epidemiological week in Chile", fontsize=20)
    for i in range(3):
        ax[i].scatter(date, statistics['median_'+typeOfEfficacity[i]], label='median')
        ax[i].set_title('Vaccine efficacy to prevent '+dicSE[typeOfEfficacity[i]]+' ajusted by age')
        ax[i].set_ylabel('Vaccine efficacy (%)')
        ax[i].set_xlabel('Epidemiological week')
        ax[i].set_ylim(0,100)
        labeled = False
        indexWeek = 0
        for w in week:
            label = 'CI(95%)' if labeled == False else ''
            labeled = True
            ax[i].axvline(x=date[indexWeek], ymin=statistics.loc[w,'lower_bound_'+typeOfEfficacity[i]]/100, ymax=statistics.loc[w,'upper_bound_'+typeOfEfficacity[i]]/100, label=label)
            indexWeek+=1
    plt.figtext(0.3, 0.01, "Elaboración a partir del base de datos abiertos COVID-19 de MinCiencia (Chile).", ha='right', fontsize=15)
    plt.legend()
    plt.savefig('output/plot-vaccine-efficacy.png')

if __name__ == "__main__":
    plot()