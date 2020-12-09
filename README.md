High-level description of the repository
========================================

The code in this repository aims to extract protein information for diseases and rank extracted 
protein with respect to their relevance for the disease. This ranking is based
on semantic concepts that are also extracted and clustered from publication
abstracts. The work was initiated based on 
[this publication](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0233956)

Note that the repository is currently under development and therefore some
features do not exist yet or are implemented in a rudimentary fashion. To provide
feedback, please use the issue tracker of the repository -- thanks.


Dependencies
------------
The code provided in this repository relies on Python 3.8 and the following additional Python packages:

* pyyaml

For ease of use a 
[conda environment file](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) 
has been provided with which a new environment can be generated or an existing one updated.


Getting started
---------------
The best way to get started is to look in the scripts folder of the repository and follow the instructions in the 
README file of this folder. The scripts illustrate the application of the different packages and allow to execute the 
pipeline. There is an example folder with an illustrative configuration file and where output results will be written
to. 