# Driver Script to connect to the status and trends postgress db
# and plot some data


# check and install packages
packages = c('DBI', 'RPostgres', 'ggplot2','lubridate')
for (package in packages) {
  if (!require(package, character.only=T, quietly=T)) {
    install.packages(package)
    library(package, character.only=T)
  }
}
#setup db connection and connect
usr = "usr"
pw <- {"your_password"}
pw <- {"pass"}
con <- dbConnect(RPostgres::Postgres(), dbname = "strends", host = "localhost",
          port = 5432, password = pw, user = usr,
          bigint = c("integer64", "integer", "numeric", "character"))
# delte the pw from memory
rm(pw)
# check for the flow_index table
table_name = "flow_index"
# construct a SQL query 
query_str =paste("SELECT * from", table_name)
# query data and load into a daframe
if(dbExistsTable(con, table_name)==TRUE){
  # query the data from postgreSQL 
  df_postgres <- dbGetQuery(con,query_str )
}
#convert the non standard date col to a date obj for plotting
df_postgres$Datesimple  <-mdy(df_postgres$Date)
#plot the data
p = ggplot(data=df_postgres, aes(x=Datesimple, y=as.numeric(OUT)))
p + geom_line() + xlab("Date") + ylab("Daily Outflow (cfs)")
