import numpy as np

class KNNClassifier:
    def __init__(self, k=3):
        """
        Initialize the KNN classifier with the number of neighbors 'k'.

        Parameters:
        - k: Number of nearest neighbors to consider (default is 3).
        """
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X_train, y_train):
        """
        Fit the classifier with the training data.

        Parameters:
        - X_train: NumPy array of training data points with shape (n_samples, n_features)
        - y_train: NumPy array of corresponding labels with shape (n_samples,)
        """
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test):
        """
        Predict the labels for the test data.

        Parameters:
        - X_test: NumPy array of test data points, can be a single point with shape (n_features,)
                  or multiple points with shape (n_samples, n_features)

        Returns:
        - Predicted label(s): A single label or a NumPy array of labels
        """
        if X_test.ndim == 1:
            # Single sample
            return self._predict_single(X_test)
        else:
            # Multiple samples
            return np.array([self._predict_single(x) for x in X_test])

    def _predict_single(self, x):
        """
        Predict the label for a single data point.

        Parameters:
        - x: NumPy array representing a single data point with shape (n_features,)

        Returns:
        - Predicted label
        """
        # Calculate Euclidean distances between x and all training points
        distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))

        # Get the indices of the k nearest neighbors
        neighbor_indices = np.argsort(distances)[:self.k]

        # Get the labels of the k nearest neighbors
        nearest_labels = self.y_train[neighbor_indices]

        # Majority vote using NumPy's unique function
        labels, counts = np.unique(nearest_labels, return_counts=True)
        majority_label = labels[np.argmax(counts)]

        return majority_label
