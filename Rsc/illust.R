file <-  sprintf("../pysc/%s.csv", pid)
X <- as.matrix(read.csv(file, header=TRUE, row.names=1))

tmp <- colnames(X)
tmp2 <- rownames(X)

tmp <- names(rev(sort(apply(X, 1, mean)))[1:2000])
X<-X[tmp,]
rcol <- c()
dr <- c()

for (i in 1:length(tmp)) {
  a <- substring(tmp[i], 1, 1)
  if (a == "D"){
    rcol[tmp[i]] <- "blue"
    dr <- append(dr, tmp[i])
  }
  if (a == "N"){
    rcol[tmp[i]] <- "LightGrey"
  }
}
hfile <-  sprintf("../pdfstore/%s_h.pdf", pid)
pdf(hfile)
heatmap(X,col=c("LightGrey", "red"), hclustfun = function(X) { hclust(X, method = "ward.D") }, scale = c("none"), RowSideColors=rcol)
dev.off()

W <- which(apply(X, 1, mean) >= 0.05)
S <- sample(names(W), 256, replace=F)
X <- X[S,]
tfile <-  sprintf("../txtstore/%s_s.txt", pid)
write.table(X, tfile, quote=F, row.names=T, col.names=T, sep="\t", append=F)
