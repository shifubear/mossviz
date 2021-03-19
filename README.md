# mossuci

A simple moss visualization tool. Currently works only for C++ projects, but adapting it to work with other languages is a simple change in parameters.  

## Requirements and Usage

The `mossuci.py` must be called in a directory with the following file structure: 

- `base/` This is the directory that contains all the base files for the project. 
- `submissions/` The directory that contains all the submissions. In this directory, each submission should be a directory with some ID for the student, containing all the files for the project. 

Once `mossuci.py` is called, a `mossdata.csv` file is created. Once this is prepared, use `generate_graph.py` to generate a graph of the data. Currently the parameters must be tweaked from within the file. 
