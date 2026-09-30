import json
from collections import defaultdict, Counter

B=json.load(open('perminov/schemes/results/serendipitous_base/2x4x13_m84_0037b2c7b93d071f204f0ae5ea31f9c937bb1b53_ZT.json'))
L={
1:json.load(open('perminov/schemes/known/alpha_tensor/2x3x4_m20_ZT.json')),
2:json.load(open('perminov/schemes/known/alpha_tensor/3x4x4_m38_Z.json')),
3:json.load(open('perminov/schemes/results/ZT/3x4x6_m54_ZT.json')),
4:json.load(open('perminov/schemes/results/ZT/3x4x8_m73_ZT.json')),
}
L[1]['u'],L[1]['v'],L[1]['w']=L[1]['v'],L[1]['w'],L[1]['u']
L[1]['n']=[3,4,2]
g=defaultdict(list)
for idx,u in enumerate(B['u']):g[tuple(u)].append(idx)
assert Counter(map(len,g.values()))==Counter({1:3,2:2,3:19,4:5})
terms=[]
for ids in g.values():
    k=len(ids); leaf=L[k]
    for u,v,w in zip(leaf['u'],leaf['v'],leaf['w']):
        U={}
        for ao,bo in enumerate(B['u'][ids[0]]):
            if not bo:continue
            ib,jb=divmod(ao,4)
            for ai,li in enumerate(u):
                if li:
                    ii,ji=divmod(ai,4)
                    U[(ib*3+ii)*16+jb*4+ji]=bo*li
        V={}
        for bo in range(4*13):
            jb,kb=divmod(bo,13)
            for js in range(4):
                for ks in range(2):
                    val=sum(B['v'][bid][bo]*v[js*(2*k)+t*2+ks] for t,bid in enumerate(ids))
                    if val:V[(jb*4+js)*26+kb*2+ks]=val
        W={}
        for co in range(13*2):
            kb,ib=divmod(co,2)
            for ks in range(2):
                for ii in range(3):
                    val=sum(B['w'][bid][co]*w[(t*2+ks)*3+ii] for t,bid in enumerate(ids))
                    if val:W[(kb*2+ks)*6+ib*3+ii]=val
        terms.append((U,V,W))
assert len(terms)==1527
print('terms',len(terms),'nonzeros',tuple(sum(len(t[i]) for t in terms) for i in range(3)),
      'operations',sum(len(u)*len(v)*len(w) for u,v,w in terms))

def verify_full():
    by_a=[[] for _ in range(96)]
    for U,V,W in terms:
        vw=[(b,c,v*w) for b,v in V.items() for c,w in W.items()]
        for a,u in U.items():by_a[a].append((u,vw))
    for a,layer in enumerate(by_a):
        got=defaultdict(int)
        for u,vw in layer:
            for b,c,x in vw:got[b,c]+=u*x
        got={bc:x for bc,x in got.items() if x}
        row,col=divmod(a,16)
        want={(col*26+k,k*6+row):1 for k in range(26)}
        assert got==want,(a,len(got),len(want),next(iter((got.items())),None))
    print('full 6x16x26 Brent tensor: OK')

if __name__=='__main__':verify_full()
