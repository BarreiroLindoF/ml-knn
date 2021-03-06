import numpy as np


def compute_euclidean_dist_two_loops(x_train, x_test):
    """
    Compute the distance between each test point in x_test and each training point
    in x_train using a nested loop over both the training data and the 
    test data.

    Inputs:
    - x_train: A numpy array of shape (num_train, D) containing test data.
    - x_test: A numpy array of shape (num_test, D) containing test data.

    Returns:
    - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
      is the Euclidean distance between the ith test point and the jth training
      point.
    """
    num_test = x_test.shape[0]
    num_train = x_train.shape[0]
    dists = np.zeros((num_test, num_train))
    for i in range(num_test):
      for j in range(num_train):
        #####################################################################
        # TODO:                                                             #
        # Compute the l2 distance between the ith test point and the jth    #
        # training point, and store the result in dists[i, j]. You should   #
        # not use a loop over dimension.                                    #
        #####################################################################
        # Your code here
        dists[i][j] = np.linalg.norm(x_test[i] - x_train[j])
        #####################################################################
        #                       END OF YOUR CODE                            #
        #####################################################################
    return dists

def compute_euclidean_dist_one_loop(x_train, x_test):
    """
    Compute the distance between each test point in x_test and each training point
    in x_train using a single loop over the test data.

    Input / Output: Same as compute_euclidean_dist_two_loops
    """
    num_test = x_test.shape[0]
    num_train = x_train.shape[0]
    dists = np.zeros((num_test, num_train))
    for i in range(num_test):
		#######################################################################
		# TODO:                                                               #
		# Compute the l2 distance between the ith test point and all training #
		# points, and store the result in dists[i, :].                        #
		#######################################################################
        # Your code here
        a = np.subtract(x_test[i], x_train)
        dists[i,:] = np.linalg.norm(a, axis=1)
		#######################################################################
		#                         END OF YOUR CODE                            #
		#######################################################################
    return dists

def compute_euclidean_dist_no_loops(x_train, x_test):
    """
    Compute the distance between each test point in x_test and each training point
    in x_train using no explicit loops.

    Input / Output: Same as compute_euclidean_dist_two_loops
    """
    num_test = x_test.shape[0]
    num_train = x_train.shape[0]
    dists = np.zeros((num_test, num_train)) 
    #########################################################################
    # TODO:                                                                 #
    # Compute the l2 distance between all test points and all training      #
    # points without using any explicit loops, and store the result in      #
    # dists.                                                                #
    #                                                                       #
    # You should implement this function using only basic array operations; #
    # in particular you should not use functions from scipy.                #
    #                                                                       #
    # HINT: Try to formulate the l2 distance using matrix multiplication    #
    #       and two broadcast sums.                                         #
    #########################################################################
    # Your code here
    test_sum = np.sum(np.square(x_test), axis=1)
    train_sum = np.sum(np.square(x_train), axis=1)

    inner_product = np.dot(x_test, x_train.T)
    dists = np.sqrt(-2 * inner_product + test_sum.reshape(-1, 1) + train_sum)
    #########################################################################
    #                         END OF YOUR CODE                              #
    #########################################################################
    return dists

def compute_mahalanobis_dist(x_train, x_test, sigma):
    """
    Compute the Mahalanobis distance between each test point in x_test and each training point
    in x_train (please feel free to choose the implementation).

    Inputs:
    - x_train: A numpy array of shape (num_train, D) containing test data.
    - x_test: A numpy array of shape (num_test, D) containing test data.
    - sigma: A numpy array of shape (D,D) containing a covariance matrix.

    Returns:
    - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
      is the Mahalanobis distance between the ith test point and the jth training
      point.
    """
    num_test = x_test.shape[0]
    num_train = x_train.shape[0]
    dists = np.zeros((num_test, num_train)) 
    #########################################################################
    # TODO:                                                                 #
    # Compute the Mahalanobis distance between all test points and all      #
    # training points (please feel free to choose the implementation), and  #
    # store the result in dists.                                            #
    #                                                                       #
    #########################################################################
    # Your code here
    for i in range(num_test):
      for j in range(num_train):
          dists[i][j] = np.sqrt((x_train[j] - x_test[i]).T.dot(np.linalg.inv(sigma)).dot(x_train[j] - x_test[i]))
    #########################################################################
    #                         END OF YOUR CODE                              #
    #########################################################################
    return dists

def get_sigma(X, method):
    """
    Define a covariance  matrix using 3 difference approaches: 
    """
    d = X.shape[1]
    
    # cov is the covariance matrix
    cov = np.cov(X.T)

    sigma = None
    if method == 'identity':
        sigma = np.identity(d)
    elif method == 'diag_average_cov':
        #########################################################################
        # TODO:                                                                 #
        # Compute sigma as a diagonal matrix that has at its diagonal the       #
        # average variance of the different features,                           #
        #  i.e. all diagonal entries sigma_ii will be the same                  #
        #                                                                       #
        # Recall : the variance is the diagonal from the covariance matrix      #
        #########################################################################
        # Your code here
        average_variance = np.mean(np.var(X, axis=0))
        sigma = np.diag(np.repeat(average_variance, d))
        #########################################################################
        #                         END OF YOUR CODE                              #
        #########################################################################
    elif method == 'diag_cov':
        #########################################################################
        # TODO:                                                                 #
        # Compute sigma as a diagonal matrix that has at its diagonal           #
        # the variance of each feature                                          #
        #                                                                       #
        #########################################################################
        # Your code here
        variances = np.var(X, axis=0)
        sigma = np.diag(variances)
        #########################################################################
        #                         END OF YOUR CODE                              #
        #########################################################################
    elif method == 'full_cov':
        #########################################################################
        # TODO:                                                                 #
        # Computre Σ as the full covariance matrix between all pairs of features#
        #                                                                       #
        #########################################################################
        # Your code here
        sigma = np.cov(X, rowvar=False)
        #########################################################################
        #                         END OF YOUR CODE                              #
        #########################################################################
    else:
        raise ValueError("Invalid value {} for method".format(method))
    return sigma