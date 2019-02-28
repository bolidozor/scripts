from sys import argv
import datetime
import subprocess

script, input_file = argv


f = open(input_file,"r")
dates = []

for line in f:
	dates.append(line) # loops over the lines in the file and store them in dates

all_data = dates[1:] # removes the first line with labeling words
keep_dates_and_times_as_str = []
keep_dates_and_times_as_obj = []
keep_dates_and_times_correct_format = []

for line in all_data:
	second_date = line.split() #creates a list of the words in each line
	
	date_and_time_str = second_date[0] + ' ' + second_date[1] #creates a variable containing both date and time by composing the first two columns together

	keep_dates_and_times_as_str.append(date_and_time_str)
	
	datetime_obj = datetime.datetime.strptime(date_and_time_str,'%d-%m-%Y %H:%M:%S') # converts the string with date and time into a datetime object
	datetime_obj_subtracted = datetime_obj - datetime.timedelta(minutes=5) #subtracts 5 minutes from datetime_obj
	keep_dates_and_times_as_obj.append(datetime_obj_subtracted)
	datetime_obj_subtracted_str = datetime_obj_subtracted.strftime('%d%m%H%M') #creates a correct format for our command
	keep_dates_and_times_correct_format.append(datetime_obj_subtracted_str)
	

print keep_dates_and_times_correct_format

for time_strings in keep_dates_and_times_correct_format:
	subprocess.call(['at', '-t', time_strings, '-f', 'FUMA-event-rec.sh'])

	
