import pystan as ps
import multiprocessing
multiprocessing.set_start_method("fork", force=True)
import pandas as pd
import numpy as np
import arviz as az

from os import mkdir
from os import path


# parse data function
def parseData(data, typeOfEfficacy):
    # dataW = data[data['epidemiologicalWeek']==week]
    NAge = int(data['ageGroup'].shape[0])
    NCases = (data[typeOfEfficacy+'Vaccinated']+data[typeOfEfficacy+'NoVaccinated']).values.astype(int)
    NCasesVaccinated = data[typeOfEfficacy+'Vaccinated'].values.astype(int)
    N = (data['populationVaccinated']+data['populationNoVaccinated']).values
    NVaccinated = data['populationVaccinated'].values
    return {'NAge':NAge,'NCases':NCases,'NCasesVaccinated':NCasesVaccinated,'N':N,'NVaccinated':NVaccinated}

# split data set with respect to a variable
def splitData(data, splitVariable):
    if(splitVariable == 'epidemiologicalWeek'):
        week = data['epidemiologicalWeek'].unique()
        listOfDataBySplit = {}
        for w in week:
            listOfDataBySplit[w] = data[data['epidemiologicalWeek']==w]

    elif(splitVariable == 'ageGroup'):
        young = [ '21 - 30 años', '31 - 40 años', '41 - 50 años',
       '51 - 60 años', '61 - 70 años']
        old = ['71 - 80 años', '80 años o más']
        listOfDataBySplit = {'21-70': data[data['ageGroup'].isin(young)], '>70': data[data['ageGroup'].isin(old)]}

    return listOfDataBySplit


def train():
    # compile in C++ stan model
    smStan = ps.StanModel(file="model.stan", verbose=True) #UNCOMMENT TO COMPILE IN C++

    # import data
    data = pd.read_csv('data/incidence-vaccinated-unvaccinated-by-age.csv')

    # # training for each type of efficacy and each epidemiological week
    # if(splitVariable =='epidemiologicalWeek'):
    #     split = data['epidemiologicalWeek'].unique().tolist()
    #     statistics = pd.DataFrame(index=split)
    #     statistics.index.name = 'epidemiologicalWeek'
    # else if(splitVariable =='ageGroup'):


    splitVariables = ['epidemiologicalWeek', 'ageGroup']

    for split in splitVariables:
        dataList= splitData(data,split)
        keys = dataList.keys()
        statistics = pd.DataFrame(index=keys)
        typeOfEfficacy= ['cases', 'icu', 'deaths']
        for k in keys:
            for typeOf in typeOfEfficacy:
                fit = smStan.sampling(data=parseData(dataList[k],typeOf), iter=10000, chains=4, warmup=5000,  seed=101, n_jobs=4)
                vaccineEfficacity = fit.extract()['VE']*100
                statistics.loc[k,[typeOf+'_VE_lower_bound',typeOf+'_VE_upper_bound']] = az.hdi(vaccineEfficacity,hdi_prob=0.95) # bounds of higher distribution interval of the posterior
                statistics.loc[k,[typeOf+'_VE_median']] = np.median(vaccineEfficacity) # median

        if not path.exists('output'):
            mkdir('output')
        statistics.to_csv('output/estimation-VE-by-'+split+'.csv')


if __name__ == "__main__":
    train()