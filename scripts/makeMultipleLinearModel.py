import random
import collections
#import statsmodels.api as sm
#import statsmodels.stats.outliers_influence as ss
import numpy as np
import cPickle
import math
import sys
#sys.path.append("..")

#import calcMedianBestIC

def make_multi_lm(profile_filename,annotation_filename,annotation_ICs_filename,ancestor_filename,out_filename):
	"""This function uses the supplied query and database profiles to generate a multiple linear model
	which will be used to calculate the expected number of similarity scores greater than or equal to n observed score 
	for a given combination of query and database profile sizes.
	The log of the query and database profile sizes will be the two independent variables
	and the similarity score (defined as the median of the best IC scores among each combination of annotations in the two profiles)
	will be the dependent variable.
	This function returns the fitted y values, the intercept and slopes of the model, and the diagonal of the hat matrix."""

	# Read in the database profiles, annotations, annotation ICs, and ancestors.
	with open(profile_filename,"r") as profile_file:
		db_profiles = cPickle.load(profile_file)
	with open(annotation_filename,"r") as annotation_file:
		annotations = [line.rstrip() for line in annotation_file]
	with open(annotation_ICs_filename,"r") as IC_file:
		annotation_ICs = cPickle.load(IC_file)
	with open(ancestor_filename,"r") as ancestor_file:
		ancestors = cPickle.load(ancestor_file)

	# Generate random queries for the linear model.
	query_profiles = make_random_queries(db_profiles,annotations)
	
	# Initialize lists for the x and y values.
	# The y list will be one dimensional and the x list will be a list of two dimensional tuples.
#	y = []
#	x = []
	num_points = float(len(query_profiles)*len(db_profiles))
#	y = np.empty(num_points,float)
#	x = np.empty((num_points,2),float)
	# Calculate the x and y values by querying each query profile
	# against each database profile.
	### Test
	out_file = open(out_filename,"w")
	i = 0
	for query in query_profiles.itervalues():
		query_log_len = math.log(len(query))
		for db in db_profiles.itervalues():
#			similarity = None
#			x.append((query_log_len,math.log(len(db))))
#			x[i,:] = (query_log_len,np.log(len(db)))
			out_file.write("%0.4f\t%0.4f\t" % (query_log_len,np.log(len(db))))
			#similarity = asymmetric_comparison(query,db,annotation_ICs,ancestors)
			best_pairs = []
			for term1 in query:
#				MICA_IC = None
				MICA_ICs = []
				for term2 in db:
					common_ancestors = ancestors[term1].intersection(ancestors[term2])
					MICA_IC = max([annotation_ICs[term] for term in common_ancestors])
					MICA_ICs.append(MICA_IC)
				best_pairs.append(max(MICA_ICs))
			similarity = np.median(best_pairs)
			out_file.write("%0.4f\n" % (similarity))
#			y.append(similarity)
#			y[i] = similarity
			i+=1
	out_file.close()
	### end test
	# Convert the x and y lists to numpy arrays for the linear regression analysis.
#	x = np.array(x)
#	y = np.array(y)
	# Add a column of ones to the x matrix so that the matrix algebra for the y-ointercept works.
#	x = sm.add_constant(x)
	# Fit the multiple linear model.
#	lm = sm.OLS(y,x).fit()
	# Get the influence results of the model and use it to get the diagonal of the hat matrix.
#	influence = ss.OLSInfluence(lm)
#	hat_diag = influence.hat_matrix_diag
#	results = (lm.fittedvalues,lm.params,hat_diag,lm.mse_resid)
#	with open(out_filename,"w") as out_file:
#		cPickle.dump(results,out_file)
#	return results
	return
	
def make_random_queries(profiles,annotations):
	"""This function generates random profile queries from the list of available annotations.
	One query is generated for each unique profile size in the database.
	These queries will be used against the database to generate values for the multiple linear regression
	that is used to produce an expect (E) value for similarity scores for a given pair of query and database profile sizes.
	A dictionary of lists with profile IDs as keys and annotations as values will be returned.
	It is better to randomize the queries rather than copy them from the database to make the 
	queries (x1 in the model) more independent from the database profiles (x2 in the model)."""
	
	# Initialize a dictionary for the queries.
	queries = collections.defaultdict(list)
	# Generate a set of database profile sizes.
	unique_sizes = set([len(i) for i in profiles.values()])
	# Loop through the set of profile sizes and randomly sample
	# the corresponding number of annotations from the annotation pool.
	for size in unique_sizes:
#	for size in xrange(10,151,10):
		for i in xrange(1,size+1):
			queries[size].append(random.choice(annotations))
	return queries

def asymmetric_comparison(query_terms,db_terms,annotation_ICs,ancestors):
	"""This function computes the IC score of the MICA between every term in profile1 with that in profile2.
	For each term in profile1, the corresponding term in profile2 that yields the highest IC score is extracted.
	The median of these best pairs is then calculated and returned."""

	best_pairs = []
	for term1 in query_terms:
		MICA_IC = None
		MICA_ICs = []
		for term2 in db_terms:
			common_ancestors = set.intersection(ancestors[term1],ancestors[term2])
			MICA_IC = max([annotation_ICs[term] for term in common_ancestors])
			MICA_ICs.append(MICA_IC)
		best_pairs.append(max(MICA_ICs))
	return np.median(best_pairs)

if __name__ == "__main__":
	make_multi_lm(*sys.argv[1:])