f=open("data_gold.txt",'r+',encoding='utf-8')
s1=f.read()
f1=open("pos_new.txt",'r+',encoding='utf-8')
s2=list(map(str,f1.read().split('\n')))
f3=open("data_gan_nhan.txt",'w+',encoding='utf-8')
for i in range(len(s2)):
    s2[i]=list(map(str,s2[i].split(' ')))
tmp=""
for i in range(len(s1)):
    if (s1[i]==' ' or s1[i]=='\n'):
        for j in s2:
            if (j[0]==tmp):
                f3.write("{}/{}{}".format(tmp,j[1],s1[i]))
                break
        tmp=""
    else:
        tmp=tmp+s1[i]
f.close()
f1.close()
f3.close()