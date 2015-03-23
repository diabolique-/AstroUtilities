# note: modules are imported in each function to reduce overhead when using these utilities. This way, only the modules
# that are needed for the functions you use will be imported, rather than the modules needed for all utilities.

def reduced_chi_sq(model, data, errors):
    # TODO: copy comments from masses function.
    if not len(model) == len(data) == len(errors):
        raise ValueError("Data, model, and errors all need to have the same length.")
    chi_sq = 0
    for i in range(len(model)):
        chi_sq += ((model[i] - data[i])/errors[i])**2
    return chi_sq/(len(data))

def mag_to_flux(mag, zeropoint):
    """Convert a magnitude into a flux.

    m = -2.5 log(F) + C  -> definition of magnitude scale
    2.5 log(F) = C - m
    F = 10^((C-m)/2.5)

    :param mag: magnitdue to be converted into a flux.
    :param zeropoint: zeropoint (in mags) of the magnitude system being used
    :return: flux that corresponds to the given magnitude
    """
    return 10**((zeropoint - mag)/2.5)


def flux_to_mag(flux, zeropoint):
    """Convert flux to magnitude with the given zeropoint.

    :param flux: flux in whatever units. Choose your zeropoint correctly to make this work with the units flux is in.
    :param zeropoint: zeropoint of the system (in mags)
    :return: magnitude that corresponds to the given flux
    """
    import math
    return -2.5 * math.log10(flux) + zeropoint

# NOTE: these flux<->mag functions need to be tested. 