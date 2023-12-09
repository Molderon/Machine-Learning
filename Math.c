#include "config.h"


static inline int clampi(int x, int low, int high)
{
    if (x < low)  x = low;
    if (x > high) x = high;
    return x;
}



void layer_fill_rect(Layer layer, int x, int y, int w, int h, float value)
{
    assert(w > 0);
    assert(h > 0);
    int x0 = clampi(x, 0, WIDTH-1);
    int y0 = clampi(y, 0, HEIGHT-1);
    int x1 = clampi(x0 + w - 1, 0, WIDTH-1);
    int y1 = clampi(y0 + h - 1, 0, HEIGHT-1);

    for (int y = y0; y <= y1; ++y) {
        for (int x = x0; x <= x1; ++x) {
            layer[y][x] = value;
        }
    }
}



void layer_fill_circle(Layer layer, int cx, int cy, int radious, float value)
{
    assert(radious > 0);
    int x0 = clampi(cx - radious, 0, WIDTH-1);
    int y0 = clampi(cy - radious, 0, HEIGHT-1);
    int x1 = clampi(cx + radious, 0, WIDTH-1);
    int y1 = clampi(cy + radious, 0, HEIGHT-1);

    for (int y = y0; y <= y1; ++y) {
        for (int x = x0; x <= x1; ++x) {
            int dx = x - cx;
            int dy = y - cy;
            if (dx*dx + dy*dy <= radious*radious) {
                layer[y][x] = value;
            }
        }
    }
}



void add_inputs_from_weights(Layer inputs, Layer weights)
{
    for (int y = 0; y < HEIGHT; ++y) {
        for (int x = 0; x < WIDTH; ++x) {
            weights[y][x] += inputs[y][x];
        }
    }
}



void sub_inputs_from_weights(Layer inputs, Layer weights)
{
    for (int y = 0; y < HEIGHT; ++y) {
        for (int x = 0; x < WIDTH; ++x) {
            weights[y][x] -= inputs[y][x];
        }
    }
}




int rand_range(int low, int high)
{
    assert(low < high);
    return rand() % (high - low) + low;
}



void layer_random_rect(Layer layer)
{
    layer_fill_rect(layer, 0, 0, WIDTH, HEIGHT, 0.0f);
    int x = rand_range(0, WIDTH);
    int y = rand_range(0, HEIGHT);

    int w = WIDTH - x;
    if (w < 2) w = 2;
    w = rand_range(1, w);

    int h = HEIGHT - x;
    if (h < 2) h = 2;
    h = rand_range(1, h);

    layer_fill_rect(layer, x, y, w, h, 1.0f);
}



void layer_random_circle(Layer layer)
{
    layer_fill_rect(layer, 0, 0, WIDTH, HEIGHT, 0.0f);

    int cx = rand_range(0, WIDTH);
    int cy = rand_range(0, HEIGHT);
    int r = INT_MAX;
    
    if (r > cx) r = cx;
    if (r > cy) r = cy;
    if (r > WIDTH - cx) r = WIDTH - cx;
    if (r > HEIGHT - cy) r = HEIGHT - cy;
    if (r < 2) r = 2;

    r = rand_range(1, r);

    layer_fill_circle(layer, cx, cy, r, 1.0f);
}