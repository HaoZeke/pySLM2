import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from scipy.constants import micro, nano, milli
import numpy as np
import time

import pySLM2
import tensorflow as tf


def task(method):
    lcos_slm = pySLM2.PLUTO_2(
    369 * nano,  # wavelength
    200 * milli, # effective focal length
  )

    # The beam illumilating the DMD is an gaussian beam with a waist of 5 mm
    input_profile = pySLM2.HermiteGaussian(0,0,1,5*milli)

    # targeted profile at the image plane
    output_profile = pySLM2.HermiteGaussian(0,0,1,30*micro, n=1, m=1)

    start = time.time()
    lcos_slm.calculate_hologram(
        input_profile,
        output_profile,
        method=method,
        N=200,
    )
    end = time.time()
    total_time = end-start
    return total_time



num_gpu  = len(tf.config.list_physical_devices('GPU'))
print("Num GPUs Available: ", num_gpu)
if num_gpu ==0:
    print("No GPU found. Exit.")
    exit()
else:
    print("Is Built with CUDA: ", tf.test.is_built_with_cuda())

num_test = 10
result = []
print(f'Total {num_test} Tests Running on GPU')
for i in range(num_test):
    ti = task('gs')
    print(f'test {i} runtime: {ti:0.02f}s')
    result.append(ti)
print(f'runtime for {num_test} runs: {np.mean(result):0.2f}s +- {np.std(result):0.2f}s')



