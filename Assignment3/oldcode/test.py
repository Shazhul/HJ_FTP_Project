import commands
import os
test = "this is a test"

print test

test_list = test.split()

print test_list

test_1 = ' '.join(test_list)

print test_1

dataBuffer = ""

for line in commands.getstatusoutput('ls -l'):
    if isinstance(line, basestring):
        dataBuffer += line

print dataBuffer

a = ( 1, 5)

b , c = a
print a
print b
print c

for root, dirs, files in os.walk("."):
    print files
        
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
