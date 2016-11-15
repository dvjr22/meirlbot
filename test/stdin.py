import sys


line = sys.stdin.readline()
while line:
    print line,
    if line == 'stop\n':
        print 'stopping'
        sys.exit(1)
    line = sys.stdin.readline()
