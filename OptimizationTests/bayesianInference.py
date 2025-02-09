import numpy as np
import pymc as pm
import matplotlib.pyplot as plt

# Observed data: 10 coin flips, 7 heads, 3 tails
data = np.array([1, 0, 1, 1, 1, 0, 1, 1, 0, 1])
n_flips = len(data)
n_heads = np.sum(data)

# Define the model
with pm.Model() as model:
    # Prior for the probability of heads (theta)
    theta = pm.Beta("theta", alpha=1, beta=1)  # Uniform prior

    # Likelihood of the observed data given theta
    likelihood = pm.Bernoulli("likelihood", p=theta, observed=data)

    # Perform MCMC sampling
    trace = pm.sample(2000, tune=1000)

# Analyze the results
pm.plot_posterior(trace)
plt.show()

# Print summary statistics
pm.summary(trace)