import csv

digs=["0","6","a","f"]
lenn = len(digs)
cols=[]

for i in range(lenn):
    for j in range(lenn):
        for k in range(lenn):
            row = []
            row.append(digs[i]+digs[j]+digs[k])
            row.append("1000.0")
            cols.append(row)

o = open("data.csv", "w", newline="")
writer = csv.writer(o)
writer.writerows(cols)
o.close()
