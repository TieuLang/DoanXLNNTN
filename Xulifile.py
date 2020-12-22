def chinh_sua_nhan():
    f=open("pos.txt",'r',encoding='utf-8')
    f1=open("pos_new.txt",'w',encoding='utf-8')

    s1=f.read()
    s1=list(map(str,s1.split('\n')))
    for i in range(len(s1)):
        s1[i]=list(map(str,s1[i].split('\t')))
    for i in range(len(s1)):
        tmp=s1[i][0]+' '
        if (s1[i][0]!=""):
            for j in s1[i][1]:
                if (j==j.upper()):
                    tmp=tmp+j
                else:
                    break
        f1.write(tmp+'\n')
    f.close()
    f1.close()
def dem_nhan():
    f=open("pos_new.txt",'r',encoding='utf-8')
    st=list(map(str,f.read().split('\n')))
    for i in range(len(st)):
        st[i]=list(map(str,st[i].split()))
    nhan=list([])
    sl=0
    for i in range(len(st)):
        if (st[i]!=[]):
            kt=True
            for j in range(len(nhan)):
                if (nhan[j]==st[i][1]):
                    kt=False
                    break
            if (kt):
                nhan.append(st[i][1])
            else:
                if (st[i][1]=='T'):
                    print(st[i])
    print(nhan)
dem_nhan()