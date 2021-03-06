import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

# Residual sum of squares
def compute_error(m, b, x_values, y_values):
    total = 0
    for i in range(0, len(x_values)):
        prediction = m * x_values[i] + b
        total += (prediction - y_values[i]) ** 2
    return total / len(x_values)

# Squared Error
def squared_error(y_values, line):
    return sum((line - y_values) ** 2)

# Coefficient of determination
def cod(y_values, m, b, x):
    line = np.array(x)
    line = line * m + b
    y_mean = np.array([mean(y_values) for y in y_values])
    ser = squared_error(y_values, line)
    sem = squared_error(y_values, y_mean)
    return 1 - (ser / sem)
        
# Find the regression line using gradient descent
def gradient_descent(x_values, y_values, current_m, current_b, learning_rate):
    m_grad = 0
    b_grad = 0
    for i in range(0, len(x_values)):
        x = x_values[i]
        y = y_values[i]
        m_grad += -(2 / len(x_values)) * x * (y - ((current_m * x) + current_b))
        b_grad += -(2 / len(x_values)) * (y - ((current_m * x) + current_b))
    current_m = current_m - (learning_rate * m_grad)
    current_b = current_b - (learning_rate * b_grad)
    return current_m, current_b

def main():
    # Load different sets (I, II, III, IV)
    dataset = pd.read_csv("anscombes.csv", index_col=0)
    data = dataset[dataset['dataset'] == 'I']
    x = data.x.tolist()
    y = data.y.tolist()

    # Initialize line (y = m*x + b)
    m = 0                   # Line's slope
    b = 0                   # Line's y-intercept
    learning_rate = 0.001   # Learning rate
    iterations = 100        # Number of iterations

    x_range = np.array([np.min(x) - 2, np.max(x) + 2])
    fig = plt.figure('Linear Regression using Gradient Descent')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title("Anscombe's Quartet Set I")
    #plt.clf()
    ax.set_xlim(np.min(x) - 2, np.max(x) + 2)
    ax.set_ylim(np.min(y) - 2, np.max(y) + 2)
    ax.scatter(x, y)

    for _ in range(iterations):
        m, b = gradient_descent(x, y, m, b, learning_rate)
        line = m * x_range + b
        ax.plot(x_range, line, linewidth=1, color='r')
        plt.pause(0.01)

    print("Residual sum of squares: " + str(round(compute_error(m, b, x, y), 5)))
    print("Coefficient of determination: " + str(round(cod(y, m, b, x), 5)))
    plt.show()

if __name__ == "__main__":
    main()