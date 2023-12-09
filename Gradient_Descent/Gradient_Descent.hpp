#ifndef GRADIANT_DESCENT_H
#define GRADIANT_DESCENT_H

#include <iostream>
#include <functional>
#include <cmath>
#include <memory.h>
#include <vector>

using namespace std;

class Gradient{
    public:
        
        Gradient();
        ~Gradient();

    void InitObjectFunc(function<double(vector<double>*)> objectFUnc);
    void SetStartPoint(const vector<double> startPoint);  
    
    // how could the init values be automated
    void Set_StepSize(double stepSize); // this is gama :)
    void Set_IterationRange(int max_Intr);
    void Set_GradiantTresh(double Gradient_Tresh);

    void Optimize(vector<double> *fincLoc, double *funcVal);

    private:
        double ComputeGradient(int dim);
        vector<double> ComputeGradientVector();
        double ComputeGradientMagnitude(vector<double> gradientVector);

    int m_nDims, m_maxIter;
    double m_gradientTresh, m_h, m_stepSize;
    vector<double> m_startPoint, m_currentPoint;
    function<double(vector<double>*)> m_objectFunc;

};
#endif