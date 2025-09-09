import pycuda.autoinit
import pycuda.driver as drv
import numpy as np
from pycuda.compiler import SourceModule

mod = SourceModule("""
#define TILE_WIDTH 32

__device__ unsigned int xorshift32(unsigned int& state) {
    state ^= state << 13;
    state ^= state >> 17;
    state ^= state << 5;
    return state;
}

__global__ void initialize_weights(float* W, int rows, int cols, float scale, unsigned int seed) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int size = rows * cols;
    if (idx < size) {
        unsigned int state = seed + idx;
        float rand_uniform = (xorshift32(state) % 10000) / 10000.0f; // [0,1)
        W[idx] = (rand_uniform * 2.0f - 1.0f) * scale; // [-scale, scale]
    }
}

__global__ void matmul(float* A, float* B, int row_A, int col_AB, int row_B) {
    __shared__ float tile_a[TILE_WIDTH][TILE_WIDTH];
    __shared__ float tile_b[TILE_WIDTH][TILE_WIDTH];

    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if(row < row_B && col < col_AB) {
        for(int i = 0; i < TILE_WIDTH; i++) {
            if((row + i * TILE_WIDTH) * col_A) tile_a[][col] = A[]
        }
    }
}
""")

initialize_weights = mod.get_function("initialize_weights")