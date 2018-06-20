
import autograd
import autograd.numpy as np

import matplotlib.pyplot as plt


def my_tanh(x):
    y = np.exp(-2.0 * x)
    return (1.0-y) / (1.0+y)


my_grad_tanh = autograd.grad(my_tanh)


if __name__ == '__main__':
    print(my_grad_tanh(1.0))

    x = np.linspace(-7, 7, 200)
    plt.plot(x, my_tanh(x),
             x, autograd.elementwise_grad(my_tanh)(x),
             x, autograd.elementwise_grad(autograd.elementwise_grad(my_tanh))(x))
    plt.show()
