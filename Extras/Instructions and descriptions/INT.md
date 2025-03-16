
# INTERRUPT
## Description
This function performs system interruption. To perform interruption, proper value of
interruption and arguments (AH and sometimes DL) must be specified. Calling proper
interruption allows to execute action. Since this functionality is mostly crucial
with actual interaction with machine, and it's quite complicated to implement
while being trivial to understand (look up proper AH and INT values, set and execute)
interrupt functionality was implemented in basic form, although allowing for further
development for anyone interested. Depending on implementation, interrupt can do nothing
or change quite a lot. 

## Supported operations
### 1. INT 21H, AH = 2   (2h)
Write character which value is stored in DL. Doesn't change flags, nor registers.
### 2. INT 21H, AH = 44  (2Ch)
Get current time in the operating system, and store it in CX and DX registers,
putting:
- CH - Hours
- CL - Minutes
- DH - Seconds
- DL - Milliseconds
### 3. INT 21H, AH = 0   (0h)
Terminate execution.
### 4. INT 21H, AH = 76  (4Ch)
Terminate execution.
### 5. INT 21H, AH = 10  (Ah)
Ask user for input with maximum specified length. At the time of calling, register
DX must contain max length (DH) and location in memory (DL). Then user will be prompted
to input text into terminal. Pressing Enter will confirmed input of the text, text
will be stored in memory under the addres, and program will be contined.
