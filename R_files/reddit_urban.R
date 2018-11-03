
library(RSQLite)

setwd("C://Users//kgoel//Desktop//Y3 Sem1//Stat 405//Overall Project//data")

dcon_reddit <- dbConnect(SQLite(), dbname = "reddit_submissions_2011.sqlite")
dcon_urban <- dbConnect(SQLite(), dbname = "urbanlitet_main.sqlite")

dbListTables(dcon_urban)
dbListFields(dcon_reddit, "per_word")


res <- dbSendQuery(conn = dcon_urban, "CREATE TABLE agt_counts_int AS
SELECT lowercase_word, SUM(thumbs_up), SUM(thumbs_down)
                   FROM per_word
                   GROUP BY lowercase_word
                   ")

res <- dbSendQuery(conn = dcon_urban, "DROP TABLE agt_counts")

res <- dbSendQuery(conn = dcon_urban, "CREATE TABLE agt_counts (
        lowercase_word TEXT,
        thumbs_up INTEGER,
        thumbs_down INTEGER
)")


res <- dbSendQuery(conn = dcon_urban, "INSERT INTO agt_counts
                  SELECT lowercase_word, SUM(thumbs_up), SUM(thumbs_down)
                   FROM per_word
                   GROUP BY lowercase_word
")
                   



query <- paste0("SELECT AVG(thumbs_up), AVG(thumbs_down)
               From agt_counts")
res <- dbSendQuery(conn = dcon_urban, query)
mydf <- dbFetch(res, -1)
dbClearResult(res)
head(mydf)
# thumbs up = 106.9924
# thumbs down = 69.31338


# get words in certain random places


get_ups_average_by_word <- function(word) {
  query <- paste0("SELECT AVG(ups) as average
                   FROM per_word
                WHERE title LIKE '%", word,
                  "%'")
  res <- dbSendQuery(conn = dcon_reddit, query)
  mydf <- dbFetch(res, -1)
  dbClearResult(res)
  mydf$average[1]
}

get_random_word_by_thumbs_up <- function(thumbs) {
  query <- paste0("SELECT *
               From agt_counts
                WHERE thumbs_up = '", thumbs, "'")
  res <- dbSendQuery(conn = dcon_urban, query)
  mydf <- dbFetch(res, -1)
  dbClearResult(res)
  mydf[floor(runif(1, 1, nrow(mydf))), ]
}


tu_vec <- floor(runif(100, 0, 500))


results <- c()
for (i in tu_vec) {
  tryCatch(
    {
      row <- get_random_word_by_thumbs_up(i)
      avg <- get_ups_average_by_word(row$lowercase_word)
      results <- c(results, avg)
    },
    error = function(cond) 
    {
      message(cond)
      results <- c(results, 0)
    }
  )
  print(results)
}
results

x <- c()
y <- c()
for (i in 1:100) {
  if (!is.na(results[i])) {
    x <- c(x, tu_vec[i])
    y <- c(y, results[i])
  }
}
plot(x, y, main=heading, xlab = "thumbs up Urban", ylab = "thumps up Reddit") 
reg <- lm(y ~ x)
summary(reg)
abline(reg)

get_random_word_by_thumbs_up(97)


get_ups_average_by_word("Krishna")






query <- paste0("SELECT *
                   FROM per_word
                WHERE title LIKE '%Krishna%'
                ")
res <- dbSendQuery(conn = dcon_reddit, query)
mydf <- dbFetch(res, -1)
dbClearResult(res)
head(mydf)
