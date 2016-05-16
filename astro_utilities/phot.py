from astropy.io import fits

import utilities

def aperture_grid(image, spacing, output=False, clobber=False):
	"""
	Makes a grid of apertures and writes to a qphot-compatible coords file.

	:param image: location of the image to be used.
	:type image: str
	:param spacing: x and y spacing between locations. For example, if one
	                aperture is located at x, the next is x + spacing. The
	                same thing holds for the y direction.
	:param spacing: float
	:param output: Either False, or the name of the coordinates file 
	                    that the output will be written to. If you don't want 
	                    to write to a file, pass in False.
	:type output: bool / str
	:param clobber: Whether or not to check for an already existing file of
	                this name. If it already exists, it will raise an error.
	:returns: List of tuples that contain the x,y coordinates of each
	          aperture.
	"""
	if output and not clobber:
		if utilities.check_if_file(coords_file):
			raise IOError("The coords file {} already exists. "
				          " Set clobber = True if you're okay with "
				          "overwriting this.")
	# if everything is fine, it will continue on.

	# get the size of the image from the header
	header = fits.getheader(image)
	x_max = header["NAXIS1"]
	y_max = header["NAXIS2"]

	# then find all the places apertures can go. The first one is spaced half
	# a spacing from the edge, so that if aperture_size = spacing, then the 
	# aperture would go to the edge of the image.
	xs = np.arange(spacing / 2.0, x_max, spacing)
	ys = np.arange(spacing / 2.0, y_max, spacing)

 	# Then turn these into ordered pairs.
 	ordered_pairs = []
	for x in xs:
		for y in ys:
			ordered_pairs.append((x, y))

	# then if the user wants to, write to the file
	if output:
		with open(output, "w") as output_file:
			for x, y in ordered_pairs:
				output_file.write("{} {}".format(x, y))

	# no matter what, return the ordered pairs
	return ordered_pairs


def fit_gaussian_negative(data, upper_cutoff):
	"""
	Fits a Gaussain to all data underneath some cutoff.

	This is useful when doing things where the lower side of a Gaussian tells
	about the intrinsic scatter of something, whereas the upper end is 
	contaminated by real objects. An example is the flux within many 
	randomly placed apertures. The lower side will tell the sky error in the
	aperture flux.

	:param data: list of data to be fitted.
	:type data: list, np.array
	:param upper_cutoff: Data below this number will be used to fit the 
	                     Gaussian, while data above this will be rejected.
	:type upper_cutoff: float
	:param plot: Whether or not to plot the Gaussian. It this is true, the
	             figure will be returned also.
	:type plot: bool
	:return: the mean, sigma, and amplitude of the best fit Gaussian.
	"""
	from scipy.optimize import curve_fit

	good_data = [item for item in data if item < upper_cutoff]

	# figure out the number of bins to have in the histogram, which is what the
	# gaussian will be fitted to under the hood
	bins = int(np.ceil(np.sqrt(len(data))))

	bin_values, bin_edges = np.histogram(data, bins=bins, density=True)

	# turn the edges into centers of the bins
	bin_centers = []
	for i in range(len(bin_edges) - 1):  # iterate through all left edges
		center = np.mean([bin_edges[i], bin_edges[i+1]])
		bin_centers.append(center)

	params, uncertainty = curve_fit(utilities.gaussian, xdata=bin_centers,
	                                ydata=bin_values)

	return params

def sky_error(image, aperture_size, flux_conv, plot=True):
	"""
	Figures out the sky error with an aperture of a given size.

	This is done by placing apertures in a grid throughout the image, then
	doing aperture photometry within those apertures. Most of those will be on
	empty sky. By examining the spread of the fluxes of the apertures that
	were on empty sky, we can get an idea of the general sky scatter in an 
	aperture of that size.

	:param image: Image to do this process on. Pass in the path to the image,
	              or just the name of the image if it is in the current
	              directory.
	:type image: str
	:param aperture_size: The diameter of the aperture you want to use. NOTE
	                      THAT THIS IS DIAMETER, NOT RADIUS!
	:type aperture_size: float
	:param flux_conv: multiplicative factor to get from counts in the image
	                  to real fluxes in whatever units you want. Should be
	                  defined such that "flux" = "counts" * `flux_conv`. This
	                  can be determined from the zeropoint of the image.
	:type flux_conv: float
	:param plot: Whether or not to plot the Gaussian that results from this
	             process.
	:type plot: bool
	:return: flux error within that aperture size, in real flux units. Note 
	         you need to multiply by the aperture correction to get total 
	         errors!
	"""

	# first define the aperture grid
	coords_file = "{}_coords_temp.txt".format(image)
	centers = aperture_grid(image, coords_file, aperture_size)

	# then do photometry at those locations. This needs to be without a 
	# background correction, so we can't use qphot.
	return

	# THIS FUNCTION IS NOT DONE.



