#include "Gradient_Descent.hpp"
Gradient::Gradient(){
    m_nDims = 0;
    m_stepSize = 0.0;
    m_maxIter = 1;
    m_h = 0.001;
    m_gradientTresh = 1e-09;
}

Gradient::~Gradient(){
    //if Anything needs cleaning
}

void Gradient::InitObjectFunc(function<double(vector<double>*)> objectFUnc){
    Gradient::m_objectFunc = objectFUnc;
}

void Gradient::SetStartPoint(const vector<double> startpoint){
    m_startPoint = startpoint;
    m_nDims = startpoint.size();
}



void Gradient::Set_StepSize(double stepsize){
    m_stepSize = stepsize;// also know as gamma OR LEARNING RATE
}



void Gradient::Set_IterationRange(int max_iterations){
    m_maxIter = max_iterations;
}



void Gradient::Set_GradiantTresh(double Gradient_Tresh){
    m_gradientTresh = Gradient_Tresh;
}


void Gradient::Optimize(std::vector<double> *funcLoc, double *funcVal){
    m_currentPoint = m_startPoint;
    int iterCount = 0;
    double gradientMagnitude = 1.0;

    while ((iterCount <m_maxIter)&&(gradientMagnitude > m_gradientTresh)){
        std::vector<double> gradientVector = ComputeGradientVector();
		gradientMagnitude = ComputeGradientMagnitude(gradientVector);
        
        std::vector<double> newPoint = m_currentPoint;
        
        for (int i=0; i<m_nDims; ++i)
		{
			newPoint[i] += -(gradientVector[i] * m_stepSize);
		}
        m_currentPoint = newPoint;
        iterCount++;
    }

    *funcLoc = m_currentPoint;
    *funcVal = m_objectFunc(&m_currentPoint);
}



double Gradient::ComputeGradient(int dim)
{
	// Make a copy of the current location.
	vector<double> newPoint = m_currentPoint;
	
	// Modify the copy, according to h and dim.
	newPoint[dim] += m_h;
	
	// Compute the two function values for these points.
	double funcVal1 = m_objectFunc(&m_currentPoint);
	double funcVal2 = m_objectFunc(&newPoint);
	
	// Compute the approximate numerical gradient.
	return (funcVal2 - funcVal1) / m_h;
}

vector<double> Gradient::ComputeGradientVector()
{
	std::vector<double> gradientVector = m_currentPoint;
	for (int i=0; i<m_nDims; ++i)
		gradientVector[i] = ComputeGradient(i);
		
	return gradientVector;
}

// Function to compute the gradient magnitude.
double Gradient::ComputeGradientMagnitude(std::vector<double> gradientVector)
{
	double vectorMagnitude = 0.0;
	for (int i=0; i<m_nDims; ++i)
		vectorMagnitude += gradientVector[i] * gradientVector[i];
		
	return sqrt(vectorMagnitude);
}
