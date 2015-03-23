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

    m = -2.5 log10(F) + C  -> definition of magnitude scale
    2.5 log10(F) = C - m
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
    return -2.5 * math.log10(flux) + zeropoint  # This is just the definition of magnitude


def mag_errors_to_percent_flux_errors(mag_error):
    """Converts a magnitude error into a percent flux error.

    m = -2.5 log10(F) + C
    dm = -2.5/(ln(10)) dF/F
    dF/F = dm * ln(10)/2.5

    The minus sign just tells us that increasing flux gives decreasing magnitudes, so we can safely ignore it.

    note: ln(10) = 2.30258509299
    I just plug in the numerical number to avoid importing things to take natural logs.

    :param mag_error: magnitude error
    :return: percentage flux error corresponding to this magnitude error.
    """
    return mag_error * (2.30258509299 / 2.5)  # math.log takes natural log unless specified.

def percent_flux_errors_to_mag_errors(percent_flux_error):
    """Converts a percentage flux error into a magnitude error.

    m = -2.5 log10(F) + C
    dm = -2.5/(ln(10)) dF/F

    note: ln(10) = 2.30258509299
    I just plug in the numerical number to avoid importing things to take natural logs.

    :param percent_flux_error: percentage flux error
    :return: magnitude error corresponding to the percentage flux error.
    """
    return (2.5 / 2.30258509299) * percent_flux_error

# Note: these all need to be tested.