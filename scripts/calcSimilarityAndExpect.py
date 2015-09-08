import math
import numpy as np

def calcPVal(query_profiles,db_profiles,fit_vals,alpha,beta1,beta2,hat_diag):
	num_db_profiles = len(db_profiles)
	for query in query_profiles:
		for db in db_profiles:
			observed = getMedianBestIC(query,db)
			predicted = np.log(len(query))*beta1+np.log(len(db))*beta2+alpha
			resid = observed-predicted
			i = fit_vals.index(predicted)
			student_resid = (resid)/(np.sqrt(mse_resid*(1-hat_diag[i])))
			p = 1.0-(np.e**(-np.e**((np.pi*student_resid)/(np.sqrt(6)-math.gamma(1)))))
			E = p*num_db_profiles
	return (observed,E)