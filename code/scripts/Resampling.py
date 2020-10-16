import numpy as np
import pdb
import random

class Resampling:

    """
    References: Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. Probabilistic robotics. MIT press, 2005.
    [Chapter 4.3]
    """

    def __init__(self):
        """
        TODO : Initialize resampling process parameters here
        """

    # def multinomial_sampler(self, X_bar):

    #     """
    #     param[in] X_bar : [num_particles x 4] sized array containing [x, y, theta, wt] values for all particles
    #     param[out] X_bar_resampled : [num_particles x 4] sized array containing [x, y, theta, wt] values for resampled set of particles
    #     """

    #     """
    #     TODO : Add your code here
    #     """

    #     return X_bar_resampled

    def low_variance_sampler(self, X_bar):

        """
        param[in] X_bar : [num_particles x 4] sized array containing [x, y, theta, wt] values for all particles
        param[out] X_bar_resampled : [num_particles x 4] sized array containing [x, y, theta, wt] values for resampled set of particles
        """

        """
        TODO : Add your code here
        References: Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. Probabilistic robotics. MIT press, 2005.
        [p. 110]
        """

        X_bar_resampled = []
        M = len(X_bar)
        r = np.random.uniform() * (M ** -1)
        w = np.array(X_bar[:, 3])
        # print(w)
        w = w / np.sum(w)
        # print(w)
        c = w[0]
        i = 0
        for m in range(M):
            U = r + (m) * (M ** -1)
            while U > c:
                i = i + 1
                # all the weights are 0
                c = c + w[i]
            X_bar_resampled.append(X_bar[i])
        
        return X_bar_resampled

    def normalize(self, v):
        norm = np.linalg.norm(v)
        if norm == 0: 
            return v
        return v / norm

if __name__ == "__main__":
    pass