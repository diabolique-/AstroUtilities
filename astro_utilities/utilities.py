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


def symmetric_match(table_1, table_2, ra_col_1="ra", ra_col_2="ra",
          dec_col_1="dec", dec_col_2="dec", max_sep=3.0):
    """
    Matches objects from two astropy tables by ra/dec.

    This function does symmetric matching. This measns that to be defined as
    a match, both objects must be each other's closest match. Their separation
    must also be less than the `max_sep` parameter.

    :param table_1: First astopy table object containing objects with ra/dec
                    information.
    :param table_2: First astopy table object containing objects with ra/dec
                    information.
    :param ra_col_1: Name of the ra column in table_1. Defaults to "ra".
    :param ra_col_2: Name of the ra column in table_2. Defaults to "ra".
    :param dec_col_1: Name of the dec column in table_1. Defaults to "dec".
    :param dec_col_2: Name of the dec column in table_2. Defaults to "dec".
    :param max_sep: Maximum separation (in arcseconds) allowed for two objects
                    to be considered a match.
    :return: Astropy table object containing the matches between the two
             input table objects. All columns from both catalogs will be
             included, as well as a separate separation column.
    """

    from astropy.coordinates import match_coordinates_sky, SkyCoord
    from astropy import units as u
    from astropy import table

    coords_1 = SkyCoord(table_1[ra_col_1], table_1[dec_col_1], unit=u.degree)
    coords_2 = SkyCoord(table_2[ra_col_2], table_2[dec_col_2], unit=u.degree)

    # find matches for objects in table 1 in table 2
    match_idx_12, sep_12, dist_12 = match_coordinates_sky(coords_1, coords_2)
    # and find matches for objects in table 2 in table 1
    match_idx_21, sep_21, dist_21 = match_coordinates_sky(coords_2, coords_1)

    # now check that the matching is symmetric
    symmetric_12 = []
    for idx_1, match_idx in enumerate(match_idx_12):
        if idx_1 == match_idx_21[match_idx] and sep_12[idx_1].arcsec < max_sep:
            symmetric_12.append((idx_1, match_idx, sep_12[idx_1].arcsec))

    idx_1, idx_2, sep = zip(*symmetric_12)

    idx_1 = list(idx_1)
    idx_2 = list(idx_2)
    sep = list(sep)

    # now turn into astropy table
    matches = table_1[idx_1]
    # get only the ones from table_2 that have matches
    matches_2 = table_2[idx_2]

    for col in matches_2.colnames:
        if col in matches.colnames:
            matches_2.rename_column(col, col + "_2")
            matches.add_column(matches_2[col + "_2"])
        else:
            matches.add_column(matches_2[col])

    matches.add_column(table.Column(data=sep, name="sep [arcsec]"))

    return matches

# Note: these all need to be tested.

