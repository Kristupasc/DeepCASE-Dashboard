import pandas as pd


# Dummy data for clusters
clusters_data = [
    {"x": 1, "y": 10, "Cluster": 0, "Risk Label": "Info"},
    {"x": 3.1, "y": 10.2, "Cluster": 0, "Risk Label": "Info"},
    {"x": 3.9, "y": 10.5, "Cluster": 0, "Risk Label": "Info"},
    {"x": 3, "y": 5, "Cluster": 2, "Risk Label": "Medium"},
    {"x": 2, "y": 5, "Cluster": 1, "Risk Label": "Low"},
    {"x": 9, "y": 3, "Cluster": 5, "Risk Label": "Suspicious"},
    {"x": 10, "y": 6, "Cluster": 4, "Risk Label": "Attack"},
    {"x": 4, "y": 1, "Cluster": 3, "Risk Label": "High"},
    {"x": 1, "y": 1, "Cluster": 6, "Risk Label": "Unlabeled"},
]

# Convert to DataFrame
df_clusters = pd.DataFrame(clusters_data)
print(df_clusters)