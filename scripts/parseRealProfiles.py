import rdflib
import collections
import sys
import re

def parse_real_profiles(profile_infile,annotation_outfile,profile_size_outfile):
	"""This function extracts the annotations and profile sizes from the .ttl file format.
	The size of a profile is equivalent to the number of annotations of that profile.
	The annotations are written to a line with duplicate annotations preserved.
	The profile sizes will be written to another file with the format (profile_ID\tprofile_size)..
	The annotations and profile sizes are written to a file because the rdflib parsing
	takes a bit of time and it would be best to have to run this script only once."""

#	pattern = re.compile("UBERON_[0-9]*")
	# Initialize the list for the annotations.
	all_annotations = []
	# Initialize the dictionary for the profile sizes.
	profile_sizes = collections.defaultdict(int)
	
	# Use the rdflib library to parse the .ttl file.	
	# The below line was in Prashanti's code. It doesn't seem to be necessary,
	# but I included it just in case.
#	register('text/rdf+n3', Parser, 'rdflib.plugins.parsers.notation3', 'N3Parser')
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
#			if "UBERON" in node[2]:
#				match = pattern.search(node[2])
#				annotation = node[2][match.start():match.end()]
			all_annotations.append(annotation)
			profile_sizes[profile_ID]+=1
	print len(profile_sizes)
	print len(all_annotations)
	count = 0
	for key in profile_sizes.iterkeys():
		count+=profile_sizes[key]
	print count
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