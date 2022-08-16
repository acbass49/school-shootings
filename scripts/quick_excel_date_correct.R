library(lubridate)
library(tidyverse)

data <- read.csv("webscraping/data_w_county_match_manual.csv")

data$Date <- lubridate::mdy(data$Date)

write.csv(data, "webscraping/data_w_county_match_manual.csv")
