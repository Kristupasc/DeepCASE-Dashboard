import numpy as np
import pandas as pd


# Dummy data for clusters
# clusters_data = [
#     {"x": 1, "y": 10, "Cluster": 0, "Risk Label": "Info"},
#     {"x": 3.1, "y": 10.2, "Cluster": 0, "Risk Label": "Info"},
#     {"x": 3.9, "y": 10.5, "Cluster": 0, "Risk Label": "Info"},
#     {"x": 3, "y": 5, "Cluster": 2, "Risk Label": "Medium"},
#     {"x": 2, "y": 5, "Cluster": 1, "Risk Label": "Low"},
#     {"x": 9, "y": 3, "Cluster": 5, "Risk Label": "Suspicious"},
#     {"x": 10, "y": 6, "Cluster": 4, "Risk Label": "Attack"},
#     {"x": 4, "y": 1, "Cluster": 3, "Risk Label": "High"},
#     {"x": 1, "y": 1, "Cluster": 6, "Risk Label": "Unlabeled"},
# ]
#
# # Convert to DataFrame
# df_clusters = pd.DataFrame(clusters_data)
# print(df_clusters)

def choose_risk(weight):
    # A weight can be between 0 and 100. The higher the weight, the higher the risk
    if weight == 0:
        return "Unlabeled"
    elif weight < 10:
        return "Info"
    elif weight < 30:
        return "Low"
    elif weight < 50:
        return "Medium"
    elif weight < 70:
        return "High"
    elif weight < 90:
        return "Suspicious"
    else:
        return "Attack"

weights = np.random.randint(0, 11, 100)
risk_labels = [choose_risk(weight) for weight in weights]

clusters_data = {
    'Time': pd.date_range(start='2023-01-01',periods=100, freq='D'),
    'Type': ['A', 'B', 'C', 'D', 'E'] * 20,
    'Source': ['X', 'Y', 'Z', 'W', 'V'] * 20,
    'Weight': weights,
    'Risk Label': risk_labels
}
df_clusters = pd.DataFrame(clusters_data)
# df_clusters.to_csv("df_clusters3.csv", index=False)
