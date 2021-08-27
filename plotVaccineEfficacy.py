import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import seaborn as sns
sns.set()

import argparse

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


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--splitVariable", help="""Plot by epidemiological week or by age""")
    return parser.parse_args()

def plot(split):
    statistics = pd.read_csv('output/estimation-VE-by-'+split+'.csv', index_col=0)
    keys = statistics.index.unique()

    typeOfEfficacity = ['cases', 'icu', 'deaths']
    title ={'epidemiologicalWeek':'epidemiological week', 'ageGroup':'age group'}
    dicSE = dict(zip(typeOfEfficacity,['cases','ICU','deaths']))
    fig, ax=plt.subplots(1,3,figsize=(25,10))
    fig.suptitle("Estimation of vaccine efficacy by "+ title[split] +" in Chile", fontsize=20)
    for i in range(3):
        ax[i].scatter(keys, statistics[typeOfEfficacity[i]+'_VE_median'], label='median')
        ax[i].set_title('Vaccine efficacy to prevent '+dicSE[typeOfEfficacity[i]]+' by ' +title[split])
        ax[i].set_ylabel('Vaccine efficacy (%)')
        ax[i].set_xlabel(title[split])
        ax[i].set_ylim(0,100)
        labeled = False
        indexWeek = 0
        for k in keys:
            label = 'CI(95%)' if labeled == False else ''
            labeled = True
            ax[i].axvline(x=k, ymin=statistics.loc[k,typeOfEfficacity[i]+'_VE_lower_bound']/100, ymax=statistics.loc[k,typeOfEfficacity[i]+'_VE_upper_bound']/100, label=label)
            indexWeek+=1
    plt.figtext(0, 0.01, "Esimation with a bayesian screening method only ajusted by age with open data from the Science Ministery of Chile. Github repository for more information: https://github.com/AntoineBraultChile/bayesian-screening-method.", ha='left', fontsize=12, color='grey')

    plt.legend()
    plt.savefig('output/plot-vaccine-efficacy-by-'+split+'.png')

if __name__ == "__main__":
    args = parse_arguments()
    plot(args.splitVariable)