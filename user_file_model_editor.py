#!/usr/bin/python3

''' This program will extract words from a file and put them into a tab delimited file '''

import sys
import re

#Take as input a list of files to run the search and replace over: output from shell script which finds all markers,
# diveplans, diveboks, etc...
if(len(sys.argv) < 2):
    print('Usage: user_marker_editor.py <file list>')
    sys.exit()

# Get the name of the file conatining .dvp, .mrk, .dpt files
fileListFile = sys.argv[1]

# Firt portion of this filename containing a list of files
baseName = fileListFile.split('.')[0]

#The names of the log files are based on the name of the input file
replacedFileName = 'replaced.txt'
errorFileName = 'errors.txt'

tdl_aliases_infodim = ['\t\"Concept Manager\",', '\t"Market DBA Name",', '\t"Corp Parent Name-1",', '\t"Corp Banner Name-2",', '\t"Corp Division Name-3",', '\t"Corp Unit Name-4",', '\t"Food Type",', '\t"Premise",', '\t"Beer Y/N",', '\t"Chain Flag",', '\t"Wine Y/N",', '\t"Spirits Y/N",', '\t"Trade Channel",','\t"Sub Channel",']

app_newcustomer = '''Name="Customers",
	dimensions={
	\"WH Customer\",
	\"Concept Manager\",
	\"Market DBA Name\",
	\"Corp Parent Name-1\",
	\"Corp Banner Name-2\",
	\"Corp Division Name-3\",
	\"Corp Unit Name-4\",
	\"Food Type\",
	\"Premise\",
	\"Beer Y/N\",
	\"Chain Flag\",
	\"Wine Y/N\",
	\"Spirits Y/N\",
	\"Trade Channel\",
	\"Sub Channel\",
	}'''

tdl_aliases = [ '\taliases={', '\t"TDLinx Index=Index (TDL)",', '\t"TDLinx Market Group=Market DBA Name",', '\t"TDLinx Census Blockid=Census BlockID (TDL)",', '\t"TDLinx Close Date=Close Date",', '\t"TDLinx Concept Owner=Concept Manager",', '\t"TDLinx Corp Parent=Corp Parent-1",', '\t"TDLinx Corp Parent Number=Corp Parent Number-1",', '\t"TDLinx Corp Parent Name=Corp Parent Name-1",', '\t"TDLinx Corp Banners=Corp Banner-2",', '\t"TDLinx Corp Banners Number=Corp Banner Number-2",', '\t"TDLinx Corp Banners Name=Corp Banner Name-2",', '\t"TDLinx Customer=Cust Name (TDL)",', '\t"TDLinx Division/Franchise=Corp Division-3",', '\t"TDLinx Division/Franchise Number=Corp Division Number-3",', '\t"TDLinx Division/Franchise Name=Corp Division Name-3",', '\t"TDLinx Unit Outlets=Corp Unit-4",', '\t"TDLinx Unit Outlets Number=Corp Unit Number-4",', '\t"TDLinx Unit Outlets Name=Corp Unit Name-4",', '\t"TDLinx Beer Flag=Beer Y/N",', '\t"TDLinx Chain Flag=Chain Flag",', '\t"TDLinx FIPS StCode=FIPS State Code (TDL)",', '\t"TDLinx FIPS CntyCode=FIPS County Code (TDL)",', '\t"TDLinx FIPS Country Name=FIPS Country Name (TDL)",', '\t"TDLinx Foodtype Desc=Food Type",', '\t"TDLinx Hier Level=Owner Levels #",', '\t"TDLinx Lat/Long Code=Lat/Long Code",', '\t"TDLinx Latitude=Latitude",', '\t"TDLinx Longitude=Longitude",', '\t"TDLinx Long-Lat=Long-Lat",', '\t"TDLinx On Premise Flag=On Premise Y/N",', '\t"TDLinx Open Date=Open Date",', '\t"TDLinx Outlet Name=Outlet Name",', '\t"TDLinx Outlet Number=Outlet Number",', '\t"TDLinx Place Name=USPS Alt. City (TDL)",', '\t"TDLinx Premise=Premise",', '\t"TDLinx Spirits Flag=Spirits Y/N",', '\t"TDLinx Store Number=Store Number (TDL)",', '\t"TDLinx Store Address=Address (TDL)",', '\t"TDLinx Store City=City (TDL)",', '\t"TDLinx Store State=State (TDL)",', '\t"TDLinx Store Zip=Zip Code (TDL)",', '\t"TDLinx Store Status=Cust Status (TDL)",', '\t"TDLinx Sub Channel Desc=Sub Channel",', '\t"TDLinx Trade Channel Desc=Trade Channel",', '\t"TDLinx Wine Flag=Wine Y/N",', '\t}' ]


dimname = re.compile(r'^Dimension_Name="(.*)",', re.IGNORECASE | re.MULTILINE | re.DOTALL)


main_tdl_edit = {'"TDLinx Market Group"': '"Market DBA Name"','"TDLinx Corp Parent Name"': '"Corp Parent Name-1"', '"TDLinx Corp Banners Name"': '"Corp Banner Name-2"','"TDLinx Division/Franchise Name"': '"Corp Division Name-3"', '"TDLinx Unit Outlets Name"': '"Corp Unit Name-4"', '"TDLinx Trade Channel Desc"': '"Trade Channel"', '"TDLinx Sub Channel Desc"': '"Sub Channel"', '"TDLinx Premise"': '"Premise"', '"TDLinx Foodtype Desc"': '"Food Type"', '"TDLinx Beer Flag"': '"Beer Y/N"', '"TDLinx Chain Flag"': '"Chain Flag"', '"TDLinx Wine Flag"': '"Wine Y/N"', '"TDLinx Spirits Flag"': '"Spirits Y/N"', '"TDLinx Corp Banners"': '"Corp Banner Name-2"', '"TDLinx Concept Owner"': '"Concept Manager"', '"TDLinx Index"': '"Index (TDL)"', '"TDLinx Close Date"': '"Close Date"', '"TDLinx Open Date"': '"Open Date"', '"TDLinx Store Number"': '"Store Number (TDL)"', '"TDLinx Lat/Long Code"': '"Lat/Long Code"', '"TDLinx Customer"': '"Cust Name (TDL)"', '"TDLinx Country Name"': '"Country Name (TDL)"', '"TDLinx Census Blockid"': '"Census BlockID (TDL)"', '"TDLinx Corp Banners Number"': '"Corp Banner Number-2"', '"TDLinx Corp Parent Number"': '"Corp Parent Number-1"', '"TDLinx Unit Outlets Number"': '"Corp Unit Number-4"', '"TDLinx FIPS CntyCode"': '"FIPS County Code (TDL)"', '"TDLinx FIPS Country"': '"FIPS Country Name (TDL)"', '"TDLinx FIPS StCode"': '"FIPS State Code (TDL)"', '"TDLinx Hier Level"': '"Owner Levels #"', '"TDLinx Latitude"': '"Latitude"', '"TDLinx Longitude"': '"Longitude"', '"TDLinx Long-Lat"': '"Long-Lat"', '"TDLinx On Premise Flag"': '"On Premise Y/N"', '"TDLinx Outlet Name"': '"Outlet Name"', '"TDLinx Outlet Number"': '"Outlet Number"', '"TDLinx Place Name"': '"USPS Alt. City (TDL)"', '"TDLinx Store Address"': '"Address (TDL)"', '"TDLinx Store City"': '"City (TDL)"', '"TDLinx Store State"': '"State (TDL)"', '"TDLinx Store Status"': '"Cust Status (TDL)"', '"TDLinx Store Zip"': '"Zip Code (TDL)"'}  


dimname_cust_edit = {'Dimension_Name="On/Off Premise",': '', 'Dimension_Name="Market Type",': '', 'Dimension_Name="Premise Market",': '','Dimension_Name="customer permit code",': '', 'Dimension_Name="Business Name",': '', 'Dimension_Name="Corp Chain",': '', 'Dimension_Name="Establishment Type",': '', 'Dimension_Name="Customer",': ''}  


tdl_alias_rem = {'Market DBA Name",': '', '"Corp Parent Name-1",': '', '"Corp Banner Name-2",': '', '"Corp Division Name-3",': '', '"Corp Unit Name-4",': '', '"Trade Channel",': '', '"Sub Channel",': '', '"Premise",': '', '"Food Type",': '', '"Beer Y/N",': '', '"Chain Flag",': '', '"Wine Y/N",': '', '"Spirits Y/N",': '', '"Concept Manager",': ''}  

infodim_cust_edit = {'"On/Off Premise",': '', '"Market Type",': '', '"Premise Market",': '','"customer permit code",': '', '"Business Name",': '', '"Corp Chain",': '', '"Establishment Type",': '', '"Customer",': '', '"On/Off Premise"': '', '"Market Type"': '', '"Premise Market"': '','"customer permit code"': '', '"Business Name"': '', '"Corp Chain"': '', '"Establishment Type"': '', '"Customer"': ''}  




category_pattern = re.compile(r"categories={", re.IGNORECASE)

info_pattern = re.compile(r"info_dimensions={.*?},", re.DOTALL | re.IGNORECASE)

model_pattern = re.compile(r'dbname=".*-.*.mdl"', re.IGNORECASE)

newinfo_pattern = re.compile(r"info_dimensions={", re.DOTALL | re.IGNORECASE)

tdlinfo_pattern = re.compile(r'"TDLinx.*,', re.IGNORECASE)

tdlcat_pattern = re.compile(r"\t*{\n*\t*Name=\"TDLinx\s*Customer\",.*?},", re.DOTALL | re.IGNORECASE)

custcat_pattern = re.compile(r"Name=\"Customers\",.*?}", re.DOTALL | re.IGNORECASE)

fileList = open(fileListFile, 'r')

logFile = open(replacedFileName, 'w')
errLogFile = open(errorFileName, 'w')
numFiles = 1

for file in fileList:

	file = file.strip()

	file_edit = ""

	try:

		file_open = open(file, 'rb')
		file_edit = file_open.read()
		file_open.close()
		
		logFile.write("Opened: " + file + "\n")

		fileout_lines = []
		
		fileout_lines = file_edit.split("\n")

 		i = 0

		while i < len(fileout_lines):
			
			if model_pattern.search(fileout_lines[i]):
				
				i += 1

				if "}" in fileout_lines[i]:

					fileout_lines[i-1] = fileout_lines[i-1] + ","

					file_head = fileout_lines[:i]
					
					file_tail = fileout_lines[i:]
		
					file_head.extend(tdl_aliases)
					
					file_head.extend(file_tail)
					
					fileout_lines = file_head

				else:
					i += 1

			else:
				i += 1		

					#if "dos_dbname=" in fileout_lines[i]:

					#	file_head = fileout_lines[:i]
					
					#	file_tail = fileout_lines[i:]
		
					#	file_head.extend(tdl_aliases)
					
					#	file_head.extend(file_tail)
					
					#	fileout_lines = file_head
					

		j = 0 

		finalout_lines = []

		while j < len(fileout_lines):

			if fileout_lines[j].strip():
				finalout_lines.append(fileout_lines[j] + "\n")
				j += 1

			else:
				j += 1

			
	except IOError, err:
		errLogFile.write(str(err)+ "\n")

	logFile.write("Finished: " + file + "\n")
	file_out = open(file, 'w')
	file_out.write(''.join(finalout_lines))
	file_out.close()

fileList.close()
