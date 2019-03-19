#import bzremote
import imp
from sys import argv
import datetime
import subprocess

bzremote = imp.load_source('bzremote', './bzremote')

for filename in argv[1:]: # enable using *.txt formulation
    f = open(filename,"r")
    dates = []

    for line in f:
        dates.append(line) # loops over the lines in the file and store them in dates

    all_data = dates[1:] # removes the first line with labeling words
    keep_dates_and_times_as_str = []
    keep_dates_and_times_as_obj = []
    keep_dates_and_times_correct_format = []

    for line in all_data:
        second_date = line.split() #creates a list of the words in each line    

        if second_date:     # check if list is not empty
            date_and_time_str = second_date[0] + ' ' + second_date[1] #creates a variable containing both date and time by composing the first two columns together

            keep_dates_and_times_as_str.append(date_and_time_str)
        
            datetime_obj = datetime.datetime.strptime(date_and_time_str,'%d-%m-%Y %H:%M:%S') # converts the string with date and time into a datetime object
            datetime_obj_subtracted = datetime_obj - datetime.timedelta(minutes=5) #subtracts 5 minutes from datetime_obj
            keep_dates_and_times_as_obj.append(datetime_obj_subtracted)
            datetime_obj_subtracted_str = datetime_obj_subtracted.strftime('%m%d%H%M') #creates a correct format for our command
            keep_dates_and_times_correct_format.append(datetime_obj_subtracted_str)
     

    print (keep_dates_and_times_correct_format)

    for time_strings in keep_dates_and_times_correct_format:
        #print('at' + ' -t ' + str(time_strings) + ' -f' +' FUMA-event-rec.sh')
        #subprocess.call(['at', ' -t ', time_strings, '-f', 'FUMA-event-rec.sh'])


        #print ('./bzremote ' + 'ssh ' + '% ' + 'at' + ' -t ' + str(time_strings) + ' -f' + ' FUMA-event-rec.sh')
        #subprocess.call(['./bzremote ', 'ssh ', '% ', 'at', ' -t ', time_strings, '-f', 'FUMA-event-rec.sh'])
	
        #print('./bzremote ' + 'ssh ' + '% ' + 'ls')
        subprocess.call(['./bzremote ', 'ssh ', '% ', 'ls'])
 
