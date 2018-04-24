##########################factors parsed... read and prepare###########################
factor_and_interaction_counts = read.csv("factor_and_interaction_counts.csv")
#rename columns to be R legible
factor_names = c("CompareQuality","CompareDryness","CompareYield","CompareWater","CompareDistance","HomophilyAge","HomophilyCornStocks","SocialPresence","flee-migrate")
factor_and_interaction_names = c()

for(factor_name_i in factor_names) {
  factor_and_interaction_names = c(factor_and_interaction_names,(paste("pos.",factor_name_i, sep = "")))
  factor_and_interaction_names = c(factor_and_interaction_names,(paste("neg.",factor_name_i, sep = "")))
}
for(factor_name_i in factor_names) {
  for(factor_name_j in factor_names) {
    factor_and_interaction_names = c(factor_and_interaction_names,(paste("pos.",factor_name_i , ".div.", factor_name_j, sep = "")))
    factor_and_interaction_names = c(factor_and_interaction_names,(paste("pos.",factor_name_i , ".mul.", factor_name_j, sep = "")))
    factor_and_interaction_names = c(factor_and_interaction_names,(paste("neg.",factor_name_i , ".div.", factor_name_j, sep = "")))
    factor_and_interaction_names = c(factor_and_interaction_names,(paste("neg.",factor_name_i , ".mul.", factor_name_j, sep = "")))
  }
}
factor_and_interaction_counts = factor_and_interaction_counts[3:ncol(factor_and_interaction_counts)]
colnames(factor_and_interaction_counts) = c("gp.syntax", factor_and_interaction_names)
#simplify multiplications
col_i = 1
while(col_i < ncol(factor_and_interaction_counts)){
  col_name = colnames(factor_and_interaction_counts)[col_i]
  if (str_count(col_name, coll(".mul.")) > 0) {
print("pair")
        print(col_name)
#    print(str_locate_all(col_name,coll(".")))
    sign = substr(colnames(factor_and_interaction_counts)[col_i], 1,3)
    term1 = substr(colnames(factor_and_interaction_counts)[col_i], 5,as.numeric(str_locate_all(col_name,coll("."))[[1]][2,1]) - 1)
    term2 = substr(colnames(factor_and_interaction_counts)[col_i], as.numeric(str_locate_all(col_name,coll("."))[[1]][3,1]) + 1, nchar(col_name))
    other_col = which(colnames(factor_and_interaction_counts) == paste(sign, ".", term2,".mul.",term1, sep = ""))
    print(colnames(factor_and_interaction_counts)[other_col])
    exists = identical(colnames(factor_and_interaction_counts)[other_col],  character(0))
    if(!exists && col_i != other_col) {
      print("remove")
      factor_and_interaction_counts[,col_i] = factor_and_interaction_counts[,col_i] + factor_and_interaction_counts[,other_col]
      factor_and_interaction_counts = factor_and_interaction_counts[,-other_col] 
    }
  }
  col_i = col_i + 1
}
############################handle connectivity###############
connectivity_names = c("AllPotentialFarms","PotentialFarmsNearFamily","PotentialFarmsNearNeighbors","PotentialFarmsNearBestPerformers")
connectivities = setNames(data.frame(matrix(ncol = length(connectivity_names), nrow = 0)), connectivity_names)
iteration = 1
for (gp_syntax_tree in factor_and_interaction_counts$gp.syntax) {
  print(iteration)
  iteration = iteration + 1
  split_syntax = strsplit(gp_syntax_tree, "\\[")
  connectivity_string = strsplit(split_syntax[[1]][1], ">\\s*\\(<")[[1]][2]
  connectivity_string = substr(connectivity_string,1,nchar(connectivity_string)-3) 
  connectivities_i = data.frame("AllPotentialFarms" = c(0),"PotentialFarmsNearFamily" = c(0),"PotentialFarmsNearNeighbors" = c(0),"PotentialFarmsNearBestPerformers" = c(0))
  switch (connectivity_string , 
    "AllPotentialFarms" = (connectivities_i[1,1] = 1), 
    "PotentialFarmsNearFamily" = (connectivities_i[1,1] = 1),
    "PotentialFarmsNearNeighbors" = (connectivities_i[1,1] = 1),
    "PotentialFarmsNearBestPerformers" = (connectivities_i[1,1] = 1)
  )
  print (connectivities_i)
  connectivities = rbind(connectivities, connectivities_i)
}
AA_10EMDRuns_AllIndividuals_connectivity_and_factor_counts= cbind(AA_10EMDRuns_AllIndividuals_FANOVA, connectivities, factor_and_interaction_counts[,2:ncol(factor_and_interaction_counts)])

###build presence table
factor_and_interaction_presence = factor_and_interaction_counts
for (i in 1:nrow(factor_and_interaction_presence)){
  for (j in 2:ncol(factor_and_interaction_presence)){
    if (factor_and_interaction_presence[i,j] > 0) {
      factor_and_interaction_presence[i,j] = 1
    }
  }
}
AA_10EMDRuns_AllIndividuals_connectivity_and_factor_presence= cbind(AA_10EMDRuns_AllIndividuals_FANOVA, connectivities, factor_and_interaction_presence[,2:ncol(factor_and_interaction_presence)])
#Now write everything out...
write.csv(AA_10EMDRuns_AllIndividuals_connectivity_and_factor_counts, "AA_10EMDRuns_AllIndividuals_connectivity_and_factor_counts.csv")
write.csv(AA_10EMDRuns_AllIndividuals_connectivity_and_factor_presence, "AA_10EMDRuns_AllIndividuals_connectivity_and_factor_presence.csv")

##############Break into file per gp run###############################
for (run_id in unique(AA_10EMDRuns_AllIndividuals_connectivity_and_factor_counts$Run)){
  write.csv(subset(AA_10EMDRuns_AllIndividuals_connectivity_and_factor_counts, Run == run_id), paste("AA_EMDRun",run_id,"_AllIndividuals_connectivity_and_factor_counts.csv",sep = ""))
}
for (run_id in unique(AA_10EMDRuns_AllIndividuals_connectivity_and_factor_presence$Run)){
  write.csv(subset(AA_10EMDRuns_AllIndividuals_connectivity_and_factor_presence, Run == run_id), paste("AA_EMDRun",run_id,"_AllIndividuals_connectivity_and_factor_presence.csv",sep = ""))
}



#################graph results###################################
t =AA_10EMDRuns_AllIndividuals_connectivity_and_factor_counts[,c(5,11:28)]

i = 2
while (i < ncol(t)){
  effective_pos = t[,i] - t[,i+1]
  effective_neg = t[,i+1] - t[,i]
  t[,i] = effective_pos
  t[,i+1] = effective_neg
  i = i + 2
}
t = t[,c(1,2,4,6,8,10,12,14,16,18)]


t = melt(t, id.vars = c("L2.error"), variable.name = "factor_", value.name = "count")
t$factor_ = gsub("Compare", "", t$factor_)
t$factor_ = gsub("pos.", "", t$factor_)
max_count = max(t$count)
t$factor.importance = (1 - t$L2.error / 5000) * t$count / max_count
ggplot(subset(t, L2.error < 1200), aes(factor_, factor.importance)) + geom_boxplot() #+ xlim(-20,20) + ylim(0,1)


s = AA_10EMDRuns_AllIndividuals_connectivity_and_factor_counts[,c(5,29:ncol(AA_10EMDRuns_AllIndividuals_connectivity_and_factor_counts))]

i = 2
while (i < ncol(s)){
  effective_pos = s[,i] - s[,i+2]
  effective_neg = s[,i+2] - s[,i]
  s[,i] = effective_pos
  s[,i+1] = effective_neg
  i = i + 1
  effective_pos = s[,i] - s[,i+2]
  effective_neg = s[,i+2] - s[,i]
  s[,i] = effective_pos
  s[,i+1] = effective_neg
  i = i + 3
}
col_i = 1
while(col_i <= ncol(s)){
  col_name = colnames(s)[col_i]
  if (str_count(col_name, coll("neg.")) > 0) {
    print("neg")
    print(col_name)
    print("remove")
    s = s[,-col_i] 
    
  } else {col_i = col_i + 1}
}
  colnames(s)
  s = melt(s, id.vars = c("L2.error"), variable.name = "factor", value.name = "count")
  max_count = max(s$count)
  s$factor.importance = (1 - s$L2.error / 5000) * s$count / max_count
  x = subset(s, L2.error < 1200)
  i = rep(1,nrow(x))
  ggplot(x, aes(i,factor.importance, group = i)) + geom_point(outlier.shape = NA) + ylim(-0.1,0.1) + facet_wrap(~factor)
  