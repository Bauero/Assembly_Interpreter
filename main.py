#########################	IMPORT NEEDED MODULES	  #########################

import sys
from GUI import GUI_process
import multiprocessing as mp

#########################	  LAUNCH WINDOW APP		  #########################

def processArgv():	...

def main():
    app_queue       = mp.Queue()
    engine_queue    = mp.Queue()
    data_queue      = mp.Queue()
    main_queue      = mp.Queue()
	
    app_proc = mp.Process(target=GUI_process, args=(app_queue, engine_queue, main_queue))
	

    app_proc.start()
    app_proc.join()

if __name__ == "__main__":
	if sys.argv:
		processArgv()
	main()
    