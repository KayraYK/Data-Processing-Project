#!/usr/bin/env python

'''
pre_process.py
  Author(s): Kayra Kazanci

  Functional Summary
      pre_process.py takes in a data file and a name for a new file, filters it accordingly, and makes a new
      file with the filtered data that is named as taken from the command line.

      There are expected to be these fields:
          1. date
          2. region
          3. occupation
          4. job vacancy
          5. statistic
          6. value
     
     Commandline Parameters: 2
        argv[1] = input file (CSV file)
        argv[2] = new file name

     References
        CSV file from https://www150.statcan.gc.ca/n1/en/catalogue/14100328
'''

#
#   Packages and modules
#

# The 'sys' module gives us access to system tools, including the
# command line parameters, as well as standard input, output and error
import sys
import pandas as pd
import matplotlib.pyplot as mpl

# The 'csv' module gives us access to a tool that will read CSV
# (Comma Separated Value) files and provide us access to each of
# the fields on each line in turn
import csv

def main(argv):

    #Main function in the script. Putting the body of the
    #script into a function allows us to separate the local
    #variables of this function from the global constants
    #declared outside.

    #
    #   Check that we have been given the right number of parameters,
    #   and store the 3 command line arguments in variables with
    #   better names
    #

    if len(argv) != 3:
        print("Incorrect amount of arguments")

        # we exit with a zero when everything goes well, so we choose
        # a non-zero value for exit in case of an error
        sys.exit(1)

    # Getting the arguments from the command line
    big_file_name = (argv[1])
    small_file_name = (argv[2])

    # Open the CSV input file.  The encoding argument
    # indicates that we want to handle the BOM (if present)
    # by simply ignoring it.
    try:
        big_file_fh = open(big_file_name, 'r', encoding="utf-8-sig")

    except IOError as err:
        # Here we are using the python format() function.
        # The arguments passed to format() are placed into
        # the string it is called on in the order in which
        # they are given.
        print("Unable to open big file '{}' : {}".format(
                big_file_name, err), file=sys.stderr)
        sys.exit(1)
    
    # Create a CSV (Comma Separated Value) reader based on this
    # open file handle.  We can use the reader in a loop iteration
    # in order to access each line in turn.
    big_reader = csv.reader(big_file_fh)

    try:
        small_file_fh = open(small_file_name, 'w', encoding="utf-8-sig", newline='')

    except IOError as err:
        print("Unable to create small file '{}' : {}".format(
                small_file_name, err), file=sys.stderr)
        sys.exit(1)

    small_writer = csv.writer(small_file_fh)

    # Header of the csv file
    small_writer.writerow(["REF_DATE","GEO","National Occupational Classification","Job vacancy characteristics","Statistics","VALUE"])

    # creating an array
    arr = []

    # Going through the CSV data
    for data_fields in big_reader:
        #Not printing the first line of the file
        if data_fields[0] != "REF_DATE": 
            if data_fields[1] == "Ontario" and data_fields[3] != "Total, all occupations" and data_fields[4] == "Seasonal" and data_fields[5] == "Job vacancies" and ("2022-07" <= data_fields[0] <= "2023-09"):
                value = data_fields[12] 
                # Sets the value to 0 in case of no value
                if data_fields[12] == "":
                    value = 0
                # uses the append function to add each line to the array called arr
                arr.append([data_fields[0], data_fields[1], data_fields[3], data_fields[4], data_fields[5], str(value)])

    # uses the sort function to sort the array called arr from highest value column to lowest value column
    arr.sort(key=lambda x: float(x[5]), reverse=True)

    # writes array to the new file
    for row in arr:
        small_writer.writerow(row)


    #open the newly created and processed file
    try:
        new_small_file_fh = open(str(argv[2]), 'r', encoding="utf-8-sig")

    except IOError as err:
        # Here we are using the python format() function.
        # The arguments passed to format() are placed into
        # the string it is called on in the order in which
        # they are given.
        print("Unable to open new small file '{}' : {}".format(
                new_small_file_fh, err), file=sys.stderr)
        sys.exit(1)

    #create a reader for the file
    new_small_reader = csv.reader(new_small_file_fh)

    #create an array to hold the graph data
    graph_data = []

    #add the data to the new array
    for data_fields in new_small_reader:
        if len(graph_data) == 24:
            break
        if data_fields[2] != "National Occupational Classification":
            job = data_fields[2]
            value = data_fields[5]
            graph_data.append((job, value))

    #sort the data again just in case
    graph_data.sort(key=lambda x: int(x[1]), reverse=True)

    top_10 = graph_data[:24]

    #get the data out of the array and into the variables job and value
    job = [row[0] for row in top_10]
    value = [int(row[1]) for row in top_10]

    #create graph
    mpl.figure(figsize=(12, 8))
    mpl.bar(job, value, color='skyblue')
    mpl.ylabel('Number of Job Vacancies')
    mpl.xticks(rotation=45, ha='right')  
    mpl.title('Top 10 Job Vacancies in Ontario')
    mpl.tight_layout()

    #display graph
    mpl.show()


#
# Call our main function, passing the system argv as the parameter
#

main(sys.argv)

#
#   End of Script
#
