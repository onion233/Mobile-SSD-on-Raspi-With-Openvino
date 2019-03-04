# used for creat_list.sh
import random, os, sys

totalNum=int(sys.argv[1])
percent=float(sys.argv[2])
outpath=sys.argv[3]

test_id=random.sample(range(totalNum),int(percent*totalNum))
test=open(outpath+'/text.txt','w')
train=open(outpath+'/trainval.txt','w+')
for i in range(totalNum):
    if i in test_id:
        test.write(str(i)+'\n')
    else:
        train.write(str(i)+'\n')
test.close()
train.close()