
def generate_guassian_normal_curve():
    
    import numpy as np
    from scipy.stats import norm

    mu = 998.8
    sigma = 73.10
    x1 = 900
    x2 = 1100

    # calculate the z-transform
    z1 = ( x1 - mu ) / sigma
    z2 = ( x2 - mu ) / sigma

    x = np.arange(z1, z2, 0.001) # range of x in spec
    x_all = np.arange(-10, 10, 0.001) # entire range of x, both in and out of spec
    # mean = 0, stddev = 1, since Z-transform was calculated
    y = norm.pdf(x,0,1)
    y2 = norm.pdf(x_all,0,1)

    fig, ax = plt.subplots(figsize=(9,6))
    plt.style.use('fivethirtyeight')
    print(x_all)
    print(y2)
    ax.plot(x_all,y2)
    ax.fill_between(x,y,0, alpha=0.3, color='b')
    ax.fill_between(x_all,y2,0, alpha=0.1)
    #ax.set_xlim([-4,4])
    ax.set_xlabel('# of Standard Deviations Outside the Mean')
    #ax.set_yticklabels([])
    ax.set_title('Normal Gaussian Curve')
    plt.savefig('normal_curve.png', dpi=72, bbox_inches='tight')
    plt.show()


def generate_guassian_fit_curve_for_data(dataFrame, componentName):
    import matplotlib.pyplot as plt
    from numpy import exp, loadtxt, pi, sqrt, arange
    from lmfit import Model
    #data = loadtxt('model1d_gauss.dat')
    x = arange(start=0, stop=len(dataFrame[componentName]), step=1) #dataFrame['Date_Time'].values #data[:, 0]
    print(x)
    y = dataFrame[componentName].values #data[:, 1]
    gmodel = Model(gaussian)
    result = gmodel.fit(y, x=x, amp=5, cen=5, wid=1)
    print(result.fit_report())
    
    plt.plot(x, y, 'bo')
    #plt.plot(x, result.init_fit, 'k--', label='initial fit')
    plt.plot(x, result.best_fit, 'r-', label='best fit')
    plt.legend(loc='best')
    plt.show()

def gaussian(x, amp, cen, wid):
    from numpy import exp, pi, sqrt
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (sqrt(2*pi) * wid)) * exp(-(x-cen)**2 / (2*wid**2))
