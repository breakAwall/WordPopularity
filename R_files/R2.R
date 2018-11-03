library(RSQLite)
setwd("C://Users//kgoel//Desktop//Y3 Sem1//Stat 405//Overall Project")

dcon <- dbConnect(SQLite(), dbname = "youtubelite.sqlite")

dbListTables(dcon)
dbListFields(dcon, "youtube_entries")

res <- dbSendQuery(conn = dcon, "
SELECT *
                   FROM youtube_entries
                   ")
mydf <- dbFetch(res, -1)
dbClearResult(res)
head(mydf)

View(mydf)

dbDisconnect(dcon)
