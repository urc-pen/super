library(ape)
file <-  sprintf("%s", newicktxt)
tree <- read.tree(file)
treefile <-  sprintf("%s.pdf", treepre)
pdf(treefile)
plot(
  tree,                    # read.treeで読み込んだデータ
  type = "cladogram",      # phylogram, cladogram, fan, unrooted, radial を指定することができる
  use.edge.length = TRUE,  # FALSE を指定すると、枝の長さは距離情報を含まなくなる！
  show.tip.label = TRUE,   # 葉のラベルを表示する
  show.node.label = F,  # ノードのラベルを表示
  edge.color = "black",    # 枝の色
  edge.width = 1,          # 枝の太さ
  edge.lty = 1,            # 枝の種類（実線、点線など）
  root.edge = TRUE,        # 根を表示する
  tip.color = "black"      # 葉の色
)
dev.off()
