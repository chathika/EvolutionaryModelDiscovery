
	simplify <- function(factors) {
###	install.packages("stringr", repos = "http://cran.us.r-project.org")
	library(stringr)
	  factors_ = factors
	  if (factors_[2] != "-" && factors_[2] != "+" && factors_[3] != ">") {
		#if there is no sign in the first element, add plus
		factors_ = append(factors_, c("<","+",">"), after = 0)
		
	  } 
	  if ((factors_[2] == "-" || factors_[2] == "+") && factors[4] == "(" ) {
		#remove covering bracket 
		sign_ = factors_[1:3]
		
		factors_ = factors_[6:length(factors_)-1]
		factors_ = c(sign_,factors_)
	  } 
	  
	  invert = ifelse(factors_[2] == "-",TRUE, FALSE)
	  if(invert){
		k = 4
		while (k <= length(factors_)) {
		  if (factors_[k] == "("){
			#this is a complex term... skip it
			#jump to end of term 
			bracket_residue = 1
			l = k + 1
			while (l <= length(factors_)) {
			  if (factors_[l] == "(") {
				bracket_residue = bracket_residue + 1
			  } else if (factors_[l] == ")") {
				bracket_residue = bracket_residue - 1
			  }
			  if (bracket_residue == 0) {
				break
			  }
			  l = l + 1
			}
			k = l
		  } else if (factors_[k] == "+") {
			factors_[k] = "-"
		  } else if (factors_[k] == "-") {
			factors_[k] = "+"
		  }
		  k = k + 1
		}
	  }
	  ## any more brackets?
	  m = 1
	  while (m <= length(factors_)) {
		if (factors_[m] == "(") {
		  
		  bracket_residue = 1
		  n = m + 1
		  while (n <= length(factors_)) {
			if (factors_[n] == "(") {
			  bracket_residue = bracket_residue + 1
			} else if (factors_[n] == ")") {
			  bracket_residue = bracket_residue - 1
			}
			if (bracket_residue == 0) {
			  break
			}
			n = n + 1
		  }
		  factors_ = c(factors_[c(0:(m-4))], simplify(factors_[(m-3):n]),  factors_[c(n:length(factors_)+1)] )
		  factors_ = factors_[!is.na(factors_)]
		}
		
		m = m + 1
	  }
	  return (factors_)
	}

parse_and_count <- function(chunk_id) {
##install.packages("stringr", repos = "http://cran.us.r-project.org")
	library(stringr)
	EMD_Results_ = read.csv( paste("AA_10EMDRuns_AllIndividuals_FANOVA_chunk" , chunk_id , ".csv", sep= ""))

	print(paste("done reading chunk", chunk_id))
	#######Build factor vector####################
	factor_names = c("<CompareQuality>","<CompareDryness>","<CompareYield>","<CompareWater>","<CompareDistance>","<HomophilyAge>","<HomophilyCornStocks>","<SocialPresence>","<flee-migrate>")
	factor_and_interaction_names = c()
	for(factor_name_i in factor_names) {
	  factor_and_interaction_names = c(factor_and_interaction_names,(paste("<+>",factor_name_i, sep = "")))
	  factor_and_interaction_names = c(factor_and_interaction_names,(paste("<->",factor_name_i, sep = "")))
	}
	for(factor_name_i in factor_names) {
	  for(factor_name_j in factor_names) {
		factor_and_interaction_names = c(factor_and_interaction_names,(paste("<+>",factor_name_i , "</>", factor_name_j, sep = "")))
		factor_and_interaction_names = c(factor_and_interaction_names,(paste("<+>",factor_name_i , "<*>", factor_name_j, sep = "")))
		factor_and_interaction_names = c(factor_and_interaction_names,(paste("<->",factor_name_i , "</>", factor_name_j, sep = "")))
		factor_and_interaction_names = c(factor_and_interaction_names,(paste("<->",factor_name_i , "<*>", factor_name_j, sep = "")))
	  }
	}
	factor_and_interaction_counts = setNames(data.frame(matrix(ncol = length(factor_and_interaction_names) + 1 , nrow = 0)), c("gp_syntax",factor_and_interaction_names))
	
	
	iteration = 1
	for (gp_syntax_tree in EMD_Results_$IndividualSyntaxLogic) {
		print(iteration)
		iteration = iteration + 1
	  split_syntax = strsplit(gp_syntax_tree, "\\[")
	  #handle min/max
	  min_or_max = 0
	  switch (substr(split_syntax[[1]][1], 2, 4) , 
		"max" = (min_or_max = 1), 
		"min" = (min_or_max = -1)
		)
	  #handle connectivity
	  #connectivity_string = strsplit(split_syntax[[1]][1], ">\\s*\\(<")[[1]][2]
	  #connectivity_string = substr(connectivity_string,1,nchar(connectivity_string)-3) 
	  #switch (connectivity_string , 
		#"AllPotentialFarms" = print(1), 
		#"PotentialFarmsNearFamily" = print(2),
		#"PotentialFarmsNearNeighbors" = print(3),
		#"PotentialFarmsNearBestPerformers" = print(4)
	  #)
	  #handle factors
	  factors_str = substr(split_syntax[[1]][2], 1, nchar(split_syntax[[1]][2])-1)
	  if(!grepl("\\(",factors_str)){
		factors_str = paste("(",factors_str,")", sep = "")
	  }
	  factors_str = strsplit(factors_str, "")[[1]]
	  factors_str = paste(simplify(factors_str),collapse="")
	  #Count linear components 
	  factor_and_interaction_counts_i = setNames(data.frame(matrix(ncol = length(factor_and_interaction_names) + 1 , nrow = 0)), c("gp_syntax",factor_and_interaction_names))
	  for (i in 1:length(factor_and_interaction_names)) {
		search_string = toString(factor_and_interaction_names[i])
		if(min_or_max == -1) {
		  if(substr(search_string,2,2) == "-") {search_string = paste("<+>",substr(search_string,4,nchar(search_string)),sep = "")} else 
		  if(substr(search_string,2,2) == "+") {search_string = paste("<->",substr(search_string,4,nchar(search_string)),sep = "")}
		} 
		if(str_count (search_string, "[*/]") == 0) {
			string_to_check = str_replace_all(factors_str, "<[+-]*><[:alnum:]*><\\*><[:alnum:]*>", "")
			factor_and_interaction_counts_i[1,(i+1)] = str_count(string_to_check, coll(search_string))
		} else {
			factor_and_interaction_counts_i[1,(i+1)] = str_count(factors_str, coll(search_string))
		}
	  }
	  factor_and_interaction_counts_i[1,1] = gp_syntax_tree
	  factor_and_interaction_counts = rbind(factor_and_interaction_counts, factor_and_interaction_counts_i)
	  #print(factor_and_interaction_counts_i)
	}
	#write out the results
	write.csv(factor_and_interaction_counts, paste("factor_and_interaction_counts", chunk_id, ".csv", sep = ""))
}


all_data = read.csv("AA_10EMDRuns_AllIndividuals_FANOVA.csv")
#Chunk the data by processors
#find processor count 
library(parallel)
#library(foreach)
no_cores = 72#detectCores() - 1  #EC2 instance had two nodes but was not detected :-/
chunk_size = nrow(all_data) / no_cores
n_chunks = no_cores

#chunk the data and write
for(chunk_i in 1:n_chunks) {
	chunk_start = floor((chunk_i - 1) * chunk_size + 1	)
	chunk_end = floor(chunk_i * chunk_size)
	if (chunk_i == n_chunks) {
		chunk_end = nrow(all_data)
	}
	chunk = all_data[chunk_start:chunk_end,]
	print (paste ("From rows ", chunk_start, " to " , chunk_end))
	chunk_size_i = nrow(chunk)
	print(paste("Size of chunk ", chunk_size_i))
	write.csv(chunk, paste("AA_10EMDRuns_AllIndividuals_FANOVA_chunk" , chunk_i , ".csv", sep= ""))
}

#make cluster
cl = makeForkCluster(no_cores)
#doParallel::registerDoParallel(cl)

print ("cluster ready... processing")
#read all chunks and process in parallel.
parLapply(cl,1:n_chunks, parse_and_count)
stopCluster(cl)

#read back in and aggregate in order
col_names = colnames(read.csv(paste("factor_and_interaction_counts1.csv" , chunk_i , ".csv", sep= "")))
all_results = setNames(data.frame(matrix(ncol = length(col_names), nrow = 0)), col_names)
for(chunk_i in 1:n_chunks) {
	all_results = rbind(all_results,read.csv(paste("AA_10EMDRuns_AllIndividuals_FANOVA_chunk" , chunk_i , ".csv", sep= "")))
}

write.csv(all_results, "all_results.csv")

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
  