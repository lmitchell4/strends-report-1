# Driver Script to connect to the status and trends postgress db
# and plot some data


# check and install packages -This isnt nice so only check to see if they are there and
# leave it to the user to install them 
packages = c('ggplot2', 'lubridate', 'dplyr', 'dbplyr')

for (package in packages) {
  if (!require(package, character.only=T, quietly=T)) {
#    install.packages(package)
    library(package, character.only=T)
  }
}
#setup db connection and connect
usr = "usr"
dbname = "strends"
pw <- {"your_password"}
pw <- {"pass"}

# query db using dplyr syntax
# Connect to local PostgreSQL via dplyr
con <- src_postgres(dbname = dbname,
                        host = 'localhost',
                        port = 5432,
                        user = usr,
                        password = pw)
# delete the pw from memory for security reasons
rm(pw)

tablenames_filename = "tablenames.txt"
tablenames = read.csv(tablenames_filename, header=FALSE,stringsAsFactors=FALSE)
# define a table to query
wqf_table_name = tablenames[3,"V1"]#"emp_wq_field"
# query emp field water quality data as a tidy dataframe, ala https://dbplyr.tidyverse.org/
wqf_datatbl = tbl(con, wqf_table_name) 
#write a query to calculate the average of all water quality parameters at station d10
station = "D10"
summary = wqf_datatbl %>% 
  filter(StationCode==station)  %>% 
  group_by(AnalyteName) %>% 
  summarise(Result = mean(Result, na.rm = TRUE)) %>% 
  arrange(desc(AnalyteName))
#print the query for QC
summary %>% show_query()
#retrieve the data as a tidy dataframe
wqf_out = summary %>% collect()
#now import a flow timeseries
flow_table_name = tablenames[1,"V1"]#"flow_index"
flow_datatbl = tbl(con, flow_table_name) #write the query
flow_out = flow_datatbl %>% collect() #get the data tinto a tidy datafrae

#convert the non standard date col to a date obj for plotting
flow_out$Datesimple  <-mdy(flow_out$Date)
#plot the data
p = ggplot(data=flow_out, aes(x=Datesimple, y=as.numeric(OUT)))
p + geom_line() + xlab("Date") + ylab("Daily Outflow (cfs)")
