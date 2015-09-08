import getRelationships
import collections
import numpy as np

def symmetric_comparison(profile1,profile2,annotation_ICs,ancestors):
	"""This function computes the IC score of the MICA between every term in profile1 with that in profile2.
	For each term in profile1, the corresponding term in profile2 that yields the highest IC score is extracted.
	The median of these best pairs is then taken.
	Next, for each term in profile2, the term in profile1 that yields the highest IC score is extracted and the median is calculated.
	The mean of these two medians is calculated and returned."""
	
	profile1_best = []
	profile2_best = []	
	for term1 in profile1:
		MICA_IC = None
		MICA_ICs = []
		for term2 in profile2:
			common_ancestors = set.intersection(ancestors[term1],ancestors[term2])
			MICA_IC = max([annotation_ICs[term] for term in common_ancestors])
			MICA_ICs.append(MICA_IC)
		profile1_best.append(max(MICA_ICs))
	profile1_median = np.median(profile1_best)
	for term2 in profile2:
		MICA_IC = None
		MICA_ICs = []
		for term1 in profile1:
			common_ancestors = set.intersection(ancestors[term1],ancestors[term2])
			MICA_IC = max([annotation_ICs[term] for term in common_ancestors])
			MICA_ICs.append(MICA_IC)
		profile2_best.append(max(MICA_ICs))
	profile2_median = np.median(profile2_best)
	return np.mean(profile1_median,profile2_median)

def asymmetric_comparison(query_terms,db_profiles,annotation_ICs,ancestors):
	"""This function computes the IC score of the MICA between every term in profile1 with that in profile2.
	For each term in profile1, the corresponding term in profile2 that yields the highest IC score is extracted.
	The median of these best pairs is then calculated and returned."""

	best_median_IC = 0
	best_ID = None
	best_match_pairs = []
	for db_ID,db_terms in db_profiles.iteritems():
		best_pairs = []
		for term1 in query_terms:
			MICA_IC = None
			MICA_ICs = []
			for term2 in db_terms:
				common_ancestors = set.intersection(ancestors[term1],ancestors[term2])
				MICA_IC = max([annotation_ICs[term] for term in common_ancestors])
				MICA_ICs.append(MICA_IC)
			best_pairs.append(max(MICA_ICs))
		median_IC = np.median(best_pairs)
		if median_IC > best_median_IC:
			best_median_IC = median_IC
			best_ID = db_ID
			best_match_pairs = best_pairs
	return (best_ID,best_median_IC,best_match_pairs)