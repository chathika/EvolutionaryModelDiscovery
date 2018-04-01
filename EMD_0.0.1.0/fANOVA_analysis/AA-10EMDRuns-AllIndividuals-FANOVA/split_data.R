all_data = read.csv("AA_10EMDRuns_AllIndividuals_FANOVA.csv")
chunk_size = 100000
n_chunks = nrow(all_data) / chunk_size

for(chunk_i in 1:n_chunks) {
	chunk_start = (chunk_i - 1) * chunk_size + 1
	chunk_end = chunk_i * chunk_size
	chunk = all_data[chunk_start:chunk_end,]
	print (paste ("From rows ", chunk_start, " to " , chunk_end))
	chunk_size_i = nrow(chunk)
	print(paste("Size of chunk ", chunk_size_i))
	write.csv(chunk, paste("AA_10EMDRuns_AllIndividuals_FANOVA_chunk" , chunk_i , ".csv", sep= ""))
}