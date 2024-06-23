import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing

data = pd.read_csv(r"C:\Users\akinola\Documents\python DATA SCIENCE FILES\datasets\iris_dataset.csv")

#clustring based on sepal shape
x = data[data.columns[data.columns.str.contains('sepal')]]

# getting clusters
kmeans = KMeans(2)
kmeans.fit(x)

id = kmeans.fit_predict(x)

clust=x.copy()
clust['id']=id
plt.scatter(clust['sepal_length'],clust['sepal_width'],c=clust['id'],cmap='rainbow')

# data is inequally wieghted and as such i will standardize and re-cluster below
x_scaled = preprocessing.scale(x)

#using the elbow method to determine the optimal number of clusters
wcss = []
for i in range(1,10):
    kmeans = KMeans(i)
    kmeans.fit(x_scaled)
    inert = kmeans.inertia_
    wcss.append(inert)
kdata = list(range(1,10))

plt.figure()
plt.plot(kdata,wcss)

kmeans_new = KMeans(3)
kmeans_new.fit(x_scaled)
new_id = kmeans_new.fit_predict(x_scaled)
cluster =x.copy()
cluster['id']=new_id
print(cluster.head())
plt.figure()
plt.scatter(cluster['sepal_length'],cluster['sepal_width'],c=cluster['id'],cmap='rainbow')
plt.xlabel("sepal length")
plt.ylabel("sepal width")
