""" This python file reads the data.csv from http://www2.projects.science.uu.nl/memotion/emotifydata/
The data is added and put into a list of lists (data) which we can use for training our Machine Learning
algorithm for mood analysis. Another Python file supplied by Barry scrapes the spotify API for audio-features
related to these tracks. In this way we can compare interviewees opinions to spotify's supplied parameters."""
import csv
from numpy import add
import sys

if(len(sys.argv) < 2):
    print("Give lower bound on votes")
    exit()

data = []

with open('./../machinelearning/data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    iterrows = iter(csv_reader)
    next(iterrows)
    numericdata = []
    
    #Iterate over all columns except text and map strings -> int
    for row in csv_reader:
        del row[1]
        for i in range(6):
            del row[10]
        for i in range(10):
            row[i] = int(row[i])
        numericdata.append(row)

    list_count = 0
    new_data = [0 for i in range(13)]
    numberofresponses = [0 for i in range(401)]

    # Add together responses on same song
    for row in numericdata:
        gradesum = sum(row[1:])
        if gradesum == 0:
            gradesum = 1

        if row[0] > list_count:
            if(numberofresponses[list_count - 1] >= int(sys.argv[1])):
                data.append([row[0]] + [value / numberofresponses[list_count - 1] for value in new_data])
            new_data = [value / gradesum for value in row[1:]]
            list_count += 1
            numberofresponses[list_count] += 1
        else:
            new_data = add(new_data,[value / gradesum for value in row[1:]])
            numberofresponses[list_count-1] += 1

with open('./../machinelearning/moods_' + sys.argv[1] +'.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerows(data)
