# Bayesian screening method to estimate vaccine efficacy in Chile

We propose a Python script to estimate the vaccine efficacy against SARS-CoV-2 in Chile. We use a Bayesian logistic regression which is strongly based on the screening method introduced in
**[Farrington, 1993](https://pubmed.ncbi.nlm.nih.gov/8225751/)**.

_**Disclamer:** We have to interpret with caution the vaccine efficacy estimated here. Age is the only confounding variable available in the dataset. To have a better estimation of the real vaccine efficacy we should take in account other important variables as sex, risk factor, location... Moreover Chile has authorized several vaccines and we do not have the data by type of vaccine._

## Data

The Science Ministry of Chile opened a [github repository](https://github.com/MinCiencia/Datos-COVID19/) of Covid-19 data. In particular, since August 1, 2021,
number of Covid-19 cases, ICU entries, and deaths are published each epidemiological week (from Sunday to Saturday) with respect to vaccination status and age (see [data](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto89)). Moreover, the number of people vaccinated and not vaccinated are given in each age group.

## Model

We propose a Bayesian logistic regression to estimate the relative risk RR of the vaccinated group vs unvaccinated group with respect to be a Covid-19 case, enter in intensive unit care (ICU) and death. The vaccine efficacy is defined as VE = 1-RR.

**Observations:**

<!-- - $N_{c}[a]$: number of cases in the age group $a$ -->
<!-- - $N_{c,v}[a]$: number of cases vaccinated in the age group $a$ -->
<!-- - $p_{v}[a]$: proportion of vaccinated in the age group $a$ -->

- Nc(a): number of cases in the age group a
- Ncv(a): number of cases vaccinated in the age group a
- pv(a): proportion of vaccinated in the age group a

**Parameters:**

- r = ln(RR)
- pvc(a): proportion of cases vaccinated, which is directly linked to r by the following relation

  ln[pvc(a)/(1-pvc(a))] = ln[pv(a)/(1-pv(a))] + r

**Prior:** r ~ Normal(0,1)

**Likelihood:** We compute the likelihood from the following distribution
Ncv(a) ~ Binomial(pvc(a),Nc(a))

**Use**

Python packages needed: Matplotlib, Seaborn, NumPy, Pandas, PyStan, ArviZ.

Then run

```
python main.py
```

**Results**

The VE estimations tables and charts are in the [ouput](https://github.com/AntoineBraultChile/bayesian-screening-method/tree/main/output) folder.

How to read column names of the tables:

- median: median of the posterior
- lower_bound: lower bound of the credible interval 95%
- upper_bound: upper bound of the credible interval 95%
- cases_VE: vaccine efficacy against cases
- icu: vaccine efficacy against entry in intensive unit care
- deaths: vaccine efficacy against death

![alt text](https://github.com/AntoineBraultChile/bayesian-screening-method/blob/main/output/plot-vaccine-efficacy-by-epidemiologicalWeek.png?raw=true)
![alt text](https://github.com/AntoineBraultChile/bayesian-screening-method/blob/main/output/plot-vaccine-efficacy-by-ageGroup.png?raw=true)
