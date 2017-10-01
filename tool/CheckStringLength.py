from __future__ import print_function
import sys

print ("Check string length : ", end='')
# print "test".strip()
checkString = sys.stdin.readline().strip('\n').strip()

# sys.stdout.write("%s : %s\n" % (checkString, len(checkString)))
print ("%s : %s" % (checkString, len(checkString)))