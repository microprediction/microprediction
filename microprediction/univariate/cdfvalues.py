from microconventions.stats_conventions import is_discrete, evenly_spaced_percentiles, cdf_values, is_process, nudged, discrete_cdf, sign_changes, quantize

if __name__=='__main__':
    x = [-3.,0.,0.,0.,0.,0.,1.]
    y = nudged(x)
