import os,sys,json,urllib.request
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit(1)
O=99;V=[0,100,320,330,500,900,20000];D={2:[-21,-19,-12,-8,8,12,19,21],3:[-11,-9,9,11],4:[-10,-1,1,10],5:[-11,-10,-9,-1,1,9,10,11],6:[-11,-10,-9,-1,1,9,10,11]}
def S(s):return(int(s[1])+1)*10+(ord(s[0])-96)
def U(i):return chr(96+(i%10))+str((i//10)-1)
class P:
 def __init__(s):s.r()
 def r(s):
  s.b=[O]*120
  for r in range(8):
   for f in range(8):s.b[(r+2)*10+(f+1)]=0
  st=[4,2,3,5,6,3,2,4]
  for f in range(8):s.b[21+f],s.b[31+f],s.b[81+f],s.b[91+f]=st[f],1,-1,-st[f]
  s.t=1
 def f(s,fen):
  s.b=[O]*120
  for r in range(8):
   for f in range(8):s.b[(r+2)*10+(f+1)]=0
  p=fen.split();rs=p[0].split('/')
  for r,row in enumerate(rs):
   f=0
   for c in row:
    if c.isdigit():f+=int(c)
    else:
     v={'p':1,'n':2,'b':3,'r':4,'q':5,'k':6}[c.lower()]*(1 if c.isupper()else -1)
     s.b[(7-r+2)*10+(f+1)]=v;f+=1
  s.t=1 if p[1]=='w' else -1
 def d(s,f,t,p=None):
  pc,cap=s.b[f],s.b[t];s.b[t],s.b[f]=pc,0
  if p:s.b[t]={'q':5,'r':4,'b':3,'n':2}.get(p,5)*(1 if pc>0 else -1)
  s.t=-s.t;return cap
 def u(s,f,t,cap,op):s.b[f],s.b[t],s.t=op,cap,-s.t
 def g(s):
  m=[]
  for p in range(120):
   pc=s.b[p]
   if pc in(O,0)or(pc>0)!=(s.t>0):continue
   pt=abs(pc)
   if pt==1:
    st=10 if s.t>0 else -10
    if s.b[p+st]==0:
     if(s.t>0 and p+st>=91)or(s.t<0 and p+st<=28):
      for pr in'qrbn':m.append((p,p+st,pr))
     else:m.append((p,p+st,None))
     sr=(p//10)-2
     if((s.t>0 and sr==1)or(s.t<0 and sr==6))and s.b[p+2*st]==0:m.append((p,p+2*st,None))
    for cd in(st-1,st+1):
     tg=s.b[p+cd]
     if tg not in(O,0)and(tg>0)!=(s.t>0):
      if(s.t>0 and p+cd>=91)or(s.t<0 and p+cd<=28):
       for pr in'qrbn':m.append((p,p+cd,pr))
      else:m.append((p,p+cd,None))
   elif pt in(2,6):
    for d in D[pt]:
     tg=s.b[p+d]
     if tg!=O and(tg==0 or(tg>0)!=(s.t>0)):m.append((p,p+d,None))
   elif pt in(3,4,5):
    for d in D[pt]:
     dest=p+d
     while 1:
      tg=s.b[dest]
      if tg==O:break
      if tg==0:m.append((p,dest,None))
      else:
       if(tg>0)!=(s.t>0):m.append((p,dest,None))
       break
      dest+=d
  return m
 def c(s):
  kp=6 if s.t>0 else -6
  k=next((i for i in range(120)if s.b[i]==kp),-1)
  if k==-1:return 1
  s.t=-s.t;om=s.g();s.t=-s.t;return any(t==k for _,t,_ in om)
 def e(s):return sum(V[abs(p)]*(1 if p>0 else -1)for p in s.b if p not in(O,0))*s.t
 def a(s,d,a,b):
  if d==0:return s.e()
  best,leg=-99999,0
  for f,t,p in s.g():
   op,cap=s.b[f],s.d(f,t,p)
   s.t=-s.t;ilg=s.c();s.t=-s.t
   if not ilg:
    leg+=1;sc=-s.a(d-1,-b,-a);s.u(f,t,cap,op)
    if sc>=b:return b
    if sc>best:best=sc
    if sc>a:a=sc
   else:s.u(f,t,cap,op)
  return-10000 if s.c()else 0 if leg==0 else best
 def s(s,fen,leg):
  s.f(fen);bm=None;bs=-99999
  for ms in leg:
   f,t=S(ms[:2]),S(ms[2:4]);pr=ms[4]if len(ms)>4 else None
   op,cap=s.b[f],s.d(f,t,pr)
   s.t=-s.t;ilg=s.c();s.t=-s.t
   if not ilg:
    sc=-s.a(2,-99999,99999);s.u(f,t,cap,op)
    if sc>bs:bs,bm=sc,ms
   else:s.u(f,t,cap,op)
  return bm or leg[0]
def P_req(p,b):
 req=urllib.request.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 with urllib.request.urlopen(req)as r:return json.load(r)
def main():
 pos=P()
 while 1:
  g=P_req("/game",{})
  if g["status"]=="done":break
  while g["status"]=="your_move":
   m=pos.s(g["fen"],g["legal_moves"])
   g=P_req("/move",{"game":g["game"],"move":m})
if __name__=="__main__":main()
