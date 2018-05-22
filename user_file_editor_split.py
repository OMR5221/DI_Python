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

app_infodim = '''info_dimensions={
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
        \"Sub Channel\",'''

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

tdl_dimname = re.compile(r".*Dimension_Name=\"TDLinx (.*)\",", re.IGNORECASE)

cust_dimname = re.compile(r".*Dimension_Name=\"(.*)\",", re.IGNORECASE)

info_pattern = re.compile(r"info_dimensions={.*?},", re.DOTALL | re.IGNORECASE)

newinfo_pattern = re.compile(r"info_dimensions={", re.DOTALL | re.IGNORECASE)

tdlinfo_pattern = re.compile(r'"TDLinx.*,', re.IGNORECASE)

tdlcat_pattern = re.compile(r"\t{\n\tName=\"TDLinx Customer\",.*?},", re.DOTALL | re.IGNORECASE)

custcat_pattern = re.compile(r"Name=\"Customers\",.*?}", re.DOTALL | re.IGNORECASE)

fileList = open(fileListFile, 'r')

logFile = open(replacedFileName, 'w')
errLogFile = open(errorFileName, 'w')
numFiles = 1

for file in fileList:

	file = file.strip()

	try:

		file_open = open(file, 'rb')
		file_edit = file_open.read()
		file_open.close()
		
		logFile.write("Opened: " + file + "\n")
		sys.stdout.write(file_edit)
		edit_info = True

	# Test if TDLinx Customer Category exists
		tdlcat_match = tdlcat_pattern.search(file_edit)

	# If it does then replace with blanks
		if tdlcat_match:
			file_edit = re.sub(tdlcat_pattern, "", file_edit)

		else:
# Newer file so do not edit
			logFile.write("DO NOT EDIT: " + file + "\n")
			continue

# if there is an info dimension section
		infodim_match = info_pattern.search(file_edit)

# Then add out new aliased Tdlinx fields to marker
		if infodim_match:
			file_edit = re.sub(r"info_dimensions={", app_infodim, file_edit)

# Test if Customer Category exists
		custcat_match = custcat_pattern.search(file_edit)

# If it does then replace with new Customer Category
		if custcat_match:
			file_edit = re.sub(custcat_pattern, app_newcustomer, file_edit)

# Turn string into a list
		file_edit = file_edit.split("\n")

		fileout_lines = []

		i = 0

		while i < len(file_edit):

			tdl_dimname_match = tdl_dimname.search(file_edit[i])

			cust_dimname_match = cust_dimname.search(file_edit[i])

			if tdl_dimname_match:
		
				if tdl_dimname_match.group(1) == "Market Group":
					file_edit[i] = "Dimension_Name=\"Market DBA Name\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Corp Parent Name":
					file_edit[i] = "Dimension_Name=\"Corp Parent Name-1\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Corp Banners Name":
					file_edit[i] = "Dimension_Name=\"Corp Banner Name-2\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Division/Franchise Nam":
					file_edit[i] = "Dimension_Name=\"Corp Division Name-3\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Unit Outlets Name":
					file_edit[i] = "Dimension_Name=\"Corp Unit Name-4\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Trade Channel Desc":
					file_edit[i] = "Dimension_Name=\"Trade Channel\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Sub Channel Desc":
					file_edit[i] = "Dimension_Name=\"Sub Channel\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Premise":
					file_edit[i] = "Dimension_Name=\"Premise\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Foodtype Desc":
					file_edit[i] = "Dimension_Name=\"Food Type\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Beer Flag":
					file_edit[i] = "Dimension_Name=\"Beer Y/N\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Chain Flag":
					file_edit[i] = "Dimension_Name=\"Chain Flag\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Wine Flag":
					file_edit[i] = "Dimension_Name=\"Wine Y/N\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				elif tdl_dimname_match.group(1) == "Spirits Flag":
					file_edit[i] = "Dimension_Name=\"Spirits Y/N\","
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

				else:
					fileout_lines.append(file_edit[i] + "\n")
					edit_info = False
					i += 1

			elif cust_dimname_match:

				if cust_dimname_match.group(1) == "On/Off Premise":
					fileout_lines.append(file_edit[i] + "\n")
					edit_info = False
					i += 1


				elif cust_dimname_match.group(1) == "Market Type":
					fileout_lines.append(file_edit[i] + "\n")
					edit_info = False
					i += 1

				elif cust_dimname_match.group(1) == "Premise Market":
					fileout_lines.append(file_edit[i] + "\n")
					edit_info = False
					i += 1

				elif cust_dimname_match.group(1) == "customer permit code":
					fileout_lines.append(file_edit[i] + "\n")
					edit_info = False
					i += 1


				elif cust_dimname_match.group(1) == "Business Name":
					fileout_lines.append(file_edit[i] + "\n")
					edit_info = False
					i += 1

				elif cust_dimname_match.group(1) == "Corp Chain":
					fileout_lines.append(file_edit[i] + "\n")
					edit_info = False
					i += 1

				elif cust_dimname_match.group(1) == "Establishment Type":
					fileout_lines.append(file_edit[i] + "\n")
					edit_info = False
					i += 1

				elif cust_dimname_match.group(1) == "Customer":
					fileout_lines.append(file_edit[i] + "\n")
					edit_info = False
					i += 1

				else:
					fileout_lines.append(file_edit[i] + "\n")
					i += 1

# Edit info_dimensions block
			elif re.search(r'.*info_dimensions={.*', file_edit[i]) != None:

				fileout_lines.append(file_edit[i] + "\n")

				i += 1

				while re.search(r'.*},.*', file_edit[i]) == None:

					if edit_info == True:

						if re.search(r'.*TDLinx.*', file_edit[i]) != None:
							i += 1
						
						elif re.search(r'.*On.*Off.*Premise.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*Market.*Type.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*Premise.*Market.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*customer.*permit.*code.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*Business.*Name.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*Corp.*Chain.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*Establishment.*Type.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*Customer.*', file_edit[i]) != None:
							i += 1
						
						else:
							fileout_lines.append(file_edit[i] + "\n")
							i += 1

					else:
						if re.search(r'.*TDLinx\s*Market\s*Group.*', file_edit[i]) != None:
							i += 1
						
						elif re.search(r'.*TDLinx\s*Corp\s*Parent\s*Name.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*TDLinx\s*Corp\s*Banners\s*Name.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*TDLinx\s*Division\s*Franchise\s*Nam.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*TDLinx\s*Unit\s*Outlets\s*Name.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*TDLinx\s*Trade\s*Channel\s*Desc.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*TDLinx\s*Sub\s*Channel\s*Desc.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*TDLinx\s*Premise.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*TDLinx\s*Foodtype\s*Desc.*', file_edit[i]) != None:
							i += 1
						
						elif re.search(r'.*TDLinx\s*Beer\s*Flag.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*TDLinx\s*Chain\s*Flag.*', file_edit[i]) != None:
							i += 1
						
						elif re.search(r'.*TDLinx\s*Wine\s*Flag.*', file_edit[i]) != None:
							i += 1

						elif re.search(r'.*TDLinx\s*Spirits\s*Flag.*', file_edit[i]) != None:
							i += 1
						else:
							fileout_lines.append(file_edit[i] + "\n")
							i += 1

			else:
				fileout_lines.append(file_edit[i] + "\n")
				i += 1

		file_out = open(file, 'wb')
		file_out.write(''.join(fileout_lines))
		file_out.close()
		logFile.write("Closed: " + file + "\n")

#Catch any IO errors and write them out the log
	except IOError, err:
		errLogFile.write(str(err)+ "\n")

fileList.close()
