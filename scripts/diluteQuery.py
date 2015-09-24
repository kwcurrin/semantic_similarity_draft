import random

def dilute_query(query,index,possible_annotations,original_annotations,duplicates="no"):
	"""This function takes a query profile and replaces one of its annotations
	with a randomly selected annotation. Annotations that were originally in
	the query before any dilutions were performed are removed from the pool of possible replacement annotations.	
	It is important to make sure none of the original annotations get back into the query because we 
	are performing an incremental dilution to show decreasing similarity scores and increasing
	E values between the query and its copy in the database as the query is diluted.
	The duplicates parameter allows specification of whether the current query annotations should be considered
	as possible replacement annotations.
	The default is not to consider the current query annotations as possible replacements.
	The query format should just be the list of annotations, not the dictionary entry ID: annotations.
	The index parameter specifies which annotation should be replaced."""
		
	# Determine if the current query annotations should be 
	# removed from the list of possible annotations
	# in addition to the original annotations.	
	removed_annotations = list(original_annotations)
	if duplicates == "no":
		removed_annotations.extend(query)
	for annotation in removed_annotations:
		for i in xrange(possible_annotations.count(annotation)):
			possible_annotations.remove(annotation)
	
	# Replace the annotation at the specified index with a random selection from the possible annotations.
	diluted_query = list(query)
	diluted_query[index] = random.choice(possible_annotations)
	return diluted_query
		