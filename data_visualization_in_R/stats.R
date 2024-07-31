# Calculate some quick stats
# Function to find the mode (most frequent value)
find_mode <- function(x) {
  x <- na.omit(x)
  if (length(x) == 0) {
    return(NA)
  }
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}
# Select columns that contain "rater" in their names
rater_columns <- surv_dat %>% select(contains("rater"))

# Find the mode for each rater column
mode_results <- sapply(rater_columns, function(column) {
  find_mode(column)
})

# Convert the results to a dataframe for better visualization
mode_df <- data.frame(Rater = names(mode_results), Mode = mode_results)

# Print the mode dataframe
print(mode_df)


t.test(surv_dat$PS_Accuracy,surv_dat$Tech_Accuracy,paired = T)
t.test(surv_dat$PS_Confidence,surv_dat$Tech_Confidence,paired = T)
t.test(surv_dat$PS_Agreement,surv_dat$Tech_Agreement,paired=T)
t.test(surv_dat$Overall_Accuracy,mu=50)

t.test(surv_dat$Agreement)
t.test(surv_dat$Overall_Confidence)


cor.test(surv_dat$Tech_Errors,surv_dat$Tech_Confidence)
cor.test(surv_dat$PS_Errors,surv_dat$PS_Confidence)
cor.test(surv_dat$PS_Errors[surv_dat$True.Label=="Low"],surv_dat$PS_Confidence[surv_dat$True.Label=="Low"])
cor.test(surv_dat$Tech_Errors[surv_dat$True.Label=="Low"],surv_dat$Tech_Confidence[surv_dat$True.Label=="Low"])
cor.test(surv_dat$PS_Errors[surv_dat$True.Label=="High"],surv_dat$PS_Confidence[surv_dat$True.Label=="High"])
cor.test(surv_dat$Tech_Errors[surv_dat$True.Label=="High"],surv_dat$Tech_Confidence[surv_dat$True.Label=="High"])
cor.test(surv_dat$Overall_Errors,surv_dat$Overall_Confidence)

# Function to calculate proportion of AI judgments
calculate_proportion_AI <- function(ratings) {
  proportion_AI <- sum(ratings == 1 | ratings == 2, na.rm = TRUE) / length(ratings)
  return(proportion_AI)
}

# Filter data for PS raters and true labels
ps_raters <- paste0("PS.Rater.", 1:13)

# Calculate proportions for Low labeled sentences
low_data <- surv_dat %>% filter(True.Label == "Low")
low_proportions <- sapply(ps_raters, function(rater) calculate_proportion_AI(low_data[[rater]]))

# Calculate proportions for High labeled sentences
high_data <- surv_dat %>% filter(True.Label == "High")
high_proportions <- sapply(ps_raters, function(rater) calculate_proportion_AI(high_data[[rater]]))

# Perform a paired t-test
t_test_result <- t.test(low_proportions, high_proportions, paired = TRUE)

# Print the result
print(t_test_result)

# Filter data for PS raters and true labels
tech_raters <- paste0("Tech.Rater.", 1:9)

# Calculate proportions for Low labeled sentences
low_proportions <- sapply(tech_raters, function(rater) calculate_proportion_AI(low_data[[rater]]))

# Calculate proportions for High labeled sentences
high_proportions <- sapply(tech_raters, function(rater) calculate_proportion_AI(high_data[[rater]]))

# Perform a paired t-test
t_test_result <- t.test(low_proportions, high_proportions, paired = TRUE)

# Print the result
print(t_test_result)


t.test(rater_metrics$Percent_Judged_Human_Actual_Human[grepl("PS",rater_metrics$Rater)],rater_metrics$Percent_Judged_Human_Actual_AI[grepl("PS",rater_metrics$Rater)],paired=T)
t.test(rater_metrics$Percent_Judged_Human_Actual_Human[grepl("Tech",rater_metrics$Rater)],rater_metrics$Percent_Judged_Human_Actual_AI[grepl("Tech",rater_metrics$Rater)],paired=T)

