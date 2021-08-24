import pandas as pd
from os import mkdir
from os import path

def downloadData():
    incidenceByAge = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto89/incidencia_en_vacunados_edad.csv')
    completeVaccination = incidenceByAge[(incidenceByAge['estado_vacunacion']=='con esquema completo') & (incidenceByAge['grupo_edad']!='Total')][['semana_epidemiologica', 'grupo_edad','casos_confirmados', 'casos_uci', 'casos_def', 'poblacion']] 
    unCompleteVaccination = incidenceByAge[(incidenceByAge['estado_vacunacion']=='sin esquema completo') & (incidenceByAge['grupo_edad']!='Total')][['semana_epidemiologica', 'grupo_edad','casos_confirmados', 'casos_uci', 'casos_def', 'poblacion']] 
    data = completeVaccination.rename(columns={'semana_epidemiologica':'epidemiologicalWeek','grupo_edad':'ageGroup', 'casos_confirmados':'casesVaccinated', 'casos_uci':'icuVaccinated', 'casos_def':'deathsVaccinated', 'poblacion':'populationVaccinated'})
    data[['casesNoVaccinated','icuNoVaccinated','deathsNoVaccinated','populationNoVaccinated']] = unCompleteVaccination[['casos_confirmados', 'casos_uci', 'casos_def', 'poblacion']].values

    # replace week epidemiological number by dates
    week = data['epidemiologicalWeek'].unique()
    numberOfWeek = week[-1]
    sundayOfWeek = pd.date_range("2021-01-03", periods=numberOfWeek, freq="W")
    sturdayOfWeek = pd.date_range("2021-01-09", periods=numberOfWeek, freq="W")
    sundayOfWeek = pd.to_datetime(sundayOfWeek,  format="%Y-%m-%d").strftime("%d-%m-%y")
    sturdayOfWeek = pd.to_datetime(sturdayOfWeek,  format="%Y-%m-%d").strftime("%d-%m-%y")
    dicWeekToDate = {}
    for w in week:
        dicWeekToDate[w] = sundayOfWeek[w-1]+'\n'+sturdayOfWeek[w-1]
    data['epidemiologicalWeek'] =  data['epidemiologicalWeek'].replace(dicWeekToDate)


    # create data folder if does not exist and save the dataframe
    if not path.exists('data'):
        mkdir('data')
    data.to_csv('./data/incidence-vaccinated-unvaccinated-by-age.csv')


if __name__ == "__main__":
    downloadData()