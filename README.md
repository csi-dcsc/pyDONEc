# pyDONEc
A python implementation of the DONE optimization algorithm. Wraps on a C++ dll


This is a Python library for fast implementation of the Data-based Online
Nonlinear Extremum-seeker (DONE) algorithm, presented by the CSI group at TU Delft for, but not limited to sensorless adaptive optics applications.

The C++ implementation uses LAPACK, OPENBLAS, and ZIGGURAT. The corresponding 64bit dlls are included in the package.
 
Openblas copyright: Copyright 2009, 2010 The University of Texas at Austin.

Lapack copyright: Copyright (c) 2010, Intel Corp.

Ziggurat copyright: Marsaglia + Tsang / Leong, Zhang et al Ziggurat generator, Copyright (C) 2013  Dirk Eddelbuettel

The library requires numpy and ctypes.
An example file is provided, with the minimization of a 10 dimensional paraboloid, with measurements affected by gaussian noise. 
For different problems the hyper-parameters might require tuning. See https://arxiv.org/abs/1603.09620 for some theoretical and practical insight into the hyper-parameters.



Description of the algorithm:

The Done algorithm is particularly efficient in minimizing unknown cost functions through the acquisition of a limited amount of measurements, affected by noise.
The DONE algorithm is an optimization algorithm based on the recursive creation of a nonlinear model of the cost function during the optimization procedure itself.
At the initialization of the algorithm for a "d" dimensional problem, a random set of "D" cosine functions C1(x), . . .,CD (x) is generated. The frequency of the cosine functions selected follows a gaussian distribution of width "sigma". The cost function model, at every step k is defined as the sum of the cosine functions multiplied by weights A1, ... ,AD.
At the k-th step, the algorithm performs a linear least square fit on the previous k measurements of the metric, determining the values of the parameters A1(k), . . ., AM(k), to obtain the cost function which best approximates the available measurements. The coordinates of the (k + 1) - th measurements are determined as those of the minimum of obtained cost function, plus a small random perturbation, determined by the exploration parameter "expl".The minimum of the cost function is estimated through nonlinear optimization. In order for the algorithm to converge even if the cost function is dynamically varying, only the most recent "m" measurements are taken into account.

