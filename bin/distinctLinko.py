#!/usr/bin/env python
import sys
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

for arg in sys.argv[1:]:
	n = int(arg)
	Ln = 0
	for i in range(1,n):
		Ln += i
	print "n = %d, Ln = %d, 2^Ln = %s" % (n,Ln,locale.format("%d", 2**Ln, grouping=True))
