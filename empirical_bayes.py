import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np

class Counting():
    ''' empirical bayes method to reduce noise (http://varianceexplained.org/r/empirical-bayes-book/)'''
    def __init__(self, alpha=None, beta=None):
        self.alpha = alpha
        self.beta = beta

    def fit_beta_prior(self, probability):
        if(probability.any()>1 or probability.any()==0): 
            raise ValueError('prior probability should be fit to (0,1) to avoid artifacts')
        self.alpha,self.beta,_,_ = stats.beta.fit(probability,floc=0,fscale=1)
        return self.alpha, self.beta
    
    def posterior(self, n_successes=0, n_trials=0, p=0.5):
        # posterior in this case is just updated with the (+successes,ntrials-successes)
        if not self.alpha or not self.beta:
            raise ValueError('first set or fit alpha and beta values for bayesian counting')
        
        alpha_post = self.alpha + n_successes
        beta_post = self.beta + n_trials - n_successes
        # in practice, p=0.5 and stats.beta.mean(alpha_post, beta_post) are within ~1%
        val_at_p = stats.beta.ppf(p, alpha_post, beta_post)
        return  val_at_p

    def plot(self, probability=None):
        fig, ax = plt.subplots(1, 1)
        nbins = 1000
        low_percent_edge = 0.01
        high_percent_edge = 0.99
        x = np.linspace(
                stats.beta.ppf(low_percent_edge, self.alpha, self.beta),
                stats.beta.ppf(high_percent_edge, self.alpha, self.beta),
                nbins)
        ax.plot(x, stats.beta.pdf(x, self.alpha,self.beta),
                'r-', lw=5, alpha=0.6, label='beta pdf')
        if probability is not None: 
            probability.hist(ax=ax,normed=1, bins=100)
