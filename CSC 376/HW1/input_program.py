#import statements
import sys 

#global vars
clargs = ["", "", False] 
sysargs = sys.argv

#start of code
print("Standard Input:")
input = sys.stdin.readline().replace("\n", "")
while input:
    print (input)
    input = sys.stdin.readline().replace("\n", "")

#loops through arg array
for args in range(1, len(sysargs)):
    if(sysargs[args] == "-o"):
        clargs[0] = sysargs[args + 1]
    elif (sysargs[args] == "-t"):
        clargs[1] = sysargs[args + 1]
    elif (sysargs[args] == "-h"):
        clargs[2] = True

#prints all commands if there appears to be on
print("Command line arguments:")
if (clargs[0] != ""):
    print("option 1: " + clargs[0])
if (clargs[1] != ""):
    print("option 2: " + clargs[1])
if (clargs[2] == True):
    print("option 3")