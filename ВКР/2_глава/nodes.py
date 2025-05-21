import pandas as pd 
group_names= ['X', 'Y', 'Данные']
all_nodes_df =['index', 'axis', 'level', 'name']
all_edges_df =['from', 'to', 'axis']
group_columns= [['x_1', 'x_2', 'x_3'], ['y_1', 'y_2', 'y_3'], ['Столбец данных']]
data_columns =['Значения']
new_nodes= []
new_nodes_full =[]
nodes_df_list_test=[{'index': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}, 'axis': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}, 'level': {0: 0, 1: 3, 2: 3, 3: 3, 4: 2, 5: 3, 6: 3, 7: 3, 8: 2, 9: 1, 10: 3}, 'name': {0: None, 1: 'x31', 2: 'x32', 3: 'x33', 4: 'x21', 5: 'x34', 6: 'x35', 7: 'x36', 8: 'x22', 9: 'x1', 10: 'x33'}, 'x_3': {0: nan, 1: 'x31', 2: 'x32', 3: 'x33', 4: nan, 5: 'x34', 6: 'x35', 7: 'x36', 8: nan, 9: nan, 10: 'x33'}, 'x_2': {0: nan, 1: 'x21', 2: 'x21', 3: 'x21', 4: 'x21', 5: 'x22', 6: 'x22', 7: 'x22', 8: 'x22', 9: nan, 10: 'x22'}, 'x_1': {0: nan, 1: 'x1', 2: 'x1', 3: 'x1', 4: 'x1', 5: 'x1', 6: 'x1', 7: 'x1', 8: 'x1', 9: 'x1', 10: 'x1'}}, {'index': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}, 'axis': {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1}, 'level': {0: 0, 1: 3, 2: 3, 3: 3, 4: 2, 5: 3, 6: 3, 7: 3, 8: 2, 9: 1, 10: 3}, 'name': {0: None, 1: 'y31', 2: 'y32', 3: 'y33', 4: 'y21', 5: 'y34', 6: 'y35', 7: 'y36', 8: 'y22', 9: 'y1', 10: 'y33'}, 'y_3': {0: nan, 1: 'y31', 2: 'y32', 3: 'y33', 4: nan, 5: 'y34', 6: 'y35', 7: 'y36', 8: nan, 9: nan, 10: 'y33'}, 'y_2': {0: nan, 1: 'y21', 2: 'y21', 3: 'y21', 4: 'y21', 5: 'y22', 6: 'y22', 7: 'y22', 8: 'y22', 9: nan, 10: 'y22'}, 'y_1': {0: nan, 1: 'y1', 2: 'y1', 3: 'y1', 4: 'y1', 5: 'y1', 6: 'y1', 7: 'y1', 8: 'y1', 9: 'y1', 10: 'y1'}}, {'index': {22: 0, 23: 1}, 'axis': {22: 2, 23: 2}, 'level': {22: 0, 23: 1}, 'name': {22: None, 23: 'Значения'}, 'Столбец данных': {22: nan, 23: 'Значения'}}]

edges_df_list_test= [{'from': {0: 0, 1: 4, 2: 4, 3: 4, 4: 8, 5: 8, 6: 8, 7: 8, 8: 9, 9: 9}, 'to': {0: 9, 1: 1, 2: 2, 3: 3, 4: 5, 5: 6, 6: 7, 7: 10, 8: 4, 9: 8}, 'axis': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}}, {'from': {10: 0, 11: 4, 12: 4, 13: 4, 14: 8, 15: 8, 16: 8, 17: 8, 18: 9, 19: 9}, 'to': {10: 9, 11: 1, 12: 2, 13: 3, 14: 5, 15: 6, 16: 7, 17: 10, 18: 4, 19: 8}, 'axis': {10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1}}, {'from': {0: 0}, 'to': {0: 1}, 'axis': {0: 2}}]
edges_df_list = []
for edge_dict in edges_df_list_test:
    df = pd.DataFrame(edge_dict)
    edges_df_list.append(df)

nodes_df_list = []
for edge_dict in nodes_df_list_test:
    df = pd.DataFrame(edge_dict)
    nodes_df_list.append(df)
# DB-  класс для выполнения запросов в базу данных
# galielo -  вспомогательный модуль

for axis in range(len(group_names)):
    # максимальный индекс аналитика +1
    new_index = all_nodes_df[all_nodes_df['axis'] == axis]['index'].max() + 1 
    ## Полная таблица сущесвтующего налитика куба
    existed_axis_nodes_df = all_nodes_df.copy()[all_nodes_df['axis'] == axis]
    existed_axis_edges_df = all_edges_df.copy()[all_edges_df['axis'] == axis]
    original_existed_axis_nodes_df = pd.merge( existed_axis_nodes_df, existed_axis_edges_df, how='left', left_on=['index', 'axis'], right_on=['to', 'axis'] ).rename( { 'from': 'parent_id', }, axis=1 ).drop('to', axis = 1)
    for level in range(0, len(group_columns[axis])):
        if level == 0:
            existed_axis_nodes_df = original_existed_axis_nodes_df[original_existed_axis_nodes_df['level'] == 0]
        if level != 0:
            level_df = level_df.rename( { 'name': group_columns[axis][level-1] }, axis = 1 )
        level_df = original_existed_axis_nodes_df[original_existed_axis_nodes_df['level'] == level+1]
        level_df = level_df[['index', 'parent_id', 'axis', 'name', 'level']]
        level_df = level_df.rename( { 'name': group_columns[axis][level] }, axis = 1 )
        level_df['level'] = level_df['level']-1
        new_existed_axis_nodes_df = pd.merge( existed_axis_nodes_df, level_df, how='right', left_on=['index', 'axis', 'level'], right_on=['parent_id', 'axis', 'level'], suffixes=('', '_parent') )
        new_existed_axis_nodes_df=new_existed_axis_nodes_df.drop(['index', 'parent_id_parent'], axis=1)
        new_existed_axis_nodes_df=new_existed_axis_nodes_df.rename({'index_parent': 'index'}, axis=1)
        new_existed_axis_nodes_df['level'] = new_existed_axis_nodes_df['level']+1
        new_existed_axis_nodes_df['name'] = new_existed_axis_nodes_df[group_columns[axis][level]]
        existed_axis_nodes_df = pd.concat( [ existed_axis_nodes_df,new_existed_axis_nodes_df ] )
    existed_axis_nodes_df = existed_axis_nodes_df.drop('parent_id', axis = 1)
    ## Полные данные новых узлов аналитика
    df_columns = list(DB.query( f"SELECT * FROM cube_{cube_id}_data_assemble LIMIT 1; " ,engine=engine, return_df=True))
    col_list = df_columns
    for col_name in data_columns:
        if col_name in col_list:
            col_list.remove(col_name)
    if 'Столбец данных' in group_columns[axis]:
        new_df_rewrite_values= pd.DataFrame({group_columns[axis][0]: data_columns})
    else:
        new_df_rewrite_values =  DB.query( query= f''' SELECT DISTINCT ON ( {' , '.join([  f'"{str(x)}"' for x in group_columns[axis] ])})  {' , '.join([  f'"{str(x)}"' for x in group_columns[axis] ])} FROM  cube_{cube_id}_data_assemble ''' , return_df=True, engine=engine) 
    axis_nodes_df = pd.DataFrame()
    for level in range(len(group_columns[axis]), 0, -1):
        col = group_columns[axis][level-1]
        level_df = new_df_rewrite_values.dropna(subset=[col]) 
        level_df.iloc[:,level:] = np.nan
        level_df['level'] = level
        level_df['axis'] = axis
        level_df['name'] = level_df.iloc[:,level-1]
        axis_nodes_df = pd.concat([axis_nodes_df, level_df])
    def convert_month_names(val):
        if str(val).lower().strip() in galileo.months_names:
            return galileo.month_dict_reverse[galileo.month_dict[str(val).lower().strip()]]
        return val
    axis_nodes_df['name'] = axis_nodes_df['name'].apply(lambda x: convert_month_names(x))
    axis_nodes_df = axis_nodes_df.drop_duplicates()
    axis_nodes_df = pd.merge(  existed_axis_nodes_df, axis_nodes_df, how='outer', on=['axis', 'level'] + group_columns[axis], suffixes=('', '_y') )
    axis_nodes_df.loc[axis_nodes_df['name'].isna(),'name'] = axis_nodes_df.loc[axis_nodes_df['name'].isna(),'name_y']
    axis_nodes_df = axis_nodes_df.drop('name_y', axis = 1)
    new_axis_df = axis_nodes_df[axis_nodes_df['index'].isna()]
    new_axis_df = new_axis_df.sort_values(by = group_columns[axis])
    new_axis_df.loc[:,'index'] = list(range(new_index, new_index + len(new_axis_df)))
    axis_nodes_df = pd.concat( [ axis_nodes_df[~axis_nodes_df['index'].isna()], new_axis_df ] )
    axis_nodes_df = axis_nodes_df[ ['index', 'axis', 'level', 'name'] + group_columns[axis][::-1] ]
    new_axis_df = new_axis_df[ ['index', 'axis', 'level', 'name'] + group_columns[axis][::-1] ]
    axis_nodes_df['index'] = axis_nodes_df['index'].astype('int')
    axis_nodes_df['level'] = axis_nodes_df['level'].astype('int')
    axis_nodes_df['axis'] = axis_nodes_df['axis'].astype('int')
    axis_nodes_df = axis_nodes_df.fillna(np.nan).replace({np.nan: None})
    new_axis_df['index'] = new_axis_df['index'].astype('int')
    new_axis_df['level'] = new_axis_df['level'].astype('int')
    new_axis_df['axis'] = new_axis_df['axis'].astype('int')
    new_axis_df = new_axis_df.fillna(np.nan).replace({np.nan: None})
    nodes_df_list[axis] = axis_nodes_df
    new_nodes_df = pd.concat([new_nodes_df, new_axis_df])
    new_nodes.extend( list( new_axis_df.T.to_dict().values() ) )
    new_nodes_full.extend( list( new_axis_df.T.to_dict().values() ) )
    ## Рассчёт новых рёбер аналитика
    levels_df_list = []
    for level in range(len(group_columns[axis]), 0, -1):
        level_children_df = axis_nodes_df[axis_nodes_df['level'] == level]
        level_parent_df = axis_nodes_df[axis_nodes_df['level'] == level-1]
        level_parent_df = level_parent_df[['index'] + group_columns[axis][:level-1]]
        level_parent_df = level_parent_df.rename(            {'index': 'parent_index'},            axis = 1        )        
        if level != 1:
            level_children_df = pd.merge( level_children_df, level_parent_df, how='left', on=group_columns[axis][:level-1], suffixes=['', '_y'] )
        else:
            level_children_df['parent_index'] = level_parent_df['parent_index'].iloc[0]
        levels_df_list.append(level_children_df)
    levels_df_list.append(axis_nodes_df[axis_nodes_df['level'] == 0])
    axis_edges_df = pd.concat(levels_df_list).sort_values(by='index')[['index', 'axis', 'parent_index']]
    axis_edges_df = axis_edges_df.rename( {'index': 'to', 'parent_index': 'from'}, axis = 1    )
    axis_edges_df = axis_edges_df[~axis_edges_df['from'].isna()]
    axis_edges_df = axis_edges_df[~axis_edges_df['to'].isna()]
    axis_edges_df = axis_edges_df.astype('int')
    existed_axis_edges_df = all_edges_df[all_edges_df['axis'] == axis]
    existed_axis_edges_df['is_existed'] = True
    all_axis_edges_df = pd.merge( axis_edges_df, existed_axis_edges_df, how='outer', on=['from', 'to', 'axis'] )
    new_axis_edges_df = all_axis_edges_df[all_axis_edges_df['is_existed'].isna()]
    new_axis_edges_df = new_axis_edges_df[['from', 'axis', 'to']]
    all_axis_edges_df = all_axis_edges_df[['from', 'axis', 'to']]
    edges_df_list[axis] = all_axis_edges_df
    new_edges_df = pd.concat([new_edges_df, new_axis_edges_df])
 

for axis_n in range(len(edges_df_list)):
    edges_df_list[axis_n] = edges_df_list[axis_n].drop_duplicates(subset = ['axis', 'from', 'to'])
for axis_n in range(len(nodes_df_list)):
    nodes_df_list[axis_n] = nodes_df_list[axis_n].drop_duplicates(subset = ['axis', 'index'])
