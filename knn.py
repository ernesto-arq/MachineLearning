# -*- coding: utf-8 -*-
"""KNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EdBTvFhjtmpeYNguBgr3ZSwoMIV1Jo_T

# K Vizinhos Mais Próximos
"""

import numpy as np
import pandas as pd

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, balanced_accuracy_score, plot_confusion_matrix
from sklearn.preprocessing import StandardScaler, MinMaxScaler


bc = datasets.load_breast_cancer()

X = pd.DataFrame(bc.data)
y = bc.target

X.describe()

pd.Series(y).value_counts()

"""## Vamos aplicar um hold out"""

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)


sc = StandardScaler()

x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

pd.DataFrame(x_train).describe()

pd.DataFrame(x_test).describe()

"""## Com essa particao de dados, qual K resolveria esse problema?"""

results = []
for k in range(1,50,5):

  knn_clf = KNeighborsClassifier(n_neighbors=k, p=2, metric='minkowski', algorithm='brute')
  knn_clf.fit(x_train, y_train)

  y_pred = knn_clf.predict(x_test)

  results.append({'k': k,
                  'acc': accuracy_score(y_test, y_pred), 
                  'bal_acc': balanced_accuracy_score(y_test, y_pred)})


df_results = pd.DataFrame(results).set_index('k').sort_values(by='k')

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.plot(df_results)
plt.legend(df_results.columns)
plt.grid()
plt.title('KNN com normalizacao', fontsize = 20)
plt.xlabel('Numero de Vizinhos', fontsize=15)
plt.xticks(fontsize=15)
plt.ylabel('Desempenho', fontsize=15)
plt.yticks(fontsize=15)

plt.show()

# Melhor K

best_k = df_results['acc'].idxmax()
print('Best K = ', best_k)

df_results.loc[best_k]

# Matriz de confusão do melhor K

knn_clf = KNeighborsClassifier(n_neighbors=best_k, p=2, metric='minkowski', algorithm='brute')
knn_clf.fit(x_train, y_train)

y_pred = knn_clf.predict(x_test)
plot_confusion_matrix(knn_clf, x_test, y_test, cmap=plt.cm.Blues)

"""## E se eu não normalizasse os dados? O resultado seria o mesmo?"""

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

results = []
for k in range(1,50,5):

  knn_clf = KNeighborsClassifier(n_neighbors=k, p=2, metric='minkowski', algorithm='brute')
  knn_clf.fit(x_train, y_train)

  y_pred = knn_clf.predict(x_test)

  results.append({'k': k,
                  'acc': accuracy_score(y_test, y_pred), 
                  'bal_acc': balanced_accuracy_score(y_test, y_pred)})


df_results_nn = pd.DataFrame(results).set_index('k').sort_values(by='k')

df_all = pd.concat([df_results, df_results_nn], axis=1)

col_names = {'acc': ['acc_norm', 'acc'], 'bal_acc': ['bal_acc_norm', 'bal_acc']}
df_all= df_all.rename(columns=lambda c: col_names[c].pop(0) if c in col_names.keys() else c)

plt.figure(figsize=(8, 6))
plt.plot(df_all)
plt.legend(df_all.columns)
plt.grid()
plt.title('Normalizacao X Não Normalizacao', fontsize = 20)
plt.xlabel('Numero de Vizinhos', fontsize=15)
plt.xticks(fontsize=15)
plt.ylabel('Desempenho', fontsize=15)
plt.yticks(fontsize=15)

plt.show()

"""# Vocês acabaram de ver o efeito que certas escolhas podem ter nos seus experimentos. 

Comparem agora o desempenho usando diferentes métodos de cálculo de distância com os dados normalizados:

- metric='chebyshev'
- metric='minkowski', p=1  (manhattan)


"""

knn_clf_chebyshev = KNeighborsClassifier(n_neighbors=best_k, p=2, metric='chebyshev', algorithm='brute')
knn_clf_chebyshev.fit(x_train, y_train)

y_pred = knn_clf.predict(x_test)

y_pred = knn_clf_chebyshev.predict(x_test)
  results.append({'k': k,
                  'acc': accuracy_score(y_test, y_pred), 
                  'bal_acc': balanced_accuracy_score(y_test, y_pred)})
df_results = pd.DataFrame(results).set_index('k').sort_values(by='k')
# Melhor K chebyshev
best_k_chebyshev = df_results['acc'].idxmax()
print('Best K = ', best_k_chebyshev)

df_results.loc[best_k_chebyshev]

knn_clf_minkowski = KNeighborsClassifier(n_neighbors=best_k, p=1, metric='minkowski', algorithm='brute')
knn_clf_minkowski.fit(x_train, y_train)
y_pred = knn_clf.predict(x_test)

y_pred = knn_clf_minkowski.predict(x_test)

  results.append({'k': k,
                  'acc': accuracy_score(y_test, y_pred), 
                  'bal_acc': balanced_accuracy_score(y_test, y_pred)})


df_results = pd.DataFrame(results).set_index('k').sort_values(by='k')
# Melhor K minkowski

best_k_knn_clf_minkowski = df_results['acc'].idxmax()
print('Best K = ', best_k_knn_clf_minkowski)

df_results.loc[best_k_knn_clf_minkowski]