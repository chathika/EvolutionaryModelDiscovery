read_params <- function(param_fn) {
  # only return param names
  # line with comment saying "instance features" are for instance features, the rest are for algorithm params
  
  lsln <- readLines(param_fn)
  lsln <- lsln[lsln != '']
  
  ls_param_names <- c()
  ls_instance_features_names <- c()
  for (ln in lsln) {
    
    # ignore comments
    if (startsWith(ln, '#'))
      next
    
    param_name <- strsplit(ln, ' ')[[1]][1]
    
    if (grepl('instance features', ln))
      ls_instance_features_names <- c(ls_instance_features_names, param_name)
    else
      ls_param_names <- c(ls_param_names, param_name)
  }
  
  return (list(ls_param_names = ls_param_names, ls_instance_features_names = ls_instance_features_names))
}

normalize_cost <- function(t_data, cost_column) {
  t <- t_data
  t_min_max <- t[,list(min=min(get(cost_column)), max = max(get(cost_column))), by = c('problem_instance')]
  t <- merge(t, t_min_max, by = c('problem_instance'), sort = FALSE)
  t$method_1 <- t[[cost_column]] / t$min
  t$method_2 <- (t[[cost_column]] - t$min) / (t$max - t$min)
  t_data$method_2 <- t$method_2
  t_data$method_1 <- t$method_1
  
  return (t_data)
}

source('./extract-param-file.R')

generate_fANOVA_data <- function(data_fn) {
  # cost_normalization_method: {none, method_1} # method_1: (cost - min) / (max - min)
  # some requirements:
  # - param file: line with comment saying "instance features" are for instance features, the rest are for algorithm params
  # - data_fn file: there must be one column with name "problem_instance" (for problem instance identification), "seed", "runtime"
  
  # for DEBUG
  #data_fn <- '/home/nttd/Dropbox/UHasselt/new/data/GP-Anasazi/files/sample-count.csv'

  cost_normalization_method <- 'none'
  outdir <- paste('../../../results/fANOVA/GP-Anasazi/',strsplit(basename(data_fn),'\\.')[[1]][1],sep='')
  cost_column <- 'L2.error'

  # create outdir
  dir.create(outdir)
  system(paste('rm -rf ',outdir,'/*',sep=''))

  # generate param-file.txt
  param_fn <- paste(outdir,'/param-file.txt',sep='')
  extract_param_file(csvFile=data_fn, outFile=param_fn)
  
  # read param names
  ls <- read_params(param_fn)
  ls_param_names <- ls$ls_param_names
  ls_instance_features <- ls$ls_instance_features_names
  ls_all_variables <- c(ls_param_names, ls_instance_features)

  # read data file  
  library(data.table)
  t_data <- fread(data_fn)
 
  # add neccesary columns 
  setnames(t_data,'V1','id')
  t_data$problem_instance <- 1
  t_data$seed <- sample(c(1000:9999),nrow(t_data),replace=TRUE)
  t_data$runtime <- 1

  # remove <MySelf>
  t_data <- t_data[IndividualSyntaxLogic!="<Myself>"]

  # fix potentialFarms
  lsFarms <- c("AllPotentialFarms","PotentialFarmsNearFamily","PotentialFarmsNearNeighbors","PotentialFarmsNearBestPerformers")
  lsVals <- c()
  for (row_id in c(1:nrow(t_data))){
    row <- t_data[row_id,]
    farm <- lsFarms[which(as.vector(row[,lsFarms,with=FALSE])==1)]
    lsVals <- c(lsVals, farm)
  }
  t_data$potentialFarms <- lsVals
  for (col in lsFarms)
    t_data[[col]] <- NULL

  #t_data <- normalize_cost(t_data, cost_column)
  
  # choose cost column
  chosen_cost_column <- cost_normalization_method
  if (chosen_cost_column == 'none')
    chosen_cost_column <- cost_column
  
  # remove rows with NaN cost value
  n_original_rows <- nrow(t_data)
  t_data <- t_data[!is.na(get(chosen_cost_column))]
  n_new_rows <- nrow(t_data)
  if (n_new_rows < n_original_rows)
    cat(paste('Eliminate ', n_original_rows - n_new_rows, ' NaN rows\n', sep = ''))
  
  # write paramstrings-it1.txt, each line in data_fn is a configuration
  paramstring_fn <- paste(outdir, '/paramstrings-it1.txt', sep = '')
  ls_out <- c()
  for (row_id in c(1:nrow(t_data))) {
    row <- t_data[row_id,]
    s <- paste(row_id, ': ', paste(sapply(ls_all_variables, function(var_name) {
      paste(var_name, "='", row[[var_name]], "'", sep = '')
    }), collapse = ', '), sep = '')
    ls_out <- c(ls_out, s)
  }
  writeLines(ls_out, con <- file(paramstring_fn, 'wt')); close(con)
  
  # write runs_and_results-it1.csv
  CSV_SPLIT <- ','
  run_and_results_fn <- paste(outdir, '/runs_and_results-it1.csv', sep = '')
  ls_out <- c(paste(c("Run Number","Run History Configuration ID","Instance ID","Response Value (y)","Censored?","Cutoff Time Used","Seed","Runtime","Run Length","Run Result Code","Run Quality","SMAC Iteration","SMAC Cumulative Runtime","Run Result","Additional Algorithm Run Data","Wall Clock Time"), collapse = CSV_SPLIT))
  ls_inst_names <- unique(t_data[['problem_instance']])
  map_inst_name_to_id <- data.table(inst_name = ls_inst_names, inst_id = c(1:length(ls_inst_names)))
  sum_runtime <- 0
  for (row_id in c(1:nrow(t_data))) {
    row <- t_data[row_id,]
    
    sum_runtime <- sum_runtime + row$runtime
    
    run_number <- row_id
    run_his <- row_id
    
    inst_id <- 1
    if (length(ls_instance_features) == 0)
      inst_id <- map_inst_name_to_id[inst_name == row$problem_instance]$inst_id
    
    response <- row[[chosen_cost_column]]
    cencored <- 0
    cutoff_time <- 36000
    seed <- row$seed
    runtime <- row$runtime
    runlength <- 0
    runresultscode <- 1
    runquality <- response
    smaciteration <- 0
    smacruntime <- sum_runtime
    runresult <- 'SAT'
    rundata <- ''
    wallclock <- runtime
    
    s <- paste(run_number, run_his, inst_id, response, cencored, cutoff_time, seed, runtime, runlength, runresultscode, runquality, smaciteration, smacruntime, runresult, rundata, wallclock, sep = CSV_SPLIT)
    
    ls_out <- c(ls_out, s)
  }
  writeLines(ls_out, con <- file(run_and_results_fn, 'wt')); close(con)
  
  # other things
  system(paste("echo ''>", outdir,'/temp.sh', sep = ''))
  #system(paste('cp ', param_fn, ' ', outdir, '/param-file.txt', sep = ''))
  writeLines(c("# dummy, just for fANOVA","algo=./temp.sh","execdir=./","deterministic=false","run_obj=quality","overall_obj=mean","cutoff_time=3600.0","tunerTimeout=2147483647","paramfile=param-file.txt","instance_file=instances.txt"), con <- file(paste(outdir, '/scenario.txt', sep = ''))); close(con)
  system(paste('mkdir ', outdir, '/plots', sep = ''))
  
  nInst <- 1
  if (length(ls_instance_features) == 0)
    nInst <- length(ls_inst_names)
  system(paste('mkdir ', outdir, '/FakeInstances', sep = ''))
  ls_out <- c()
  for (inst_id in c(1:nInst)) {
    system(paste("echo ''>", outdir, '/FakeInstances/', inst_id, sep = ''))
    ls_out <- c(ls_out, paste('FakeInstances/', inst_id, sep = ''))
  }
  writeLines(ls_out, paste(outdir, '/instances.txt', sep = ''))
  
  system(paste('cp ../../common/run.py ', outdir, sep = ''))
  system(paste('cp ../../data/common/run.sh ', outdir, sep = ''))
}

#args = commandArgs(trailingOnly=TRUE)
#generate_fANOVA_data(data_fn=args[1])

lsDataFiles <- list.files('../files/',pattern='*.csv', full.names=TRUE)
for (fn in lsDataFiles){
    print(fn)
    generate_fANOVA_data(data_fn=fn)
}
