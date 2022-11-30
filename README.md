# school-shootings-bayesian-analysis

Blog post write up [here](https://alexbass.me/posts/bayesian_county/)!!

Recently, gun violence has taken center stage in national news coverage with Congress recently passing a bipartisan gun bill. This study focuses on deepening our understanding of the types of counties in which gun violence in schools is prevalent. Our report aims to answer questions like: What are the characteristics of a county that are more susceptible to gun violence? Are gun violence incidents concentrated in particular regions in America? If so, which? How do state laws play a role in deterring gun violence in schools? In the end, our motivation is to provide more context, information, and understanding on a major debate in American politics today using predictions from Bayesian regression modeling.

We evaluated several different bayesian poisson regression models, but our final - intermediary model ended up being a heirarchical zero-inflated poisson regression model, but ultimatley after the second phase, I used the heirarchical Negative Binomial model. Final findings are detailed in the blog post - and intermediary findings are detailed in the report.

We initially wrote a report having most of the data joined in, but later joined the rest of the counties in (manually), did additional analysis, then wrote a final blog post. The presentation and final_report represent the findings given the missing data whereas the blog post and "final" items below are after additional analysis.

### Breakdown of repository:

Cleaning:
1. Webscraping script matching cities to counties - webscraping/city_to_county.ipynb
2. Script combining all datasets - scripts/joining_script.R
3. Script combining all datasets for eda - scripts/joining_additional.R  
4. All data files in this folder - county_level_data_raw/  
5. Intermediary dataset used in intermediary modeling script - Finalized_data/train.csv  
6. Final training dataset with all counties joined in - Finalized_data/new_train.csv

Modeling:
1. Exploratory Data Analysis - additional_analysis/eda.ipynb
2. Intermediary notebook - scripts/combined_poisson.ipynb
3. Final Blog post notebook - additional_analysis/modeling.ipynb

Report:
1. Intermediary Written report - Final_Report.pdf
2. Intermediary Presentation slides - Presentation.pdf
3. Final [blog post write up](https://alexbass.me/posts/bayesian_county/)
