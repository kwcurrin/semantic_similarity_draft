import sys
import collections
import cPickle
import string

import makeRandomProfiles
#import getRelationships
import getQueryProfiles
import diluteQuery
import calcAllICs
import calcMedianBestIC
import makeMultipleLinearModel
#import calcSimilarityAndExpect

#import getContainerMemory

def main(annotation_filename,annotation_IC_filename,profile_filename,ancestor_filename,lm_filename,random_profile_filename,out_filename):
	annotations,profile_sizes = read_files(annotation_filename,profile_filename)
#	ancestors,children = getRelationships.get_relationships(ancestor_filename)
	#random_profiles = makeRandomProfiles.with_replacement(annotations,profile_sizes)
	with open(random_profile_filename,"r") as random_file:
		random_profiles = cPickle.load(random_file)
	num_db_profiles = len(random_profiles)
#	unique_annotations = set(annotations)
	with open(annotation_IC_filename,"r") as annotation_IC_file:
		annotation_ICs = cPickle.load(annotation_IC_file)
#	print getContainerMemory.total_size(annotation_ICs)
#	annotation_ICs = calcAllICs.annotation_denominator(annotation_filename,ancestor_filename,None)
#	ancestors = getRelationships.get_relationships(ancestor_filename,unique_annotations)
	with open(ancestor_filename,"r") as ancestor_file:
		ancestors = cPickle.load(ancestor_file)
#	print len(random_profiles.values()[0])
	del(profile_sizes)
#	ancestors = getRelationships.get_relationships(ancestor_filename,unique_annotations)
	with open(lm_filename,"r") as lm_file:
		lm_results = cPickle.load(lm_file)
	queries = getQueryProfiles.get_query_profiles(random_profiles,5,10)
	results = []
#	count = 0
	for query_ID,query_terms in queries.iteritems():
#		if count > 0:
#			break
		best_ID,best_IC,best_pairs,E_val = calcMedianBestIC.asymmetric_comparison(query_terms,random_profiles,annotation_ICs,ancestors,lm_results)
		results.append((query_ID,0,best_ID,best_IC,E_val,string.join([str(round(i,4)) for i in best_pairs],",")))
		diluted_query = diluteQuery.dilute_query(query_terms,0,annotations,query_terms,duplicates="yes")
#		print len(diluted_query)
		best_ID,best_IC,best_pairs,E_val = calcMedianBestIC.asymmetric_comparison(diluted_query,random_profiles,annotation_ICs,ancestors,lm_results)
		results.append((query_ID,1,best_ID,best_IC,E_val,string.join([str(round(i,4)) for i in best_pairs],",")))
		for i in xrange(1,10):
			diluted_query = diluteQuery.dilute_query(diluted_query,i,annotations,query_terms,duplicates="yes")
#			diluted_query = diluteQuery.new_dilute_query(query_terms,i,annotations,duplicates="yes")
#			print len(diluted_query)
#			print len(query_terms)
			best_ID,best_IC,best_pairs,E_val = calcMedianBestIC.asymmetric_comparison(diluted_query,random_profiles,annotation_ICs,ancestors,lm_results)
			results.append((query_ID,i+1,best_ID,best_IC,E_val,string.join([str(round(i,4)) for i in best_pairs],",")))
#			count+=1
	with open(out_filename,"w") as test_file:
		for result in results:
			test_file.write("%s\t%d\t%s\t%0.4f\t%0.8f\t%s\n" % tuple(result))
#	query_ID = queries.keys()[0]
#	query_terms = queries[query_ID]
#	best_match = calcMedianBestIC.asymmetric_comparison(query_terms,random_profiles,annotation_ICs,ancestors)
#	print (query_ID,best_match[0],best_match[1])

#	fitted_values,params,hat_diag = makeMultipleLinearModel.make_multi_lm(random_profiles,annotations,annotation_ICs,ancestors)
#	print len(fitted_values)
#	print params
#	print len(hat_diag)
#	print query
#	diluted_query = diluteQuery.dilute_query(query,0,annotations,query)
#	print diluted_query
#	diluted_query = diluteQuery.dilute_query(diluted_query,1,annotations,query)
#	print diluted_query
#	diluted_query = diluteQuery.dilute_query(diluted_query,2,annotations,query)
#	print diluted_query
	#annotation_ICs = calcAllICs.annotation_denominator(random_profiles,annotations,ancestor_filename)
#	print len(annotation_ICs)
#	print annotation_ICs.values()[:5]
#	check_inf = annotation_ICs.keys()[2]
#	print check_inf in annotations
#	for query_profile in queries.itervalues():
#		for db_profile in random_profiles.itervalues():
#			calcMedianBestIC.asymmetric_comparison(query_profile,db_profile,annotation_ICs,ancestors)
	return

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
	main(*sys.argv[1:])