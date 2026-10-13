import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
rng=np.random.default_rng(7)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"; RED="#c92a2a"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
def hr(h,m): return h+m/60
S,E,R=hr(8,0),hr(16,0),5; W=E-S; mid=S+W/2; RT=W/R
def clock(x,_=None):
    x=x%24; h=int(x); m=int(round((x-h)*60)); 
    if m==60: h,m=h+1,0
    return f"{h:02d}:{m:02d}"
def Pi(midpt): z=R*((midpt-S)/W-.5); return np.exp(-z*z/2)
def Lam(mins,clamp=True): v=np.minimum(1,(np.asarray(mins)-3)/15); return np.maximum(0,v) if clamp else v
lay=[("08:26–08:49",hr(8,26),hr(8,49)),("11:53–12:04",hr(11,53),hr(12,4)),("12:51–13:04",hr(12,51),hr(13,4))]
cols=[ORANGE,GREEN,BLUE]
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white"); plt.close(fig)

# 1 Length factor
fig,ax=plt.subplots(figsize=(8,4.2))
m=np.linspace(0,25,501); ax.plot(m,Lam(m),color=BLUE,lw=2.6)
ax.axvspan(0,3,color=GREY,alpha=.15); ax.text(1.5,.55,"3 min\nloading\nbefore\ndeparture",ha="center",va="center",fontsize=9,color=GREY)
ax.axvline(18,color=GREY,ls=":",lw=1)
ax.annotate("Full value at 18 min\n(15 minutes of rest\nplus 3 of loading)",xy=(18,1),xytext=(18.6,.62),fontsize=9.5,arrowprops=dict(arrowstyle="->",color=INK))
for mm,c,lab,off in [(11,GREEN,"11 min",(8,-16)),(13,BLUE,"13 min",(8,-16)),(23,ORANGE,"23 min",(-30,-22))]:
    ax.plot(mm,Lam(mm),"o",color=c,ms=8,zorder=5); ax.annotate(f"{lab}: Λ = {float(Lam(mm)):.3f}",xy=(mm,Lam(mm)),xytext=off,textcoords="offset points",fontsize=9.5,color=c)
ax.set_xlim(0,25); ax.set_ylim(-.03,1.12); ax.set_xlabel("Layover length (minutes)"); ax.set_ylabel("Length factor Λ")
ax.set_title("Length Factor:  Λ = (minutes − 3) ÷ 15, between 0 and 1",loc="left"); save(fig,"length_factor")

# 2 Placement factor over the shift
fig,ax=plt.subplots(figsize=(9,4.4))
t=np.linspace(S,E,600); ax.plot(t,Pi(t),color=BLUE,lw=2.6)
for k,a in [(1,.12),(2,.06)]: ax.axvspan(mid-k*RT,mid+k*RT,color=BLUE,alpha=a,lw=0)
ax.axvline(mid,color=INK,ls="--",lw=1); ax.text(mid,1.07,"Mid-shift 12:00",ha="center",fontsize=9.5)
ax.text(mid+RT/2,.04,"±1 round trip",ha="center",fontsize=9,color=BLUE); ax.text(mid+1.5*RT,.04,"±2",ha="center",fontsize=9,color=BLUE)
for (lab,a,b),c in zip(lay,cols):
    mp=(a+b)/2; ax.plot(mp,Pi(mp),"o",color=c,ms=9,zorder=5)
    off={0:(10,8),1:(-150,-38),2:(12,2)}[cols.index(c)]
    ax.annotate(f"{lab}\nz = {R*((mp-S)/W-.5):+.2f},  Π = {Pi(mp):.3f}",xy=(mp,Pi(mp)),xytext=off,textcoords="offset points",fontsize=9,color=c,bbox=dict(fc="white",ec="none",alpha=.85,pad=1))
ax.set_xlim(S,E); ax.set_ylim(0,1.15); ticks=np.arange(9,16); ax.set_xticks([S,*ticks,E])
ax.xaxis.set_major_formatter(FuncFormatter(clock)); ax.set_xlabel(f"Layover midpoint (shift {clock(S)}–{clock(E)}, {R} round trips of {RT*60:.0f} min)")
ax.set_ylabel("Placement factor Π"); ax.set_title("Placement Factor:  Π = e^(−z²/2),  z = R × (M ÷ W − 0.5)",loc="left"); save(fig,"placement_factor")

# 3 Index map
fig,ax=plt.subplots(figsize=(9,5))
mp=np.linspace(S,E,400); mins=np.linspace(0,26,300); MP,MN=np.meshgrid(mp,mins); G=Lam(MN)*Pi(MP)*100
cf=ax.contourf(MP,MN,G,levels=np.arange(0,101,10),cmap="Blues"); cs=ax.contour(MP,MN,G,levels=[10,25,50,75,90],colors=INK,linewidths=.7)
lv=[10,25,50,75,90]; ax.clabel(cs,fmt="%d",fontsize=8.5,manual=[(S+W*(.5-np.sqrt(-2*np.log(l/100))/R),24.5) for l in lv]); cb=fig.colorbar(cf,ax=ax,pad=.02); cb.set_label("Gainfulness index Γ (%)")
for (lab,a,b),c in zip(lay,cols):
    p=(a+b)/2; u=(b-a)*60; g=float(Lam(u)*Pi(p)*100)
    off={0:(28,-48),1:(-110,-52),2:(40,-48)}[cols.index(c)]
    ax.plot(p,u,"o",color=c,mec="white",mew=1.5,ms=11,zorder=6); ax.annotate(f"{lab}\nΓ = {g:.1f}",xy=(p,u),xytext=off,textcoords="offset points",fontsize=9.5,color=INK,fontweight="bold",bbox=dict(fc="white",ec=c,alpha=.95,pad=2.5,boxstyle="round"),arrowprops=dict(arrowstyle="-",color=c,lw=1.2,shrinkB=6),zorder=5)
ax.axhline(3,color=GREY,ls=":",lw=1); ax.text(S+.05,3.4,"3 min",fontsize=8.5,color=INK)
ax.set_xlim(S,E); ax.set_ylim(0,26); ax.set_xticks([S,*ticks,E]); ax.xaxis.set_major_formatter(FuncFormatter(clock))
ax.grid(False); ax.set_xlabel("Layover midpoint"); ax.set_ylabel("Layover length (minutes)")
ax.set_title("Layover Gainfulness Index:  Γ = Λ × Π × 100",loc="left"); save(fig,"gainfulness_map")

# 4 Lateness model
n,Sx,Sy,Sxy=200,292,100,-176.5; P=(n-Sy)/n; mu=(Sx-Sxy)/(n-Sy); Fm=Sxy/Sy; sc=mu/2
fig,ax=plt.subplots(figsize=(8.5,4.3))
x=np.linspace(0,20,500); dens=P*x/sc**2*np.exp(-x/sc); ax.fill_between(x,dens,color=ORANGE,alpha=.25); ax.plot(x,dens,color=ORANGE,lw=2.4)
Sx2=3939; varN=(Sx2-(n-Sy)*1.5*mu**2)/Sy-Fm**2; sdN=varN**.5; kN=(Fm/sdN)**2; thN=sdN**2/abs(Fm)
from math import gamma as Gf
xe=np.linspace(-12,-0.1,400); de=(1-P)*(-xe)**(kN-1)*np.exp(xe/thN)/(Gf(kN)*thN**kN)
ax.fill_between(xe,de,color=GREEN,alpha=.25); ax.plot(xe,de,color=GREEN,lw=2.4)
ax.axvline(Fm,color=GREEN,ls="--",lw=1.6)
ax.annotate(f"On time or early: {1-P:.0%} of days,\nestimated spread from Σx²\n(SD ≈ {sdN:.1f} min)",xy=(-3.6,(1-P)*3.6**(kN-1)*np.exp(-3.6/thN)/(Gf(kN)*thN**kN)),xytext=(-11.7,.24),fontsize=9.5,color=GREEN,arrowprops=dict(arrowstyle="->",color=GREEN))
ax.annotate(f"The simulation uses their\naverage, F = −1.77 min,\nfor every non-late day",xy=(Fm,.14),xytext=(-11.7,.13),fontsize=9.5,color=GREEN,fontweight="bold",arrowprops=dict(arrowstyle="->",color=GREEN))
ax.axvline(mu,color=ORANGE,ls="--",lw=1); ax.annotate(f"Late: {P:.0%} of days\ngamma, shape 2, mean μ = 4.69 min\nℓ = −(μ ÷ 2) × ln(r₁ × r₂)",xy=(mu,P*mu/sc**2*np.exp(-mu/sc)),xytext=(8.2,.075),fontsize=9.5,color=ORANGE,arrowprops=dict(arrowstyle="->",color=ORANGE))
ax.axvline(0,color=INK,lw=.8); ax.set_xlim(-12,20); ax.set_ylim(0,.32)
ax.set_xlabel("Arrival deviation (minutes; negative = early)"); ax.set_ylabel("Probability density")
ax.set_title("Lateness Model, from n = 200, Σx = 292, Σy = 100, Σxy = −176.5",loc="left"); save(fig,"lateness_model")

# 5 Simulated layover distribution, 17:19
A,B=hr(12,51),hr(13,4); U=B-A; T=A-S; N=200000
late=rng.random(N)<P; l=np.where(late,-(sc/60)*np.log(rng.random(N)*rng.random(N)),Fm/60)
u=np.maximum(0,U-l)*60; z=R*((T+(U+l/1)/2)/W-.5); g=Lam(u)*np.exp(-z*z/2)*100
fig,ax=plt.subplots(figsize=(8.5,4.3))
ax.hist(u[late],bins=np.arange(0,16.01,.5),color=ORANGE,alpha=.8,label="Late arrivals",weights=np.ones(late.sum())/N*100)
ax.bar(13-Fm,(~late).mean()*100,width=.45,color=GREEN,label="Not late",align="center")
ax.text(15.25,5.0,f"Not late: {(~late).mean():.0%} of days,\nall at {13-Fm:.1f} min using\nthe average F (bar off scale)",fontsize=9,color=GREEN)
ax.axvspan(0,3,color=RED,alpha=.08); ax.text(1.5,4.4,f"Not usable\n≤ 3 min\n{(u<=3).mean():.1%} of days",ha="center",fontsize=9.5,color=RED)
ax.axvline(13,color=INK,ls="--",lw=1); ax.text(13.15,4.0,"Scheduled\n13 min",fontsize=9)
ax.axvline(u.mean(),color=BLUE,lw=1.5); ax.text(u.mean()-.15,5.2,f"Average\n{u.mean():.1f} min",ha="right",fontsize=9,color=BLUE,bbox=dict(fc="white",ec="none",pad=1))
ax.set_xlim(0,19.5); ax.set_ylim(0,6); ax.set_xlabel("Actual layover received (minutes)"); ax.set_ylabel("Share of days per ½ minute (%)")
ax.legend(loc="upper left",bbox_to_anchor=(.22,1),frameon=False); ax.set_title("Simulated Layover, 12:51–13:04 (200,000 days)",loc="left"); save(fig,"simulated_layover")

# 6 Convergence
fig,ax=plt.subplots(figsize=(8.5,4.3)); Nmax=10000
for s,c in zip(range(5),[BLUE,"#5b8def","#93b4f5","#2c4f9e","#7aa2f7"]):
    r=np.random.default_rng(100+s); lt=r.random(Nmax)<P; ll=np.where(lt,-(sc/60)*np.log(r.random(Nmax)*r.random(Nmax)),Fm/60)
    uu=np.maximum(0,U-ll)*60; zz=R*((T+(U+ll)/2)/W-.5); gg=Lam(uu)*np.exp(-zz*zz/2)*100
    ax.plot(np.arange(1,Nmax+1),np.cumsum(gg)/np.arange(1,Nmax+1),color=c,lw=1.3,alpha=.9)
paper=float(Lam(13)*Pi(A+U/2)*100); exp_=g.mean()
ax.axhline(paper,color=ORANGE,ls="--",lw=1.6); ax.text(9500,paper+.8,f"Paper score {paper:.1f}",color=ORANGE,fontsize=9.5,ha="right")
ax.axhline(exp_,color=INK,ls=":",lw=1.2); ax.text(9500,exp_-2.4,f"Expected score ≈ {exp_:.1f}",fontsize=9.5,ha="right")
ax.annotate("",xy=(1500,exp_),xytext=(1500,paper),arrowprops=dict(arrowstyle="<->",color=RED)); ax.text(1650,(paper+exp_)/2,f"Deficit ≈ {paper-exp_:.1f}",color=RED,fontsize=9.5,va="center")
ax.set_xscale("log"); ax.set_xlim(10,Nmax); ax.set_ylim(30,70); ax.set_xlabel("Simulated days N (log scale)"); ax.set_ylabel("Running average score (%)")
ax.set_title("Monte Carlo Convergence, five runs of 10,000 days",loc="left"); save(fig,"convergence")
print(paper,exp_,u.mean(),(u<=3).mean(),(g>0).mean())
