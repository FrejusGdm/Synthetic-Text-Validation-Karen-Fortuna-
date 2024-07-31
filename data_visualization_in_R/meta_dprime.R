# Load necessary libraries
library(dplyr)
library(tidyr)
library(purrr)
library(optimx)

# Function to calculate the negative log-likelihood
negative_log_likelihood <- function(parameters, nR_S1, nR_S2, s = 1) {
  meta_d1 <- parameters[1]
  t2c1 <- parameters[-1]
  
  S1mu <- -meta_d1 / 2
  S1sd <- 1
  S2mu <- meta_d1 / 2
  S2sd <- S1sd / s
  
  t2c1 <- c(-Inf, t2c1, Inf)
  
  prC_rS1 <- diff(pnorm(t2c1, S1mu, S1sd))
  prI_rS1 <- diff(pnorm(t2c1, S2mu, S2sd))
  
  # Add a larger constant to avoid log(0)
  epsilon <- 1e-6
  prC_rS1 <- ifelse(prC_rS1 <= 0, epsilon, prC_rS1)
  prI_rS1 <- ifelse(prI_rS1 <= 0, epsilon, prI_rS1)
  
  logL_rS1 <- sum(nR_S1 * log(prC_rS1), na.rm = TRUE) + sum(nR_S2 * log(prI_rS1), na.rm = TRUE)
  
  if (is.nan(logL_rS1) || is.infinite(logL_rS1)) {
    logL_rS1 <- -1e+300
  }
  
  return(-logL_rS1)
}

# Function to calculate meta-d' for each rater and return detailed results
calculate_meta_dprime <- function(nR_S1, nR_S2, s = 1) {
  nRatings <- length(nR_S1)
  nCriteria <- nRatings - 1
  
  t2c1 <- rep(0, nCriteria)
  initial_guess <- c(1, t2c1)
  
  result <- optimx(initial_guess, negative_log_likelihood, nR_S1 = nR_S1, nR_S2 = nR_S2, s = s,
                   method = "L-BFGS-B", lower = -10, upper = 10, control = list(trace = 1))
  
  meta_d_prime <- result$p1[1]
  return(list(meta_d_prime = meta_d_prime, result = result))
}

# Function to prepare the data for each rater and handle NA values
prepare_data_for_rater <- function(data) {
  human_data <- data %>% filter(True.Origin == "Human")
  ai_data <- data %>% filter(True.Origin == "Synthetic")
  
  nR_S1 <- c(sum(human_data$`0`, na.rm = TRUE), sum(human_data$`60`, na.rm = TRUE), sum(human_data$`100`, na.rm = TRUE))
  nR_S2 <- c(sum(ai_data$`0`, na.rm = TRUE), sum(ai_data$`60`, na.rm = TRUE), sum(ai_data$`100`, na.rm = TRUE))
  
  # Ensure the lengths match
  if (length(nR_S1) != length(nR_S2)) {
    stop("Length mismatch between nR_S1 and nR_S2")
  }
  
  list(nR_S1 = nR_S1, nR_S2 = nR_S2)
}

# Aggregate data by Rater
prepared_data <- surv_dat %>%
  pivot_longer(cols = starts_with("Tech.Rater.") | starts_with("PS.Rater."),
               names_to = "Rater", values_to = "Rating") %>%
  group_by(Rater, True.Origin) %>%
  summarise(`0` = sum(Rating == 0, na.rm = TRUE),
            `60` = sum(Rating == 60, na.rm = TRUE),
            `100` = sum(Rating == 100, na.rm = TRUE), .groups = 'drop') %>%
  pivot_wider(names_from = True.Origin, values_from = c(`0`, `60`, `100`)) %>%
  group_by(Rater) %>%
  summarise(prepared_data = list(prepare_data_for_rater(cur_data())), .groups = 'drop')

# Apply meta-d' calculation to each rater and return detailed results
meta_dprime_results <- prepared_data %>%
  mutate(meta_d_prime = map(prepared_data, ~ calculate_meta_dprime(.x$nR_S1, .x$nR_S2)))

# Extract and display detailed results
meta_dprime_summary <- meta_dprime_results %>%
  select(Rater, meta_d_prime) %>%
  unnest_wider(meta_d_prime)

# Print the summary
print(meta_dprime_summary)

all_prime_results<-meta_dprime_summary %>% select(Rater,meta_d_prime) %>%
  full_join(combined_measures)

# Add Rater Type (Peer Supporter or IT Professional)
all_prime_results <- all_prime_results %>%
  mutate(Rater_Type = ifelse(grepl("PS.Rater", Rater), "Peer Supporter", "IT Professional"))

# Plot meta_d_prime vs d_prime_combined
insight_detection_plot<-ggplot(all_prime_results, aes(y = d_prime_human, x = meta_d_prime, color = Rater_Type)) +
  geom_point(size = 3) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray30") +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray30") +
  labs(x = "Insight (Meta d')",
       y = "Signal Detection Score (d')",
       color = "Rater Type") +
  theme_minimal() +
  scale_color_brewer(palette = "Set1", labels = c("IT Professional", "Peer Supporter"))

