#include <iostream>
#include <chrono>
#include <cmath>
#include <ctime>

using namespace std;
using namespace std::chrono;

// Try to optimize the learning process.
// Try to improve the end results

#define eps 1e-3
#define Learning_rate eps
#define set_size 4


float training_set[][3]={
        {0,0,    0},
        {0,1,    1},
        {1,0,    1},
        {1,1,    1}
};
// w -> parameters


float generate_rand(){
    srand(time(0));
    return static_cast<float>(rand()*100) / static_cast<float>(RAND_MAX);
}



float sigmoidf(float x){ return 1.0f / (1.f + expf(-x)); }


float cost_func(float w1, float w2, float bias){
    float Result = 0.0f;

    for(size_t i = 0; i<set_size; ++i){
    
        float x1 =training_set[i][0];
        float x2 = training_set[i][1];

        float y = sigmoidf(( x1*w1 + x2*w2 + bias ));

        float d = y - training_set[i][2];

        Result += (d*d);
    }
    return (Result/set_size);
}




void Forwarding(float& w1, float& w2, float& bias){
    cout<<"  <-------Forwarding------->\n";
    for(int i =0; i<2;++i){
        for(int j = 0; j<2;++j){
            cout<<"       "<<i<<"<->"<<j<<" | "<<sigmoidf(i*w1 + j*w2 + bias)<<endl;
        }
    }
}




void OR_gates_solve(){

    float err = 0.0f, w1 = generate_rand(), w2 = generate_rand();
    float bias = generate_rand();

    for(size_t i =0; i<(130*1000); ++i){

        err = cost_func(w1,w2, bias);

       
        float dw1 = (cost_func(w1 + eps, w2, bias)- err)/eps;
        w1 -= Learning_rate * dw1;
       
       
        float dw2 = (cost_func(w1, w2+eps, bias)- err)/eps;
        w2 -= Learning_rate * dw2;
       

        float dbias = (cost_func(w1,w2, bias+ eps)-err)/eps;
        bias -= Learning_rate* dbias;
        //cout<<"\t| w1 = "<<w1<<"|\n\t| w2 = "<<w2<<"|\n\t| cost = "<<err<<"|\n\t| Bias = "<<bias<<"\n\n";
    }
    cout<<"   Cost_Fucntion::"<<err<<endl;
    Forwarding(w1,w2,bias);
}




int main(void){
    auto start = high_resolution_clock::now();   
    OR_gates_solve();
    auto stop = high_resolution_clock::now();

    auto duration = duration_cast<milliseconds>(stop - start);

    cout<<"\n\nTime for execution -> "<<duration.count();

    return 0;
}