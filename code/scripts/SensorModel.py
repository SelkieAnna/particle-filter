import numpy as np
import math
import time
from matplotlib import pyplot as plt
from scipy.stats import norm
import pdb

from MapReader import MapReader

class SensorModel:

    """
    References: Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. Probabilistic robotics. MIT press, 2005.
    [Chapter 6.3]
    """

    def __init__(self, occupancy_map):

        """
        TODO : Initialize Sensor Model parameters here
        """
        self.map = occupancy_map
        self.grid_size = 10

        self.sigma_hit = 20
        self.lambda_short = 0.1

        self.z_hit = 0.95
        self.z_short = 0.01
        self.z_max = 0.05
        self.z_rand = 0.05

        self.max = 8000

        self.offset = 25

    def beam_range_finder_model(self, z_t1_arr, x_t1):
        """
        param[in] z_t1_arr : laser range readings [array of 180 values] at time t
        param[in] x_t1 : particle state belief [x, y, theta] at time t [world_frame]
        param[out] prob_zt1 : likelihood of a range scan zt1 at time t
        """

        """
        TODO : Add your code here
        References: Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. Probabilistic robotics. MIT press, 2005.
        [p. 158, 160]
        """

        q = 0
        for k in range(len(z_t1_arr)):

            z_tk_true = self.ray_casting(k, x_t1)
            # print(z_tk_true)

            if 0 <= z_t1_arr[k] <= self.max:
                p_hit = (np.exp(-(z_t1_arr[k] - z_tk_true) ** 2 / (2 * self.sigma_hit ** 2))) \
                         / np.sqrt(2 * np.pi * self.sigma_hit ** 2)
            else:
                p_hit = 0
            if 0 <= z_t1_arr[k] <= z_tk_true:
                p_short = (1 / (1 - np.exp(-self.lambda_short * z_tk_true))) \
                           * self.lambda_short * np.exp(-self.lambda_short * z_t1_arr[k])
            else:
                p_short = 0
            if z_t1_arr[k] == self.max:
                p_max = 1
            else:
                p_max = 0
            if 0 <= z_t1_arr[k] < self.max:
                p_rand = 1 / self.max
            else:
                p_rand = 0
            
            p = self.z_hit * p_hit + self.z_short * p_short + self.z_max * p_max + self.z_rand * p_rand
            if p > 0:
                q = q + np.log(p)

        q = q /10
        return np.exp(q)    

    def ray_casting(self, i, x_t1):
        angle = x_t1[2] + math.radians((i - 90))
        start_point = [x_t1[0] + self.offset * np.cos(x_t1[2]), \
                       x_t1[1] + self.offset * np.sin(x_t1[2])]
        start_point = [int(round(start_point[0])), int(round(start_point[1]))]
        finish_point = start_point
        while 0 < finish_point[0] < self.map.shape[1] and 0 < finish_point[1] < self.map.shape[0] \
                                    and abs(self.map[finish_point[0], finish_point[1]]) < 0.0000001: 
            finish_point[0] += 2 * np.cos(angle)
            finish_point[1] += 2 * np.sin(angle)
            finish_point = [int(round(finish_point[0])), int(round(finish_point[1]))]
            
        start_point = np.array(start_point)
        finish_point = np.array(finish_point)
        return np.linalg.norm(finish_point - start_point)
 
if __name__=='__main__':
    pass