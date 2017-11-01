library(paleobioDB)
library(readr)

rm(list = ls())
taxa <- read_csv("~/Projects/dtdi-api/PBDB-api/get_pbdb_data_by_taxa_no/data/large list_marine genera.csv")
df <- read_csv("~/Projects/dtdi-api/PBDB-api/get_pbdb_data_by_taxa_no/data/PBDB_output_all.csv")

df$paleolat <- as.numeric(df$paleolat)
df$paleolng <- as.numeric(df$paleolng)
df <- df[which(!is.na(df$paleolat) & !is.na(df$paleolng)), ]
df <- df[which(df$paleolng != 0 & df$paleolat != 0), ]

df_subset <- df[which(df$accepted_no %in% taxa$taxon_no |
                        df$phylum_no %in% taxa$taxon_no |
                        df$class_no %in% taxa$taxon_no |
                        df$order_no %in% taxa$taxon_no |
                        df$family_no %in% taxa$taxon_no |
                        df$genus_no %in% taxa$taxon_no |
                        df$subgenus_no %in% taxa$taxon_no), ]

adjacency_matrix <- matrix(nrow = nrow(taxa), ncol = nrow(taxa),
                           dimnames = list(taxa$taxon_no, taxa$taxon_no))
