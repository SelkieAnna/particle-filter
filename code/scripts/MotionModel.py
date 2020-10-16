import sys
import numpy as np
import math

class MotionModel:

    """
    References: Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. Probabilistic robotics. MIT press, 2005.
    [Chapter 5]
    """

    def __init__(self):

        """
        TODO : Initialize Motion Model parameters here
        """

        # noise initialization
        self.alpha_1 = 0.0001
        self.alpha_2 = 0.0001
        self.alpha_3 = 0.1
        self.alpha_4 = 0.1


    def update(self, u_t0, u_t1, x_t0):
        """
        param[in] u_t0 : particle state odometry reading [x, y, theta] at time (t-1) [odometry_frame]   
        param[in] u_t1 : particle state odometry reading [x, y, theta] at time t [odometry_frame]
        param[in] x_t0 : particle state belief [x, y, theta] at time (t-1) [world_frame]
        param[out] x_t1 : particle state belief [x, y, theta] at time t [world_frame]
        """

        """
        TODO : Add your code here
        References: Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. Probabilistic robotics. MIT press, 2005.
        [p. 136]
        """

        delta_rot1 = np.arctan2(u_t1[1]-u_t0[1], u_t1[0]-u_t0[0]) - u_t0[2]
        delta_trans = np.sqrt((u_t1[1]-u_t0[1]) ** 2 + (u_t1[0]-u_t0[0]) ** 2)
        delta_rot2 = u_t1[2] - u_t0[2] - delta_rot1

        delta_rot1_hat = delta_rot1 - np.random.normal(0, self.alpha_1 * delta_rot1 ** 2 + self.alpha_2 * delta_trans ** 2)
        delta_trans_hat = delta_trans - np.random.normal(0, self.alpha_3 * delta_trans ** 2 + 
                                                            self.alpha_4 * delta_rot1 ** 2 +
                                                            self.alpha_4 * delta_rot2 ** 2)
        delta_rot2_hat = delta_rot2 - np.random.normal(0, self.alpha_1 * delta_rot2 ** 2 + self.alpha_2 * delta_trans ** 2)

        x = x_t0[0] + delta_trans_hat * np.cos(x_t0[2] + delta_rot1_hat)
        y = x_t0[1] + delta_trans_hat * np.sin(x_t0[2] + delta_rot1_hat)
        theta = x_t0[2] + delta_rot1_hat + delta_rot2_hat

        x_t1 = [x, y, theta]

        return x_t1

if __name__=="__main__":
    pass