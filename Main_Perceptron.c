#include "./config.h"

/*
            (HOME PROJECT)
        -Simple Neural Network-

___  ___      _     _        powered by:             
|  \/  |     | |   | |                      
| .  . | ___ | | __| | ___ _ __ ___  _ __  
| |\/| |/ _ \| |/ _` |/ _ \ '__/ _ \| '_ \ 
| |  | | (_) | | (_| |  __/ | | (_) | | | |
\_|  |_/\___/|_|\__,_|\___|_|  \___/|_| |_|

[Tribute to the first PERCEPTRON && inspired by "Veritasium"'s video]
-> https://www.youtube.com/watch?v=GVsUOuSjvcg

*/



float feed_forward(Layer inputs, Layer weights)
{
    float output = 0.0f;

    for (int y = 0; y < HEIGHT; ++y) {
        for (int x = 0; x < WIDTH; ++x) {
            output += inputs[y][x] * weights[y][x];
        }
    }

    return output;
}



int train_pass(Layer inputs, Layer weights)
{
    static char file_path[256];
    static int count = 0;

    int adjusted = 0;

    for (int i = 0; i < SAMPLE_SIZE; ++i) {
        layer_random_rect(inputs);

        if (feed_forward(inputs, weights) > BIAS) {

            sub_inputs_from_weights(inputs, weights);

            snprintf(file_path, sizeof(file_path), DATA_FOLDER"/weights-%03d.ppm", count++);

            layer_save_as_ppm(weights, file_path);
            adjusted += 1;
        }

        layer_random_circle(inputs);

        if (feed_forward(inputs, weights) < BIAS) {

            add_inputs_from_weights(inputs, weights);

            snprintf(file_path, sizeof(file_path), DATA_FOLDER"/weights-%03d.ppm", count++);

            layer_save_as_ppm(weights, file_path);
            adjusted += 1;
        }
    }
    printf("[INFO] saving %s\n", file_path);
    return adjusted;
}



int check_pass(Layer inputs, Layer weights)
{
    int adjusted = 0;

    for (int i = 0; i < SAMPLE_SIZE; ++i) {
        layer_random_rect(inputs);
        
        if (feed_forward(inputs, weights) > BIAS) {
            adjusted += 1;
        }

        layer_random_circle(inputs);
        if (feed_forward(inputs, weights) < BIAS) {
            adjusted += 1;
        }
    }
    return adjusted;
}



int main(void)
{   
    Create_Directory();
    srand(CHECK_SEED);

    int adjusted = check_pass(inputs, weights);
    printf("\n\n[INFO] fail rate of untrained model is %f\n\n\n", adjusted / (SAMPLE_SIZE * 2.0));

    for (int i = 0; i < TRAIN_PASSES; ++i) {
        srand(TRAIN_SEED);
        int adjusted = train_pass(inputs, weights);
        if (adjusted <= 0){printf("[INFO] Passed %d:: adjusted %d times\n", i, adjusted); break;}
    }

    srand(CHECK_SEED);
    adjusted = check_pass(inputs, weights);

    printf("\n\n[INFO] fail rate of trained model is %f\n", adjusted / (SAMPLE_SIZE * 2.0));

    return 0;
}