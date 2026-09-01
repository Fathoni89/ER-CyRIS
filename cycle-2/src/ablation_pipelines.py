"""M0–M4 preprocessing/augmentation classes extracted from ER-CyRIS Cycle 2.

Source lineage: ER_CyRIS_Siklus2_v4_FINAL_fixed.ipynb (Step 4).
M0–M4 are experimental ablation configurations; they should not be confused
with the conceptual M1–M7 architecture used elsewhere in the dissertation.
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.ensemble import IsolationForest
from imblearn.over_sampling import BorderlineSMOTE

CFG = {
    'K_SMOTE': 5,
    'CONTAM': 0.1,
}

# ── M0: Baseline (replicate Cycle 1) ────────────────────────────────
class M0:
    name='M0'
    def __init__(self): self.med=None; self.sc=MinMaxScaler()
    def fit(self,X):
        X=np.where(np.isfinite(X),X,np.nan)
        self.med=np.nanmedian(X,0)
        self.sc.fit(np.where(np.isnan(X),self.med,X)); return self
    def tr(self,X):
        X=np.where(np.isfinite(X),X,np.nan)
        return self.sc.transform(np.where(np.isnan(X),self.med,X))
    def fit_tr(self,X): return self.fit(X).tr(X)

# ── M1: + Dual-View (P1) ────────────────────────────────────────────
class M1(M0):
    name='M1'
    # For structured public datasets, P1 impact shows through the IDF
    # weighting applied in M2. M1 here documents the SV/CDV split.
    pass

# ── M2: + Dynamic Token Encoding (P2) ───────────────────────────────
class M2(M1):
    name='M2'
    def __init__(self): super().__init__(); self.idf=None; self.mu=None; self.sd=None
    def fit(self,X):
        super().fit(X); Xs=super().tr(X)
        v=np.var(Xs,0)+1e-9
        self.idf=np.log(1/v+1); self.idf/=(self.idf.max()+1e-9)
        self.mu=Xs.mean(0); self.sd=Xs.std(0)+1e-9; return self
    def tr(self,X):
        Xb=super().tr(X)
        dev=np.clip(np.abs(Xb-self.mu)/self.sd,0,5)/5
        return np.hstack([Xb*(1+0.3*self.idf), dev[:,:min(5,dev.shape[1])]])
    def fit_tr(self,X): return self.fit(X).tr(X)

# ── M3: + TOS-KNN + IF augmentation (P2+P3) ─────────────────────────
class M3(M2):
    name='M3'
    def __init__(self):
        super().__init__()
        self.knn=NearestNeighbors(n_neighbors=11,n_jobs=-1)
        self.knn_mn=0; self.knn_mx=1
        self.ifo=IsolationForest(contamination=CFG['CONTAM'],random_state=42,n_jobs=-1)
        self.if_mn=0; self.if_mx=1
    def fit(self,X):
        super().fit(X); Xa=super().tr(X)
        self.knn.fit(Xa)
        d,_=self.knn.kneighbors(Xa); av=d[:,1:].mean(1)
        self.knn_mn=float(av.min()); self.knn_mx=float(av.max())+1e-9
        self.ifo.fit(Xa)
        r=-self.ifo.score_samples(Xa)
        self.if_mn=float(r.min()); self.if_mx=float(r.max())+1e-9
        return self
    def tr(self,X):
        Xa=super().tr(X)
        d,_=self.knn.kneighbors(Xa)
        knn=np.clip((d[:,1:].mean(1)-self.knn_mn)/(self.knn_mx-self.knn_mn),0,1)
        r=-self.ifo.score_samples(Xa)
        ifs=np.clip((r-self.if_mn)/(self.if_mx-self.if_mn),0,1)
        ifl=(self.ifo.predict(Xa)==-1).astype(float)
        return np.hstack([Xa,knn[:,None],ifs[:,None],ifl[:,None]])
    def fit_tr(self,X): return self.fit(X).tr(X)

# ── M4: + BorderlineSMOTE + rescale (Full Pipeline) ──────────────────
class M4(M3):
    name='M4'
    def __init__(self): super().__init__(); self.sc2=MinMaxScaler()
    def fit_smote(self,X,y):
        self.fit(X); Xa=self.tr(X)
        mn=int(sum(y==1)); k=min(CFG['K_SMOTE'],mn-1) if mn>1 else 1
        if mn>=2 and k>=1:
            try:
                Xa,y=BorderlineSMOTE(k_neighbors=k,random_state=42).fit_resample(Xa,y)
                print(f"     SMOTE {X.shape[0]}→{len(Xa)}")
            except Exception as e: print(f"     SMOTE skip: {e}")
        self.sc2.fit(Xa); return self.sc2.transform(Xa), y
    def tr(self,X):
        Xa=super().tr(X)
        try: return self.sc2.transform(Xa)
        except: return Xa
    def fit_tr(self,X): return self.fit(X).tr(X)

PIPES={'M0':M0,'M1':M1,'M2':M2,'M3':M3,'M4':M4}

PIPES={'M0':M0,'M1':M1,'M2':M2,'M3':M3,'M4':M4}
