# note: modules are imported in each function to reduce overhead when using these utilities. This way, only the modules
# that are needed for the functions you use will be imported, rather than the modules needed for all utilities.

def reduced_chi_sq(model, data, errors):
    """ Does a reduced chi squared calculation

    .. math::
        \\chi^2 = \\sum_{k=1}^{n} \\left( \\frac{\\text{model}_k - \\text{data}_k}{\\text{error}_k} \\right) ^2

        \\chi^2_{\\text{red}} = \\frac{\\chi^2}{n}

    where :math:`n` is the number of data points.

    :param model: list of values that describe a possible fit to the data
    :param data: list of values that are the data do be fitted
    :param errors: list of errors on the data
    :return: value for the reduced chi squared value of the fit of the model to the data
    """
    if not len(model) == len(data) == len(errors):
        raise ValueError("The length of the model, data, and errors need to be the same.")
    chi_sq = 0
    for i in range(len(model)):
        chi_sq += ((model[i] - data[i])/errors[i])**2
    return chi_sq/(len(data))

def mag_to_flux(mag, zeropoint):
    """Convert a magnitude into a flux.

    We get the conversion by starting with the definition of the magnitude scale.

    .. math::
        m = -2.5 \\log_{10}(F) + C 

        2.5 \\log_{10}(F) = C - m

        F = 10^{\\frac{C-m}{2.5}}

    :param mag: magnitdue to be converted into a flux.
    :param zeropoint: zeropoint (in mags) of the magnitude system being used
    :return: flux that corresponds to the given magnitude
    """
    return 10**((zeropoint - mag)/2.5)


def flux_to_mag(flux, zeropoint):
    """Convert flux to magnitude with the given zeropoint.

    .. math::
        m = -2.5 \\log_{10} (F) + C

    :param flux: flux in whatever units. Choose your zeropoint correctly to make this work with the units flux is in.
    :param zeropoint: zeropoint of the system (in mags)
    :return: magnitude that corresponds to the given flux
    """
    import numpy as np
    try:
        return -2.5 * np.log10(flux) + zeropoint  # This is just the definition of magnitude
    except ValueError:  # the flux might be negative, and will mess things up
        return np.nan


def mag_errors_to_percent_flux_errors(mag_error):
    """Converts a magnitude error into a percent flux error.

    .. math::
        m = -2.5 \\log_{10} (F) + C

        dm = \\frac{-2.5}{\ln(10)} \\frac{dF}{F}

        \\frac{dF}{F} = \\frac{\\ln(10)}{2.5} dm 

    The minus sign just tells us that increasing flux gives decreasing magnitudes, so we can safely ignore it.

    note: :math:`ln(10) = 2.30258509299`
    I just plug in the numerical number to avoid importing things to take natural logs.

    :param mag_error: magnitude error
    :return: percentage flux error corresponding to this magnitude error.
    """
    return mag_error * (2.30258509299 / 2.5)  # math.log takes natural log unless specified.

def percent_flux_errors_to_mag_errors(percent_flux_error):
    """Converts a percentage flux error into a magnitude error.

    .. math::
        m = -2.5 \\log_{10} (F) + C

        dm = \\frac{-2.5}{\ln(10)} \\frac{dF}{F}

    note: :math:`ln(10) = 2.30258509299`
    I just plug in the numerical number to avoid importing things to take natural logs.

    :param percent_flux_error: percentage flux error
    :return: magnitude error corresponding to the percentage flux error.
    """
    return (2.5 / 2.30258509299) * percent_flux_error

# Note: these all need to be tested.
