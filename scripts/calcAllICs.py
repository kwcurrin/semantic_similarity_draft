import collections
import numpy as np
import cPickle
import sys

def annotation_denominator(annotation_filename,ancestor_filename,out_filename): 
	"""This function calculates the IC of each annotation and normalizes it by the maximum possible IC.
	The IC of an annotation is defined as the negative log of the frequency of the annotation in the pool of all annotations including duplicates.
	The maximum IC score used to normalize the IC scores is -log(1/num_annotations).
	A dictionary is returned with annotations as keys and normalized ICs as values."""

	with open(annotation_filename,"r") as annotation_file:
		annotations = [line.rstrip() for line in annotation_file]
	# Initialize the dictionary for the annotation ICs.
	annotation_ICs = collections.defaultdict(float)
	# Calculate the maximum possible IC from the number of annotations.
	num_all_annotations = len(annotations)
	max_IC = -np.log(1.0/num_all_annotations)
	# Initialize a dictionary for the annotation counts.
	annotation_count = collections.defaultdict(int)
	# Loop through profiles and find out the frequency of each annotation.
#	for ID in profiles.iterkeys():
#		for annotation in profiles[ID]:
	for annotation in annotations:
		annotation_count[annotation]+=1
#	count=set()
	### memory efficient code:
	# Add the counts of the children nodes to their parents.
	# Open the ancestors file.
	with open(ancestor_filename,"r") as ancestor_file:
		for line in ancestor_file:
			split_line = line.replace(">","").replace("<","").rstrip().split("\t")
			child = split_line[0]
			parent = split_line[1]
#			if "UBERON" not in split_line[0] or "UBERON" not in split_line[1]:
#				continue
#			child_match = pattern.search(split_line[0])
#			if child_match:
#			child = split_line[0][child_match.start():child_match.end()]
#			parent_match = pattern.search(split_line[1])
#			if parent_match:
#			parent = split_line[1][parent_match.start():parent_match.end()]
			### The below four lines are not required because after removing the "<" symbols,
			### all of the children are in the unique_annotations set.
#			if child not in unique_annotations:
#				print child
#				exit()
#				continue
			annotation_count[parent]+=annotation_count[child]
#	print len(count)
#	print list(count)[0]
	### memory inefficient code:
	# Add the counts of the children nodes to their parents.
#	for annotation,count in raw_count.iteritems():
#		subsumer_count[annotation] = count
#		for child in children(annotation):
#			subsumer_count[annotation]+=raw_count[child]

	# Calculate the IC for each annotation.
	for annotation,count in annotation_count.iteritems():
		if count == 0:
			print "One of the annotations had a count of 0, exiting"
			exit()
		IC = None
		IC = -np.log(float(count)/num_all_annotations)
		if IC == -0.0:
			norm_IC = 0.0
		else:
			norm_IC = IC/max_IC
		annotation_ICs[annotation] = norm_IC
	with open(out_filename,"w") as out_file:
		cPickle.dump(dict(annotation_ICs),out_file)
	return annotation_ICs

### This function has not been updated to have subsumer count adjustments
def taxa_denominator(profiles):
	"""This function calculates the IC of each annotation and normalizes it by the maximum possible IC.
	The IC of an annotation is defined as the negative log of the percentage of taxa (or genes or something else) that map to the annotation.
	The maximum IC score used to normalize the IC scores is -log(1/num_taxa).
	A dictionary is returned with annotations as keys and normalized ICs as values."""
	
	# Initialize the dictionary for the annotation ICs.
	annotation_ICs = collections.defaultdict(float)
	# Calculate the maximum possible IC from the number of taxa in the database.
	num_all_taxa = len(profiles)
	max_IC = -np.log(1.0/num_all_taxa)
	# Initialize a dictionary to keep track of the number of taxa mapping to each annotation.
	taxa_per_annotation = collections.defaultdict(int)
	# Loop through profiles and find out how many taxa map to each annotation.
	for ID in profiles.iterkeys():
		for annotation in profiles[ID]:
			taxa_per_annotation[annotation]+=1
	
	# Calculate the IC for each annotation.
	for annotation,num_taxa in taxa_per_annotation.iteritems():
		IC = None
		IC = -np.log(float(num_taxa)/num_all_taxa)
		norm_IC = IC/max_IC
		annotation_ICs[annotation] = norm_IC
	return annotation_ICs

if __name__ == "__main__":
	annotation_denominator(*sys.argv[1:])