import numpy as np

def predict_next_elements(input_list, num_elements_to_predict):
    # Convert the input list to a numpy array
    x = np.array(range(1, len(input_list) + 1))

    # Fit a linear regression model
    coefficients = np.polyfit(x, input_list, 1)

    # Predict the next elements in the sequence
    next_indices = np.array(range(len(input_list) + 1, len(input_list) + 1 + num_elements_to_predict))
    next_elements = np.polyval(coefficients, next_indices)

    return next_elements

# Example of usage
input_list = [368.0, 238.0, 242.0, 236.0, 232.0, 249.0, 232.0, 237.0, 237.0, 232.0, 240.0, 232.0, 238.0, 235.0, 232.0, 239.0, 233.0, 235.0, 239.0, 231.0, 240.0, 232.0, 236.0, 237.0, 232.0, 240.0, 232.0, 238.0, 237.0, 231.0, 239.0, 236.0, 231.0, 239.0, 233.0, 234.0, 239.0, 231.0, 237.0, 237.0, 231.0, 245.0]

predicted_elements = predict_next_elements(input_list, 60000)

print(f"Input List: {input_list}")
print(f"Predicted Next Elements: {predicted_elements}")
