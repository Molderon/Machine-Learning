#include "Gradient_Descent.hpp"


double ObjectFcn(vector<double> *funcLoc)
{
	// one parameter
	double x = funcLoc->at(0);
	double y = funcLoc->at(1);
	//return (x*x*x*x) + (2*(x*x*x)) - (6*(x*x))+ (4*x) + 2;
	return (x*x) + (x*y) + (y*y);
}

// #Research
//------------------------------------------
// escape local minimas
// estimate set-up parameters


// # Assistance Requiered
// Create a proper model of a lung


//# To be optimised
// ------------------------------------------
// multithread - the descent
// refactor bitwise operators
// use smaller data-types


int main(int argc, char* argv[])
{
	function<double(vector<double>*)> p_ObjectFcn{ ObjectFcn };
	Gradient solver;

// -------------------------------------------------*
	solver.InitObjectFunc(p_ObjectFcn);			    // --> Can the initialization
	vector<double> startPoint = {5.0f, 5.0f};	    //     of the `et-up params,
												    //	   be automated?
	solver.SetStartPoint(startPoint);			    //
	solver.Set_IterationRange(50);				    //
	solver.Set_StepSize(0.1);					    //
// -------------------------------------------------*

	vector<double> funcLoc;
	double funcVal;
	solver.Optimize(&funcLoc, &funcVal);
	
	cout << "Function location: " << funcLoc[0] << endl;
	cout << "Function value: " << funcVal << endl;
	
	return 0;
}