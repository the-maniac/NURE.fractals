import numpy as np
import matplotlib.pyplot as plt


def motion(steps, sigma, hurst):
    X_t = []
    step_X = []
    g = pow(0.5, hurst)
    x0 = 0
    x1 = sigma*g
    X_t.extend([x0, x1])
    for step in range(1, steps+1):
        # replace 2 to 1 if need recalculate each point
        k_lst = list(range(1, pow(2, step), 2))
        sigma = np.std(X_t)
        new_points = []
        idx = 0
        for k in k_lst:
            # its alternative solution to skip steps
            # don't do anything for already calculated points
            # if k % 2 == 0:
            #     continue
            new_points.append(X_t[idx])
            new_points.append(((1/2)*(X_t[idx] + X_t[idx+1]))+((1/(pow(2, (step + 1)/2)))*sigma*g))
            # print(f'{k}/{pow(2, step)}')
            # print(new_points)
            idx += 1
        # applying last point
        new_points.append(X_t[idx])
        X_t = new_points
        step_X.append(X_t + [])
        # print(len(X_t))
    return X_t, step_X



if __name__ == '__main__':
    # 2^9 = 512 points + 1
    steps = 9
    X_t, step_X = motion(steps, 1, 0.5)

    # Plot
    f, ax = plt.subplots()
    # ax.plot(np.arange(0, 1, 1 / len(X_t)), X_t, color="deepskyblue")
    ax.plot(np.arange(0, 1, 1 / len(X_t)), X_t)
    # for x in step_X:
    #     ax.plot(np.arange(0, 1, 1 / len(x)), x)
    ax.grid(True)
    plt.show()