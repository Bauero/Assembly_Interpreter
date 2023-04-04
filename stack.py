from datatypes import *

#	4096 16-bit places 
STACK = [Node(0) for _ in range(65536)]
stackCount = len(STACK)//8