import collections
import cPickle
import sys
import random

def with_replacement(annotation_filename,profile_size_filename,out_filename=None):
	"""This function generates random profiles with the same size distribution as the real profiles.
	The annotations that are matched to each profile are what are randomized.
	The random sampling of annotations for a given profile is performed with replacement.
	The random sampling between profiles is without replacement.
	This function returns a dictionary with profile IDs as keys and lists of corresponding annotations as values."""

	# Read in the annotations and profile sizes.
	annotations,profile_sizes = read_files(annotation_filename,profile_size_filename)	
	# Initialize the dictionary for the random profiles.
	random_profiles = collections.defaultdict(list)
	# Loop through the profile_sizes list, randomly sample a list of annotations the size of the profile from the annotations list,
	# and add it to the random_profiles dictionary.
	for ID,size in profile_sizes:
		random_annotations = random.sample(annotations,size)
		random_profiles[ID] = random_annotations
	if out_filename:
		with open(out_filename,"w") as out_file:
			cPickle.dump(random_profiles,out_file)
	return random_profiles

def without_replacement(annotation_filename,profile_filename):
	"""This function generates random profiles with the same size distribution as the real profiles.
	The annotations that are matched to each profile is what is randomized.
	The random sampling of annotations for a given profile is performed without replacement.
	The random sampling between profiles is also without replacement.
	and the profile sizes file into a dictionary.
	This function returns a dictionary with profile IDs as keys and lists of corresponding annotations as values."""

	# Initialize the dictionary for the random profiles.
	random_profiles = collections.defaultdict(list)
	# Read in the annotations and profile sizes.
	annotations,profile_sizes = read_files(annotation_filename,profile_filename)
	# Generate a randomized copy of the annotations list.
	# Note: I did not use random.shuffle because the documentation said something about permutations of large sequences not being good.
	random_annotations = random.sample(annotations,len(annotations))
	# Populate the random profiles dictionary by popping values from random_annotations.
	# The number of pops needed will be determined from the size of the corresponding real profiles.
	for ID,size in profile_sizes:
		for i in xrange(size):
			random_profiles[ID].append(random_annotations.pop())
	# random_annotations should now be empty.
	return random_profiles
	
def read_files(annotation_filename,profile_filename):
	"""This function reads the file of all annotations into a list and the file of 
	profile sizes into a list of tuples containing (profile_ID,size).
	Both the annotations list and profile_sizes dictionary are returned."""
	# Initialize the dictionary of profile sizes.
	random_profiles = collections.defaultdict(list)
	# Read the annotations into a list.
	with open(annotation_filename,"r") as annotation_file:
		annotations = [line.rstrip() for line in annotation_file]
	# Read the profile IDs and sizes into a list of tuples.
	profile_sizes = []
	with open(profile_filename,"r") as profile_file:
		for line in profile_file:
		# Split the lines on a tab and remove line termination characters.
			split_line = line.rstrip().split("\t")
			profile_sizes.append((split_line[0],int(split_line[1])))
	return (annotations,profile_sizes)

if __name__ == "__main__":
	with_replacement(sys.argv[1],sys.argv[2],out_filename=sys.argv[3])