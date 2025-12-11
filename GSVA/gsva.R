library("BiocManager")
library("GSVA")
library("SummarizedExperiment")
library("GSEABase")
library("tidyverse")
library("purrr")
library("ReactomePA")

# data loading 
data <- read_tsv("data/flatfile/GSE211781_norm_counts_TPM_GRCh38.p13_NCBI.tsv")
data_counts <- read_tsv("data/flatfile/GSE211781_raw_counts_GRCh38.p13_NCBI.tsv")
names_temp <- data |> 
  arrange(GeneID) |> 
  pull("GeneID") |> 
  as.character()
data_matrix <- data |> 
  arrange(GeneID) |> 
  select(-GeneID) |> 
  as.matrix()
rownames(data_matrix) <- names_temp
gene_groups <- data |> 
  arrange(GeneID)
gene_data <- read_tsv("data/flatfile/Human.GRCh38.p13.annot.tsv")
gene_data_list <- gene_data |> 
  group_by(GOProcessID) |> 
  select(GOProcessID, GeneID) |> 
  nest(gene_list = GeneID)  |> 
  rowwise() |> 
  mutate(n = purrr::map(.x = gene_list, .f = ~ length(.x))) |> 
  drop_na() |> 
  unnest(n) |> 
  arrange(desc(n)) |> 
  filter(n > 1) |> 
  mutate(lol = str_count(GOProcessID, "///")) |> 
  filter(lol == 0)

# sample data: 
sample <- c("ATT-ARN.DHT-RNA.3, biol rep 1",	"ATT-ARN.DHT-RNA.7, biol rep 2",	
            "ATT-ARN.VEH-RNA.3C, biol rep 1", "ATT-ARN.VEH-RNA.7, biol rep 2", 
            "ATT-BIC.DHT-RNA.3A, biol rep 1", "ATT-BIC.DHT-RNA.7, biol rep 2", 
            "ATT-BIC.VEH-RNA.3A, biol rep 1", "ATT-BIC.VEH-RNA.7, biol rep 2", 
            "ATT-DHT-RNA.3C, biol rep 1", "ATT-DHT-RNA.7B, biol rep 2", 
            "ATT-ENZ.DHT-RNA.3, biol rep 1", "ATT-ENZ.DHT-RNA.7, biol rep 2", 
            "ATT-ENZ.VEH-RNA.3, biol rep 1", "ATT-ENZ.VEH-RNA.7, biol rep 2", 
            "ATT-VEH-RNA.3A, biol rep 1", "ATT-VEH-RNA.7B, biol rep 2")
assencion	<- c("GSM6500910", "GSM6500911",
               "GSM6500912", "GSM6500913",
               "GSM6500914", "GSM6500915",
               "GSM6500916", "GSM6500917",
               "GSM6500918", "GSM6500919",
               "GSM6500920", "GSM6500921",
               "GSM6500922", "GSM6500923",
               "GSM6500924", "GSM6500925")
sample_short <- c("ARN-DHT_1", "ARN-DHT_2", 
                  "ARN-VEH_1", "ARN-VEH_2", 
                  "BIC-DHT_1", "BIC-DHT_2", 
                  "BIC-VEH_1", "BIC-VEH_2", 
                  "DHT_1", "DHT_2", 
                  "ENZ-DHT_1", "ENZ-DHT_2", 
                  "ENZ-VEH_1", "ENZ-VEH_2", 
                  "VEH_1", "VEH_2")
active_drug <- c("ARN", "ARN", 
  "ARN", "ARN", 
  "BIC", "BIC", 
  "BIC", "BIC", 
  "", "", 
  "ENZ", "ENZ", 
  "ENZ", "ENZ", 
  "", "")
vehicle <- c("DHT", "DHT", 
                  "VEH", "VEH", 
                  "DHT", "DHT", 
                  "VEH", "VEH", 
                  "DHT", "DHT", 
                  "DHT", "DHT", 
                  "VEH", "VEH", 
                  "VEH", "VEH")

ARN <- "Apalutamide"
BIC <- "Bicalutamide"
ENZ <- "Enzalutamide"


# Running gsva
setup_tbl <- tibble(sample, assencion, sample_short, active_drug, vehicle)
gene_set_list <- list()
for (i in 1:length(gene_data_list$GOProcessID)){
  name <- gene_data_list$GOProcessID[i]
  list_d <- gene_data_list$gene_list[i][[1]] |> pull(GeneID) |> list()
  gene_set_list[name] <- list_d
}


# 
gsvsa_data <- gsvaParam(exprData = data_matrix, 
          geneSets = gene_set_list)
results <- gsva(gsvsa_data)
results |> 
  as_tibble() |> 
  pivot_longer(everything()) |> 
  filter(value > 0.8 | value < -0.8) 
