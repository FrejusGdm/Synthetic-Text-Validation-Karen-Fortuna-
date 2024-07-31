# Load necessary packages
if (!requireNamespace("ggplot2", quietly = TRUE)) {
  install.packages("ggplot2")
}
if (!requireNamespace("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}
if (!requireNamespace("tidyr", quietly = TRUE)) {
  install.packages("tidyr")
}
if (!requireNamespace("ggpubr", quietly = TRUE)) {
  install.packages("ggpubr")
}
library(ggplot2)
library(dplyr)
library(tidyr)
library(ggpubr)
library(reshape2)

# Distribution of outcomes
# Melt the data for ggplot
columns_to_check <- c("Tech_Agreement", "PS_Agreement", "Tech_Accuracy", "PS_Accuracy", "Tech_Confidence", "PS_Confidence")
melted_data <- melt(surv_dat, measure.vars = columns_to_check, variable.name = "Metric_Type", value.name = "Value")

# Add a column to distinguish between Tech and PS
melted_data$Rater_Type <- ifelse(grepl("Tech", melted_data$Metric_Type), "IT Professional", "Peer Supporter")

# Rename Metric_Type to a simpler form
melted_data$Metric_Type <- gsub("Tech_|PS_", "", melted_data$Metric_Type)

agree_plot<-ggplot(subset(melted_data, Metric_Type == "Agreement"), aes(x = Value, fill = Rater_Type)) +
  geom_density(alpha = 0.5) +
  theme_minimal() +
  labs(x = "% Agreement",
       y = "Density",
       fill = "Rater Type") +
  scale_fill_brewer(palette = "Set1", labels = c("IT Professional", "Peer Supporter"))

#ggsave("agreement.png",height=6,width=6,units="in",dpi = 200)

acc_plot<-ggplot(subset(melted_data, Metric_Type == "Accuracy"), aes(x = Value, fill = Rater_Type)) +
  geom_density(alpha = 0.5) +
  geom_vline(xintercept=50,linetype="dashed",color="grey30") +
  theme_minimal() +
  labs(x = "Weighted Accuracy",
       y = "Density",
       fill = "Rater Type") +
  scale_fill_brewer(palette = "Set1", labels = c("IT Professional", "Peer Supporter"))

conf_plot<-ggplot(subset(melted_data, Metric_Type == "Confidence"), aes(x = Value, fill = Rater_Type)) +
  geom_density(alpha = 0.5) +
  theme_minimal() +
  labs(x = "Confidence",
       y = "Density",
       fill = "Rater Type") +
  scale_fill_brewer(palette = "Set1", labels = c("IT Professional", "Peer Supporter"))

# Function to calculate % judged human for individual votes
calculate_percentage_judged_human <- function(ratings) {
  ratings <- as.numeric(ratings)
  percentage_human <- sum(ratings == 5 | ratings == 4, na.rm = TRUE) / sum(!is.na(ratings)) * 100
  return(percentage_human)
}

# Split the data by True.Origin
human_data <- surv_dat %>% filter(True.Origin == "Human")
synthetic_data <- surv_dat %>% filter(True.Origin == "Synthetic")

# Calculate percentages for each subset
calculate_percentages_for_subset <- function(subset_data) {
  data.frame(
    True.Origin = unique(subset_data$True.Origin),
    Overall = calculate_percentage_judged_human(as.numeric(unlist(subset_data[4:25]))),
    Tech_Professional = calculate_percentage_judged_human(as.numeric(unlist(subset_data[4:12]))),
    Peer_Supporter = calculate_percentage_judged_human(as.numeric(unlist(subset_data[13:25])))
  )
}

# Apply the function to each subset and combine the results
percentages_human <- calculate_percentages_for_subset(human_data)
percentages_synthetic <- calculate_percentages_for_subset(synthetic_data)
percentages <- rbind(percentages_human, percentages_synthetic)
# Convert the data to long format for ggplot2
percentages_long <- percentages %>%
  pivot_longer(cols = c(Overall, Tech_Professional, Peer_Supporter), names_to = "Rater_Group", values_to = "Percentage")

# Create the grouped bar chart using ggplot2
p <- ggplot(percentages_long, aes(x = Rater_Group, y = Percentage, fill = True.Origin)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(x = "Rater Group",
       y = "% Judged Human",
       fill = "True Origin") +
  scale_fill_brewer(palette = "Set2") +
  theme(text = element_text(size = 12),
        axis.text.x = element_text(angle = 45, hjust = 1))


# Print the plot
p


# Function to add correlation text to plots
add_corr_text <- function(p, data, x, y) {
  cor_test <- cor.test(data[[x]], data[[y]], method = "pearson")
  cor_text <- paste("r = ", round(cor_test$estimate, 2), "\np = ", format.pval(cor_test$p.value, digits = 2, eps = 0.001), sep = "")
  p + annotate("text", x = -Inf, y = Inf, label = cor_text, hjust = -0.1, vjust = 1.5, size = 5)
}

overall_conf_errors <- ggplot(surv_dat, aes(x = Overall_Confidence, y = Overall_Errors)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE) +
  theme_minimal() +
  labs(x = "Rating Confidence",
       y = "% Errors")
# Add correlation text
overall_conf_errors <- add_corr_text(overall_conf_errors, surv_dat, "Overall_Confidence", "Overall_Errors")


# Filter data for High labels
high_data <- surv_dat %>% filter(True.Label == "High")

# Scatter plot for Tech Errors vs. Tech Confidence for High labels
p1_high <- ggplot(high_data, aes(x = Tech_Confidence, y = Tech_Errors)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE) +
  theme_minimal() +
  labs(title = "Tech: Confidence vs. % Errors (High)",
       x = "Tech Confidence",
       y = "Tech % Errors")

# Add correlation text
p1_high <- add_corr_text(p1_high, high_data, "Tech_Confidence", "Tech_Errors")

# Print the plot
print(p1_high)

# Scatter plot for PS Errors vs. PS Confidence for High labels
p2_high <- ggplot(high_data, aes(x = PS_Confidence, y = PS_Errors)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE) +
  theme_minimal() +
  labs(title = "Peer Supporter: Confidence vs. % Errors (High)",
       x = "Peer Supporter Confidence",
       y = "Peer Supporter % Errors")

# Add correlation text
p2_high <- add_corr_text(p2_high, high_data, "PS_Confidence", "PS_Errors")

# Print the plot
print(p2_high)

# Filter data for Low labels
low_data <- surv_dat %>% filter(True.Label == "Low")

# Scatter plot for Tech Errors vs. Tech Confidence for Low labels
p1_low <- ggplot(low_data, aes(x = Tech_Confidence, y = Tech_Errors)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE) +
  theme_minimal() +
  labs(x = "IT Professional Confidence",
       y = "% Errors")

# Add correlation text
p1_low <- add_corr_text(p1_low, low_data, "Tech_Confidence", "Tech_Errors")

# Print the plot
print(p1_low)

# Scatter plot for PS Errors vs. PS Confidence for Low labels
p2_low <- ggplot(low_data, aes(x = PS_Confidence, y = PS_Errors)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE) +
  theme_minimal() +
  labs(x = "Peer Supporter Confidence",
       y = "% Errors")

# Add correlation text
p2_low <- add_corr_text(p2_low, low_data, "PS_Confidence", "PS_Errors")

# Print the plot
print(p2_low)

png("survey_stats_plots.png",height=8.5,width=11,units="in",res=300)
ggarrange(acc_plot,agree_plot,conf_plot,overall_conf_errors,p1_low,p2_low,
          nrow=3, ncol = 2,common.legend = T,labels="AUTO")
dev.off()
