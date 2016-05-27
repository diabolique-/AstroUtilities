from setuptools import setup, find_packages

setup(
	name="sinistra",

	version="0.1.0",

	description="A collection of astronomy related tools.",
	long_description="A collection of astronomy related tools. This project contains a bunch of functions and classes I've written in my time doing astronomy. They may or may not be useful to anyone else.\nThe name sinistra comes from the name of the Hogwarts professor of astronomy in the Harry Potter books, who is names Professor Sinistra.",

	url="http://sinistra.readthedocs.io/en/latest/",

	author="Gillen Brown",
	author_email="gillenb@umich.edu",

	license="GNU GPLv3",

	keywords="astronomy tools utilities astrophysics",

	packages=find_packages(exclude=["docs"]),

	install_requires=["astropy", "numpy", "scipy"]


	)
