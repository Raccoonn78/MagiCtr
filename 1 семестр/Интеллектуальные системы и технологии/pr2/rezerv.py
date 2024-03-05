import umap
# from umap import UMAP

scaler = MinMaxScaler()
X= scaler.fit_transform(df)
y=list(df)


manifold = umap.UMAP().fit(X)
X_reduced = manifold.transform(X)


# X_reduced.shape
fig = px.scatter(None, x=X_embedded[:,0], y=X_embedded[:,1]   , labels={
                        "x": "1",
                        "y": "2",
                    },
                    opacity=1  )

# Изменение цвета фона графика
fig.update_layout(dict(plot_bgcolor = 'white'))

# Обновление линий осей
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', 
                zeroline=True, zerolinewidth=1, zerolinecolor='lightgrey', 
                showline=True, linewidth=1, linecolor='black')

fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', 
                zeroline=True, zerolinewidth=1, zerolinecolor='lightgrey', 
                showline=True, linewidth=1, linecolor='black')

# Установка названия рисунка
fig.update_layout(title_text="UMAP")

# Обновление размера маркера
fig.update_traces(marker=dict(size=3))
