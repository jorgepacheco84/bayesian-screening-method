import pystan as ps
import multiprocessing
multiprocessing.set_start_method("fork", force=True)
import pandas as pd
import numpy as np
import arviz as az

from os import mkdir
from os import path


# parse data function
def parseData(data, typeOfEfficacy, week):
    dataW = data[data['semana_epidemiologica']==week]
    NAge = int(dataW['grupo_edad'].shape[0])
    NCases = (dataW[typeOfEfficacy+'Vac']+dataW[typeOfEfficacy+'NoVac']).values.astype(int)
    NCasesVaccinated = dataW[typeOfEfficacy+'Vac'].values.astype(int)
    N = (dataW['pobVac']+dataW['pobNoVac']).values
    NVaccinated = dataW['pobVac'].values
    return {'NAge':NAge,'NCases':NCases,'NCasesVaccinated':NCasesVaccinated,'N':N,'NVaccinated':NVaccinated }


def train():
    # compile in C++ stan model
    smStan = ps.StanModel(file="model.stan", verbose=True) #UNCOMMENT TO COMPILE IN C++

    # import data
    data = pd.read_csv('data/incidence-vaccinated-unvaccinated-by-age.csv')

    # training for each type of efficacy and each epidemiological week
    typeOfEfficacy= ['casos', 'uci', 'def']
    week = data['semana_epidemiologica'].unique().tolist()
    statistics = pd.DataFrame(index=week)
    statistics.index.name = 'semana_epidemiologica'

    for typeOf in typeOfEfficacy:
        for w in week:
            fit = smStan.sampling(data=parseData(data,typeOf, w), iter=10000, chains=4, warmup=5000,  seed=101, n_jobs=4)
            vaccineEfficacity = fit.extract()['VE']*100
            statistics.loc[w,['lower_bound_'+typeOf,'upper_bound_'+typeOf]] = az.hdi(vaccineEfficacity,hdi_prob=0.95) # bounds of higher distribution interval of the posterior
            statistics.loc[w,['median_'+typeOf]] = np.median(vaccineEfficacity) # median

    if not path.exists('output'):
        mkdir('output')
    statistics.to_csv('output/estimation-VE-ajusted-by-age-each-week.csv')


if __name__ == "__main__":
    train()