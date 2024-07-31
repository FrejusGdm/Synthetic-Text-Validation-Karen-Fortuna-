# Function to calculate accuracy for a single rater
calculate_rater_accuracy <- function(ratings, true_origin) {
  true_origin_values <- ifelse(true_origin == "Human", 5, 1)
  weights <- ifelse(ratings == true_origin_values, 1, ifelse(ratings == 2 | ratings == 4, 0.6, 0))
  accuracy <- sum(weights, na.rm = TRUE) / length(ratings)
  return(accuracy * 100)
}

# Function to calculate errors for a single rater
calculate_rater_errors <- function(ratings, true_origin) {
    true_origin_value <- ifelse(true_origin == "Human", 5, 1)
    incorrect_ratings <- ifelse(true_origin_value == 1, 
                                ratings %in% c(3, 4, 5), 
                                ratings %in% c(1, 2, 3))
    error_percentage <- sum(incorrect_ratings, na.rm = TRUE) / length(ratings) * 100
    return(error_percentage)
  }
# Function to calculate confidence for a single rater
calculate_rater_confidence <- function(ratings) {
  confidence <- sum(ifelse(ratings == 1 | ratings == 5, 100, ifelse(ratings == 2 | ratings == 4, 60, 0)), na.rm = TRUE) / length(ratings)
  return(confidence)
}

# Function to calculate percentage judged human that were actually human
calculate_rater_percentage_judged_human_actual_human <- function(ratings, true_origin) {
  true_origin_human <- true_origin == "Human"
  judged_human <- ratings == 5 | ratings == 4
  percentage_human_actual_human <- sum(judged_human & true_origin_human, na.rm = TRUE) / sum(judged_human, na.rm = TRUE) * 100
  return(percentage_human_actual_human)
}

# Function to calculate percentage judged human that were actually AI
calculate_rater_percentage_judged_human_actual_AI <- function(ratings, true_origin) {
  true_origin_AI <- true_origin == "Synthetic"
  judged_human <- ratings == 5 | ratings == 4
  percentage_human_actual_AI <- sum(judged_human & true_origin_AI, na.rm = TRUE) / sum(judged_human, na.rm = TRUE) * 100
  return(percentage_human_actual_AI)
}


# Initialize a data frame to store the results
rater_metrics <- data.frame(Rater = character(),
                            Accuracy = numeric(),
                            Errors = numeric(),
                            Confidence = numeric(),
                            Percent_Judged_Human_Actual_Human = numeric(),
                            Percent_Judged_Human_Actual_AI = numeric(),
                            stringsAsFactors = FALSE)

# List of rater columns
tech_raters <- paste0("Tech.Rater.", 1:9)
ps_raters <- paste0("PS.Rater.", 1:13)

# Combine all rater columns
all_raters <- c(tech_raters, ps_raters)

# Calculate metrics for each rater
for (rater in all_raters) {
  rater_data <- surv_dat[, c("True.Origin", rater)]
  colnames(rater_data) <- c("True.Origin", "Rating")
  
  accuracy <- calculate_rater_accuracy(rater_data$Rating, rater_data$True.Origin)
  errors <- calculate_rater_errors(rater_data$Rating, rater_data$True.Origin)
  confidence <- calculate_rater_confidence(rater_data$Rating)
  percent_judged_human_actual_human <- calculate_rater_percentage_judged_human_actual_human(rater_data$Rating, rater_data$True.Origin)
  percent_judged_human_actual_AI <- calculate_rater_percentage_judged_human_actual_AI(rater_data$Rating, rater_data$True.Origin)
  
  rater_metrics <- rbind(rater_metrics, data.frame(Rater = rater,
                                                   Accuracy = accuracy,
                                                   Errors = errors,
                                                   Confidence = confidence,
                                                   Percent_Judged_Human_Actual_Human = percent_judged_human_actual_human,
                                                   Percent_Judged_Human_Actual_AI = percent_judged_human_actual_AI))
}

# Print the rater metrics data frame
print(rater_metrics)




# Create a new column to distinguish between IT Professional and Peer Supporter
rater_metrics$Rater_Type <- ifelse(grepl("Tech", rater_metrics$Rater), "IT Professional", "Peer Supporter")

# Melt the data
melted_metrics <- melt(rater_metrics, id.vars = c("Rater", "Rater_Type"),
                       measure.vars = c("Percent_Judged_Human_Actual_Human", "Percent_Judged_Human_Actual_AI"),
                       variable.name = "Judgment_Type", value.name = "Percentage")

# Rename the levels of Judgment_Type for better readability
levels(melted_metrics$Judgment_Type) <- c("Human", "AI")

# Function to compute t-test and return formatted p-value
compute_t_test <- function(data, group_var, value_var) {
  t_test <- t.test(data[[value_var]] ~ data[[group_var]])
  p_val <- format.pval(t_test$p.value, digits = 3)
  return(paste("p =", p_val))
}

# Compute t-test for each Rater_Type
ps_t_test <- compute_t_test(subset(melted_metrics, Rater_Type == "Peer Supporter"), "Judgment_Type", "Percentage")
tech_t_test <- compute_t_test(subset(melted_metrics, Rater_Type == "IT Professional"), "Judgment_Type", "Percentage")

# Create the grouped bar graph
p=ggplot(melted_metrics, aes(x = Rater_Type, y = Percentage, fill = Judgment_Type)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(x = "Rater Type",
       y = "% Judged Human",
       fill = "Judgment") +
  scale_fill_brewer(palette = "Set2") +
  theme(text = element_text(size = 12))

# Add annotations for t-test results
p <- p + annotate("text", x = 1, y = max(melted_metrics$Percentage) + 5, label = ps_t_test, size = 5, color = "black", vjust = 0) +
  annotate("text", x = 2, y = max(melted_metrics$Percentage) + 5, label = tech_t_test, size = 5, color = "black", vjust = 0)

