[Updated 2/13/2017]

# RRUFF-api
This API aims to generate date-locality datasets of mineral discoveries using all existing data in [RRUFF](http://rruff.info/ima/). The output datasets may be serve as the starting points of various data analysis and visualization - more data from other sources can be joined with this dataset.

## Instructions

### From a list of minerals to its evolution data
	
1. Open link in browser:
	```
	http://rruff.info/mineral_list/locality.php?no_combine&mineral_name=[LIST OF MINERALS, SEPARATED BY COMMAS]
	```
	(This page does NOT combine the data at all and displays only one mineral per line)
2. Wait, then scroll up-and-down the page to confirm the page the fully loaded
3. Choose option “Show GPS”, “Hide Undated Localities”, and “Hide Locality Longname”
4. Select all the data **WITHOUT the header line**
5. Be ready for the next steps

###***Notes on next steps***

***With considerations of effectiveness and efficiency, we adopt spreadsheet method to aggregate all relevant information from RRUFF and generate date-locality datasets of mineral discoveries.***

***There are 2 versions of this method, one uses a Microsoft Excel spreadsheet while the other uses a Google Sheet. Although the direct outputs produced in both MS Excel and Google Sheet can be viewed and used to an extent, the final output of both procedures should be in CSV format with UTF-8 encoding to ensure consistency, minimize size, and facilitate our data visualization process in R, Python, and/or other environments.***

***We RECOMMEND using the Google Sheet method since it can be exported as CSV in UTF-8 encoding conviniently, while MS Excel could incur CSV encoding issues depending on different operating systems.***



### Generate using Google Sheet (Recommended)

1. Make a copy of [TEMPLATE (Make a copy to use).gsheet](https://drive.google.com/open?id=1JcMR-Kp6IpgwslwbwHLVrcYiqNCAdvuZceABH83mCMU) and name it. I suggest using a unified prefix such as "RRUFF_Data_" to help file management.
2. Open this new copy. In this file you will see 4 sheets:
	- RRUFF: The newest RRUFF IMA mineral list obtained from http://rruff.info/ima/ (all export options enabled except "Status Notes"; downloaded as CSV)
	- RRUFF_LESS_COLUMNS: Data from sheet RRUFF with only columns we need
	- INPUT: Where you paste the evolution data
	- OUTPUT: Where the result from INPUT is carried over with only columns we need
3. Navigate to sheet INPUT. Paste the evolution data in columns A to W. Make sure the headers are matched and do a quick double-check across the region.
4. Copy the formulas in X2:AD2, then paste it down the columns till the last line of data on the left. The formula will match the mineral information from RRUFF_LESS_COLUMNS and populate through the region
5. Navigate to sheet OUTPUT. Needed columns of data should have been populted automatically (unlike that you will need to copy-paste through the region if you do it in Excel, as below). Click File > Download as > Comma-separated values to download the output CSV file in UTF-8 encoding.


### Generate using Microsoft Excel

1. Make a copy of [TEMPLATE (Make a copy to use).xlsx](https://github.com/tetherless-world/dtdi-api/blob/master/RRUFF-api/TEMPLATE%20(Make%20a%20copy%20to%20use).xlsx) and name it. I suggest using a unified prefix such as "RRUFF_Data_" to help file management.
2. (Same as in the Google Sheet method)
3. (Same as in the Google Sheet method)
4. (Same as in the Google Sheet method)
5. Navigate to sheet OUTPUT. You should be able to see the first line of data (except for the header line) is already populated. Copy the paste the formulas in A2:U2 down each column for the exactly same number of rows in our INPUT data. (Otherwise there will be lines of 0's at the bottom)






