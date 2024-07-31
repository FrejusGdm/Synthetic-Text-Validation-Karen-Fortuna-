# Install and load necessary packages
if (!requireNamespace("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}
if (!requireNamespace("tidyr", quietly = TRUE)) {
  install.packages("tidyr")
}
if (!requireNamespace("purrr", quietly = TRUE)) {
  install.packages("purrr")
}
if (!requireNamespace("ggplot2", quietly = TRUE)) {
  install.packages("ggplot2")
}
if (!requireNamespace("pROC", quietly = TRUE)) {
  install.packages("pROC")
}

library(dplyr)
library(tidyr)
library(purrr)
library(ggplot2)
library(pROC)

# Function to calculate sensitivity and specificity for each rater with Human as the positive case
calculate_sensitivity_specificity_human_positive <- function(data) {
  TP_human <- sum(data$Rating %in% c(4, 5) & data$True.Origin == "Human", na.rm = TRUE)
  FN_human <- sum(data$Rating %in% c(1, 2, 3) & data$True.Origin == "Human", na.rm = TRUE)
  TN_AI <- sum(data$Rating %in% c(1, 2) & data$True.Origin == "Synthetic", na.rm = TRUE)
  FP_AI <- sum(data$Rating %in% c(3, 4, 5) & data$True.Origin == "Synthetic", na.rm = TRUE)
  
  sensitivity <- ifelse((TP_human + FN_human) == 0, NA, TP_human / (TP_human + FN_human))
  specificity <- ifelse((TN_AI + FP_AI) == 0, NA, TN_AI / (TN_AI + FP_AI))
  
  return(list(sensitivity = sensitivity, specificity = specificity))
}

# Calculate sensitivity and specificity for each rater
sensitivity_specificity_results_human_positive <- surv_dat %>%
  pivot_longer(cols = starts_with("Tech.Rater.") | starts_with("PS.Rater."),
               names_to = "Rater", values_to = "Rating") %>%
  group_by(Rater) %>%
  summarise(sensitivity_specificity = list(calculate_sensitivity_specificity_human_positive(cur_data())), .groups = 'drop')

# Extract and display sensitivity and specificity results
sensitivity_specificity_summary_human_positive <- sensitivity_specificity_results_human_positive %>%
  select(Rater, sensitivity_specificity) %>%
  unnest_wider(sensitivity_specificity)

# Add Rater Type (Peer Supporter or IT Professional) to sensitivity_specificity_summary
sensitivity_specificity_summary_human_positive <- sensitivity_specificity_summary_human_positive %>%
  mutate(Rater_Type = ifelse(grepl("PS.Rater", Rater), "Peer Supporter", "IT Professional"))

# Print the summary
print(sensitivity_specificity_summary_human_positive)

# Visualize Sensitivity vs Specificity colored by Rater Type
spec_sens_scatter<-ggplot(sensitivity_specificity_summary_human_positive, aes(x = specificity, y = sensitivity, color = Rater_Type)) +
  geom_point(size = 3) +
  geom_hline(yintercept = 0.7,linetype="dashed",color="grey30")+
  geom_vline(xintercept = 0.7,linetype="dashed",color="grey30")+
  labs(x = "Specificity",
       y = "Sensitivity") +
  theme_minimal() + 
  scale_color_brewer(palette = "Set1", labels = c("IT Professional", "Peer Supporter"))

# Prepare data for ROC curve
roc_data <- surv_dat %>%
  pivot_longer(cols = starts_with("Tech.Rater.") | starts_with("PS.Rater."),
               names_to = "Rater", values_to = "Rating") %>%
  mutate(Label = ifelse(True.Origin == "Human", 1, 0))

# Calculate ROC and AUC for each rater
roc_results <- roc_data %>%
  group_by(Rater) %>%
  summarise(roc_curve = list(roc(Label, Rating)), .groups = 'drop') %>%
  mutate(AUC = map_dbl(roc_curve, auc))

# Extract AUC values
auc_values <- roc_results %>%
  mutate(AUC = map_dbl(roc_curve, auc))

# Print the AUC values
print(auc_values)

# Identify best, worst, and most average rater based on AUC
best_rater <- roc_results %>% filter(AUC == max(AUC)) %>% slice(1)
worst_rater <- roc_results %>% filter(AUC == min(AUC)) %>% slice(1)
median_auc <- median(roc_results$AUC)
average_rater <- roc_results %>% filter(abs(AUC - median_auc) == min(abs(AUC - median_auc))) %>% slice(1)

# Combine the selected raters
selected_raters <- bind_rows(best_rater, worst_rater, average_rater)

# Plot the ROC curves for the selected raters
auc_plot<-ggplot() +
  geom_line(data = as.data.frame(coords(selected_raters$roc_curve[[1]])), aes(x = 1 - specificity, y = sensitivity), color = "goldenrod1") +
  geom_line(data = as.data.frame(coords(selected_raters$roc_curve[[2]])), aes(x = 1 - specificity, y = sensitivity), color = "purple3") +
  geom_line(data = as.data.frame(coords(selected_raters$roc_curve[[3]])), aes(x = 1 - specificity, y = sensitivity), color = "deeppink") +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "gray") +
  labs(x = "1 - Specificity",
       y = "Sensitivity",
       color = "Rater Type") +
  theme_minimal() +
  scale_color_manual(values = c("Best Rater" = "goldenrod1", "Worst Rater" = "purple3", "Most Average Rater" = "deeppink")) +
  annotate("text", x = 0.7, y = 0.19, label = paste("Best AUC =", round(best_rater$AUC, 2)), color = "goldenrod1", hjust = 0,size=2.5) +
  annotate("text", x = 0.7, y = 0.12, label = paste("Worst AUC =", round(worst_rater$AUC, 2)), color = "purple3", hjust = 0,size=2.5) +
  annotate("text", x = 0.7, y = 0.05, label = paste("Median AUC =", round(average_rater$AUC, 2)), color = "deeppink", hjust = 0,size=2.5)

# Add Rater Type (Peer Supporter or IT Professional)
roc_results <- roc_results %>%
  mutate(Rater_Type = ifelse(grepl("PS.Rater", Rater), "Peer Supporter", "IT Professional"))

# Print the summary
print(head(roc_results))

# Create boxplot of AUC values
auc_boxplot<-ggplot(roc_results, aes(x = Rater_Type, y = AUC, fill = Rater_Type)) +
  geom_boxplot() +
  labs(x = "Rater Type",
       y = "AUROC") +
  theme_minimal() +
  scale_fill_brewer(palette = "Set1", labels = c("IT Professional", "Peer Supporter"))

# Create a layout matrix
layout_matrix <- matrix(c(1, 1, 2, 3, 4, 5), ncol = 2, byrow = TRUE)

# Arrange the plots
combined_plot <- ggarrange(
  p, insight_detection_plot, spec_sens_scatter, auc_boxplot, auc_plot,
  ncol = 2, nrow = 3, labels = "AUTO", common.legend = TRUE, legend = "bottom",
  layout_matrix = layout_matrix
)

# Print the combined plot
print(combined_plot)
