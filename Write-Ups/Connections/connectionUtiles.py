import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import minimize


def gaussian(x, mean=0., stdev=1., pmax=1.):
    """Gaussian function. Default is the PDF of standard normal distribution
    Note mean parameter sets min distance a connection can be made
    """
    x = (x - mean) / stdev
    return pmax * np.exp(- x * x / 2)


def pmf(K, P):
    """probability mass function"""
    return np.array([p if k else 1 - p for k, p in zip(K, P)])


def nll(p):
    "negative log-likelihood"
    return -np.sum(np.log(p))


def fit_data(data_config):
    data = []
    for d in data_config:
        dat = np.zeros((d[2], 2))
        dat[:, 0] = d[0]
        dat[:d[1], 1] = 1.
        data.append(dat)
    data = np.vstack(data)

    def negloglikelihood(params):
        return nll(pmf(data[:, 1], gaussian(
            data[:, 0], pmax=params[0], stdev=params[1], mean=0.)))

    initParams = [.5, 50.]
    results = minimize(negloglikelihood, initParams, method='Nelder-Mead')
    params = results.x

    #print("Pmax:",params[0])
    #print("stdev:",params[1])

    hist = np.array([(d[0], d[1] / d[2]) for d in data_config])
    x = np.linspace(0,300,100)
    plt.bar(hist[:, 0], hist[:, 1], width=50.,label='Bio data')
    plt.plot(x, gaussian(x, pmax=params[0], stdev=params[1]), 'r',label=f'Fit: $P_{{max}}={params[0]:.2f}$, $\sigma={params[1]:.2f}$')
    plt.title("Fitted Gaussian from data")
    plt.xlabel("Distance")
    plt.ylabel("probability")
    plt.legend()
    plt.show()
    return params


def histoFit(hist_data):
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from scipy.stats import norm

    # Given histogram data 
    # [binStart,binEnd,ProbInBin]

    # Extract start, end, and probabilities
    start = hist_data[:, 0]
    end = hist_data[:, 1]
    frequencies = hist_data[:, 2]

    # Calculate bin centers
    bin_centers = (start + end) / 2

    # Define a Gaussian function
    def gaussian(x, sigma, A):
        return A * np.exp(-0.5 * (x / sigma) ** 2)

    # Initial guess for the parameters: standard deviation, amplitude
    initial_guess = [np.std(bin_centers), max(frequencies)]

    # Set bounds for the fitting parameters: mu=0, sigma>0, A>0, we force mu to be 0 
    bounds = ([0, 0], [np.inf, np.inf])

    # Perform the curve fit with bounds
    popt, pcov = curve_fit(gaussian, bin_centers, frequencies, p0=initial_guess, bounds=bounds, maxfev=2000)

    # Extract the parameters
    sigma, A = popt

    # Calculate Pmax
    Pmax = A

    residuals = frequencies - gaussian(bin_centers, sigma, A)
    RSS = np.sum(residuals ** 2)
    TSS = np.sum((frequencies - np.mean(frequencies)) ** 2)
    R_squared = 1 - (RSS / TSS)


    # Print the fitted parameters and R-squared
    print(f"Pmax (max probability): {Pmax}")
    print(f"Standard deviation: {sigma}")
    print(f"R-squared: {R_squared}")

    # Plot the histogram
    plt.bar(bin_centers, frequencies, width=(end - start), alpha=0.6, color='g', edgecolor='black')

    # Plot the fitted Gaussian
    x = np.linspace(min(start), max(end), 100)
    plt.plot(x, gaussian(x, sigma, A), 'k', linewidth=2, label=f'Fit: $P_{{max}}={Pmax:.2f}$, $\sigma={sigma:.2f}$')
    plt.xlabel('Data values')
    plt.ylabel('Probability')
    plt.title('Histogram and Fitted Gaussian')
    plt.legend()

    # Show the plot
    plt.show()

def networkTest(num_cells,width,height,Pmax,sigma,plot=False):
    import numpy as np
    import matplotlib.pyplot as plt

    # Parameters
    cylinder_width = width  # mm
    cylinder_height = height  # mm
    central_cell = (cylinder_width / 2, cylinder_height / 2)


    # Step 1: Place cells randomly within the cylinder
    cell_positions = np.random.rand(num_cells, 2)
    cell_positions[:, 0] *= cylinder_width
    cell_positions[:, 1] *= cylinder_height

    # Step 2: Define the Gaussian probability function
    def connection_probability(distance, Pmax, sigma):
        return Pmax * np.exp(-distance**2 / (2 * sigma**2))

    # Step 3: Connect cells to the central cell based on distance
    distances = np.linalg.norm(cell_positions - central_cell, axis=1)
    probabilities = connection_probability(distances, Pmax, sigma)
    connections = np.random.rand(num_cells) < probabilities

    # Step 4: Calculate the number of connections and the percent connectivity
    num_connections = np.sum(connections)
    percent_connectivity = (num_connections / num_cells) * 100

    # Output results
    print(f"Number of connections: {num_connections}")
    print(f"Percent connectivity: {percent_connectivity:.2f}%")

    # Visualization
    if plot:
        plt.figure(figsize=(10, 5))
        plt.scatter(cell_positions[:, 0], cell_positions[:, 1], c='blue', label='Cells')
        plt.scatter(*central_cell, c='red', label='Central Cell')
        for i, connected in enumerate(connections):
            if connected:
                plt.plot([central_cell[0], cell_positions[i, 0]], [central_cell[1], cell_positions[i, 1]], 'g-', alpha=0.3)
        plt.xlim(0, cylinder_width)
        plt.ylim(0, cylinder_height)
        plt.xlabel('Width (mm)')
        plt.ylabel('Height (mm)')
        plt.title('Cell Connections to Central Cell')
        plt.legend()
        plt.show()
