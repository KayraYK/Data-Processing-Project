#!/usr/bin/env python

import sys
import matplotlib.pyplot as mpl
import csv



def main(argv):

    new_small_file_name = (argv[1])

    #open the newly created and processed file
    try:
        new_small_file_fh = open(str(argv[1]), 'r', encoding="utf-8-sig")

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
