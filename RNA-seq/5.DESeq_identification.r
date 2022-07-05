setwd("C:\\Users\\86188\\Desktop\\work\\xuelab\\p9.LACE-seq_mouse_SRSF1\\RNA-seq\\countDat")

library("DESeq2")
library("RColorBrewer")
library("gplots")
library("amap")
library("ggplot2")

## 1. count data
count <- read.table('./sample_read_count_v1.tsv', header = T, sep = "\t", row.names = 1)
count <- count[,6:11]
colnames(count) <- gsub('^...5.uniq.', '', colnames(count))
colnames(count) <- gsub('.uniq.sort.bam$', '', colnames(count))

## 2. design matrix
design_matrix <- data.frame("condition"=c("Ctrl", "Ctrl", "Ctrl", "KO", "KO", "KO"))
rownames(design_matrix) <- colnames(count)

## 3. pre-processing
dds <- DESeqDataSetFromMatrix(countData = count, colData = design_matrix, design= ~ condition)
dds <- dds[rowSums(counts(dds)) > 0,]

## 4. differential express analysis
dds <- DESeq(dds)
res <- results(dds, name=resultsNames(dds)[2])

baseA <- counts(dds, normalized=TRUE)[, colData(dds)$condition == "Ctrl"]
baseMeanA <- as.data.frame(rowMeans(baseA))
colnames(baseMeanA) <- 'Ctrl'
baseB <- counts(dds, normalized=TRUE)[, colData(dds)$condition == "KO"]
baseMeanB <- as.data.frame(rowMeans(baseB))
colnames(baseMeanB) <- 'KO'
res2 <- cbind(baseMeanA, baseMeanB, as.data.frame(res) )
res2$padj[is.na(res2$padj)] <- 1
res2$pvalue[is.na(res2$pvalue)] <- 1

## 6. volcano plot (p-value, p-adj)
library(ggplot2)
res2$Group <- 'N'
res2$Group[res2$log2FoldChange >= 0.6 & res2$pvalue < 0.05] <- 'Up'
res2$Group[res2$log2FoldChange <= -0.6 & res2$pvalue < 0.05] <- 'Down'
write.table(res2[order(res2$pvalue),], './diff_expr_gene_v1.tsv', quote = F, row.names = T, sep = "\t")

ggplot(res2, aes(y = -log10(res$pvalue), x = res$log2FoldChange, color = Group)) + 
  geom_point(size = 1, alpha = 1) + 
  xlab('log2(FC)') + ylab('log10 Pvalue') + 
  scale_colour_manual(values=c('blue', 'grey60', 'red')) + 
  theme_bw() + xlim(c(-6, 6)) + 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank() ) + 
  annotate('text', 4, 23, label = 'Up   312\nDown 332')

## 7. total PCA
vsd <- vst(dds, blind=FALSE)
pcaData <- plotPCA(vsd, intgroup=c("condition"), returnData = T)
percentVar <- round(100 * attr(pcaData, "percentVar"))
ggplot(pcaData, aes(PC1, PC2, color=condition)) +
  geom_point(size=5) +
  xlab(paste0("PC1: ",percentVar[1],"% variance")) +
  ylab(paste0("PC2: ",percentVar[2],"% variance")) + 
  geom_text(label=rownames(design_matrix), color="black") +
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())

## 8. diff expressed PCA
normalized_counts <- counts(dds, normalized=TRUE)
cor(log2(normalized_counts+0.1), method = "spearman")

write.table(normalized_counts, "./normalized_counts_v1.txt", row.name=T, quote=F, sep="\t")
res_sig <- res2[res2$Group != 'N',]
normalized_counts_sig <- normalized_counts[rownames(res_sig), ]
pca <- prcomp( t(log2(normalized_counts_sig + 1)), scale. = T)
pca_data <- data.frame('PC1' = pca$x[ ,1], 'PC2' = pca$x[ ,2], 'Group'=design_matrix$condition)
colnames(pca_data) <- c('PC1', 'PC2', 'Group')
ggplot(data = pca_data, aes(PC1, PC2, color = Group)) + 
  geom_point( size = 4) +
  #geom_path(data=df_ell, aes(x=PCA1, y=PCA2,colour=group), size=1, linetype=2)+
  #annotate("text",x=PCA.mean$PCA1,y=PCA.mean$PCA2,label=PCA.mean$group)+
  geom_text(data = pca_data, aes(x = PC1, y = PC2, label=rownames(pca_data)), colour = 'black', size = 4) +
  xlab('PC 1') + ylab('PC 2') +
  #xlim(c(-100, 100)) + #ylim(c(-100, 50)) +
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())

library(pheatmap)
a <- normalized_counts_sig[rownames(res_sig),]
anno_row <- as.data.frame(res_sig$Group)
rownames(anno_row) <- rownames(res_sig)
colnames(anno_row) <- " "
norm_a <- log2(a+1)
pheatmap(norm_a, scale = "row", cluster_cols = F,
         #color = colorRampPalette(c("blue", "red"))(21),
         clustering_distance_rows = "correlation",
         clustering_distance_cols = "correlation",
         show_rownames = F,
         annotation_col = design_matrix, 
         annotation_row = anno_row )

library(clusterProfiler)
library(org.Mm.eg.db)
up_gene <- rownames(res_sig[res_sig$Group=="Up", ])
up_gene <- unlist(strsplit(up_gene, ".", fixed=TRUE))[seq(1, length(up_gene)*2, 2)]
down_gene <- rownames(res_sig[res_sig$Group=="Down", ])
down_gene <- unlist(strsplit(down_gene, ".", fixed=TRUE))[seq(1, length(down_gene)*2, 2)]

up_go <- enrichGO(up_gene, OrgDb = org.Mm.eg.db, keyType = "ENSEMBL", ont = "all", 
                  pvalueCutoff = 0.5, qvalueCutoff = 1)
dotplot(up_go, color = "pvalue")

down_go <- enrichGO(down_gene, OrgDb = org.Mm.eg.db, keyType = "ENSEMBL", ont = "all", 
                    pvalueCutoff = 0.5, qvalueCutoff = 1)
dotplot(down_go, color = "pvalue", showCategory=15)


a <- data.frame(up_go)
b <- data.frame(down_go)
write.table(a, file="diff_up_GO.tsv", row.name=T, quote=F, sep="\t")
write.table(b, file="diff_down_GO.tsv", row.name=T, quote=F, sep="\t")



##################################################################
## 删除一个样本
##################################################################
library("DESeq2")
library("RColorBrewer")
library("gplots")
library("amap")
library("ggplot2")





## 1. count data
count <- read.table('./sample_read_count_v1.tsv', header = T, sep = "\t", row.names = 1)
count <- count[,6:11]
colnames(count) <- gsub('^...5.uniq.', '', colnames(count))
colnames(count) <- gsub('.uniq.sort.bam$', '', colnames(count))
count <- count[, -5]


## 2. design matrix
design_matrix <- data.frame("condition"=c("Ctrl", "Ctrl", "Ctrl", "KO", "KO"))
rownames(design_matrix) <- colnames(count)

## 3. pre-processing
dds <- DESeqDataSetFromMatrix(countData = count, colData = design_matrix, design= ~ condition)
dds <- dds[rowSums(counts(dds)) > 0,]

## 4. differential express analysis
dds <- DESeq(dds)
res <- results(dds, name=resultsNames(dds)[2])

baseA <- counts(dds, normalized=TRUE)[, colData(dds)$condition == "Ctrl"]
baseMeanA <- as.data.frame(rowMeans(baseA))
colnames(baseMeanA) <- 'Ctrl'
baseB <- counts(dds, normalized=TRUE)[, colData(dds)$condition == "KO"]
baseMeanB <- as.data.frame(rowMeans(baseB))
colnames(baseMeanB) <- 'KO'
res2 <- cbind(baseMeanA, baseMeanB, as.data.frame(res) )
res2$padj[is.na(res2$padj)] <- 1
res2$pvalue[is.na(res2$pvalue)] <- 1

## 6. volcano plot (p-value, p-adj)
library(ggplot2)
res2$Group <- 'N'
res2$Group[res2$log2FoldChange >= 0.6 & res2$pvalue < 0.05] <- 'Up'
res2$Group[res2$log2FoldChange <= -0.6 & res2$pvalue < 0.05] <- 'Down'
write.table(res2[order(res2$pvalue),], './diff_expr_gene_v1.5sample.tsv', quote = F, row.names = T, sep = "\t")

ggplot(res2, aes(y = -log10(res$pvalue), x = res$log2FoldChange, color = Group)) + 
  geom_point(size = 1, alpha = 1) + 
  xlab('log2(FC)') + ylab('log10 Pvalue') + 
  scale_colour_manual(values=c('blue', 'grey60', 'red')) + 
  theme_bw() + xlim(c(-6, 6)) + ylim(c(0, 30)) +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank() ) + 
  annotate('text', 4, 23, label = 'Up   260\nDown 315')

## 7. total PCA
vsd <- vst(dds, blind=FALSE)
pcaData <- plotPCA(vsd, intgroup=c("condition"), returnData = T)
percentVar <- round(100 * attr(pcaData, "percentVar"))
ggplot(pcaData, aes(PC1, PC2, color=condition)) +
  geom_point(size=5) +
  xlab(paste0("PC1: ",percentVar[1],"% variance")) +
  ylab(paste0("PC2: ",percentVar[2],"% variance")) + 
  geom_text(label=rownames(design_matrix), color="black") +
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())

## 8. diff expressed PCA
normalized_counts <- counts(dds, normalized=TRUE)
cor(log2(normalized_counts+0.1), method = "spearman")









write.table(normalized_counts, "./normalized_counts_v1.5sample.txt", row.name=T, quote=F, sep="\t")
res_sig <- res2[res2$Group != 'N',]
normalized_counts_sig <- normalized_counts[rownames(res_sig), ]
pca <- prcomp( t(log2(normalized_counts_sig + 1)), scale. = T)
pca_data <- data.frame('PC1' = pca$x[ ,1], 'PC2' = pca$x[ ,2], 'Group'=design_matrix$condition)
colnames(pca_data) <- c('PC1', 'PC2', 'Group')
ggplot(data = pca_data, aes(PC1, PC2, color = Group)) + 
  geom_point( size = 4) +
  #geom_path(data=df_ell, aes(x=PCA1, y=PCA2,colour=group), size=1, linetype=2)+
  #annotate("text",x=PCA.mean$PCA1,y=PCA.mean$PCA2,label=PCA.mean$group)+
  geom_text(data = pca_data, aes(x = PC1, y = PC2, label=rownames(pca_data)), colour = 'black', size = 4) +
  xlab('PC 1') + ylab('PC 2') +
  #xlim(c(-100, 100)) + #ylim(c(-100, 50)) +
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())

library(pheatmap)
a <- normalized_counts_sig[rownames(res_sig),]
anno_row <- as.data.frame(res_sig$Group)
rownames(anno_row) <- rownames(res_sig)
colnames(anno_row) <- " "
norm_a <- log2(a+1)
pheatmap(norm_a, scale = "row", cluster_cols = F,
         #color = colorRampPalette(c("blue", "red"))(21),
         clustering_distance_rows = "correlation",
         clustering_distance_cols = "correlation",
         show_rownames = F,
         annotation_col = design_matrix, 
         annotation_row = anno_row )

library(clusterProfiler)
library(org.Mm.eg.db)
up_gene <- rownames(res_sig[res_sig$Group=="Up", ])
up_gene <- unlist(strsplit(up_gene, ".", fixed=TRUE))[seq(1, length(up_gene)*2, 2)]
down_gene <- rownames(res_sig[res_sig$Group=="Down", ])
down_gene <- unlist(strsplit(down_gene, ".", fixed=TRUE))[seq(1, length(down_gene)*2, 2)]

up_go <- enrichGO(up_gene, OrgDb = org.Mm.eg.db, keyType = "ENSEMBL", ont = "all", 
                  pvalueCutoff = 0.5, qvalueCutoff = 1)
dotplot(up_go, color = "pvalue")

down_go <- enrichGO(down_gene, OrgDb = org.Mm.eg.db, keyType = "ENSEMBL", ont = "all", 
                  pvalueCutoff = 0.5, qvalueCutoff = 1)
dotplot(down_go, color = "pvalue", showCategory=15)


a <- data.frame(up_go)
b <- data.frame(down_go)
write.table(a, file="5sample_diff_up_GO.tsv", row.name=T, quote=F, sep="\t")
write.table(b, file="5sample_diff_down_GO.tsv", row.name=T, quote=F, sep="\t")











