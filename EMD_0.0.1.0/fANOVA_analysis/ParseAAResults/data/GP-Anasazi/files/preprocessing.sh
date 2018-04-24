for fn in *.csv
do
    #sed -i "s/\\^M//g" ${fn}
    dos2unix ${fn}
done
