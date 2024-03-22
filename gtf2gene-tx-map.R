#!/usr/bin/Rscript

#####################
# GTF 2 GENE-TX MAP #
#####################

library(GenomicFeatures)
library(rtracklayer)
library(dplyr)
library(stringr)

args <- commandArgs(trailingOnly = TRUE)

file_path <- args[1]

if (is.na(file_path) || file_path == "-help" || file_path == "-h"){
  cat(" COMMAND : Rscript gtf2gene-tx-map.R <PATH/TO/TARGet/GTF/FILE>
      ")
  quit(save="no")
}

gtf <- import.gff(file_path)
mapping <- data.frame(
  transcript_id = mcols(gtf)$transcript_id,
  gene_id = mcols(gtf)$gene_id
)

mapping <- mapping %>%
  mutate(transcript_id = str_extract(transcript_id, "[^|]+$"))

mapping <- mapping[,c(2, 1)]

write.table(mapping, file = "output_mapping.txt", sep = "\t", quote = FALSE, row.names = FALSE, eol = "\n")
























