from sklearn.datasets import make_classification
import pandas as pd
from imblearn.over_sampling import KMeansSMOTE,SMOTE

'''X, y = make_classification(
    n_classes=2, class_sep=1.5, weights=[0.9, 0.1],
    n_informative=3, n_redundant=1, flip_y=0,
    n_features=20, n_clusters_per_class=1,
    n_samples=100, random_state=10
)
X = pd.DataFrame(X)
X['target'] = y

print(X)
print(y)


num_0 = len(X[X['target']==0])
num_1 = len(X[X['target']==1])

print(num_0,num_1)
# random undersample

# random oversample

X_resampled, y_resampled = SMOTE().fit_resample(X, y)

print(len(X_resampled), len(y_resampled))'''

X = pd.read_csv('tensorflowMultiLangMetrics.csv')
print(X)
y = list(X.iloc[:,8])
print(len(y))
print(y)

Counter = 0

for num in y:
    if num==1:
        Counter +=1

print("number of trues is : ", Counter )


X_resampled, y_resampled = SMOTE().fit_resample(X, y)

print(len(X_resampled),len(y_resampled))

print(X_resampled)
print(y_resampled)

for num in y_resampled:
    if num==1:
        Counter +=1

print("number of trues is : ", Counter )

X_resampled.to_csv('tensorflowResampleMetrics.csv', encoding='utf-8', index=False)