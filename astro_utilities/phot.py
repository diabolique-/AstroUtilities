from astropy.io import fits

import utilities

def aperture_grid(image, coords_file, spacing, clobber=False):
	"""
	Makes a grid of apertures and writes to a qphot-compatible coords file.

	:param image: location of the image to be used.
	:param coords_file: name of the coordinates file that the output will be 
	                    written to.
	:param spacing: x and y spacing between locations. For example, if one
	                aperture is located at x, the next is x + spacing. The
	                same thing holds for the y direction.
	:param clobber: Whether or not to check for an already existing file of
	                this name. If it already exists, it will raise an error.
	:returns: none, but the output is written to the `coords_file`.
	"""
	if not clobber:
		if utilities.check_if_file(coords_file):
			raise IOError("The coords file {} already exists. "
				          " Set clobber = True if you're okay with "
				          "overwriting this.")
	# if everything is fine, it will continue on.

	header = fits.getheader(image)
	x_max = header["NAXIS1"]
	y_max = header["NAXIS2"]

	xs = np.arange(spacing / 2.0, x_max, spacing)
	ys = np.arange(spacing / 2.0, y_max, spacing)

	with open(coords_file, "w") as output:
		for x in xs:
			for y in ys:
				output.write("{} {}\n".format(x, y))



