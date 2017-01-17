// ExecDoneDLL.cpp : Defines the entry point for the console application.
//

#include <iostream>	  
#include <ctime>
#include "DONEdll.h"


double * TestFunc(double *dataset, int dim, void * para) {
	dataset[dim] = 0;

	for (int jjj = 0; jjj < dim; jjj++) {
		dataset[dim] += (dataset[jjj] + 0.1)* (dataset[jjj] + 0.1);
	}
	dataset[dim] = -exp(-dataset[dim])+3;
	std::cout << "\n" << dataset[dim];
	//dataset[dim] = 1;
	return dataset;
}


int main()
{
	/*int  answertoall;
	answertoall = fnTestdll(5);
	std::cout << " The answer to all is " << answertoall << "\n";	*/			

	int d = 6; //dimension of input function
	int N = 100;
	int D = 1000; //dimension of random Fourier expansion
	int windowsize = 10;
	double sigma = sqrt(2); //kernel bandwidth 
	double lam = 0.2; // regularization parameter
	double lb = -5; // lower bound 
	double ub = 5; // upper bound 
	double expl = (0.1)*sqrt(3.0) / sqrt((double)d); // perturbation for next measurement //double sigmaend = sigma1 / 2; //int explstrategy = 1;
	double *x0;
	x0 = new double[d];
	double *measurementinfo;
	measurementinfo = new double[d+1];
	for (int jjj = 0; jjj < d; jjj++) {
		x0[jjj] = 7 * 0.2 / d;
		measurementinfo[jjj] = 7 * 0.2 / d;
	}
	double *lbv = new double[d]; lbv[0] = -2; lbv[1] = -1.8; lbv[2] = -2; lbv[3] = -.5; lbv[4] = -.5; lbv[5] = -.2; // lower bound 
	double *ubv = new double[d]; ubv[0] = 2; ubv[1] = 1.8; ubv[2] = 2; ubv[3] = .5; ubv[4] = .5; ubv[5] = .2; // upper bound  
	double *explv = new double[d]; explv[0] = 0.15; explv[1] = 0.15; explv[2] = 0.15; explv[2] = 0.07; explv[4] = 0.07; explv[5] = 0.03; // perturbation for next measurement //double sigmaend = sigma1 / 2; //int explstrategy = 1;
	
	std::clock_t start;
	double duration;
	start = std::clock();
	for (int jjj = 0; jjj < (N); jjj++) {
		TestFunc(measurementinfo, d, (void *)&lam);
		DONE(measurementinfo, x0, d, lb, ub, D, lam, sigma, expl, windowsize, 0);
		}
	duration = (std::clock() - start) / (double)CLOCKS_PER_SEC;
	std::cout << "\nDuration DONE algorithm : " << duration << "  seconds \n";
	double avg = 0;
	for (int jjj = 0; jjj < d; jjj++) {
		avg += abs(x0[jjj]);
	}
	avg /= d;
	std::cout << "Optimized average final x: \n" << avg << "\n";	   

	for (int jjj = 0; jjj < d; jjj++) {
		x0[jjj] = 7 * 0.2 / d;
		measurementinfo[jjj] = 7 * 0.2 / d;
	}
	
	start = std::clock();
	TestFunc(measurementinfo, d, (void *)&lam);
	DONE(measurementinfo, x0, d, lbv, ubv, D, lam, sigma, explv, windowsize, 1);
	for (int jjj = 0; jjj < (N-1); jjj++) {
		TestFunc(measurementinfo, d, (void *)&lam);
		DONE(measurementinfo, x0, d, lbv, ubv, D, lam, sigma, explv, windowsize, 0);
	}
	duration = (std::clock() - start) / (double)CLOCKS_PER_SEC;
	std::cout << "\nDuration DONEv algorithm : " << duration << "  seconds \n";

	avg = 0;
	for (int jjj = 0; jjj < d; jjj++) {
		avg += abs(x0[jjj]);
	}
	avg /= d;
	std::cout << "Optimized average final x: \n" << avg << "\n TEST COMPLETE";

	getchar();
	return 0;
}