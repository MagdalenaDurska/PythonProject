## Project Overview

This project processes financial instrument price data from time series input files. A *financial instrument* represents assets such as currencies or 
commodities with historical prices.

The program reads an input text file containing multiple time series for instruments like `Instrument1`, `Instrument2`, and `Instrument3`. 
It passes this data to a calculation engine that performs specific statistical analyses:

- Calculates the **mean** price for `Instrument1`.
- Calculates the **mean** price for `Instrument2` filtered for November 2014.
- Calculates the **standard deviation** for `Instrument3`.
- For all other instruments, it sums the **10 most recent** price entries.

To simulate real-world factors affecting prices, a **value multiplier** is applied to each instrument's price. These multipliers are dynamically loaded from 
a database table called `INSTRUMENT_PRICE_MODIFIER`. 
Multipliers may change, but refresh no more frequently than every 5 seconds. If no multiplier is found for an instrument, its original value is used.

----------------------------------------------

## Justification of selected design decisions:

### Data parsing:
The program processes potentially very large data files, so parsing the data line by line is a good choice for efficient memory management. 
Loading the entire file into memory at once would be impractical and could lead to memory exhaustion or program crashes.
This solution uses minimal memory is scalable and simple - for simple calculations like those addressed in this project, in my opinion, this is the best option

### Mockup database
SQLite (sqlite3 lib) has been selected for emulating real database behavior with minimal overhead and complexity during development.
What is also important - sqlite3 library is included in Python’s standard library, ensuring easy integration without external dependencies

### Centralized settings
From the project requirements it looks that it is expected that name of the instruments for different types of calcualtion as well as date 
on which INSTRUMENT2 calculations needs to be filtered are fixed. For this reason, to allow easier runs, I have created a config file as part of the repository. 
This solutions guarantees centralized settings, easy to find, read, re-use and easy to change. If these parameters were to be changed on a frequently basis, 
then reading them from the yaml file would be much better option, as no code changes would be required.

### Logging
Logging functionality is enabled. Log levels, might need to be updated based on the business requirements.

----------------------------------------------

## How to run the program

### inputs/outputs
The program can be run with an input file of any name and saved to any location. For the batch run it is expected that input file is called 
input.txt and is located in the input folder and the outputs are saved in output folder. (A sample input file is already provided in the input folder)

### run main.py
you can run the program in python terminal or cmd, by going to project location and using below commands:

for input file located anywhere and with any file name, and for self-defined output folder:

  ```python main.py -i C:/Users/s6sal/Downloads/input.txt -o C:/Users/s6sal/Downloads```
  
(for example: python main.py -i C:/Users/user1/Downloads/input_file.txt -o C:/Users/user1/Downloads)


for a default input location and file name (you can replace input file in the project folder to a different one, but it also need to be called input,txt), 
and a default ouput location

  ```python main.py -b```

### run run_batch.bat
you can do a batch run by opening cmd, going to project location and typing:

  ```run_batch.bat```

### run unit tests
to run all the unit test, please go to the project location in Python terminal and type:

  ```python -m unittest discover -s tests -p "test_*.py"```

