############################
####### ORTHOLOGER  ########
############################

library(stringr)

args <- commandArgs(trailingOnly = TRUE)

file_path <- args[1]
prefix <- args[2]

if (is.na(file_path) || is.na(prefix) || file_path == "-help" || file_path == "-h"){
  cat(" COMMAND : Rscript tree_post.R <PATH/TO/TARGET/ORTHOLOG/FILES> <prefix_of_.fasta>
      ")
  quit(save="no")
}

file_name <- list.files(file_path)

# READ in ortholog results from Orthologer run
if (substr(file_path, nchar(file_path), nchar(file_path)) == "/"){
  raw_table <- read.csv(paste0(file_path,file_name), header = FALSE, sep = ' ')
}else{
  raw_table <- read.csv(paste0(file_path, "/",file_name), header = FALSE, sep = ' ')
}

raw_table <- raw_table[-c(1:9,(nrow(raw_table)-1), nrow(raw_table)), -c(3:ncol(raw_table))]

new_table <- data.frame(matrix(ncol=3, nrow=0))
query_index <- c()
for (i in 1:nrow(raw_table)){
  temp_str <- raw_table[,2][i]
  if (substr(temp_str,1,nchar(prefix)) == prefix){
    query_index <- append(query_index, i)
  }
}

for (i in 1:length(query_index)){
  new_table <- rbind(new_table, c(raw_table[query_index[i],]))
}

new_table$V3 <- " "
raw_table <- raw_table[-c(query_index),]

newest_table <- data.frame(matrix(ncol=3, nrow=0))
counter <- 1
for (i in 1:nrow(new_table)){
  key = 0
  group <- new_table[,1][i]
  for (j in 1:nrow(raw_table)){
    if (raw_table[,1][j] == group){
      print(group)
      if (key == 0){
        newest_table <- rbind(newest_table, c(group, new_table[,2][i], substr(raw_table[,2][j], 1, nchar(raw_table[,2][j]))))
        key = 1
      }else{
        newest_table <- rbind(newest_table, c("   ", "   ", substr(raw_table[,2][j], 1, nchar(raw_table[,2][j]))))
        }
    }
  }
}

new_table <- newest_table[,-1]


colnames(new_table) <- c("QUERY", "MATCH")


write.csv(new_table, file = "./ortho_l_std.csv", col.names = TRUE, row.names = FALSE)








