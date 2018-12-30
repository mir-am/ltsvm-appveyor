/*
LightTwinSVM Program - Simple and Fast
Version: 0.2.0-alpha - 2018-05-30
Developer: Mir, A. (mir-am@hotmail.com)
License: GNU General Public License v3.0

The ClippDCD algorithm is implmeneted for solving dual optimization problems of TwinSVM.
Its speed is improved significantly by Mir, A. 

This algorithm was proposed by:
Peng, X., Chen, D., & Kong, L. (2014). A clipping dual coordinate descent algorithm for solving support vector machines. Knowledge-Based Systems, 71, 266-278.

This C++ extension depends on the follwing libraries:
- Armadillo C++ Linear Agebra Library (http://arma.sourceforge.net)
- pybind11 for creating python bindings on Linux (https://pybind11.readthedocs.io)
- Cython for building C++ extension module on Windows (http://cython.org/)

Change log:
Mar 21, 2018: A bug related to the WLTSVM classifier was fixed. the bug caused poor accuracy. 
Bug was in section which filters out indices.

Mar 23, 2018: execution time improved significantly by computing dot product in temp var.

May 4, 2018: A trick for improving dot product computation. It imporves speed by 4-5x times.

*/

#include <vector>

// For consistency between Cython and Pybind11
// same interface for Python will be generated.
#if defined __unix__ || defined __APPLE__
    #define clippdcd_func_name clippDCD_optimizer
#elif defined _WIN64
    #define clippdcd_func_name clippDCDOptimizer
#endif

std::vector<double> clippdcd_func_name(std::vector<std::vector<double> > &dual, const double c);
