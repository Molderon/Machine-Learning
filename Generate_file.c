#include"config.h"

void layer_save_as_ppm(Layer layer, const char *file_path){
    FILE *file = fopen(file_path, "wb");
    if (file == NULL) {
        fprintf(stderr, "ERROR: could not open file %s: %m\n", file_path);
        exit(1);
    }

    fprintf(file, "P6\n%d %d 255\n", WIDTH * PPM_SCALER, HEIGHT * PPM_SCALER);

    for (int y = 0; y < HEIGHT * PPM_SCALER; ++y) {
        for (int x = 0; x < WIDTH * PPM_SCALER; ++x) {
            float s = (layer[y / PPM_SCALER][x / PPM_SCALER] + PPM_RANGE) / (1.1f * PPM_RANGE); //backgound color
            char pixel[3] = {
                (char) floorf(PPM_COLOR_INTENSITY * (1.23f - s)),
                (char) floorf(PPM_COLOR_INTENSITY * (1.23f - s)),
                (char) floorf(PPM_COLOR_INTENSITY * 1.81f - s),
            };

            fwrite(pixel, sizeof(pixel), 1, file);
        }
    }

    fclose(file);
}



void layer_save_as_bin(Layer layer, const char *file_path)
{
    FILE *file = fopen(file_path, "wb");
    if (file == NULL) {
        fprintf(stderr, "ERROR: could not open file %s: %m", file_path);
        exit(1);
    }
    fwrite(layer, sizeof(Layer), 1, file);
    fclose(file);
}


void Create_Directory(){
    printf("[INFO] creating %s\n", DATA_FOLDER);
    if (mkdir(DATA_FOLDER, 0755) < 0 && errno != EEXIST) {
        fprintf(stderr, "ERROR: could not create folder %s: %s", DATA_FOLDER,
                strerror(errno));
        exit(1);
    }
}