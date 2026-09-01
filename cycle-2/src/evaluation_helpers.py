"""Reusable evaluation helpers extracted from ER-CyRIS Cycle 2 v4 FINAL fixed notebook.

The executed notebook remains the primary research artifact. This module is provided
for easier code inspection and reuse in the public repository.
"""

import json
import numpy as np
from sklearn.metrics import average_precision_score, confusion_matrix, f1_score, precision_score, recall_score

def evaluate(model, X, y, name='', ds=''):
    yp = model.predict(X)
    yb = model.predict_proba(X)[:,1]
    p  = precision_score(y,yp,zero_division=0)
    r  = recall_score(y,yp,zero_division=0)
    f  = f1_score(y,yp,zero_division=0)
    a  = average_precision_score(y,yb)
    tn,fp,fn,tp = confusion_matrix(y,yp,labels=[0,1]).ravel()
    N  = tn+fp+fn+tp
    return dict(model=name,dataset=ds,
                Precision=round(p,6),Recall=round(r,6),
                F1=round(f,6),PR_AUC=round(a,6),
                FAR=round(fp/(fp+tn) if fp+tn>0 else 0,6),
                Alert_Rate=round((tp+fp)/N if N>0 else 0,5),
                TN=int(tn),FP=int(fp),FN=int(fn),TP=int(tp))

def add_noise(X, sigma, seed=42):
    return np.clip(X + np.random.RandomState(seed).normal(0,sigma,X.shape),0,1)

def safe_float(v):
    if isinstance(v,(np.floating,np.integer)): return float(v)
    if isinstance(v,np.ndarray): return v.tolist()
    return v

def save_results():
    """Save RESULTS to disk immediately after every run."""
    out = {}
    for k,v in RESULTS.items():
        out[k] = {
            'config':v['config'],'dataset':v['dataset'],
            'S0': {m:{kk:safe_float(vv) for kk,vv in r.items()
                      if kk!='shap_values'} for m,r in v['S0'].items()},
            'S2': {str(s):{m:{kk:safe_float(vv) for kk,vv in r.items()
                              if kk!='shap_values'} for m,r in sv.items()}
                   for s,sv in v.get('S2',{}).items()},
            'FSS': v.get('FSS',{}),
        }
    with open('results/all_results_complete.json','w') as f:
        json.dump(out,f,indent=2,default=str)

print("✅ Helpers ready")

