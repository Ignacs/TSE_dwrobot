# -*- coding: big5 -*-
import csv
import glob, os, sys, platform
import sqlite3 as lite
from os.path import basename

con = None
idx_fileCSV=1
idx_outputFolder=2

##########################################
# arguments check 
if len(sys.argv) < 3:
	print "Too few arguments. Usage:"
	print "python trans_CSV_DB.py (CSV folder) (database folder)"
	sys.exit(1)

##########################################
# main section
# check CSV folder exist?
try :
	os.stat(str(sys.argv[idx_fileCSV]))
except:
	print sys.argv[idx_fileCSV] + " doesnt exist" 
	sys.exit()
	
# check db folder exist?
try :
	os.stat(str(sys.argv[idx_outputFolder]))
except:
	print sys.argv[idx_outputFolder] + " doesnt exist" 
	print "try to make it "
	try :
		os.makedirs(sys.argv[idx_outputFolder])
	except:
		print "Failed to create it."
		sys.exit()

print "Processing CSV folder " + sys.argv[idx_fileCSV] 
print "Output DB folder " + sys.argv[idx_outputFolder] 

# through all CSV files
os.chdir(str(sys.argv[idx_outputFolder]))
# for csv_file in glob.glob("*"):
# stock data CSV file
csv_fpath=sys.argv[idx_fileCSV]
csv_file = open(csv_fpath,'r' )
csv_fn=basename(csv_fpath)
print ">>>>> handle " + csv_fn + " <<<<<"
# dont support non-stock id , debt of foreign stock  (more than 4 digit number) 
# 
#if len(csv_fn) > 7:
#	if csv_fn[4].isdigit():
#		print "But not accept ..."
#		sys.exit()
#if len(csv_fn) > 6:
#	if csv_fn[4].isdigit():
#		print "But not accept ..."
#		sys.exit()


# putput database file name
db_name = csv_fn[0] + csv_fn[1] + csv_fn[2] + csv_fn[3] + ".sl3"

print "build database [" + db_name + "]"
con = lite.connect(db_name)
# "with" keyword will release resource autombatically and handle error.
with con:
	cur = con.cursor()    
	# table format 
	# "ら戳","Θユ计","Θユ掸计","Θユ肂","秨絃基","程蔼基","程基","Μ絃基","害禴(+/-)","害禴基畉","程处ボ禦基","程处ボ禦秖","程处ボ芥基","程处ボ芥秖","セ痲ゑ"
	# cur.execute("DROP TABLE IF EXISTS " + str(db_name))
	cur.execute(''' CREATE TABLE IF NOT EXISTS stock (
			Date INT,
			Stock_number INT, 
			volumn INT,
			Trade_money INT,
			Open REAL, 
			HIGHEST REAL,
			LOWEST REAL,
			CLOSE REAL,
			UP_DOWN TEXT, 
			DIFF REAL,
			BUY REAL, 
			BUY_VOL INT, 
			SELL REAL,
			SELL_VOL INT,
			PE INT)''')
	# create INDEX for speed-up quary
	# cur.execute("CREATE INDEX stock ON stock(title);

	# Insert a row of data
	# csv_line = 0
	for nline_data in csv.reader(csv_file, delimiter=';'):
		# csv_line = csv_line+1
		# print str(csv_line),
		for idx in range(0, len(nline_data)):
			date_line=str(nline_data[idx])
		 	print '[' + str(idx) + ':' +  date_line + ']',
			cur.execute("INSERT INTO stock VALUES ( '" + str(nline_data[0]) + "','" + str(nline_data[1]) + "','" + str(nline_data[2]) + "','" + str(nline_data[3]) + "','" + str(nline_data[4]) + "','" + str(nline_data[5]) + "','" + str(nline_data[6]) + "','" + str(nline_data[7]) + "','" + str(nline_data[8]) + "','" + str(nline_data[9]) + "','" + str(nline_data[10]) + "','" + str(nline_data[11]) + "','" + str(nline_data[12]) + "','" + str(nline_data[13]) + "','" + str(nline_data[14]) + "')" )

	# Save (commit) the changes
	# cur.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	# cur.close()
csv_file.close()
sys.exit()


