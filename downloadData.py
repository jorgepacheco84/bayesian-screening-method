import pandas as pd
from os import mkdir
from os import path

def downloadData():
    incidenceByAge = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto89/incidencia_en_vacunados_edad.csv')
    completeVaccination = incidenceByAge[(incidenceByAge['estado_vacunacion']=='con esquema completo') & (incidenceByAge['grupo_edad']!='Total')][['semana_epidemiologica', 'grupo_edad','casos_confirmados', 'casos_uci', 'casos_def', 'poblacion']] 
    unCompleteVaccination = incidenceByAge[(incidenceByAge['estado_vacunacion']=='sin esquema completo') & (incidenceByAge['grupo_edad']!='Total')][['semana_epidemiologica', 'grupo_edad','casos_confirmados', 'casos_uci', 'casos_def', 'poblacion']] 
    data = completeVaccination.rename(columns={'casos_confirmados':'casosVac', 'casos_uci':'uciVac', 'casos_def':'defVac', 'poblacion':'pobVac'})
    data[['casosNoVac','uciNoVac','defNoVac','pobNoVac']] = unCompleteVaccination[['casos_confirmados', 'casos_uci', 'casos_def', 'poblacion']].values
    if not path.exists('data'):
        mkdir('data')
    data.to_csv('./data/incidence-vaccinated-unvaccinated-by-age.csv')


if __name__ == "__main__":
    downloadData()