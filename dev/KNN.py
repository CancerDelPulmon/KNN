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
        - X_train: List of training data points (list of tuples)
        - y_train: List of corresponding labels
        """
        # Convert the list of tuples to a NumPy array
        self.X_train = np.array(X_train)
        self.y_train = np.array(y_train)

        # Check that X_train has the correct shape
        if self.X_train.ndim != 2 or self.X_train.shape[1] != 3:
            raise ValueError("X_train must be a 2D array with shape (n_samples, 3) representing x, y, z coordinates.")

    def predict(self, X_test):
        """
        Predict the labels for the test data.

        Parameters:
        - X_test: Single test point (tuple or list) or list of test points

        Returns:
        - Predicted label(s): A single label or a NumPy array of labels
        """
        # Ensure X_test is a NumPy array
        X_test = np.array(X_test)

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
        - x: NumPy array representing a single data point with shape (3,)

        Returns:
        - Predicted label
        """
        # Ensure x is a NumPy array
        x = np.array(x)

        if x.shape[0] != 3:
            raise ValueError("Each test point must have exactly three features representing x, y, z coordinates.")

        # Calculate Euclidean distances between x and all training points using vectorized operations
        distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))

        # Get the indices of the k nearest neighbors
        neighbor_indices = np.argsort(distances)[:self.k]

        # Get the labels of the k nearest neighbors
        nearest_labels = self.y_train[neighbor_indices]

        # Majority vote
        labels, counts = np.unique(nearest_labels, return_counts=True)
        majority_label = labels[np.argmax(counts)]

        return majority_label
