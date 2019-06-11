# TSP

On solving(!Maybe Maybe not) the Travelling sales person problem.

## Requirements

    python2.7+ or python3.5+
    numpy
    networkx

Required python packages maybe installed by calling

    pip install -r requirements.txt

## Code structure

    ./algorithms
        branch_and_bound.py
        approx.py
        local_search_1.py
        local_search_2.py
        hybrid_1.py
    ./DATA
        *.tsp
    ./helpers
        graph.py
    main.py
    other_python_scripts

## Executing algorithms

    python .\main.py -inst <a .tsp file> -alg <BnB | Approx | LS1 | LS2 | H1 > -time <cut off time in seconds> [-seed <random_seed>]

example

    python main.py -inst DATA/small.tsp -alg BnB -time 10

## For the Competetion

    Our best algorithm is present in hybrid_1.py. It is a combination of the approximation algorithm with the local search algorithm.

    In case you decide to judge by running the code for 10 mins. Please use 'H1' as alg argument. Remember to bind the time to 600.
    If you want our best case polynomial time approximation(<2OPT). Please use 'Approx' as alg argument. It runs in no time even for Roanoke.

## The Rest of the files

Every other python script used is for generating the plots and tables. They require 

    matplotlib
    seaborn
    pandas

These need not be executed and the packages are not a part of reuirements.txt file
