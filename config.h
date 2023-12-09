#ifndef CONFIG_H_

#define CONFIG_H_
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <errno.h>
#include <math.h>
#include <limits.h>
#include <float.h>

#include <sys/stat.h>
#include <sys/types.h>

#define WIDTH 20
#define HEIGHT 20
#define BIAS 20.0
#define SAMPLE_SIZE 75
#define TRAIN_PASSES 1000

#define PPM_SCALER 25
#define PPM_COLOR_INTENSITY 255
#define PPM_RANGE 10.0

#define DATA_FOLDER "data"

#define TRAIN_SEED 69 // nice
#define CHECK_SEED 66

typedef float Layer[HEIGHT][WIDTH];

static Layer inputs;
static Layer weights;


static inline int clampi(int x, int low, int high);
void layer_fill_rect(Layer layer, int x, int y, int w, int h, float value);
void layer_fill_circle(Layer layer, int cx, int cy, int r, float value);
void layer_save_as_ppm(Layer layer, const char *file_path);
void layer_save_as_bin(Layer layer, const char *file_path);
void add_inputs_from_weights(Layer inputs, Layer weights);
void sub_inputs_from_weights(Layer inputs, Layer weights);
int rand_range(int low, int high);
void layer_random_rect(Layer layer);
void layer_random_circle(Layer layer);
void Create_Directory();


#endif 