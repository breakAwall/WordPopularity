setwd("C://Users//kgoel//Desktop//Y3 Sem1//Stat 405//Overall Project")

library(dplyr)
library(stringi)
library(ggplot2)

word_frequencies <- read.csv("data.csv")
fixed_words <- mutate(word_frequencies, word = stri_sub(word, 3, -4))
head(fixed_words)

arranged <- arrange(fixed_words, desc(total_upvotes))
head(arranged)

filtered_top <- filter(arranged, total_upvotes > 10000)
head(filtered_top)
nrow(filtered_top)

filtered_mid <- filter(arranged, total_upvotes > 6000, total_upvotes < 10000)
head(filtered_mid)
nrow(filtered_mid)

filtered_mid_low <- filter(arranged, total_upvotes > 2000, total_upvotes < 3000)
head(filtered_mid_low)
nrow(filtered_mid_low)

filtered_low <- filter(arranged, total_upvotes > 500, total_upvotes < 1000)
head(filtered_low)
nrow(filtered_low)


ggplot(data = filtered_top) +
  aes(factor(word), total_upvotes, fill = "#2e7f1e") +
  geom_col(position = "identity") +
  labs(x = "Word", 
       y = "Number of Up-votes",
       title = "Top Words") +
  theme(axis.text.x = element_text(angle = 40, hjust = 1)) +
  theme(legend.position="none")

ggplot(data = filtered_mid) +
  aes(factor(word), total_upvotes, fill = "#1a2e89") +
  geom_col(position = "identity") +
  labs(x = "Word", 
       y = "Number of Up-votes",
       title = "Mid Words") +
  theme(axis.text.x = element_text(angle = 40, hjust = 1)) +
  theme(legend.position="none")

ggplot(data = filtered_mid_low) +
  aes(factor(word), total_upvotes, fill = "#1a2e89") +
  geom_col(position = "identity") +
  labs(x = "Word", 
       y = "Number of Up-votes",
       title = "Mid to Low Words") +
  theme(axis.text.x = element_text(angle = 40, hjust = 1)) +
  theme(legend.position="none")

ggplot(data = filtered_low) +
  aes(factor(word), total_upvotes, fill = "#1a2e89") +
  geom_col(position = "identity") +
  labs(x = "Word", 
       y = "Number of Up-votes",
       title = "Low Words") +
  theme(axis.text.x = element_text(angle = 40, hjust = 1)) +
  theme(legend.position="none")



