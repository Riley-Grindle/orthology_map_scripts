############################
## HEXADECIMAL Correction ##
############################

library(stringr)

args <- commandArgs(trailingOnly = TRUE)

fasta_path <- args[1]
gene_path <- args[2]
out_path <- args[3]

if (is.na(fasta_path) || fasta_path == "-help" || fasta_path == "-h"){
  cat(" COMMAND : Rscript tree_post.R <PATH/TO/TARGET/FASTA/FILES> <PATH/TO/HEADER_DIR> <PATH/TO/OUTS_TABLE>
      ")
  quit(save="no")
}

file_list <- list.files(fasta_path) 
genes_list <- list.files(gene_path)

loger_out <- read.csv(paste0(out_path, "ortho_l_std.csv"))

search_ids <- c()
for (file in file_list){
  temp_str <- unlist(strsplit(file, ".", fixed = TRUE))
  search_ids <- append(search_ids, temp_str[1])
}

replacement_list <- c()
for (file in genes_list){
  replacement_list <- append(replacement_list, read.csv(paste0(gene_path, file), header = FALSE))
}

loger_out$FASTA <- unlist(strsplit(loger_out$MATCH, ":"))[c(TRUE, FALSE)]
loger_out$HEXI_M <- unlist(strsplit(loger_out$MATCH, ":"))[c(FALSE, TRUE)]

revised_names <- c()
for (i in 1:nrow(loger_out)){
  replacement_idx <- as.numeric(which(search_ids == loger_out$FASTA[i]))
  if (substr(loger_out$HEXI_M[i],nchar(loger_out$HEXI_M[i]), nchar(loger_out$HEXI_M[i])) == " "){
    hexi <- substr(loger_out$HEXI_M[i],1, nchar(loger_out$HEXI_M[i])-1)
  }else{
    hexi <- substr(loger_out$HEXI_M[i],1, nchar(loger_out$HEXI_M[i]))
  }
  hex_idx <- as.numeric(strtoi(hexi, base = 16))
  hex_idx <- hex_idx + 1
  revised_names <- append(revised_names, substr(unlist(replacement_list[replacement_idx])[hex_idx], 2, nchar(unlist(replacement_list[replacement_idx])[hex_idx])))
  
}

revised_names <- as.data.frame(revised_names)


for (i in 1:nrow(loger_out)){
  temp_str <- loger_out$QUERY[i]
  temp_list <- unlist(strsplit(temp_str, ":"))
  replacement_idx <- as.numeric(which(search_ids == temp_list[1]))
  hex_idx <- as.numeric(strtoi(temp_list[2], base = 16))
  hex_idx <- hex_idx + 1
  if (temp_list[1] != "   "){
    loger_out$QUERY[i] <- substr(unlist(replacement_list[replacement_idx])[hex_idx], 2, nchar(unlist(replacement_list[replacement_idx])[hex_idx]))
  }
}

new_table <- cbind(loger_out$QUERY, revised_names[,1])

colnames(new_table) <- c("QUERY", "MATCH")

new_table <- as.data.frame(new_table)
# Extract Gene name from sequence headers
get_gene_info <- function(id) {
  result <- sub(".*GN=", "", id)
  
  return(result)
}

# Extract Taxa id from sequence headers
get_taxa_info <- function(id) {
  result <- sub(".*OX=(.*?)_.*", "\\1", id)
  
  return(result)
}

gene_list <- lapply(new_table$MATCH, get_gene_info)
taxa_list <- lapply(new_table$MATCH, get_taxa_info)

newest_table <- cbind(new_table, unlist(gene_list), unlist(taxa_list))
colnames(newest_table) <- c("QUERY", "MATCH", "GENE", "SPECIES")


write.csv(newest_table, file = "./ortho_l_std.csv", row.names = FALSE)


