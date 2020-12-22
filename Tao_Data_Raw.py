f=open("new.txt",'r+',encoding="utf-8")
f1=open("data_raw.txt",'w+',encoding="utf-8")
c=f.read()
for i in c:
    if (i=='_'):
        f1.write(' ')
    else:
        f1.write(i)
f.close()
f1.close()

