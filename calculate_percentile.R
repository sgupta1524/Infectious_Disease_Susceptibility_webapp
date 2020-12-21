args = commandArgs(trailingOnly=TRUE)

data_table <- read.table(args[1],header = TRUE)
percentile <- ecdf(data_table$PRScore) 
output <- percentile(args[2])
write.table(output,args[3],sep = "")

