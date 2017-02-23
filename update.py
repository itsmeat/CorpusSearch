import subprocess
test = subprocess.Popen(["python","tok_lem.py"], stdout=subprocess.PIPE)
print("updating docs2.csv")
output = test.communicate()[0]
test = subprocess.Popen(["python","db_stats.py"], stdout=subprocess.PIPE)
print("updating dict.pickle")
output = test.communicate()[0]
test = subprocess.Popen(["python","vector.py"], stdout=subprocess.PIPE)
print("updating vector.pickle")
output = test.communicate()[0]
