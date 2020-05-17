import numpy as np
from distances import *

class KNearestNeighbor(object):
    """ a kNN classifier with L2 distance """

    def __init__(self):
        pass

    def train(self, X, y):
        """
        Train the classifier. For k-nearest neighbors this is just 
        memorizing the training data.

        Inputs:
        - X: A numpy array of shape (num_train, D) containing the training data
        consisting of num_train samples each of dimension D.
        - y: A numpy array of shape (N,) containing the training labels, where
            y[i] is the label for X[i].
        """
        self.X_train = X
        self.y_train = y
        
    def predict(self, X, k=1, distance='euclidean', num_loops=0, sigma_method=None):
        """
        Predict labels for test data using this classifier.

        Inputs:
        - X: A numpy array of shape (num_test, D) containing test data consisting
            of num_test samples each of dimension D.
        - k: The number of nearest neighbors that vote for the predicted labels.
        - distance: Determines with distance to use, the choices are 'euclidean' or
        'mahalanobis'.
        - num_loops: Determines which implementation to use to compute euclidean 
        distance between training points and testing points.

        Returns:
        - y: A numpy array of shape (num_test,) containing predicted labels for the
        test data, where y[i] is the predicted label for the test point X[i].  
        """
        if distance == 'euclidean':
            if num_loops == 0:
                dists = compute_euclidean_dist_no_loops(self.X_train, X)
            elif num_loops == 1:
                dists = compute_euclidean_dist_one_loop(self.X_train, X)
            elif num_loops == 2:
                dists = compute_euclidean_dist_no_loops(self.X_train, X)
            else:
                raise ValueError('Invalid value %d for num_loops' % num_loops)
        elif distance == 'mahalanobis' and sigma_method != None:
            dists = compute_mahalanobis_dist(self.X_train, X, get_sigma(self.X_train, sigma_method))
        else:
            raise ValueError('Invalid value %s for distance' % distance)

        return self.predict_labels(dists, k=k)

    def predict_labels(self, dists, k=1):
        """
        Given a matrix of distances between test points and training points,
        predict a label for each test point.

        Inputs:
        - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
        gives the distance betwen the ith test point and the jth training point.

        Returns:
        - y: A numpy array of shape (num_test,) containing predicted labels for the
        test data, where y[i] is the predicted label for the test point X[i].  
        """
        num_test = dists.shape[0]
        y_pred = np.zeros(num_test)
        for i in range(num_test):
        # A list of length k storing the labels of the k nearest neighbors to
        # the ith test point.

            closest_y = []

            #########################################################################
            # TODO:                                                                 #
            # Use the distance matrix to find the k nearest neighbors of the ith    #
            # testing point, and use self.y_train to find the labels of these       #
            # neighbors. Store these labels in closest_y.                           #
            # Hint: Look up the function numpy.argsort.                             #
            #########################################################################
            # Your code here
            sorted_array_indeces = np.argsort(dists[i])
            closest_y = np.take(self.y_train, sorted_array_indeces[:k])        
            #########################################################################
            # TODO:                                                                 #
            # Now that you have found the labels of the k nearest neighbors, you    #
            # need to find the most common label in the list closest_y of labels.   #
            # Store this label in y_pred[i]. Break ties by choosing the smaller     #
            # label.                                                                #
            #########################################################################
            # Your code here
            unique, counts = np.unique(closest_y, return_counts=True)
            y_pred[i] = unique[np.argmax(counts)]
            #########################################################################
            #                           END OF YOUR CODE                            #
            #########################################################################
        return y_pred