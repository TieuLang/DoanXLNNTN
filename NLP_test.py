from vncorenlp import VnCoreNLP
from pyvi import ViTokenizer,ViPosTagger

client = VnCoreNLP(address="http://127.0.0.1", port=9001)
def tach_tu():
    file=open("test.txt","r",encoding="utf-8")
    st=file.readlines()
    out=list([])

    for i in range(len(st)):
        tmp1=""
        for j in range(len(st[i])):
            if (st[i][j]!='_'):
                tmp1+=st[i][j]
            else:
                tmp1+=' '
        s=client.tokenize(tmp1)
        tmp2=""
        for j in range(len(s[0])-1):
            tmp2+=s[0][j]+' '
        tmp2+=s[0][len(s[0])-1]
        out.append(tmp2)

    tp=0
    fp=0
    fn=0

    for i in range(len(out)):
        for j in range(len(out[i])):
            if (out[i][j] == '_'):
                if (st[i][j] == '_'):
                    tp += 1
                fp += 1
            if (st[i][j] == '_'):
                fn += 1
    precision=float(tp/fp)
    recal=float(tp/fn)
    f1_score=float(2*precision*recal/(precision+recal))
    print("Precision: "+str(precision))
    print("Recall: "+str(recal))
    print("F1-score cua tach tu cua VNCoreNLP: "+str(f1_score))
    file.close()

tach_tu()
def pos():
    file=open("test_gan_nhan.txt","r",encoding="utf-8")
    st=file.readlines()
    for i in range(len(st)):
        st[i]=list(map(str,st[i].split()))
        for j in range(len(st[i])):
            st[i][j]=list(map(str,st[i][j].split('/')))
    s1=list([])
    kq=list([])

    for i in range(len(st)):
        tmp=""
        for j in range(len(st[i])):
            tmp2=list(map(str,st[i][j][0].split('_')))
            for k in range(len(tmp2)):
                tmp=tmp+tmp2[k]+' '
        s1.append(tmp)
        s = client.pos_tag(s1[i])
        kq.append(list([]))
        for j in range(len(s[0])):
            kq[i].append(list([s[0][j][0],s[0][j][1]]))

    H=0
    T=0
    for i in range(len(st)):
        for j in range(len(kq[i])):
            if (kq[i][j][1]!="CH"):
                kq[i][j][1]=kq[i][j][1][0]
        #print(kq[i])
        #print(st[i])
        for j in range(len(kq[i])):
            T+=1
            if (j<len(st[i]) and st[i][j][1]==kq[i][j][1]):
                H+=1
    print("Do chinh xac cua gan nhan tu loai cua VNCoreNLP la: " + str(float(H) / float(T)))

pos()

def tach_tu_pyvi():
    file=open("test.txt","r",encoding="utf-8")
    st=file.readlines()
    out=list([])

    for i in range(len(st)):
        tmp1=""
        for j in range(len(st[i])):
            if (st[i][j]!='_'):
                tmp1+=st[i][j]
            else:
                tmp1+=' '
        s=ViTokenizer.tokenize(tmp1)
        s=s.replace("count - back","count-back")
        out.append(s)

    tp=0
    fp=0
    fn=0

    for i in range(len(out)):
        for j in range(len(out[i])):
            if (out[i][j] == '_'):
                if (st[i][j] == '_'):
                    tp += 1
                fp += 1
            if (st[i][j] == '_'):
                fn += 1
    precision=float(tp/fp)
    recal=float(tp/fn)
    f1_score=float(2*precision*recal/(precision+recal))
    print("Precision: "+str(precision))
    print("Recall: "+str(recal))
    print("F1-score cua tach tu cua Pyvi: "+str(f1_score))
    file.close()

tach_tu_pyvi()

def pos_pyvi():
    file=open("test_gan_nhan.txt","r",encoding="utf-8")
    st=file.readlines()
    for i in range(len(st)):
        st[i]=list(map(str,st[i].split()))
        for j in range(len(st[i])):
            st[i][j]=list(map(str,st[i][j].split('/')))
    s1=list([])
    kq=list([])

    for i in range(len(st)):
        tmp=""
        for j in range(len(st[i])):
            tmp=tmp+st[i][j][0]+' '
        s1.append(tmp)
        s = ViPosTagger.postagging(tmp)
        kq.append(list([]))
        for j in range(len(s[0])):
            kq[i].append(list([s[0][j],s[1][j]]))

    H=0
    T=0
    for i in range(len(st)):
        for j in range(len(kq[i])):
            if (kq[i][j][1]!="CH"):
                kq[i][j][1]=kq[i][j][1][0]
            if (kq[i][j][1]=="F"):
                kq[i][j][1]="CH"

        for j in range(len(kq[i])):
            T+=1
            if (j<len(st[i]) and st[i][j][1]==kq[i][j][1]):
                H+=1
    print("Do chinh xac cua gan nhan tu loai cua Pyvi la: " + str(float(H) / float(T)))

pos_pyvi()
