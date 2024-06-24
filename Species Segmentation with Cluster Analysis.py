#importing relevant librairies
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing
import plotly.graph_objs as go 
from plotly.offline import iplot
import plotly.colors as pc
import chart_studio.plotly as py
import chart_studio

#setting up the credentials to my plotly chart studio account
chart_studio.tools.set_credentials_file(username='akinola', api_key='9GM9ArSm3hHaEIw5acQb')

# Loading the dataset
data = pd.read_csv(r"C:\Users\akinola\Documents\python DATA SCIENCE FILES\datasets\iris_dataset.csv")

# Clustering based on sepal shape
x = data[data.columns[data.columns.str.contains('sepal')]]

# Initial KMeans clustering
kmeans = KMeans(2, random_state=42)
kmeans.fit(x)
id = kmeans.predict(x)

clust = x.copy()
clust['id'] = id
plt.scatter(clust['sepal_length'], clust['sepal_width'], c=clust['id'], cmap='rainbow')
plt.title('Initial Clustering')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.show()

# Standardizing the data to give both metrics equal weight
x_scaled = preprocessing.scale(x)

# using the Elbow method to determine the optimal number of clusters
wcss = []
for i in range(1, 10):
    kmeans = KMeans(i, random_state=42)
    kmeans.fit(x_scaled)
    wcss.append(kmeans.inertia_)

plt.figure()
plt.plot(range(1, 10), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# Re-clustering using the optimal number of clusters
kmeans_new = KMeans(3, random_state=42)
kmeans_new.fit(x_scaled)
new_id = kmeans_new.predict(x_scaled)
cluster = x.copy()
cluster['id'] = new_id

print(cluster.head())

# making it interactive using plotly
color_scale = pc.qualitative.Plotly

#empty list to store each instance of the plots
scatter = []

#fetching unique values
unique_ids = cluster['id'].unique()

#declaring color map
color_map = {id_value: color_scale[i % len(color_scale)] for i, id_value in enumerate(unique_ids)}

# Grouping by 'id' and creating a trace for each group
for id_value, group in cluster.groupby('id'):
    scat = go.Scatter(
        x=group['sepal_length'],
        y=group['sepal_width'],
        text=group['id'],
        mode='markers',
        marker=dict(
            color=color_map[id_value]
        ),
        hoverinfo='text+x+y',
        name=f'CLUSTER {id_value}'
    )
    scatter.append(scat)
#determining layout
lay = go.Layout(
    title='KMeans Clustering on Iris Dataset',
    xaxis=dict(title='Sepal Length'),
    yaxis=dict(title='Sepal Width'),
    showlegend=True
)
fig = go.Figure(data=scatter, layout=lay)

#plotting
py.iplot(fig,filename='Kmeans clustering on an iris dataset')
