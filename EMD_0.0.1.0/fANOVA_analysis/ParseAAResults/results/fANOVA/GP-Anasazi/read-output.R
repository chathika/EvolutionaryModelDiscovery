lsDirs <- list.dirs('./counts/',recursive=FALSE) # use either "presence" or "counts"
lsDirs <- lsDirs[grep('AA_EMDRun',lsDirs)]
lsFiles <- paste(lsDirs,'fANOVA.out',sep='/')

threshold <- 1 # only print effects with contribution not less than this threshold (in percentage)
for (fn in lsFiles){
    lsLines <- readLines(con <- file(fn))
    close(con)
    
    cat('\n-----',fn,'------\n')
    
    # sum of effects
    lss <- lsLines[grep('Sum of',lsLines)]
    if (length(lss) == 0){
        cat('Memory error!!\n')
        next
    }
    cat(lss,sep='\n')

    # effects (>=threshold)
    lsEffects <- lsLines[grep('due to',lsLines)]
    lsEffects <- lsEffects[sapply(lsEffects, function(s){
        lss <- strsplit(s,'%')[[1]]
        if (as.numeric(lss[1])>=threshold)
            return (TRUE)
        return (FALSE)
    })]
    cat(lsEffects,sep='\n')
}
