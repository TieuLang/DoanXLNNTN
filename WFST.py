import subprocess
from matplotlib import image, pyplot
import math
from numpy import asarray

f=open("data_gold.txt", 'r', encoding='utf-8')
c = f.read()
f.close()
tam=""

#Xay dung tu dien
dictt=list([])
sl_tu=int(0)
for i in c:
    if (i!=" " and i!='\n'):
        tam=tam+i
    else:
        sl_tu+=1
        kt=True
        for j in range(len(dictt)):
            if (dictt[j][0]==tam):
                dictt[j][1]+=1
                kt=False
                break
        if (kt):
            dictt.append([tam,1])
        tam=""
for i in range(len(dictt)):
    dictt[i][1]=-math.log(dictt[i][1]/sl_tu,2)

#Luu tu dien
dict={key:value for key, value in dictt}

def makeSymbols(dictionary):
    f = open('sym.txt', "wt", encoding='utf-8')
    i = 0
    f.write('# {}\n'.format(i))
    for word in dictionary:
        i += 1
        f.write("{} {}\n".format(word, i))
    f.close()

#Luu tu dien vao file sym.txt
makeSymbols(dict)

def Dijkstra(inp):
    f = open("tmp.txt", "r", encoding='utf-8')
    c=list(map(str,f.read().split('\n')))

    #Xay dung danh sach ke luu cac dinh do thi

    s=list([])

    #Xu ly du lieu
    for i in range(len(c)-1):
        tam=c[i].split(' ')
        s.append([int(tam[0]),int(tam[1]),float(tam[4])])
    n=int(s[len(s)-1][1])+1 #so luong dinh trong do thi

    #Khoi tao mang de luu cac gia tri can thiet
    ke=list([])
    dai=list([])
    kt = list([])
    d = list([])
    tr = list([])

    #Khoi tao mang de luu danh sach ke
    for i in range(n):
        ke.append(list([])) #Mang dung de luu cac dinh ke voi dinh i
        dai.append(list([])) #Mang dung de luu do dai tu dinh i den dinh ke no
        kt.append(True) #Mang de kiem tra dinh i da duoc duyet chua trong thuat toan dijkstra
        d.append(float(20000000000)) #Mang de luu duong di ngan nhat tu dinh dau toi dinh i
        tr.append(float(20000000000)) #Mang de luu dinh ke truoc dinh i trong duong di ngan nhat tu dinh dau toi dinh i

    #Xay dung danh sach ke
    for i in range(len(s)):
        #Luu lai cac dinh lien thong voi dinh i
        ke[s[i][0]].append(s[i][1]) #Luu dinh ke voi dinh s[i][0] la dinh s[i][1] vao mang
        dai[s[i][0]].append(s[i][2]) #Luu do dai tu dinh s[i][0] den dinh s[i][1] vao mang
        #ke[s[i][1]].append(s[i][0]) #tuong tu nhu tren
        #dai[s[i][1]].append(s[i][2])

    #Khoi tao gia tri ban dau cho thuat toan dijkstra
    dau=int(0) #Khoi tao dinh bat dau la dinh 0
    kt[dau]=False #Dinh bat dau da duoc chon de tim duong di ngan nhat
    d[dau]=0 #Do dai tu ngan nhat tu dinh bat dau den dinh dau bang 0

    #Dung thuat toan dijkstra de tim duong di ngan nhat
    while (dau!=n-1): #Neu dinh dau la dinh can tim duong di ngan nhat(dinh cuoi) thi ket thuc

        #Duyet cac dinh ke voi dinh dau
        for i in range(len(ke[dau])):
            #Neu do dai tu dinh dau den dinh ke[dau][i]
            #cong voi duong di ngan nhat tu dinh dau den dinh ke[dau][i]
            #ngan hon so voi d[ke[dau][i]](duong di ngan nhat da tim duoc)
            #thi cap nhat la gia tri duong di ngan nhat va luu tr cua dinh ke[dau][i] la dinh dau
            if (kt[ke[dau][i]] and d[ke[dau][i]]>d[dau]+dai[dau][i]):
                d[ke[dau][i]]=d[dau]+dai[dau][i] #Cap nhat lai gia tri duong di ngan nhat tu dinh dau den dinh ke[dau][i]
                tr[ke[dau][i]]=dau #Cap nhat thang dau la truoc cua thang ke[dau][i] trong duong di ngan nhat

        #tim dinh co duong di ngan nhat chua duoc chon
        dau=-1
        for i in range(n):
            if (kt[i] and (dau==-1 or d[dau]>d[i])):
                dau=i

        #Neu tat ca cac dinh da duoc chon thi ket thuc
        if (dau==-1):
            break

        kt[dau]=False #Danh dau dinh da duoc chon

    #In ket qua
    if (dau==-1):
        print("Khong tach tu duoc")
    else:
        #Truy vet ket qua
        kq=list([])
        Do_dai=d[n-1]
        dau=n-1
        kq.append(int(n-1))
        while (dau!=0):
            kq.append(int(tr[dau]))
            dau=tr[dau]
        out = ""
        vt = 0
        tmp2 = inp.split()
        for i in range(len(kq) - 1, 0, -1):
            tmp = kq[i-1]-kq[i]
            for j in range(tmp-1):
                out = out + tmp2[vt] + '_'
                vt += 1
            if (i!=1):
                out = out + tmp2[vt] + ' '
            else:
                out=out+tmp2[vt]
            vt += 1
        return out
    return ""

def WFSTSegmentation(dictionary, sent):
    words = sent.split()
    f = open("tmp.txt", "wt", encoding='utf-8')
    nwords = len(words)
    i = 0
    dai_max=float(0);
    for i in range(nwords):
        for j in range(nwords):
            if i + j >= nwords:
                break
            word = words[i]
            for k in range(1, j + 1):
                word = word + "_" + words[i + k]
            weight = dict.get(word)
            if weight == None:
                continue
            if (weight>dai_max):
                dai_max=weight
            f.write("{} {} {} {} {}\n".format(i, i + j + 1, word, word, weight))

    dai_max=dai_max*nwords
    for i in range(nwords):
        word = words[i]
        f.write("{} {} {} {} {}\n".format(i, i + 1, word, word, dai_max))
    f.close()
    return Dijkstra(sent)


#Tach tu
def Tach_Tu():
    f_raw=open("data_raw.txt",'r',encoding='utf-8')
    st_raw = f_raw.read()
    st_raw = list(map(str, st_raw.split('\n')))

    f_gold=open("data_gold.txt",'r',encoding='utf-8')
    st_gold=f_gold.read()
    st_gold = list(map(str, st_gold.split('\n')))

    f1=open("Kq_TachTu.txt",'w',encoding='utf-8')
    dem=0
    for s in range(len(st_raw)):
        if (st_raw[s]==""):
            break
        out=WFSTSegmentation(dict, st_raw[s])
        if (out==st_gold[s]):
            dem+=1
        f1.write(out+'\n')
    f1.close()

    #test
    f1=open("test.txt",'r',encoding='utf-8')
    f2=open("test_kq.txt",'w',encoding='utf-8')
    st_real=list(map(str,f1.read().split('\n')))
    st_raw=list([])
    for i in range(len(st_real)):
        tmp=""
        for j in range(len(st_real[i])):
            if (st_real[i][j]=='_'):
                tmp=tmp+" "
            else:
                tmp=tmp+st_real[i][j]
        st_raw.append(tmp)
    dem=1
    sl_tu=1
    tp=0
    fp=0
    fn=0
    for s in range(len(st_raw)):
        if (st_raw[s] == ""):
            break
        for i in range(len(st_raw[s])):
            if (st_raw[s][i]==' '):
                sl_tu+=1
        out = WFSTSegmentation(dict, st_raw[s])
        for i in range(len(out)):
            if (out[i]=='_'):
                if (st_real[s][i]=='_'):
                    tp+=1
                fp+=1
            if (st_real[s][i]=='_'):
                fn+=1
            if (out[i]==' ' and st_real[s][i]==' ') or (out[i]=='_' and st_real[s][i]=='_'):
                dem+=1
        f2.write(out+'\n')
    precision=float(tp/fp)
    recal=float(tp/fn)
    f1_score=float(2*precision*recal/(precision+recal))
    print("Precision: "+str(precision))
    print("Recall: "+str(recal))
    print("F1-score cua tach tu: "+str(f1_score))

    f1 = open("demo.txt", 'r', encoding='utf-8')
    f2 = open("test_demo.txt", 'w', encoding='utf-8')
    st_real = list(map(str, f1.read().split('\n')))
    st_raw = list([])
    for i in range(len(st_real)):
        tmp = ""
        for j in range(len(st_real[i])):
            if (st_real[i][j] == '_'):
                tmp = tmp + " "
            else:
                tmp = tmp + st_real[i][j]
        st_raw.append(tmp)
    dem = 1
    sl_tu = 1
    tp = 0
    fp = 0
    fn = 0
    for s in range(len(st_raw)):
        if (st_raw[s] == ""):
            break
        for i in range(len(st_raw[s])):
            if (st_raw[s][i] == ' '):
                sl_tu += 1
        out = WFSTSegmentation(dict, st_raw[s])
        f2.write(out + '\n')

Tach_Tu()

def build_matrix_A(data_gan_nhan,Nhan):
    matrixA = list([])

    for i in range(len(Nhan)+1):
        tmp=list([])
        for j in range(len(Nhan)+1):
            tmp.append(int(0))
        matrixA.append(tmp)

    def inc(x,y):
        x1=int(0)
        y1=int(0)
        for i in range(len(Nhan)):
            if (x==Nhan[i]):
                x1=i+1
                break
        for i in range(len(Nhan)):
            if (y==Nhan[i]):
                y1=i
                break
        matrixA[x1][y1]+=1

    for i in range(len(data_gan_nhan)):

        inc('z',data_gan_nhan[i][0][1])

        for j in range(1,len(data_gan_nhan[i])):
            inc(data_gan_nhan[i][j-1][1],data_gan_nhan[i][j][1])
    for i in range(len(matrixA)):
        tmp=int(0)
        for j in range(len(matrixA[i])-1):
            matrixA[i][j]+=1
            tmp+=matrixA[i][j]
        matrixA[i][len(matrixA[i])-1]=tmp
        for j in range(len(matrixA)-1):
            matrixA[i][j]=float(matrixA[i][j]/tmp)
    return matrixA

def build_matrix_B(Nhan,danh_sach_tu,data_gan_nhan):
    matrixB=list([])
    for i in range(len(Nhan)):
        tmp=list([])
        for j in range(len(danh_sach_tu)+2):
            tmp.append(int(0))
        matrixB.append(tmp)
    for i in range(len(data_gan_nhan)):
        for j in range(len(data_gan_nhan[i])):
            matrixB[Nhan.index(data_gan_nhan[i][j][1])][danh_sach_tu.index(data_gan_nhan[i][j][0])]+=1
    for i in range(len(matrixB)):
        for j in range(len(matrixB[i])-1):
            matrixB[i][j]+=1
            matrixB[i][len(matrixB[i])-1]+=matrixB[i][j]
        for j in range(len(matrixB[i])-1):
            matrixB[i][j]=float(matrixB[i][j]/matrixB[i][len(matrixB[i])-1])
    return matrixB

def Gan_Nhan_Tu_Loai():
    Nhan=list(["N","V","A","P","M","D","R","E","C","I","O","Z","CH","X"])
    #Nhan=list(["UN","NN","VB","PRP"])

    f = open("data_gan_nhan.txt", 'r', encoding='utf-8')
    data_gan_nhan = list(map(str, f.read().split('\n')))
    f.close()
    for i in range(len(data_gan_nhan)):
        data_gan_nhan[i] = list(map(str, data_gan_nhan[i].split()))
        for j in range(len(data_gan_nhan[i])):
            data_gan_nhan[i][j] = list(map(str, data_gan_nhan[i][j].split('/')))

    matrixA=build_matrix_A(data_gan_nhan,Nhan)

   #Tinh Matrix B
    danh_sach_tu=list([])
    for i in range(len(data_gan_nhan)):
        for j in range(len(data_gan_nhan[i])):
            if not (data_gan_nhan[i][j][0] in danh_sach_tu):
                danh_sach_tu.append(data_gan_nhan[i][j][0])

    matrixB=build_matrix_B(Nhan,danh_sach_tu,data_gan_nhan)

    f1 = open("test.txt", 'r', encoding='utf-8')
    test_gan_nhan = list(map(str, f1.read().split('\n')))
    f2=open("Kq_GanNhan.txt",'w',encoding='utf-8')

    def viterbi(test_gan_nhan):
        kq_out=str("")
        for s in test_gan_nhan:
            s1=list(map(str,s.split()))
            if (s1==[]):
                continue
            vtb=list([])
            tr=list([])
            for i in range(len(Nhan)):
                vtb.append(list([]))
                tr.append(list([]))
            for i in range(len(Nhan)):
                if (danh_sach_tu.count(s1[0])==0):
                    vtb[i].append(float(matrixA[0][i]*matrixB[i][len(matrixB[i])-2]))
                else:
                    vtb[i].append(float(matrixA[0][i]*matrixB[i][danh_sach_tu.index(s1[0])]))
                tr[i].append(int(-1))
            for j in range(1,len(s1)):
                for i in range(len(Nhan)):
                    tmp=list([])
                    for k in range(len(Nhan)):
                        if (danh_sach_tu.count(s1[j])==0):
                            tmp.append(float(vtb[k][j-1]*matrixA[k+1][i]*matrixB[i][len(matrixB[i])-2]))
                        else:
                            tmp.append(float(vtb[k][j-1]*matrixA[k+1][i]*matrixB[i][danh_sach_tu.index(s1[j])]))
                    vtb[i].append(tmp[0])
                    tr[i].append(0)
                    for k in range(1,len(tmp)):
                        if (vtb[i][j]<tmp[k]):
                            vtb[i][j]=tmp[k]
                            tr[i][j]=k
            x=int(0)
            for i in range(len(Nhan)):
                if (vtb[x][len(s1)-1]<vtb[i][len(s1)-1]):
                    x=i
            Nhan_kq=list([])
            for i in range(len(s1)):
                Nhan_kq.append(str(""))
            for i in range(len(s1)-1,-1,-1):
                Nhan_kq[i]=Nhan[x]
                x=tr[x][i]
            out = ""
            for i in range(len(s1) - 1):
                out = out + s1[i] + '/' + Nhan_kq[i] + ' '
            out = out + s1[len(s1) - 1] + '/' + Nhan_kq[len(Nhan_kq) - 1] + '\n'
            kq_out=kq_out+out
        return kq_out

    kq_out = viterbi(test_gan_nhan)
    f2.write(kq_out)
    f1.close()
    f2.close()
    f = open("kq_GanNhan.txt", 'r', encoding='utf-8')
    out_gan_nhan = list(map(str, f.read().split('\n')))
    f.close()
    for i in range(len(out_gan_nhan)):
        out_gan_nhan[i] = list(map(str, out_gan_nhan[i].split()))
        for j in range(len(out_gan_nhan[i])):
            out_gan_nhan[i][j] = list(map(str, out_gan_nhan[i][j].split('/')))

    H = 0
    T = 0
    H1 = 0
    f3 = open("test_gan_nhan.txt", "r+", encoding="utf-8")
    data_gan_nhan = list(map(str, f3.read().split('\n')))
    f.close()
    for i in range(len(data_gan_nhan)):
        data_gan_nhan[i] = list(map(str, data_gan_nhan[i].split()))
        for j in range(len(data_gan_nhan[i])):
            data_gan_nhan[i][j] = list(map(str, data_gan_nhan[i][j].split('/')))
    for i in range(len(data_gan_nhan)):
        for j in range(len(data_gan_nhan[i])):
            T += 1
            if (out_gan_nhan[i][j][1] != "X"):
                H1 += 1
            if (data_gan_nhan[i][j] == out_gan_nhan[i][j]):
                H += 1

    print("Do chinh xac cua gan nhan tu loai la: " + str(float(H) / float(T)))
    f1 = open("test_demo.txt", 'r', encoding='utf-8')
    test_gan_nhan = list(map(str, f1.read().split('\n')))
    f2 = open("test_Kq_demo.txt", 'w', encoding='utf-8')
    kq_out=viterbi(test_gan_nhan)
    f2.write(kq_out)
    f1.close()
    f2.close()

Gan_Nhan_Tu_Loai()