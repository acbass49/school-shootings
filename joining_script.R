# Merging data
# Author : Alex Bass
# Date : 2022 - 06 - 29

library(tidyverse)

data <- read.csv('webscraping/data_w_county_match.csv')

data <- data[!data$CountyName == '',]

counts_by_fips <- data %>% 
  group_by(countyFIPS) %>% 
  summarise(
    n = n()
  ) %>% 
  mutate(countyFIPS = stringr::str_pad(countyFIPS, 5, side = 'left', pad = 0))

data <- read.csv('webscraping/county_pop.csv')

base_data <- data%>% 
  mutate(countyFIPS = stringr::str_pad(countyFIPS, 5, side = 'left', pad = 0)) %>% 
  left_join(counts_by_fips, by = 'countyFIPS') %>% 
  mutate(n = ifelse(is.na(n), 0, n)) %>% 
  filter(CountyName != 'Statewide Unallocated')

## Education

educ <- openxlsx::read.xlsx('county_level_data_raw/Education.xlsx', startRow = 5)

intermediate_df <- educ %>% 
  select(countyFIPS = `Federal.Information.Processing.Standards.(FIPS).Code`,
         ba_plus = `Percent.of.adults.with.a.bachelor's.degree.or.higher.2016-20`,
         less_than_hs = `Percent.of.adults.with.less.than.a.high.school.diploma,.2016-20`,
         hs = `Percent.of.adults.with.a.high.school.diploma.only,.2016-20`,
         some_col = `Percent.of.adults.completing.some.college.or.associate's.degree,.2016-20`,
         urban_rural = `2013.Rural-Urban.Continuum.Code`
         ) %>% 
  mutate(urban_rural = as.factor(car::recode(urban_rural, 
                                             '1:3="urban";4:6="suburban";7:9="rural"',
                                             as.factor = T,
                                             levels = c('urban', 'suburban', 'rural')
                                             )),
         countyFIPS = stringr::str_pad(countyFIPS, 5, side = 'left', pad = 0)) %>% 
  right_join(base_data, by = 'countyFIPS')

unemp <- openxlsx::read.xlsx('county_level_data_raw/Unemployment.xlsx', startRow = 5)

intermediate_df <- unemp %>% 
  select(
    countyFIPS = FIPS_code,
    Unemployment_rate_2021,
    Median_Household_Income_2020
  ) %>% 
  mutate(countyFIPS = stringr::str_pad(countyFIPS, 5, side = 'left', pad = 0)) %>% 
  right_join(intermediate_df, by = 'countyFIPS') %>% 
  mutate(CountyName = stringr::str_to_upper(CountyName))

race_gender <- read.csv('county_level_data_raw/age.csv')
state_match <- read.csv('county_level_data_raw/state_codes.csv')

race_gender <- race_gender %>%
  filter(AGEGRP %in% 0 & YEAR %in% 12)

race_gender <- race_gender %>% 
  left_join(state_match, by = c('STNAME' = 'Name')) %>% 
  rename(CountyName = CTYNAME) %>% 
  select(
    State,
    STATE, 
    COUNTY,
    CountyName,
    TOT_POP,
    TOT_MALE,
    TOT_FEMALE,
    WA_MALE,
    WA_FEMALE,
    BA_MALE,
    BA_FEMALE,
    AA_MALE,
    AA_FEMALE,
    H_MALE,
    H_FEMALE
  )

recodes <- list(
  'Male' = c('TOT_MALE'),
  'White' = c('WA_MALE', 'WA_FEMALE'),
  'Black' = c('BA_MALE', 'BA_FEMALE'),
  'Asian' = c('AA_MALE', 'AA_FEMALE'),
  'Hispanic' = c('H_MALE', 'H_FEMALE')
)

race_add <- purrr::imap_dfr(recodes, ~{
  if (length(.x) > 1) tot <- rowSums(race_gender[,.x]) else tot <- race_gender[[.x]]
  tot/race_gender$TOT_POP
})

race_gender <- race_gender %>% 
  bind_cols(race_add) %>% 
  select(names(recodes),
         State,
         STATE, 
         COUNTY,
         CountyName,
         TOT_POP) %>% 
  mutate(CountyName = stringr::str_to_upper(CountyName))

race_gender[race_gender$CountyName == 'ANCHORAGE MUNICIPALITY', 'CountyName'] <- 'MUNICIPALITY OF ANCHORAGE'
race_gender[race_gender$CountyName == 'JUNEAU CITY AND BOROUGH', 'CountyName'] <- 'CITY AND BOROUGH OF JUNEAU'
race_gender[race_gender$CountyName == 'PETERSBURG BOROUGH', 'CountyName'] <- 'PETERSBURG CENSUS AREA'
race_gender[race_gender$CountyName == 'BROOMFIELD COUNTY', 'CountyName'] <- 'BROOMFIELD COUNTY AND CITY'
race_gender[race_gender$CountyName == 'DISTRICT OF COLUMBIA', 'CountyName'] <- 'WASHINGTON'
race_gender[race_gender$CountyName == 'WASHINGTON', 'State'] <- 'DC'
race_gender[race_gender$CountyName == 'LASALLE PARISH', 'CountyName'] <- 'LA SALLE PARISH'
race_gender[race_gender$CountyName == 'JACKSON COUNTY' & race_gender$State == 'MO', 'CountyName'] <- 'JACKSON COUNTY (INCLUDING OTHER PORTIONS OF KANSAS CITY)'
race_gender[race_gender$CountyName == 'ST. LOUIS CITY', 'CountyName'] <- 'ST. LOUIS COUNTY'
intermediate_df[intermediate_df$CountyName == 'DOÑA ANA COUNTY', 'CountyName'] <- 'DONA ANA COUNTY'
race_gender[race_gender$CountyName == 'MATHEWS COUNTY', 'CountyName'] <- 'MATTHEWS COUNTY'
race_gender[1803, 'CountyName'] <- 'DONA ANA COUNTY'

race_gender %>% 
  anti_join(intermediate_df, by = c('CountyName', 'State'))

intermediate_df <- race_gender %>% 
  inner_join(intermediate_df, by = c('CountyName', 'State')) %>% 
  select(-TOT_POP)

age_df <- read.csv('county_level_data_raw/age.csv')

intermediate_df <- age_df %>% 
  filter(YEAR %in% 12) %>% 
  select(
    STATE,
    COUNTY,
    AGEGRP,
    TOT_POP
  ) %>% 
  pivot_wider(id_cols = c('STATE', 'COUNTY'), 
              names_from = 'AGEGRP', 
              values_from = 'TOT_POP',
              names_prefix = 'a') %>% 
  mutate(under40 = (a1 + a2 + a3 + a5 + a6 + a7 + a8)/a0) %>% 
  select(
    STATE,
    COUNTY,
    under40
  ) %>% 
  inner_join(intermediate_df, by = c('COUNTY', 'STATE'))

gun_df <- read.csv('county_level_data_raw/Gun_Laws.csv')

final_df <- intermediate_df %>% 
  left_join(gun_df, by = 'State')

final_df %>% 
  summarise(across(everything(), function(x) sum(is.na(x)))) %>% 
  View()

final_df <- final_df %>% 
  mutate(across(13:18, function(x) replace(x, is.na(x), mean(x, na.rm = T)))) %>%
  select(-TOT_POP)

write.csv(final_df,'Finalized_data/train.csv')
