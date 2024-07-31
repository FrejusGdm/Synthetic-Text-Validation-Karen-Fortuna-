# Install and load necessary packages
if (!requireNamespace("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}
if (!requireNamespace("tidyr", quietly = TRUE)) {
  install.packages("tidyr")
}
if (!requireNamespace("psycho", quietly = TRUE)) {
  install.packages("psycho")
}
if (!requireNamespace("purrr", quietly = TRUE)) {
  install.packages("purrr")
}
library(dplyr)
library(tidyr)
library(psycho)
library(purrr)

# Reshape the data to long format
long_data <- surv_dat %>%
  pivot_longer(cols = starts_with("Tech.Rater.") | starts_with("PS.Rater."),
               names_to = "Rater", values_to = "Rating") %>%
  mutate(Rater_Type = ifelse(grepl("Tech", Rater), "Tech", "PS"))

# Define weights
weight_definite <- 1
weight_maybe <- 0.6

# Function to calculate weighted SDT measures for a group of ratings
calculate_weighted_sdt_measures <- function(ratings, true_origin) {
  true_origin <- unique(true_origin)
  if (length(true_origin) != 1) stop("true_origin must be a single value")
  
  if (true_origin == "Human") {
    n_hit <- sum(ratings == 5, na.rm = TRUE) * weight_definite + sum(ratings == 4, na.rm = TRUE) * weight_maybe  # True positive: Definitely Human or Maybe Human
    n_miss <- sum(ratings != 5 & ratings != 4, na.rm = TRUE) # False negative
    n_fa <- sum(ratings == 1, na.rm = TRUE) * weight_definite + sum(ratings == 2, na.rm = TRUE) * weight_maybe  # False positive: Definitely AI or Maybe AI
    n_cr <- sum(ratings != 1 & ratings != 2, na.rm = TRUE)   # True negative
  } else {
    n_hit <- sum(ratings == 1, na.rm = TRUE) * weight_definite + sum(ratings == 2, na.rm = TRUE) * weight_maybe  # True positive: Definitely AI or Maybe AI
    n_miss <- sum(ratings != 1 & ratings != 2, na.rm = TRUE) # False negative
    n_fa <- sum(ratings == 5, na.rm = TRUE) * weight_definite + sum(ratings == 4, na.rm = TRUE) * weight_maybe  # False positive: Definitely Human or Maybe Human
    n_cr <- sum(ratings != 5 & ratings != 4, na.rm = TRUE)   # True negative
  }
  return(data.frame(n_hit = n_hit, n_fa = n_fa, n_miss = n_miss, n_cr = n_cr))
}

# Function to calculate d', beta, and c for each rater
calculate_weighted_sdt_measures_rater <- function(data) {
  sdt_measures_human <- calculate_weighted_sdt_measures(data %>% filter(True.Origin == "Human") %>% pull(Rating), "Human")
  sdt_measures_synthetic <- calculate_weighted_sdt_measures(data %>% filter(True.Origin == "Synthetic") %>% pull(Rating), "Synthetic")
  
  dprime_human <- psycho::dprime(sdt_measures_human$n_hit, sdt_measures_human$n_fa, sdt_measures_human$n_miss, sdt_measures_human$n_cr)
  dprime_synthetic <- psycho::dprime(sdt_measures_synthetic$n_hit, sdt_measures_synthetic$n_fa, sdt_measures_synthetic$n_miss, sdt_measures_synthetic$n_cr)
  
  return(data.frame(
    d_prime_human = dprime_human$dprime,
    beta_human = dprime_human$beta,
    c_human = dprime_human$c,
    d_prime_synthetic = dprime_synthetic$dprime,
    beta_synthetic = dprime_synthetic$beta,
    c_synthetic = dprime_synthetic$c
  ))
}

# Initialize an empty list to store SDT measures
rater_sdt_measures_list <- list()

# Iterate over each rater and calculate SDT measures
for (rater in unique(long_data$Rater)) {
  rater_data <- long_data %>% filter(Rater == rater)
  sdt_measures <- calculate_weighted_sdt_measures_rater(rater_data)
  rater_sdt_measures_list[[rater]] <- sdt_measures
}

# Convert the list to a data frame
rater_sdt_measures <- do.call(rbind, lapply(names(rater_sdt_measures_list), function(rater) {
  data.frame(Rater = rater, rater_sdt_measures_list[[rater]])
}))

# Combine human and synthetic measures for qqnorm and t.test
combined_measures <- rater_sdt_measures %>%
  mutate(
    d_prime_combined = (d_prime_human + d_prime_synthetic) / 2,
    beta_combined = (beta_human + beta_synthetic) / 2,
    c_combined = (c_human + c_synthetic) / 2
  )

# Print the combined measures
print(combined_measures)

# QQ plot and t-test for d'
qqnorm(combined_measures$d_prime_combined)
qqline(combined_measures$d_prime_combined)
print(t.test(combined_measures$d_prime_combined, mu = 0))
# print(t.test(combined_measures$d_prime_human, mu = 0))
# print(t.test(combined_measures$d_prime_synthetic, mu = 0))

print(t.test(combined_measures$d_prime_combined[grepl("tech",combined_measures$Rater,ignore.case=T)], mu = 0))
print(t.test(combined_measures$d_prime_combined[grepl("ps",combined_measures$Rater,ignore.case=T)], mu = 0))


# QQ plot and t-test for beta
qqnorm(combined_measures$beta_combined)
qqline(combined_measures$beta_combined)
print(t.test(combined_measures$beta_combined, mu = 0))
print(t.test(combined_measures$beta_combined, mu = 0))
print(t.test(combined_measures$beta_combined, mu = 0))

# QQ plot and t-test for c
qqnorm(combined_measures$c_combined)
qqline(combined_measures$c_combined)
print(t.test(combined_measures$c_combined, mu = 0))
