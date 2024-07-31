surv_dat<- read.csv("~/Library/CloudStorage/GoogleDrive-carly.a.bobak@dartmouth.edu/Shared drives/RC - RIG Faculty Shared Projects/Fortuna - Mental Health/Survery_Results_For_R.csv")
surv_dat$True.Label<-trimws(surv_dat$True.Label)

# Numeric Key
# 1: Definitely AI
# 2: Maybe AI
# 3: I don't know
# 4: Maybe Human
# 5: Definitely Human

# Confidence key
# Definitely: 100 for confidence
# Maybe: 60 for confidence
# I don't know: 0 for confidence

# Load necessary libraries
library(dplyr)
library(tidyr)

# Calculate the percentage agreement for each sentence
calculate_agreement <- function(row) {
  ratings <- row[4:25]
  ratings <- ratings[!is.na(ratings)]
  agreement <- sum(ratings == ratings[1], na.rm = TRUE) / length(ratings)
  return(agreement * 100)
}

# Calculate percentage agreement for each sentence
surv_dat$Agreement <- apply(surv_dat, 1, calculate_agreement)

# Calculate percentage agreement within Tech Raters
calculate_group_agreement <- function(row, start, end) {
  ratings <- row[start:end]
  ratings <- ratings[!is.na(ratings)]
  agreement <- sum(ratings == ratings[1], na.rm = TRUE) / length(ratings)
  return(agreement * 100)
}

surv_dat$Tech_Agreement <- apply(surv_dat, 1, calculate_group_agreement, start=4, end=12)
surv_dat$PS_Agreement <- apply(surv_dat, 1, calculate_group_agreement, start=13, end=25)

# Adjusted Accuracy: Comparing the ratings to the true origin with weighted confidence
# Function to calculate weighted accuracy
calculate_accuracy <- function(row, start, end) {
  true_origin <- ifelse(row["True.Origin"] == "Human", 5, 1)
  ratings <- as.numeric(row[start:end])
  ratings <- ratings[!is.na(ratings)]
  weights <- ifelse(ratings == true_origin, 1,
                    ifelse(ratings == 2 | ratings == 4, 0.6, 0))
  accuracy <- sum(weights, na.rm = TRUE) / length(ratings)
  return(accuracy * 100)
}

surv_dat$Tech_Accuracy <- apply(surv_dat, 1, calculate_accuracy, start=4, end=12)
surv_dat$PS_Accuracy <- apply(surv_dat, 1, calculate_accuracy, start=13, end=25)
surv_dat$Overall_Accuracy <- apply(surv_dat, 1, calculate_accuracy, start=4, end=25)


# Percentage of errors
calculate_errors <- function(row, start, end) {
  true_origin <- ifelse(row["True.Origin"] == "Human", 5, 1)
  ratings <- as.numeric(row[start:end])
  ratings <- ratings[!is.na(ratings)]
  
  # Determine incorrect ratings
  if (true_origin == 1) {
    errors <- sum(ratings == 3 | ratings == 4 | ratings == 5, na.rm = TRUE)
  } else {
    errors <- sum(ratings == 1 | ratings == 2 | ratings == 3, na.rm = TRUE)
  }
  
  error_percentage <- errors / length(ratings) * 100
  return(error_percentage)
}

surv_dat$Tech_Errors <- apply(surv_dat, 1, calculate_errors, start=4, end=12)
surv_dat$PS_Errors <- apply(surv_dat, 1, calculate_errors, start=13, end=25)
surv_dat$Overall_Errors <- apply(surv_dat, 1, calculate_errors, start=4, end=25)

# Average confidence
calculate_confidence <- function(row, start, end) {
  ratings <- row[start:end]
  ratings <- ratings[!is.na(ratings)]
  confidence <- sum(ifelse(ratings == 1 | ratings == 5, 100, ifelse(ratings == 2 | ratings == 4, 60, 0)), na.rm = TRUE) / length(ratings)
  return(confidence)
}

surv_dat$Tech_Confidence <- apply(surv_dat, 1, calculate_confidence, start=4, end=12)
surv_dat$PS_Confidence <- apply(surv_dat, 1, calculate_confidence, start=13, end=25)
surv_dat$Overall_Confidence <- apply(surv_dat, 1, calculate_confidence, start=4, end=25)

# Summarize the results
summary_results <- surv_dat %>%
  summarise(
    Overall_Agreement = mean(Agreement, na.rm = TRUE),
    Tech_Agreement = mean(Tech_Agreement, na.rm = TRUE),
    PS_Agreement = mean(PS_Agreement, na.rm = TRUE),
    Overall_Accuracy = mean(Overall_Accuracy, na.rm = TRUE),
    Tech_Accuracy = mean(Tech_Accuracy, na.rm = TRUE),
    PS_Accuracy = mean(PS_Accuracy, na.rm = TRUE),
    Overall_Errors = mean(Overall_Errors, na.rm = TRUE),
    Tech_Errors = mean(Tech_Errors, na.rm = TRUE),
    PS_Errors = mean(PS_Errors, na.rm = TRUE),
    Overall_Confidence = mean(Overall_Confidence, na.rm = TRUE),
    Tech_Confidence = mean(Tech_Confidence, na.rm = TRUE),
    PS_Confidence = mean(PS_Confidence, na.rm = TRUE)
  )


write.csv(surv_dat,"clean_r_dat.csv",row.names=F)

