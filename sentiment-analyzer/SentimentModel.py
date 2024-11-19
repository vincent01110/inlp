import tensorflow as tf

class SentimentModel:
    def __init__(self, input_shape):
        # Initialize model
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(1, activation='sigmoid', input_shape=(input_shape,))
        ])
        
        # Compile the model
        self.model.compile(optimizer='adam',
                           loss='binary_crossentropy',
                           metrics=['accuracy'])
        
    def train(self, train_data, train_labels, val_data, val_labels, epochs=5):
        """
        Trains the model with the given training data and labels.

        Args:
            train_data: Features of the training set.
            train_labels: Labels of the training set.
            val_data: Features of the validation set.
            val_labels: Labels of the validation set.
            epochs: Number of training epochs.
        """
        self.history = self.model.fit(train_data, train_labels, epochs=epochs,
                                      validation_data=(val_data, val_labels))
    
    def evaluate(self, test_data, test_labels):
        """
        Evaluates the model with the given test data and labels.

        Args:
            test_data: Features of the test set.
            test_labels: Labels of the test set.
        
        Returns:
            Test loss and accuracy.
        """
        return self.model.evaluate(test_data, test_labels)
    
    def predict(self, new_data):
        """
        Predicts the output for new data.

        Args:
            new_data: New data samples for prediction.
        
        Returns:
            Predictions as probabilities.
        """
        return self.model.predict(new_data)
