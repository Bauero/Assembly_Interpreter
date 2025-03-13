# Instruction on how to run code tests

1. Make sure you have pytest installed - can be done by running 
```python
pip install pytest
```
while your virtual environemnt is activated
2. Copy file to main folder - it has to run from that location as there are some imports - if that would work some other way around, good for you. For 'plug&play' experience, copy file to root folder (same as `main.py`)
3. Run test using:
```python
pytest script_name.py
```