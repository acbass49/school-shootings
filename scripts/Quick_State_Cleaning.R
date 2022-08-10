# Adding statenames back in
library(tidyverse)

# I got this crosswalk from here: https://www.nrcs.usda.gov/wps/portal/nrcs/detail/?cid=nrcs143_013696
join_me <- read.csv('./county_level_data_raw/State_fips_to_state.csv', header = F)
join_me <- join_me %>% 
  select(FULL=V1, ABBR=V2, State_fips=V3)

final <- read.csv('./Finalized_data/state_scores.csv') %>% 
  select(State_fips=STATE, mean) %>% 
  left_join(join_me, by = 'State_fips') %>% 
  select(FULL, mean)

write.csv(final,'./Finalized_data/state_scores_final.csv', row.names = F)
