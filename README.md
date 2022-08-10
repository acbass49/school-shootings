# school-shootings-bayesian-analysis

Recently, gun violence has taken center stage in national news coverage with Congress recently passing a bipartisan gun bill. This study focuses on deepening our understanding of the types of counties in which gun violence in schools is prevalent. Our report aims to answer questions like: What are the characteristics of a county that are more susceptible to gun violence? Are gun violence incidents concentrated in particular regions in America? If so, which? How do state laws play a role in deterring gun violence in schools? In the end, our motivation is to provide more context, information, and understanding on a major debate in American politics today using predictions from Bayesian regression modeling.

### Breakdown of repository:

Cleaning:
1. Webscraping script matching cities to counties - webscraping/city_to_county.ipynb
2. Script combining all datasets - scripts/joining_script.R
3. All data - county_level_data_raw/
4. Finalized dataset - Finalized_data/train.csv

Modeling:
1. Final notebook with all models - scripts/combined_poisson.ipynb

Report:
1. Written report - Final_Report.pdf
2. Presentation slides - Presentation.pdf
