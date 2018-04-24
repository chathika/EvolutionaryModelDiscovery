extract_param_file <- function(csvFile, outFile){
    f <- file(outFile,'wt')

    require(data.table)
    t <- fread(csvFile)
    lsCols <- colnames(t)
    
    # potential farms
    startColId <- 8
    nCols <- 4
    s <- paste('potentialFarms {', paste(lsCols[startColId:(startColId+nCols-1)],collapse=',',sep=''),'} [AllPotentialFarms]', sep='')
    write(s,file=f)

    # count or presence 
    count <- FALSE
    if (grepl('count',basename(csvFile)))
        count <- TRUE

    # others
    warn <- FALSE # warning if lb==ub
    ignoreEmptyFeatures <- TRUE # if lb==ub, ignore the feature
    startColId <- startColId + nCols
    for (col in lsCols[startColId:length(lsCols)]){
        lb <- min(t[[col]])
        ub <- max(t[[col]])
        if (lb==ub){
            if (warn){
                print(paste(col, ': ', lb, ' ', ub, sep=''))
            }
            # fix or ignore
            if (ignoreEmptyFeatures)
                next
            ub <- 1
        }
        if (count)
            s <- paste(col, ' [',lb,',',ub,'] [',lb,']i', sep='') 
        else
            s <- paste(col, ' {',lb,',',ub,'} [',lb,']', sep='')
        write(s, file=f)
    }

    close(f)
}

#dataFile <- '../files/sample-count.csv')
#dataFile <- '../files/AA_EMDRun10_AllIndividuals_connectivity_and_factor_counts.csv'
#extract_param_file(csvFile=dataFile, outFile='./param-file-count.txt')

args <- commandArgs(trailingOnly=TRUE)
if (length(args)>=2)
    extract_param_file(csvFile=args[1],outFile=args[2])
