data {
    // Number of ages group
    int NAge;
    
    // Number of cases by age and number of cases vaccinated by age
    int NCases[NAge];
    int NCasesVaccinated[NAge];
    
    // Number of people  and of vaccinated in each age group
    vector[NAge] N;
    vector[NAge] NVaccinated;
    
}

parameters {
    // log relative risk vaccinated vs non vaccinated
    real logRR; 
}

transformed parameters {        
        real probVaccinatedIfCases[NAge];
        for (a in 1:NAge){
            probVaccinatedIfCases[a]= 1/(1+exp(-log(NVaccinated[a]/(N[a]-NVaccinated[a])) - logRR));
        }
}

model {

    // Priors
    logRR ~ normal(0,1);
    
    for (a in 1:NAge){
        NCasesVaccinated[a] ~ binomial(NCases[a], probVaccinatedIfCases[a]);
        
    }
    
}

generated quantities {
    
    // Vaccine efficacy
    real VE;
    VE = 1-exp(logRR);
}