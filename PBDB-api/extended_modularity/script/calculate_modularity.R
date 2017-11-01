# Author: Hao Zhong
# Date: October 12, 2017

# Clear memory (Caution: This clears up all variables in RStudio memory)
rm(list = ls())

# Set path
setwd("/Users/Hao/Projects/dtdi-api/PBDB-api/extended_modularity")

# Import data
library(readxl)
filename = "sample.xlsx"  # Input file name

# Note 1: You may only change the input file name each time and then run rest of 
#       the scripts as an unchanged bulk, which will give you modularity score
#       on the current input file

# Note 2: Input file format requirements:
#       The input .xlsx file should contain 2 sheets, namely "edge_list" and "community_list"
#       The sheet "edge_list" should contain 3 columns, namely: "from", "to", and "value" (= 0 or 1)
#       The sheet "community_list" should contain 3 columns, namely: "taxon", "group", "coefficient" (i.e. the "belong coefficient")

# Mote 3: The input file should be under directory "data/", as implied below

# Read the input file under directory "date/"
edge.list <- read_excel(paste("data/", filename, sep = ""), sheet = "edge_list")
community.list <- read_excel(paste("data/", filename, sep = ""), sheet = "community_list")[1:3]

# Retain only NONZERO edges connecting DISTINCT nodes
edge.list <- edge.list[which(edge.list$from != edge.list$to & edge.list$value != 0), ]

# Retain only taxon-group information with NONZERO coefficients, i.e. nodes 
#   actually belonging to the communites.
community.list <- community.list[which(community.list$coefficient != 0), ]

# |E| = number of all edges
E <- sum(edge.list$value[which(edge.list$from != edge.list$to)])

# Merge the community information into the edge list
suppressPackageStartupMessages(library(dplyr))
merged <- left_join(edge.list, community.list, by = c("from" = "taxon"))
merged <- left_join(merged, community.list, by = c("to" = "taxon"), suffix = c(".from", ".to"))

# Define f
f <- function(x, y){x * y}

# Initialize Q = 0
Q <- 0
for (c in  unique(community.list$group)){
  in.indices <- which(merged$group.from == c & merged$group.to == c)
  out.indices <- which(merged$group.from == c & merged$group.to != c)
  in.edges <- merged[in.indices, ]
  out.edges <- merged[out.indices, ]
  E.in <- 0.5 * sum(in.edges$value * f(in.edges$coefficient.from, in.edges$coefficient.to))
  E.out <- sum(out.edges$value * f(out.edges$coefficient.from, out.edges$coefficient.to))
  Q <- Q + (E.in/E) - ( (2*E.in + E.out)/( 2*E ) )^2
}

# View result:
Q