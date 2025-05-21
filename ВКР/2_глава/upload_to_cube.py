def upload(df, cube_id, engine, user_id=None, current_user=None, dtype_dist = None, new_data = True, file_name = 'no filename passed'):
    if current_user is not None:
        user_id = current_user.id
    db_prefix = 'cube'
    query = f''' SELECT * FROM cubes WHERE id = '{cube_id}' LIMIT 1 '''
    cube_in_cubes = galileo.db.query(query, engine=engine, return_df = True)
    cube_name = cube_in_cubes['name'].squeeze()
    if len(cube_in_cubes) == 0:
        return {'code': 0, 'message': f"Куб с id {cube_id} не найден", "data": None }
    if new_data:        table_name = f'{db_prefix}_{cube_id}_newdata'
    else:        table_name = f'{db_prefix}_{cube_id}_data'
    query = f''' SELECT * FROM {table_name} LIMIT 1'''
    new_table_flag = False
    try:
        galileo.db.query(query, engine=engine, return_df = False)
    except:
        new_table_flag = True
    ## проверка наличия необходимых столбцов
    query = f''' SELECT * from cube_{cube_id}_info ORDER BY primary_key'''
    structure_response = galileo.cubes.get_structure(cube_id=cube_id, engine=engine, convert=True, old_format = False, user_id = None)
    if structure_response['code'] == 0:
        return { 'code': 0, 'message': 'Оишбка получения структуры куба', 'data': None }
    structure = structure_response['data']['structure']
    mapping = structure_response['data']['mapping']
    analitic_columns = structure_response['data']['analitic_columns']
    not_mapped_analitic_columns = structure_response['data']['not_mapped_analitic_columns']
    rewrite_group_names = structure_response['data']['rewrite_group_names']
    data_columns = structure_response['data']['data_columns']
    group_names = structure_response['data']['group_names']
    rewrite_columns = structure_response['data']['rewrite_columns']
    merge_analytics= structure_response['data']['structure']['analytics_merge']
    missing_columns = []
    for col in not_mapped_analitic_columns:
        if col not in list(df.columns):
            missing_columns.append(col)
            df[col] = np.nan
        else:
            df[col] = df[col].astype('string')

    if len(missing_columns)>0:
        return {'code': 0, 'message': f'''не хватает столбцов для аналитиков: {", ".join([f"'{col}'" for col in missing_columns])} ''', "data": None            }
    missing_columns = []
    not_float_data_columns = []
    for col in data_columns:
        if col not in list(df.columns):
            df[col] = 0
        else:
            try:
                df[col] = df[col].astype('float')
            except:
                not_float_data_columns.append(col)
                df[col] = df[col].fillna(0)
    if len(missing_columns)>0:
        return {'code': 0, 'message': f'''Не хватает столбцов с данными: {", ".join([f"'{col}'" for col in missing_columns])} ''', "data": None            }
    if len(not_float_data_columns)>0:
        return {'code': 0, 'message': f'''Не удалась конвертация в число в столбцах с данными: {", ".join([f"'{col}'" for col in not_float_data_columns])}, проверьте, нет ли ячеек со значениями отличными от числа (или пустых) ''', "data": None            }
    cols = not_mapped_analitic_columns + data_columns
    df = df[cols + list(df.columns.difference(cols))]
    for analitic_column in not_mapped_analitic_columns:
        # print(df[analitic_column])
        df[analitic_column] = df[analitic_column].map(lambda x: str(x).replace("'", '"'))
        df[analitic_column] = df[analitic_column].map(lambda x: re.sub('''[^0-9а-яА-Яa-zA-Z!?_,.()#№:/&<>[]{}*-" ]+''', '*', str(x)))
    for column_name in df.columns.difference(data_columns):
        df[column_name] = df[column_name].map(lambda x: str(x)[:128].strip())
    month_columns = []
    for column in not_mapped_analitic_columns:
        if all([str(row_value).lower().strip() in galileo.months_names for row_value in list(df[column].unique())]):
            month_columns.append(column)
            df[column].apply(lambda x: x.lower().strip())
            df[column] = df[column].replace(galileo.month_dict)
            df[column] = df[column].astype('int')
    df = df.sort_values(by=list(df.columns))
    for column in month_columns:
        df[column] = df[column].replace(galileo.month_dict_reverse)
    df = df.reset_index(drop = True)
    non_boolean_columns = list(df.dtypes[df.dtypes != 'boolean'].index)
    df[non_boolean_columns] = df[non_boolean_columns].replace({'None': None})
    df[non_boolean_columns] = df[non_boolean_columns].replace({'nan': None})
    df[non_boolean_columns] = df[non_boolean_columns].replace({'<NA>': np.nan})
    df[non_boolean_columns] = df[non_boolean_columns].replace({'*NA*': np.nan})
    dtype_dist = dict()
    for analitic_column in not_mapped_analitic_columns:
        dtype_dist[analitic_column] = String
    for data_column in data_columns:
        dtype_dist[data_column] = Float
    for other_column in  list(df.columns.difference(not_mapped_analitic_columns + data_columns)):
        dtype_dist[other_column] = String
    if new_table_flag: ## Скорее всего никгда не будет исполняться т.к. таблицы создаются при define куба
        if dtype_dist is not None:
            dtype_dist = dict()
        for col_name in not_mapped_analitic_columns:
            dtype_dist[col_name] = String
        for col_name in data_columns:
            dtype_dist[col_name] = Float
        upload_response = galileo.db.upload_df_to_postgres(df=df,  table_name=table_name,  engine=engine,  chunksize = 10000000,
  append = False,  cols = list(df.columns),  log = False,  string_default_length = 128,
  dtype_dist = dtype_dist,  col_name_max_length = None,  primary_key = None,  skip_check_col = False)
        if upload_response['code'] == 1:
            log_response = galileo.db.cubes.log( cube_id = cube_id, action = 'upload', value = file_name,
             user_id = user_id, engine = engine )
            if log_response['code'] != 1:
                log_message = ' (ошибка логирования)'
            else:
                log_message = ''
            return {'code': 1, 'message': f'''Создана очередь на сборку для куба "{cube_name}" {log_message}''', "data": None}
        else:
            return {'code': 0, 'message': upload_response['message'], 'error_message': upload_response.get('error_message', None), "data": None            }
    else:
        constraint_columns =merge_analytics #rewrite_columns
        if len(constraint_columns) > 0:
            update_response = galileo.db.update_df_in_postgres(df=df, constraint_cols=constraint_columns, table_name=table_name, engine = engine,
             cols = list(df.columns), constraint_values = None, col_name_max_length = 30, dtype_dist = dtype_dist,
             check_for_int = False, skip_check_col = False, )
        else:
            update_response = galileo.db.upload(df=df, table_name=table_name, engine = engine, append = True,
             log = False, cols = list(df.columns), col_name_max_length = 30, string_default_length = 128,
             dtype_dist = dtype_dist, primary_key = None, skip_check_col = False,         )
        if update_response['code'] == 1:
            return {'code': 1, 'message': f'''Обновлена очередь на сборку куба "{cube_name}": {update_response['message']}''', 'error_message': update_response.get('error_message', None), 'data': update_response['data']}
        else:
            return {'code': 0, 'message': update_response['message'], 'error_message': update_response.get('error_message', None), 'data': update_response['data']            }