import collections
import sys
import cPickle

#import getContainerMemory

def get_relationships(ancestor_filename,annotation_filename,out_filename):
	"""This function finds the ancestors and children of each annotation.
	For ancestors, a dictionary with children as keys and unique ancestors as values will be returned.
	For children, a dictionary with ancestors as keys and unique children as values will be returned."""
	
	with open(annotation_filename,"r") as annotation_file:
		unique_annotations = set([line.rstrip() for line in annotation_file])
	# Initialize the dictionaries for the ancestors and children.
	ancestors = collections.defaultdict(set)
#	children = collections.defaultdict(set)
	# Open the ancestors file.
	with open(ancestor_filename,"r") as ancestor_file:
		for line in ancestor_file:
			split_line = line.replace("<","").replace(">","").rstrip().split("\t")
			child = split_line[0]
			if child not in unique_annotations:
				continue
			parent = split_line[1]
			ancestors[child].add(parent)
			# Make sure to make a child a superclass of itself
			# which is useful when a term is queried against itself.
			ancestors[child].add(child)
#			children[parent].add(child)
#	print len(ancestors)
#	print len(children)
#	print getContainerMemory.total_size(ancestors)
	with open(out_filename,"w") as out_file:
		cPickle.dump(ancestors,out_file)
	return ancestors # (ancestors,children)

def get_children(ancestor_filename):
	children = collections.defaultdict(set)
	# Open the ancestors file.
	with open(ancestor_filename,"r") as ancestor_file:
		for line in ancestor_file:
			split_line = line.replace("<http://purl.obolibrary.org/obo/","").replace(">","").rstrip().split("\t")
			child = split_line[0]
			parent = split_line[1]
			children[parent].add(child)
	print len(children)	
	return children
	
if __name__ == "__main__":
	get_relationships(*sys.argv[1:])