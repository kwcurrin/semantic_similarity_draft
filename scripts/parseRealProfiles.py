import rdflib
import collections
import sys

def parse_real_profiles(profile_infile,annotation_outfile,profile_size_outfile):
	"""This function extracts the annotations and profile sizes from the .ttl file format.
	The size of a profile is equivalent to the number of annotations of that profile.
	The annotations are written to a line with duplicate annotations preserved.
	The profile sizes will be written to another file with the format (profile_ID\tprofile_size)..
	The annotations and profile sizes are written to a file because the rdflib parsing
	takes a bit of time and it would be best to have to run this script only once."""

	# Initialize the list for the annotations.
	all_annotations = []
	# Initialize the dictionary for the profile sizes.
	profile_sizes = collections.defaultdict(int)
	
	# Use the rdflib library to parse the .ttl file.	
	g = rdflib.Graph()
	result = g.parse(profile_infile,format="n3")
	
	# Each node in the rdflib graph (g) links one annotation to a profile ID.
	# The profile ID is the first index and the annotation is the third.
	# So if a profile has 30 annotations, there will be 30 different nodes in the graph.
	# We only want profile IDs that contain "VTO".
	for node in g:
		profile_ID = node[0]
		if "VTO" in profile_ID:			
			# The profile ID contains some extra markings that we need to remove.
			profile_ID = profile_ID.replace("http://purl.obolibrary.org/obo/","").replace("#profile","")
			annotation = node[2].replace(">","").replace("<","").rstrip()
			all_annotations.append(annotation)
			profile_sizes[profile_ID]+=1
	# Write the annotations to a file.
	with open(annotation_outfile,"wb") as annotation_file:
		for annotation in all_annotations:
			annotation_file.write(annotation+"\n")
	# Write the profile IDs and sizes to a file.
	with open(profile_size_outfile,"wb") as profile_file:
		for ID,size in profile_sizes.iteritems():
			profile_file.write("%s\t%d\n" % (ID,size))
	return

if __name__ == "__main__":
	parse_real_profiles(*sys.argv[1:])