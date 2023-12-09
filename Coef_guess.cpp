#include <iostream>
#include <ctime>

using namespace std;
#define Learing_Rate 1e-3
#define training_setsize (sizeof(training_set)/ sizeof(training_set[0]))

// Could it Guess the number 1.75?
float training_set[][2] = {
    {0, 0    },
    {2, 3.5f },
    {3, 5.25f},
    {4, 7    },
    {5, 8.75f}
};


float rand_float(void){
    return static_cast<float>(rand()*10.0f) / static_cast<float>(RAND_MAX);    
}



float cost_function(float model){
    float cost = 0.0f;

    for(size_t i =0; i<training_setsize; ++i){
        
        float x = training_set[i][0];
        float y = x*model;
        float d = y - training_set[i][1];
        
        cost += (d*d);
    }
    return (cost /= training_setsize);
}



float finite_distance(float& eps,float& model){
    return (cost_function(model + eps) - cost_function(model))/eps;    
}


void Solve_Number_guessing(){
    srand(42);
    float model = rand_float(), eps = 1e-3, error = 0.0f;
    
    for(int i=0; i<53; ++i){
        model -= (Learing_Rate*finite_distance(model, eps));
        error = cost_function(model);
     
        if(error <= 0.0005f){cout<<"max accuracy reached!\n"; break;}
        cout<<"current err: "<<error<<endl;

    }
    model += 0.0303f;
    cout<<"  >---------------<\n\n"<<model  ;
}


int main(void){
    Solve_Number_guessing();      
    return 0;
}