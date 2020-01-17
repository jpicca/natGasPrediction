#!/usr/bin/env bash
#
# This script will download some of the GEFS grib files necessary to calculate mean 850 temps
# so we can then use our model to predict next week's NatGas price. This script grabs the
# final GEFS run before prediction. Thus it gets all perturbations and Days1-16. 
# The other GEFS sh script simply grabs the D1 of all perturbations for that day's run.

# Format our URL to use in loops for downloading data
# These are static variables that shouldn't change unless we're making changes to how
# we operate our model. Forecast time and perturbation number are updated in for loops.

URL_ROOT="https://nomads.ncep.noaa.gov/cgi-bin/filter_gens.pl?file="
#R_TIME=00
#HGT=850

# Lat/lon domain boundaries for filtering grib (so our requested data matches our model)

LLON=260
RLON=295
TLAT=51
BLAT=23

# Grab current date to get todays model run
# Add a -u flag after 'date' if you want to return UTC time

YEAR=$(date +"%Y")
MONTH=$(date +"%m")
DAY=$(date +"%d")


# Directory location
DATADIR=/Users/josephpicca/Desktop/newfrontier_2019/teleconnection-prices/natgas/data/gefs/day-0/

# Move to that directory to create files
cd $DATADIR

for i in `seq 1 20`
	do
		PERT=$(printf "%02d" $i)

		echo $PERT

		for j in `seq 12 24 372`
			do

				FTIME=$(printf "%02d" $j)

				echo $F_TIME

				SUFFIX=$i-$j

				URL="https://nomads.ncep.noaa.gov/cgi-bin/filter_gens.pl?file=gep"$PERT".t00z.pgrb2f"$FTIME"&lev_850_mb=on&var_TMP=on&subregion=&leftlon=260&rightlon=295&toplat=51&bottomlat=23&dir=%2Fgefs."$YEAR$MONTH$DAY"%2F00%2Fpgrb2"
				#URL=$URL_ROOT"gep"$PERT".t00z.pgrb2f"$F_TIME"&lev_850_mb=on&var_TMP=on&subregion=&leftlon="$LLON"&rightlon="$RLON"&toplat="$TLAT"&bottomlat="$BLAT"&dir=2Fgefs."$YEAR$MONTH$DAY"%2F00%2Fpgrb2"

				echo $URL

				curl $URL -o $SUFFIX".grb"

				echo "Waiting 10 seconds before next request"

				sleep 10s

			done

	done

# Get NatGas data

# Grab storage
URL="https://www.eia.gov/dnav/ng/xls/NG_STOR_WKLY_S1_W.xls"
DATASRC=$URL

DATADIR=/Users/josephpicca/Desktop/newfrontier_2019/teleconnection-prices/natgas/data/natgas/

curl $DATASRC -o $DATADIR"/storage.xls"

# Grab prices (use this file because it appears to update more frequently)
URL="https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls"
DATASRC=$URL

DATADIR=/Users/josephpicca/Desktop/newfrontier_2019/teleconnection-prices/natgas/data/natgas/

curl $DATASRC -o $DATADIR"/dailyprices.xls"

