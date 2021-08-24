# Bayesian screening method to estimate vaccine efficacy in Chile

We propose a Python script to estimate the vaccine efficacy in Chile. We use a Bayesian regression strongly based on the screening method introduced in
**[Farrington, 1993](https://pubmed.ncbi.nlm.nih.gov/8225751/)**.

**\*Disclamer:** We have to interpret with caution the vaccine efficacy estimated here. Age is the only confounding variable available in the dataset. To have a better estimation of the real vaccine efficacy we should take in account other important variables as sex, risk factor, location...\*

## Data

The Science Ministry of Chile opened a [github repository](https://github.com/MinCiencia/Datos-COVID19/) of Covid-19 data. In particular, since August 1, 2021,
number of Covid-19 cases, ICU entries, and deaths are published each epidemiological week (from Sunday to Saturday) with respect to vaccination status and age (see [data](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto89)). Moreover, the number of people vaccinated and not vaccinated are given in each age group.

## Model

We propose a Bayesian logistic regression to estimate the relative risk $RR$ of the vaccinated group vs unvaccinated group with respect to be a Covid-19 case, enter in intensive unit care (ICU) and death. The vaccine efficacy is defined as $VE = 1-RR$.

$VE$ **does not** depend on the age group variable $a$ in this model.

**Observations:**

- $N_{c}[a]$: number of cases in the age group $a$
- $N_{c,v}[a]$: number of cases vaccinated in the age group $a$
- $p_{v}[a]$: proportion of vaccinated in the age group $a$

**Parameters:**

- $r=\log(RR)$
- $p_{v|c}[a]$: the proportion of vaccinated in the cases, which is directly link to $r$ by the following relation:
  $$
  \ln\left(\frac{p_{v|c}[a]}{1-p_{v|c}[a]}\right) = \ln\left(\frac{p_{v}[a]}{1-p_{v}[a]}\right) + r
  $$

**Prior:** $r \sim \mathcal{N}(0,1)$

**Likelihood:** We compute the likelihood from the following distribution $$N_{c,v}[a] \sim \mathrm{Binomial}\left(p_{v|c}[a],N_{c}[a]\right)$$

**Use**

Python packages needed: Matplotlib, Seaborn, NumPy, Pandas, PyStan, ArviZ.

Then run

```
python main.py
```

The VE estimations and charts are in the [ouput]() folder.
