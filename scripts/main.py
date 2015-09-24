import sys
import collections
import cPickle
import string

import getQueryProfiles
import diluteQuery
import calcAllICs
import calcMedianBestIC
import makeMultipleLinearModel

def main(annotation_filename,annotation_IC_filename,ancestor_filename,lm_filename,random_profile_filename,num_queries,query_size,out_filename):
	"""This function tests the ability of our
	semantic similarity and expect score calculations to
	distinguish signal from noise in finding true matches to a query.
	The experiment follows the following steps:
	1. Generates a database of random profiles.
	2. Selects a specified number of queries of uniform size from the database.
	3. Determines the similarity and expect scores for each query with its
	closest match in the random database. Because the queries are also in
	the database, the best match for a query should initially be itself.
	4. Each term in each query is then randomly replaced. The terms
	initially present in the queries are excluded from the pool of replacement terms. The similarity
	and expect scores after each replacement are calculated."""

	# The num_queries and query_size variables represent the
	# number of random profiles to generate.
	num_queries = int(num_queries)
	query_size = int(query_size)
	# Read the annotations into a list.
	with open(annotation_filename,"r") as annotation_file:
		annotations = [line.rstrip() for line in annotation_file]
	# The random profiles, annotation ancestors, linear model results,
	# and annotation ICs are stored as pickled python dictionaries
	# in files to save computation time.
	with open(random_profile_filename,"r") as random_file:
		random_profiles = cPickle.load(random_file)
	num_db_profiles = len(random_profiles)
	with open(annotation_IC_filename,"r") as annotation_IC_file:
		annotation_ICs = cPickle.load(annotation_IC_file)
	with open(ancestor_filename,"r") as ancestor_file:
		ancestors = cPickle.load(ancestor_file)
	with open(lm_filename,"r") as lm_file:
		lm_results = cPickle.load(lm_file)

	# A specified number of queries (num_queries) of specified size (query_size)
	# will be generated from the database of random profiles.
	queries = getQueryProfiles.get_query_profiles(random_profiles,num_queries,query_size)

	# A list will be initialized to keep track of the 
	# similarity and expect score results.
	results = []
#	count = 0
	# The closest database for each query will be determined
	# based on similarity score. The corresponding expect
	# score will also be computed.
	for query_ID,query_terms in queries.iteritems():
#		if count > 0:
#			break
		best_ID,best_IC,best_pairs,E_val = calcMedianBestIC.asymmetric_comparison(query_terms,random_profiles,annotation_ICs,ancestors,lm_results)
		results.append((query_ID,0,best_ID,best_IC,E_val,string.join([str(round(i,4)) for i in best_pairs],",")))
		# Each term in each query will be randomly replaced.
		# The similarity and expect scores at each replacement will be computed.
		diluted_query = diluteQuery.dilute_query(query_terms,0,annotations,query_terms,duplicates="yes")
		best_ID,best_IC,best_pairs,E_val = calcMedianBestIC.asymmetric_comparison(diluted_query,random_profiles,annotation_ICs,ancestors,lm_results)
		results.append((query_ID,1,best_ID,best_IC,E_val,string.join([str(round(i,4)) for i in best_pairs],",")))
		for i in xrange(1,10):
			diluted_query = diluteQuery.dilute_query(diluted_query,i,annotations,query_terms,duplicates="yes")
			best_ID,best_IC,best_pairs,E_val = calcMedianBestIC.asymmetric_comparison(diluted_query,random_profiles,annotation_ICs,ancestors,lm_results)
			results.append((query_ID,i+1,best_ID,best_IC,E_val,string.join([str(round(i,4)) for i in best_pairs],",")))
#			count+=1

	# The results will be written to an output file.
	with open(out_filename,"w") as test_file:
		for result in results:
			test_file.write("%s\t%d\t%s\t%0.4f\t%0.8f\t%s\n" % tuple(result))
	return

if __name__ == "__main__":
	main(*sys.argv[1:])