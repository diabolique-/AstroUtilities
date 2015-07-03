# note: modules are imported in each function to reduce overhead when using these utilities. This way, only the modules
# that are needed for the functions you use will be imported, rather than the modules needed for all utilities.

def reduced_chi_sq(model, data, errors):
    """ Does a reduced chi squared calculation

    :param model: list of values that describe a possible fit to the data
    :param data: list of values that are the data do be fitted
    :param errors: list of errors on the data
    :return: value for the chi_squared value of the fit of the model to the data
    """
    if not len(model) == len(data) == len(errors):
        raise ValueError("The length of the model, data, and errors need to be the same.")
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
# Note: these^ all need to be tested.


def fl_to_fv(fls, wavelengths):
    """ Converts flux from fl (flux per wavelength, with units of
    ergs/s/cm^2/Angstrom) to fv (flux per hertz, with units of ergs/s/cm^2/Hz).



    :param fls: list of flux per wavelength. Make sure they are in the units
                specified above.
    :type fls: list
    :param wavelengths: list of wavelengths. This must correspond to the
                        fluxes passed in above.
    :type wavelengths: list
    :return: flux per frequency, with the units specified above.
    :rtype: list
    """
    return [10**(-10) * wavelength**2 * fl / (3*(10**8))
            for wavelength, fl in zip(wavelengths, fls)]

def save_as_one_pdf(figs, filename):
    """
    Save a bunch of matplotlib figures to one pdf file at once.

    :param figs: list of figures to be saved as PDFs
    :type figs: list
    :param filename: place where the PDFs will be saved
    :type filename: str
    :return: none
    """
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt

    # save the objects with a pdfpages object
    pp = PdfPages(filename)
    for fig in figs:
        pp.savefig(fig)
    pp.close()

    # close the figures, too
    for fig in figs:
        plt.close(fig)

def abs_path(path):
    """Makes a given path into an absolute path.

    Works for paths that are already absolute, paths which start with ~/ and
    . and .. as well as paths that are just a file or folder. All relative
    paths are assumed to be relative to the current working directory.

    :param path: path to be made absolute
    :return: string with the absolute path
    """

    import os

    if path.startswith("/"):
        # is an absolute path, so we don't need to do anything
        return path
    elif path.startswith("~/"):
        # is relative to home, which is easy.
        return os.path.expanduser(path)
    elif path.startswith("../"):  # parent directory
        above = os.sep.join(os.getcwd().split(os.sep)[0:-1])
        # The 0:-1 is to get rid of the last path (our current directory),
        # which will give us the directory above
        return above + path[2:]  # get rid of ..
    elif path.startswith("./"):  # current directory
        return os.getcwd() + path[1:]  # get rid of .
    elif path[0].isalnum():  # relative to current directory
        return os.getcwd() + os.sep + path
    else:
        raise ValueError("Path format not recognized.")

def get_files_with_extension(parent_directory, extension):
    """Gets all the files in the parent directory (and its subdirectories)
    that end with extension.

    :param parent_directory: parent directory to search for catalogs.
    :param extension: extension of the files that will be returned
    :return: List of paths to files in parent_directory that end with
             extension.
    """
    catalogs = []
    for dirpath, dirnames, filenames in os.walk(parent_directory):
        for filename in filenames:
            if filename.endswith(extension):
                catalogs.append(os.path.join(dirpath, filename))
    return catalogs

def convert_flux(flux, zeropoint1, zeropoint2):
    """Converts flux from one unit to another.

    The flux units must be f_nu units, like Janskys. The zeropoints passed
    in are the conversion to AB mags.

    Math behind this:
    -2.5 log(f1) + zp1 = -2.5 log(f2) + zp2   # mag will be the same
    log(f2) = log(f1) + (zp2 - zp1)/2.5
    f2 = f1 * 10^((zp2 - zp1)/2.5)

    :param flux: flux to be converted
    :param zeropoint1: zeropoint of the AB magnitude system for the units of
                       of the flux being passed in.
    :param zeropoint2: zeropoint of the AB magnitude system for the units of
                       the result.
    Some common zeropoints:
        uJ: 23.9
        maggies: 0
    :return: flux in the units corresponding to zeropoint2
    """
    import math
    return flux * 10**((zeropoint2 - zeropoint1)/2.5)

# TODO: error checking in flux and mag calculations
# TODO: Vega to AB mags


