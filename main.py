#########################	IMPORT NEEDED MODULES	  #########################

import sys
from gui_2 import GUI_process
import multiprocessing as mp

#########################	  LAUNCH WINDOW APP		  #########################

def processArgv():	...

def main():
    app_queue = mp.Queue()
    outside_queue = mp.Queue()

    app_proc = mp.Process(target=GUI_process, args=(app_queue, outside_queue))

    app_proc.start()
    app_proc.join()

if __name__ == "__main__":
	if sys.argv:
		processArgv()
	main()
    