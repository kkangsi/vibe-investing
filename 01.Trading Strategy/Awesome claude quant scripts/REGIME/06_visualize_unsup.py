"""06_visualize_unsup.py — 비지도 레짐 + 베타 + 총수익 vs 잔차알파 레짐의존"""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import matplotlib, statsmodels.api as sm
from scipy import stats
matplotlib.rcParams["axes.unicode_minus"]=False

df=pd.read_csv("/home/claude/market_data_2020_2026.csv",parse_dates=["Date"],index_col="Date")
reg=pd.read_csv("/home/claude/out_unsup_regime.csv",parse_dates=["Date"],index_col="Date")
betas=pd.read_csv("/home/claude/out_betas.csv",index_col=0).iloc[:,0]
alpha=pd.read_csv("/home/claude/out_residual_alpha.csv")

M7=["AAPL","MSFT","GOOGL","AMZN","META","NVDA","TSLA"]
INFRA=["AVGO","AMD","TSM","ASML","MU","VRT","ETN","SMCI","DLR","GEV"]
STOCKS=M7+INFRA

# 잔차/총수익 레짐 의존 p값 재계산
rets=np.log(df[["QQQ"]+STOCKS]).diff().dropna()
mkt=sm.add_constant(rets["QQQ"]); resid=pd.DataFrame(index=rets.index)
for s in STOCKS: resid[s]=sm.OLS(rets[s],mkt).fit().resid
hmm=reg["hmm"].reindex(rets.index).ffill(); states=sorted(hmm.dropna().unique())
praw,pres=[],[]
for s in STOCKS:
    g1=[rets[s][hmm==st].dropna().values for st in states]
    g2=[resid[s][hmm==st].dropna().values for st in states]
    praw.append(stats.kruskal(*[g for g in g1 if len(g)>20])[1])
    pres.append(stats.kruskal(*[g for g in g2 if len(g)>20])[1])

fig=plt.figure(figsize=(15,10))

# (1) HMM 레짐 타임라인 + CPI
ax1=plt.subplot2grid((2,2),(0,0),colspan=2)
cmap=plt.cm.Set2
hmm_full=reg["hmm"]
prev=None;start=None
for d,r in hmm_full.items():
    if r!=prev:
        if prev is not None: ax1.axvspan(start,d,color=cmap(int(prev)),alpha=0.3)
        start=d;prev=r
ax1.axvspan(start,hmm_full.index[-1],color=cmap(int(prev)),alpha=0.3)
ax1b=ax1.twinx()
ax1b.plot(df.index,df["CPI_YoY"],color="black",lw=1.4,label="CPI YoY%")
ax1b.plot(df.index,df["UST10Y"],color="#c0392b",lw=1,ls="--",label="UST10Y%")
ax1b.legend(fontsize=8,loc="upper right")
ax1.set_title("HMM Unsupervised Regimes (background) — auto-detected high-inflation regime",fontsize=11)
ax1.set_yticks([])

# (2) QQQ 베타
ax2=plt.subplot2grid((2,2),(1,0))
b=betas.sort_values()
colors=["#2980b9" if x in M7 else "#16a085" for x in b.index]
ax2.barh(b.index,b.values,color=colors)
ax2.axvline(1.0,color="red",ls="--",lw=1,label="beta=1")
ax2.set_xlabel("QQQ Beta (market sensitivity)")
ax2.set_title("Market Beta: SMCI/NVDA/TSLA move ~1.6-1.8x market",fontsize=10)
ax2.tick_params(labelsize=8);ax2.legend(fontsize=8)

# (3) 총수익 vs 잔차알파 레짐 의존 p값
ax3=plt.subplot2grid((2,2),(1,1))
y=np.arange(len(STOCKS))
ax3.scatter(praw,y,color="#e67e22",label="Total return",s=40,zorder=3)
ax3.scatter(pres,y,color="#2980b9",label="Residual alpha (mkt removed)",s=40,zorder=3)
for i in range(len(STOCKS)): ax3.plot([praw[i],pres[i]],[i,i],color="gray",lw=0.6,zorder=1)
ax3.axvline(0.05,color="red",ls="--",lw=1,label="p=0.05")
ax3.set_yticks(y);ax3.set_yticklabels(STOCKS,fontsize=8)
ax3.set_xlabel("Kruskal-Wallis p-value (regime dependence)")
ax3.set_title("Removing market kills regime dependence\n(3/17 -> 1/17 significant)",fontsize=10)
ax3.legend(fontsize=7,loc="lower right")

plt.tight_layout()
plt.savefig("/home/claude/unsup_dashboard.png",dpi=130,bbox_inches="tight")
print("saved unsup_dashboard.png")
