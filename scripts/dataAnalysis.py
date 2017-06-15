import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import sys

names = []
vgMq = {}
score = {}
vglrMq = {}
correct = {}
for line in sys.stdin:
    splitList = line.rstrip().split('\t')
    if len(splitList)<4:
        print(splitList)
        continue
    names.append(splitList[0])
    vgMq[splitList[0]] = splitList[1]
    score[splitList[0]] = splitList[2]
    #vglrMq[splitList[0]] = splitList[3]
    #if len(splitList)>3:
    correct[splitList[0]] = splitList[3]

print(len(names))

fig1 = plt.figure(2, figsize=(16, 12))
count = 0
x = []
y = []
x2 = []
y2 = []
gb = []
correctly_mapped_value = 0
incorrectly_mapped_value = 0
total = 0
mqDc = {key: 0 for key in range(0,61)}

for key in names:
    #y.append(int(correct[key]))
    mqDc[int(vgMq[key])]+=1
print("Plotting Now")
#plt.scatter(x,y,alpha=0.3,color=gb)
#n, bins, patches = plt.hist(y, 10, normed=1, facecolor='green', alpha=0.5)
#n, bins, patches = plt.hist(y, 2, facecolor='red', alpha=0.5)
#print("Plot ended")
total = sum(mqDc.values())
performance = [mqDc[key]/total for key in mqDc.keys()]
objects = [str(i)+"("+str(round(mqDc[i]*100/total,2))+"%)" for i in range(0,61)]

y_pos = np.arange(len(objects))

plt.bar(y_pos, performance, align='center', alpha=0.5, color='blue')
plt.xticks(y_pos, objects, rotation='vertical')
plt.ylabel('Frequency')
plt.title('Frequency of mapping qualities in curated training set')

#plt.xlabel('Mapping Quality-VG')
#plt.ylabel('Frequency')

plt.savefig('analysis.png')
