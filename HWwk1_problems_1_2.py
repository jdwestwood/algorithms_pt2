# first line of input file is number of jobs n.
# subsequent lines are weight wj and length lj of each job.
# completion time Cj of job j is the sum of job lengths up to and including j.
# objective is to minimize the weighted sum of completion times (sum of wjCj).
# 
# problem 1: prioritize according to wj - lj.
# problem 2: prioritize according to wj/lj.

# read 1st line of input file into n
# read rest of input file into a list of jobs
# sort the list according to the priority function
# iterate through the list and calculated the weighted sum of completion times.

class job:
    weight = 0
    length = 0
    priority = 0
    completion_time = 0

dataFile = open('HWwk1_problems_1_2_job_file.txt', 'r')
#dataFile = open('HWwk1_short.txt', 'r')
n = int(dataFile.readline())

jobList = []
for line in dataFile:
    jobDesc = line.split()
    jobObj = job()
    jobObj.weight = int(jobDesc[0])
    jobObj.length = int(jobDesc[1])
    jobObj.priority = jobObj.weight - jobObj.length
#    jobObj.priority = jobObj.weight/float(jobObj.length)
    jobObj.completion_time = 0
#    print line, jobObj.weight, jobObj.length, jobObj.priority
    jobList.append(jobObj)

# sort by priority, then by weight in descending order; trick is to return a tuple
# from the sorting function
jobList.sort(key=lambda jobObj: (jobObj.priority, jobObj.weight), reverse=True)

completion_time = 0
wt_sum_completion_time = 0
for jobObj in jobList:
    completion_time += jobObj.length
    wt_sum_completion_time += jobObj.weight*completion_time
    jobObj.completion_time = completion_time
#    print jobObj.weight, jobObj.length, jobObj.priority, jobObj.completion_time

print 'Completion time:', completion_time
print 'Weighted sum of completion times:', wt_sum_completion_time





