import datetime

def macro_model(data):
    score=0
    def sc(v,a,b): return (0,'favorable') if v<a else (1,'neutral') if v<b else (2,'restrictiu')
    ry,s1=sc(data['real_yield'],0,1.5); score+=ry*2
    dxy,s2=sc(data['dxy'],100,105); score+=dxy
    vix,s3=sc(data['vix'],15,20); score+=vix
    cv,s4=sc(data['yield_curve'],0,-0.5); score+=cv
    state='RISC FAVORABLE' if score<=2 else 'TRANSICIÓ' if score<=4 else 'RISC RESTRICTIU'
    return {'date':datetime.date.today().isoformat(),'macro_state':state,'score':score,'details':{'real_yield':s1,'dxy':s2,'vix':s3,'curve':s4}}
