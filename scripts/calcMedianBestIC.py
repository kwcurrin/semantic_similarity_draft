import getRelationships
import collections
import numpy as np
import math
import scipy.special as ss

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

def asymmetric_comparison(query_terms,db_profiles,annotation_ICs,ancestors,lm_results):
	"""This function computes the IC score of the MICA between every term in profile1 with that in profile2.
	For each term in profile1, the corresponding term in profile2 that yields the highest IC score is extracted.
	The median of these best pairs is then calculated and returned."""

	fit_vals = lm_results[0]
	alpha,beta1,beta2 = lm_results[1]
	hat_diag = lm_results[2]
	mse_resid = lm_results[3]
	num_db_profiles = len(db_profiles)
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
		query_len = len(query_terms)
		match_len = len(db_profiles[best_ID])
#		print (query_len,match_len)
		predicted_IC = np.log(query_len)*beta1+np.log(match_len)*beta2+alpha
		resid = best_median_IC-predicted_IC
		### For now, I will just divide by standard deviation
		# to adjust residuals.
	#	i = list(fit_vals).index(predicted_IC)
		#student_resid = (resid)/(np.sqrt(mse_resid*(1-hat_diag[i])))
		student_resid = (resid)/np.sqrt(mse_resid)
		p = 1.0-(np.e**(-np.e**((-np.pi*student_resid)/(np.sqrt(6)-(ss.psi(1)*math.gamma(1))))))
		E = p*num_db_profiles
	return (best_ID,best_median_IC,best_match_pairs,E)