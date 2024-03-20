############################
####### TREEGRAFTER ########
############################

library(stringr)

args <- commandArgs(trailingOnly = TRUE)

file_path <- args[1]

if (is.na(file_path) || file_path == "-help" || file_path == "-h"){
  cat(" COMMAND : Rscript tree_post.R <PATH/TO/TARGET/ORTHOLOG/FILES>
      ")
  quit(save="no")
}

file_name <- list.files(file_path)

# READ in ortholog results from Treegraft run 
if (substr(file_path, nchar(file_path), nchar(file_path)) == "/"){
  raw_table <- read.csv(paste0(file_path,file_name), header = FALSE)
}else{
  raw_table <- read.csv(paste0(file_path, "/",file_name), header = FALSE)
}

raw_table <- as.data.frame(raw_table[,-2])

# Delete Spacer Rows
delete_rows <- c()

for (i in 1:nrow(raw_table)){
  if (substr(raw_table[i,1], 1, 3) == "___" ){
    delete_rows <- append(delete_rows, i)
  }
}

raw_table <- raw_table[-delete_rows,]
raw_table <- as.data.frame(raw_table)

# Format in QUERY - MATCH data frame
new_table <- as.data.frame(matrix(nrow=0, ncol=2))

for (i in 1:nrow(raw_table)){
  temp_str <- raw_table[i,1]
  addition <- c()
  if (substr(temp_str, 1, 7) != "gene_id"){
    if (i < nrow(raw_table) && substr(raw_table[i+1,1], 1, 7) == "gene_id"){
      addition <- c(str_trim(gsub("_", "|", temp_str)), substr(raw_table[i+1, 1], 9, nchar(raw_table[i+1, 1])))
      new_table <- rbind(new_table, addition)
    }else{
      addition <- c(str_trim(gsub("_", "|", temp_str)), "NO MATCH")
      new_table <- rbind(new_table, addition)
    }
  }else{
    for (j in 1:ncol(raw_table)){
      addition <- c("     ", substr(raw_table[i, j], 9, nchar(raw_table[i, j])))
      new_table <- rbind(new_table, addition)
    }
  }
}

colnames(new_table) <- c("QUERY", "MATCH")

write.csv(new_table, file = "./tree_std.csv", col.names = TRUE, row.names = FALSE)








