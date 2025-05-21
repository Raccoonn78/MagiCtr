
class Sql_cube_created:
    '''
    ищи создателя
    '''
    def __init__(self, engine, user_id, cube_id , group_names=None, group_columns=None, reassemble=False, without_root=False ) -> None:

        self.engine=engine 
        self.user_id=user_id 
        self.cube_id=cube_id
        self.structure = galileo.cubes.get_structure(engine=engine, cube_id=cube_id)['data']  
        self.table_name=f'test_temp_{cube_id}_cube'
        self.cube_id_temp_data= f'cube_{cube_id}_data'
        self.group_names=group_columns
        self.group_columns=group_names
        self.list_query=[]
        self.reassemble=reassemble
        self.analytics_merge= self.structure['analytics_merge'][::-1]
        self.bool_access_merge=False
        self.without_root=without_root
        # удалаяем двойные разные кавычки 
        self.group_names=[[j.replace('"','') for j in i] for i in self.group_names]
        # удаляем "Столбец данных"
        self.group_names=self.group_names[:-1]
        # удалаяем двойные разные кавычки 
        self.group_columns=[i.replace('"','') for i in self.group_columns]
        # список со всеми столбцами Данные
        self.group_data_columns =     [ i['name'] for i in self.structure['data_columns']+self.structure['data_columns_operations']+self.structure['data_columns_preoperations']   ] # список всех столбцов куба 
        #  раньше нужны были псевдо названии для запроса JOIN  <таблица> AS ...
        self.group_names_join_nodes = [ 'n'+str(xx)           for xx in range(len(self.group_columns)) ] # название аналитиков для join 
        # длина каждого аналитика 
        self.group_lenghts =          [ int(ax['id_length'])  for ax in self.structure['axis'] ] # длина 
        #  все оригинальные столбцы с Данными
        self.dict_name_col={ i['name']:i['name']  for i in galileo.cubes.get_structure(engine=self.engine, cube_id=self.cube_id)['data']['data_columns']}
        # словарь   {'Столбец данных':2 }  для того чтобы сделать запрос в таблицу  cube_{self.cube_id}_nodes_2
        self.dict_name_col_and_index={ i['columns'][0]:i['id'] for i in galileo.cubes.get_structure(engine=self.engine, cube_id=self.cube_id)['data']['axis']   if  'Столбец данных' in i['columns']}
        # не помню зачем )
        self.dict_name_col_and_={ i['columns'][0]:i['id'] for i in galileo.cubes.get_structure(engine=self.engine, cube_id=self.cube_id)['data']['axis']   if  'Столбец данных' in i['columns']}
        #  df где есть все столбцы Данные и их иднексы (index)
        self.df_name_nodes_columns=DB.query(query=f"""SELECT name , index FROM  cube_{self.cube_id}_nodes_2  where axis={self.dict_name_col_and_index['Столбец данных']} """ , engine=engine , return_df=True )
        # у каждого столбца данных повялется нужный индекс  потом он превращатся в 001, 002, 003, ...
        for name, index in zip(self.df_name_nodes_columns['name'].to_list(), self.df_name_nodes_columns['index'].to_list()):
            self.dict_name_col_and_index[name]=index
            
        dict_last_agg={}
        for i in  self.structure['data_columns']:
            if  3 in [ j['aggregation_id'] for j in  i['aggregation'] ]:
                dict_last_agg[i['name']]={   j['analytics']:j['aggregation_id'] for j in  i['aggregation']  if j['aggregation_id']==3 }
            # массивы внутри ключа это axis_id  galileo.cubes.get_nodes(cube_id=, engine=, axis_id=8)

        self.list_name_last_analytic=list(set([list(i.keys())[0] for i in list(dict_last_agg.values())]))

        radical_column=  ''
        # создается запрос при котором доатсюатся ВСЕ столбцы с Данными , и если в столбце одни Nan , он заменится на 0
        for i in self.group_data_columns: radical_column += f'COALESCE("{i}", 0 ) + '
        # удаляем плюсик послежний в строке 
        radical_column = radical_column[:-2]
        self.group_data_columns_name_origin=self.group_data_columns.copy()
        # добавляем в начало Корень
        self.group_data_columns_name_origin.insert(0,"Корень") 
        # так де добавляем чтобы первым поситать корень
        self.group_data_columns.insert(0,radical_column)

        self.data_columns_operation_all= {}
        # удаляем пустой ключ из словаря так как он появляется из за cube_{self.cube_id}_nodes_2
        try:
            del self.dict_name_col_and_index[None]
        except:
            pass
        # ключ это название солбцца Данные :значение это либо формула либо само название столбца   
        # Пример:  {'Корень': (COALESCE("столб1", 0 ) + COALESCE("столб2", 0 ) + COALESCE("столб3", 0 ) ), столб1: a+b+c , столб2:столб2 ,столб3:столб3}
        for group_data_column ,name  in zip(self.group_data_columns[1:], self.dict_name_col.keys()):
            if name=='Столбец данных':
                self.data_columns_operation_all['Корень']=group_data_column
            else:
                self.data_columns_operation_all[name]=group_data_column
        
        self.data_columns_operation_all['Корень']= self.group_data_columns[0]  
        if self.structure['data_columns_operations']:
            for data_columns_operation in self.structure['data_columns_operations']:
                self.data_columns_operation_all[data_columns_operation['name']]=data_columns_operation['operation']
        self.list_arg_no=[]
        self.dict_no_agg={} # словарь со всеми нащзваниями аналитиков у которых нет агрегаций    
        self.dict_no_agg['Корень']=[]
        for data_col  in self.structure['data_columns'] :
            self.dict_no_agg[data_col['name']]=[]
            for aggr in data_col['aggregation']:
                if aggr['aggregation_id']==1:
                    for ax in self.structure['axis']:
                        if ax['name']==aggr['analytics']:
                            self.list_arg_no.append(ax['columns'])
                            self.dict_no_agg[data_col['name']].append(ax['columns'])
                            self.dict_no_agg['Корень'].append(ax['columns'])
        for key,val in self.dict_no_agg.items():
            res=[]
            [res.append(x) for x in val if x not in res]
            self.dict_no_agg[key]=res
       
        self.dict_name_and_list_col={}   
        for ax in self.structure['axis']:
            self.dict_name_and_list_col[ax['name']]=ax['columns']

    def create_param(self): # пример входных данных , просто закрой 
       
        structure = galileo.cubes.get_structure(engine=self.engine, cube_id=self.cube_id)['data']  
        self.table_name=f'test_temp_{self.cube_id}_cube'
        self.cube_id_temp_data= f'cube_{self.cube_id}_data'
        # cube_id=28 
        self.group_names= [['x1','x2', 'x3'],
                    ['y1','y2','y3'],
                    ['z1','z2','z3'],
                    ['Данные']]
        # ubrat kavichki
        self.group_names= [['Год подписания', 'Транзакция'],
                                            ['"Договор"'],
                                            ['"Договор исходящий"'],
                                            ['"Страхователь"', '"ИНН Контрагента"'],
                                            ['"Категория контрагента"'],
                                            ['"Программа страхования"'],
                                            ['"Ответственный руководитель упр"'],
                                            ['"Линия бизнеса упр2"'],
                                            ['"Столбец данных"']]
        
        self.group_names=[[j.replace('"','') for j in i] for i in self.group_names]

        self.group_names=self.group_names[:-1]
        # group_names.append('Корень')
        self.group_columns= ['x', 'y','z','Данные'] # group_columns
        self.group_columns= ['"Год подписания1"',
                        '"Договор1"',
                        '"Договор исходящий1"',
                        '"Страхователь1"',
                        '"Категория контрагента1"',
                        '"Программа страхования1"',
                        '"Ответственный руководитель упр1"',
                        '"Линия бизнеса упр21"',
                        '"Данные"'] 
        
        self.group_columns=[i.replace('"','') for i in self.group_columns]
        # group_data=['values']
        self.group_data_columns =     [ i['name']             for i in structure['data_columns_order']    ] # список всех столбцов куба 
        try:
            self.group_data_columns.remove("qwe")
        except:
            ...

        # group_data_columns.insert(0,'Корень')
        self.group_names_join_nodes = [ 'n'+str(xx)           for xx in range(len(self.group_columns)) ] # название аналитиков для join 
        self.group_lenghts =          [ int(ax['id_length'])  for ax in structure['axis'] ] # длина 
        self.list_query=[] # список запросов


        radical_column=  ''
        for i in self.group_data_columns: radical_column += f'"{i}" + '

        radical_column = radical_column[:-2]
        self.group_data_columns_name_origin=self.group_data_columns.copy()
        self.group_data_columns_name_origin.insert(0,"Корень")
        self.group_data_columns.insert(0,radical_column)

    def create_data_assemble_index(self):
        
        print(f'self.group_columns {self.group_columns}')
        print(f'self.group_names  {self.group_names }')
        print(f'self.structure {self.structure}')
        print(f'self.group_data_columns {self.group_data_columns}')
        #Создания distinct 
        distinct_string= f''' '''
        for group_column  , group_name in zip(self.group_columns[:-1], self.group_names ):
            for number ,name in enumerate(group_name):
                    distinct_string+=f'''  cube_{self.cube_id}_data_assemble."{name}",'''
        distinct_string=distinct_string[:-1]  
         

        # просто заменяем значения аналитиков на значение их индексов 
        name_dict_df_nodes_and_axis={ i['name']:i['id'] for i in self.structure['axis']}

        string_create= f'''   CREATE UNLOGGED TABLE IF NOT EXISTS  cube_{self.cube_id}_data_assemble_index AS (  
            SELECT distinct on({distinct_string})    ''' 
        
        for i in self.group_data_columns[1:]:
            string_create+= f''' cube_{self.cube_id}_data_assemble."{i}", '''
        a=0
        list_index_for_nodes_n=[]
        for group_column  , group_name in zip(self.group_columns[:-1], self.group_names):
            temp_l=[]
            # print('group_name[::-1]', group_name[::-1])
            for name in group_name:
                temp_l.append(a)
                string_create+=f'''  n{a}.index AS "{name}",'''
                a+=1
            list_index_for_nodes_n.append(temp_l[::-1])
        string_create=string_create[:-1]+f''' FROM  cube_{self.cube_id}_data_assemble \n'''
        a=0
        for group_column  , group_name, numb in zip(self.group_columns[:-1], self.group_names, list_index_for_nodes_n ):
            for i in range(len(group_name)):
                string_create+=f''' \n LEFT OUTER JOIN  cube_{self.cube_id}_nodes_axis_{name_dict_df_nodes_and_axis[group_column]} n{numb[i]} USING( '''
                 
                if i==0:
                    for number ,name in enumerate(group_name):
                        string_create+=f''' "{name}",'''
                    string_create=string_create[:-1] + f''' )'''
                    a+=1
                else:
                    for number ,name in enumerate(group_name[:-i]):
                        string_create+=f''' "{name}",'''
                    string_create=string_create[:-1] + f''' )'''
                    a+=1
          
            list_index_for_nodes_n.append(temp_l[::-1])
        a=0
        string_create+=f''' \n WHERE '''
        for group_column  , group_name , n_index_nodes  in zip(self.group_columns[:-1], self.group_names, list_index_for_nodes_n):
                schet_null=1
                for number ,name in zip(n_index_nodes[::-1], group_name):
                    if schet_null==0:
                        string_create+=f''' cube_{self.cube_id}_data_assemble."{name}"= n{number}."name" and \n'''
                    else:
                        # print('group_name', group_name[schet_null:])
                        string_create+=f'''( cube_{self.cube_id}_data_assemble."{name}"= n{number}."name"  '''   #  n1."день" is  null
                        for i in group_name[schet_null:]:
                            string_create+=f''' and  n{number}."{i}" is NULL '''
                        string_create+= f'''  )  and \n''' 
                        # for i in group_name[]
                    schet_null+=1
                    a+=1
        string_create=string_create[:-5] + f''' );'''
        self.assemble_index=string_create[86:-2]
        print(f'string_create {string_create}')
        return string_create

    def group_by_tuple(self, group_data_column,   name_number,copy_group_name ):
        temp_list_str=''
        for n , mini_val in enumerate(copy_group_name):
            if n != name_number  :
                temp_list_str+= f""" {tuple(mini_val)}"""+""",""".replace("(",'').replace(")",'').replace(",,",',').replace(",)", ")").replace("'",'"')
        return temp_list_str
    
    def calculation_of_indexes_reassemble(self):


        pass
    
    def reassemble_index_leaves(self, list_query ): # создание индексов на листьях для reassemble # val2
        cube_cube_id_data_index = f'cube_{self.cube_id}_data_assemble_index'
        cube_cube_id_reassemble_template=f'cube_{self.cube_id}_reassemble_template'
        cube_cube_id_reassemble=f'cube_{self.cube_id}_reassemble'
        data_table_temp_index= f"temp_{self.cube_id}_index" 



        dict_name_col_and_index={ i['columns'][0]:i['id'] for i in galileo.cubes.get_structure(engine=self.engine, cube_id=self.cube_id)['data']['axis']   if  'Столбец данных' in i['columns']}
        
        df_name_nodes_columns=DB.query(query=f"""SELECT name , index FROM  cube_{self.cube_id}_nodes_2  where axis={dict_name_col_and_index['Столбец данных']} """ , engine=self.engine , return_df=True )
        for name, index in zip(df_name_nodes_columns['name'].to_list(), df_name_nodes_columns['index'].to_list()):
            dict_name_col_and_index[name]=index
        # список всех нужных столбцов на каждую итерацию цикла 
        group_names_all=list(chain.from_iterable(self.group_names))
        striing_group_names= ' '
        for k in group_names_all:
            striing_group_names+=f'"{k}"'+','
        
            
        # список из строк
            # что в строке: "аналитик1","аналитик2",...,(либо Корень т.е. сумма столбцов которую мы формировали ранне либо название столбца с данными по счету ) 
            # эта строка пойдет в SELECT {...} FROM 
        itterable_columns= list(map( lambda x:  striing_group_names+ f'"{self.group_data_columns[x]}"'   if x!=0  else  striing_group_names+ f' {self.group_data_columns[x]} AS Корень'  , range(len(self.group_data_columns))))
        
        
        coalesce_data_columns=[]
        coalesce_string_data_columns=f''
         
        for i in self.group_data_columns_name_origin[1:]:
            coalesce_string_data_columns+=f' COALESCE("{i}", 0 )  +'
        coalesce_string_data_columns=coalesce_string_data_columns[:-2] 
        coalesce_string_data_columns+= f' AS Корень'  
        coalesce_data_columns.append(coalesce_string_data_columns)



 
        temp_str=''
        for group_name, group_column in zip(self.group_names, self.group_columns[:-1]):
            temp_tuple=f"{tuple(group_name)},".replace("(","").replace(")","")
            temp_str+= f"""  COALESCE{tuple(group_name[::-1])} AS "{group_column}", """
            temp_str=temp_str.replace("'",'"').replace(",,",',').replace(",)",')')

        
         
        for enumerate_number, group_data_column in enumerate(self.group_data_columns_name_origin):  
            temp_list_rollup=''
            distinc_on=''
            rec = coalesce_string_data_columns if enumerate_number==0 else group_data_column
            data_table_temp_index_reassemble= f"temp_{self.cube_id}_index_reassemble" 
            # print('res',rec)
            list_query.append(f""" DROP TABLE IF EXISTS  {data_table_temp_index_reassemble}""")
            if enumerate_number ==0: query_create_temp_index= f"""CREATE UNLOGGED TABLE IF NOT EXISTS {data_table_temp_index_reassemble} AS (SELECT  DISTINCT  {temp_str}  {rec}  FROM {cube_cube_id_data_index} )"""
            else:  query_create_temp_index= f"""CREATE UNLOGGED TABLE IF NOT EXISTS {data_table_temp_index_reassemble} AS (SELECT  DISTINCT  {temp_str}  "{rec}"  FROM {cube_cube_id_data_index} )"""
            # query_create_temp_index= f"""CREATE TABLE IF NOT EXISTS {data_table_temp_index_reassemble} AS (SELECT  {itterable_columns[enumerate_number]}  FROM {cube_cube_id_data_index} )"""
            list_query.append(query_create_temp_index)
            
            for group_names_join_node, lenght, group_column  in zip(self.group_names_join_nodes[:-1], self.group_lenghts[:-1] ,self.group_columns[:-1]):
                temp_list_rollup+=f"""   COALESCE(LPAD( "{group_column}",{lenght}, '0') ,'{lenght*"0"}'), """
                distinc_on+=f""" "{group_column}" ,"""

            if enumerate_number ==0:
                list_query.append(f'''  DROP TABLE IF EXISTS  {cube_cube_id_reassemble} ''')
                query= f''' CREATE UNLOGGED TABLE IF NOT EXISTS  {cube_cube_id_reassemble}   AS (SELECT DISTINCT ON ({distinc_on}) concat_ws(  '' ,{temp_list_rollup[:-2]}  ,'{(int(self.group_lenghts[-1])-1)*'0'+str(enumerate_number)}') AS index, {'Корень'} AS value  FROM {data_table_temp_index_reassemble} )'''
            else: query= f''' INSERT INTO  {cube_cube_id_reassemble} (SELECT DISTINCT ON ({distinc_on})  concat_ws( '' ,{temp_list_rollup[:-2]}  ,'{  ( int(self.group_lenghts[-1]) -len( str(self.dict_name_col_and_index[group_data_column]) ) ) *'0'+str(self.dict_name_col_and_index[group_data_column])  }') AS index, "{group_data_column}" AS value  FROM {data_table_temp_index_reassemble} )'''  # data_table_temp_index
            list_query.append(query.replace(',)',')'))
        return list_query
        
    def reassemble_del_copys(self, list_query, distinc_on, temp_list_rollup, group_data_column, enumerate_number):

        cube_cube_id_data_index = f'cube_{self.cube_id}_data_assemble_index '
        cube_cube_id_reassemble_template=f'cube_{self.cube_id}_reassemble_template'  # арифмет операц
        cube_cube_id_reassemble=f'cube_{self.cube_id}_reassemble'    # арифмет операц
        cube_cube_id_clearcube= f'cube_{self.cube_id}_clearcube'   
        data_table_temp_index= f"temp_{self.cube_id}_index" 
        value3=f'cube_cube_{self.cube_id}_reassemble_value3' # арифмет операц
        table_with_reassemble_last_coren=  f'cube_cube_{self.cube_id}_coren'
        # list_query.append(f'''  DROP TABLE IF EXISTS  {cube_cube_id_reassemble_template} ''')

        if enumerate_number==0:   
            list_query.append(f'''  DROP TABLE IF EXISTS  {cube_cube_id_reassemble_template} ''')
            list_query.append(f'''  DROP TABLE IF EXISTS  {cube_cube_id_reassemble_template} ''')
            list_query.append(f'''  DROP TABLE IF EXISTS  {value3} ''')
            # новые индесы
            query_BIG=f''' CREATE UNLOGGED TABLE IF NOT EXISTS {cube_cube_id_reassemble_template} AS ( SELECT DISTINCT ON ({distinc_on}) concat_ws(  '' ,{temp_list_rollup[:-2]}  ,'{(int(self.group_lenghts[-1])-1)*'0'+str(enumerate_number)}') AS index, {'Корень'} AS value  '''
            query_BIG+=f''' FROM {data_table_temp_index}    ''' 
            query_BIG+="    );" 
            list_query.append(query_BIG)
        
        else:  
            for name_all_col in self.group_data_columns[1:] : 
                query_BIG=f''' INSERT INTO  {cube_cube_id_reassemble_template}  (SELECT DISTINCT ON ({distinc_on})  concat_ws( '' ,{temp_list_rollup[:-2]}  ,'{  ( int(self.group_lenghts[-1]) -len( str(self.dict_name_col_and_index[name_all_col]) ) ) *'0'+str(self.dict_name_col_and_index[name_all_col])  }') AS index, "{name_all_col}" AS value'''
                query_BIG+=f''' FROM {data_table_temp_index}    ''' 
                query_BIG+="    );" 
                list_query.append(query_BIG)
            # list_query.append( f''' DELETE FROM   {cube_cube_id_reassemble}   ''')
            
        if enumerate_number==0:   
            list_query.append(f'''  DROP TABLE IF EXISTS  {value3} ''')
            query=f''' CREATE UNLOGGED TABLE IF  NOT EXISTS {value3} AS
                        ( SELECT {cube_cube_id_clearcube}.* FROM {cube_cube_id_clearcube} 
                        LEFT OUTER JOIN {cube_cube_id_reassemble_template} as val3  ON {cube_cube_id_clearcube}.index=val3.index
                        WHERE {cube_cube_id_clearcube}.index=val3.index )   
                        '''
            list_query.append(query)
        else:

            query=f'''  INSERT INTO {value3}  
                        ( SELECT {cube_cube_id_clearcube}.* FROM {cube_cube_id_clearcube} 
                        LEFT OUTER JOIN {cube_cube_id_reassemble_template} as val3  ON {cube_cube_id_clearcube}.index=val3.index
                        WHERE {cube_cube_id_clearcube}.index=val3.index )   
                        '''
            list_query.append(query)

        
        if enumerate_number==0:   # для последнего 
            list_query.append(f'''  DROP TABLE IF EXISTS  {table_with_reassemble_last_coren} ''')
            query = f'''   CREATE UNLOGGED TABLE IF NOT EXISTS {table_with_reassemble_last_coren} AS ( SELECT * FROM {cube_cube_id_clearcube}  
                                        WHERE {cube_cube_id_clearcube}.index  =  ANY ( SELECT index FROM  {value3} ) )   '''
            list_query.append(query)
        else:
            query = f'''  INSERT INTO  {table_with_reassemble_last_coren}   ( SELECT * FROM {cube_cube_id_clearcube}  
                                        WHERE {cube_cube_id_clearcube}.index  =  ANY ( SELECT index FROM  {value3} ))    '''
            list_query.append(query)

        query=f''' DELETE FROM {cube_cube_id_clearcube}  
                    WHERE {cube_cube_id_clearcube}.index  =  ANY ( SELECT index FROM  {value3} ) 
                       '''
        
        list_query.append(query)
        # сука самое сложное !!!!!!!!!!!!!!!!!!!!!!!!
        # query_BIG=f''' INSERT INTO  {cube_cube_id_clearcube} (SELECT DISTINCT  COALESCE({value3}.index,    {cube_cube_id_reassemble}.index,  {cube_cube_id_reassemble_template}.index  ) as index  ,
        #                   (COALESCE({value3}.value::float,0) - COALESCE({cube_cube_id_reassemble}.value::float,0) + COALESCE({cube_cube_id_reassemble_template}.value::float,0)) as value FROM {cube_cube_id_reassemble_template} 
        #                 LEFT JOIN  {cube_cube_id_reassemble}  ON {cube_cube_id_reassemble_template}.index={cube_cube_id_reassemble}.index
        #                 LEFT JOIN  {value3}  ON {cube_cube_id_reassemble_template}.index={value3}.index
        #                -- WHERE {cube_cube_id_reassemble_template}.index={cube_cube_id_reassemble}.index AND {cube_cube_id_reassemble_template}.index={value3}.index
        #                   )
                        
        #                 '''
        # list_query.append(query_BIG)

        # query_BIG=f''' INSERT INTO  {cube_cube_id_clearcube} (SELECT DISTINCT  COALESCE(  {cube_cube_id_reassemble_template}.index ,{cube_cube_id_reassemble}.index  )  ,
        #                   ( COALESCE({cube_cube_id_reassemble}.value::float,0) + COALESCE({cube_cube_id_reassemble_template}.value::float,0)) as value 
        #                   FROM {cube_cube_id_reassemble_template} 
        #                 LEFT JOIN  {cube_cube_id_reassemble}  ON {cube_cube_id_reassemble_template}.index={cube_cube_id_reassemble}.index
        #                 LEFT JOIN  {value3}  ON {cube_cube_id_reassemble_template}.index={value3}.index
        #                -- WHERE {cube_cube_id_reassemble_template}.index={cube_cube_id_reassemble}.index AND {cube_cube_id_reassemble_template}.index={value3}.index
        #                   )
                        
        #                 '''
        # list_query.append(query_BIG)
        # if self.without_root:
        #     cube_cube_id_reassemble_template=f'cube_{self.cube_id}_reassemble_template'  # арифмет операц
        #     cube_cube_id_reassemble=f'cube_{self.cube_id}_reassemble'    # арифмет операц
        #     value3=f'cube_cube_{self.cube_id}_reassemble_value3' # арифмет операц
        #     query_BIG=f''' INSERT INTO  {cube_cube_id_clearcube}
        #                     ( SELECT DISTINCT    {cube_cube_id_reassemble_template}.index  as index  ,
        #                     COALESCE({cube_cube_id_reassemble_template}.value::float,0)  as value FROM {cube_cube_id_reassemble_template} 
        #                     )                             '''
        #     list_query.append(query_BIG)
            
        #     query_BIG=f'''  DELETE FROM {cube_cube_id_reassemble_template} '''
        #     list_query.append(query_BIG)

        
        return list_query

    def create_table_analytics_merge(self, itterable_columns, enumerate_number, cube_cube_id_data_index):
        cube_cube_id_analytics_merge=f'cube_{self.cube_id}_analytics_merge'
        cube_cube_id_data_temp=f'cube_{self.cube_id}_data_temp'
        query_create_table= f'''    CREATE UNLOGGED TABLE IF NOT EXISTS {cube_cube_id_analytics_merge} AS (SELECT * FROM  {cube_cube_id_data_temp} )    '''
        return  query_create_table

    def analytics_merge_function(self   ):
        cube_cube_id_analytics_merge=f'cube_{self.cube_id}_analytics_merge'
        pass
    
    def create_where_for_last(self, cube_cube_id_data_temp,group_names_asemble , number ):

        string_name=''
        for i in group_names_asemble:
            string_name+=f'cube_{self.cube_id}_data_assemble."{i}",'
        string_name=string_name[:-1]   #  n7.index AS "год",  n8.index AS "месяц",  n9.index AS "день"
         
        dist_df= DB.query( query = f''' SELECT distinct on("год", "месяц",  "день") "год", "месяц",  "день" FROM 
        ({self.assemble_index} ) as t
         ''', engine=self.engine, return_df=True)
        # dist_df=DB.query(query=f''' SELECT distinct on ({string_name}) n7.index AS "год",  n8.index AS "месяц",  n9.index AS "день" FROM   cube_{self.cube_id}_data_assemble    LEFT OUTER JOIN  cube_133_nodes_axis_8 n9 USING(  "год", "месяц", "день" ) \n LEFT OUTER JOIN  cube_133_nodes_axis_8 n8 USING(  "год", "месяц" ) \n LEFT OUTER JOIN  cube_133_nodes_axis_8 n7 USING(  "год" ) ''',engine=DB.e, return_df=True)
        # dist_df=pd.concat([dist_df, pd.DataFrame({'год':['2021','2022','2021','2023'],'месяц':['02','02','05','12'],'день':['06','07','08','12']})])
        # dist_df['год']=dist_df['год'].astype(str)
        dist_df['test']=1
        if number==0:
            dist_df2=dist_df.groupby(['месяц','день']).agg({'test':sum})
            dist_df2
            g=dist_df2['test'].groupby('месяц', group_keys=False)
            g=g.apply(lambda x: x.sort_values(ascending=True).tail(1))
            g=g.reset_index()
            g=g.drop(['test'],axis=1)
            strafs=''
            for i in g.T.to_dict().values():
                strafs+= f''' ( "месяц"='{i['месяц']}'  and "день"='{i['день']}'  ) or'''
            strafs=strafs[:-2]
            return strafs
        if number==1:
            dist_df=dist_df.sort_values(by=["год","месяц","день"])
            dist_df=dist_df.drop(['test'],axis=1)
            dist_df=dist_df.sort_values(by=["год","месяц","день"])
            dist_df2=dist_df[['год','месяц',"день"]].groupby(['год']).last().reset_index()  # 'год'
            dist_df2
            
            g=dist_df2.reset_index()

            strafs=''
            for i in g.T.to_dict().values():
                strafs+= f''' ( "год"='{i['год']}'   and "месяц"='{i['месяц']}'  and "день"='{i['день']}'  ) or'''
            strafs=strafs[:-2]
            return strafs
        if number==2:
            dist_df=dist_df.sort_values(by=["год","месяц","день"])
            dist_df=dist_df.drop(['test'],axis=1)
            dist_df=dist_df.sort_values(by=["год","месяц","день"])
            g=dist_df.groupby(['год']).last().reset_index()  # 'год'

            strafs=''
            for i in g.T.to_dict().values():
                # strafs+= f''' ( "год"='{i['год']}'   and "месяц"='{i['месяц']}'  and "день"='{i['день']}'  ) or'''
                strafs+= f''' (  "месяц"='{i['месяц']}'  and "день"='{i['день']}'  ) or'''
            strafs=strafs[:-2]
            return strafs

    def create_main_querys(self, drop_axis=True):

        
        cube_cube_id_data= f'cube_{self.cube_id}_data_assemble' # таблицы с начальными данными
        cube_cube_id_data_index = f'cube_{self.cube_id}_data_assemble_index' # для создания таблицы из индексов в место всех начальных значений
        cube_cube_id_clearcube= f'cube_{self.cube_id}_clearcube'
        cube_cube_id_data_temp=f'cube_{self.cube_id}_data_temp'
        cube_cube_id_reassemble_template=f'cube_{self.cube_id}_reassemble_template'
        cube_cube_id_reassemble=f'cube_{self.cube_id}_reassemble'
        cube_cube_id_analytics_merge=f'cube_{self.cube_id}_analytics_merge'        
        
        flag_union_all=False
        last_analytic=False # если аналитик "последний"
        last_analytic_number=0

        list_query=[   ]
        list_query.append(f'''  DROP TABLE IF EXISTS  {cube_cube_id_data_index} ''')
        list_query.append(self.create_data_assemble_index()) 

        if self.reassemble: self.reassemble_index_leaves(list_query)
        
 
        dict_name_col_and_index={ i['columns'][0]:i['id'] for i in galileo.cubes.get_structure(engine=self.engine, cube_id=self.cube_id)['data']['axis']   if  'Столбец данных' in i['columns']}
        
        df_name_nodes_columns=DB.query(query=f"""SELECT name , index FROM  cube_{self.cube_id}_nodes_2  where axis={dict_name_col_and_index['Столбец данных']} """ , engine=self.engine , return_df=True )
        for name, index in zip(df_name_nodes_columns['name'].to_list(), df_name_nodes_columns['index'].to_list()):
            dict_name_col_and_index[name]=index
        # список всех нужных столбцов на каждую итерацию цикла 
        group_names_all=list(chain.from_iterable(self.group_names))
        striing_group_names= ' '
        for k in group_names_all:
            striing_group_names+=f'"{k}"'+','
        striing_group_names=striing_group_names[:-1] 
        # список из строк
            # что в строке: "аналитик1","аналитик2",...,(либо Корень т.е. сумма столбцов которую мы формировали ранне либо название столбца с данными по счету ) 
            # эта строка пойдет в SELECT {...} FROM 
        all_columns_Data_to_itterable_columns= f''
        for name_data in self.group_data_columns[1:]:
            all_columns_Data_to_itterable_columns += f',"{name_data}"'
        all_columns_Data_to_Group_By= f''
        for name_data in self.group_data_columns[1:]:
            all_columns_Data_to_Group_By += f',SUM("{name_data}"::float) as "{name_data}"'
        itterable_columns= list(map( lambda x:  striing_group_names+ ' ' +all_columns_Data_to_itterable_columns   if x!=0  else  striing_group_names+ f', {self.group_data_columns[x]} AS Корень'  , range(len(self.group_data_columns[:2]))))
        # цикл по кол-ву солбцов с данными +1 (плюс один это Корень)
        for enumerate_number, group_data_column in enumerate(self.group_data_columns_name_origin[:2]): # измнили подход теперь идет корень и все столбцы данных !!!!!!!!!!
            # удалаяем промежуточную таблицу , она нужна только из за того что мы идем по кадому столбцу Данных  
            list_query.append(f'''  DROP TABLE IF EXISTS  {cube_cube_id_data_temp} ''')
            # создаем промежуточную таблицу 
            list_query.append(f'''  CREATE UNLOGGED TABLE IF NOT EXISTS {cube_cube_id_data_temp} AS (SELECT {itterable_columns[enumerate_number]} FROM  {cube_cube_id_data_index} ) ''')
            
            # удаляем пустые или нуливые значения 
            list_query.append(f"""DELETE  FROM {cube_cube_id_data_temp} WHERE   "{group_data_column}" IS NULL;""")
            # добавялем в промежуточнуцю таблицу сгруппированные значения 
            query_BIG= f''' INSERT INTO {cube_cube_id_data_temp}  SELECT '''
            # состяавляется SELECT 
            # но самое главное , когда группируется аналитики ([x3,x2,x1] от корня-> к ->листьям), то удаляется самый первый (то есть лист, "листья") ,при ROLLUP его нужно убирать, а  при SELECT запросе нужно превратить в дефолтное пустое значение 
            # пример 
                    # SELECT x3 , x2 , NULL as x1 FROM <table>   GROUP BY ROLLUP(x3,x2)
            # самый ебучий кейс если аналитик выглядит так [x1] то  
            #                                                       SELECT NULL as x1 FROM <table>   GROUP BY              
                                                                                                            # ROLLUP убирается нахер отсюда 
            # более подробный пример [x3,x2,x1], [y3,y2,y1] ( от корня-> к ->листьям )   и столбец данных не забываем  values
            # самый первый не корневой запрос запрос будет: 
            #       SELECT x3 , x2 , NULL as x1, y3,y2,y1   , SUM(values) as values FROM <table>   GROUP BY  y3,y2,y1 , ROLLUP(x3,x2)
            # если  [x1] то
            #       SELECT NULL as x1, y3, y2, y1, SUM(values) as values FROM <table>   GROUP BY  y3,y2,y1 
            # при этом все это еще в INSERT чтобы агрегировать и сразу добавлять 
            group_names_asemble=self.group_names.copy()
            # dis_assemble=False
            list_dis_assemble=[]
            try:
                for i in self.dict_no_agg[group_data_column]:
                    if i in group_names_asemble: 
                        group_names_asemble.remove(i)
                        list_dis_assemble.append(i)
            except:
                pass

            temp_a=0
            break_flag=False
            temp_check_create_table=0
            if self.analytics_merge :
                list_analytics_merge=[]
                
            if self.analytics_merge :
                group_names_asemble.append(['х'])
                self.group_columns.append('х')
                
                list_analytics_merge.append('х')
                self.analytics_merge.append('х')

            # print('self.analytics_merge ', self.analytics_merge)
            for name_number, name_an in enumerate(group_names_asemble):
                temp_str=''
                # print('name_an ', name_an)
                for group_name, group_column in zip(group_names_asemble, self.group_columns[:-1]):
                     
                    if group_name[-1] in  self.analytics_merge  and  name_an[-1] in  self.analytics_merge and  (group_name[-1] != self.analytics_merge[temp_a] or  self.analytics_merge[-1]==group_name[-1]):

                        if temp_check_create_table==0:
                        
                            temp_check_create_table+=1
                            list_query.append(f'''  DROP TABLE IF EXISTS  {cube_cube_id_analytics_merge} ''')
                            list_query.append(self.create_table_analytics_merge(itterable_columns=itterable_columns, enumerate_number=enumerate_number, cube_cube_id_data_index=cube_cube_id_data_index))
                             
                        query_BIG= f''' INSERT INTO {cube_cube_id_data_temp}   SELECT '''
                        self.bool_access_merge=True
                        list_analytics_merge.append(group_name[-1])
                        
                        if group_name[-1]==self.analytics_merge[-1]:
                        
                            query_BIG= f''' INSERT INTO {cube_cube_id_data_temp}   SELECT '''
                            self.bool_access_merge=True
                            list_analytics_merge.append(group_name[-1])
                        
                            if  'х' not in  self.group_columns:
                        
                                group_names_asemble.append(['х'])
                                self.group_columns.append('х')
                                list_analytics_merge.append('х')
                                self.analytics_merge.append('х')
                    
                    if  name_an[-1]=='x':
                        self.bool_access_merge=True
                        
                    if group_column in self.list_name_last_analytic and group_names_asemble[name_number]== group_name:# если аналитик "последний"
                            last_analytic=True
                             

                    if group_names_asemble[name_number]== group_name:# and not last_analytic:
                       

                        if group_name[:-1]:
                            temp_tuple = f'''{tuple(group_name[:-1])}, NULL as "{group_name[-1]}"  , '''.replace("(","").replace(")","")

                        elif   group_name[-1] in  self.analytics_merge:
                            self.bool_access_merge=True
                            temp_tuple = f'''    "{group_name[-1]}"  , '''.replace("(","").replace(")","") # а тут не было null as

                        else:
                            temp_tuple = f''' NULL as "{group_name[-1]}"  , '''.replace("(","").replace(")","")
                 

                    else:
                         
                        if group_name[-1] in  self.analytics_merge and (self.bool_access_merge  or name_an[-1] =='х' ): # or group_name[-1] ==     [qwerty[-1] for qwerty in group_names_asemble if qwerty[-1] in self.analytics_merge][0]
                            # print('group_name[-1]', group_name[-1], '   self.analytics_merge     ', self.analytics_merge, '   self.bool_access_merge    ', self.bool_access_merge)
                            # print( group_name[-1] in  self.analytics_merge and (self.bool_access_merge  or name_an[-1] =='х' ))
                            
                            temp_tuple = f'  NULL as   "{group_name[-1]}",'.replace("(","").replace(")","").replace('""','"').replace('""','')  # NULL as

                        else:
                            # print('group_name[-1]', group_name[-1], '   self.analytics_merge     ', self.analytics_merge, '   self.bool_access_merge    ', self.bool_access_merge)
                            # print( group_name[-1] in  self.analytics_merge and (self.bool_access_merge  or name_an[-1] =='х' ))
                            temp_tuple = f"{tuple(group_name)},".replace("(","").replace(")","").replace('""','"').replace('""','')
                    
                    if last_analytic and last_analytic_number==0: 
                        
                        last_analytic_number+=1
                        list_duplicates=[]
                        list_duplicates.append(temp_tuple)
                        
                        for number, last_name in enumerate(group_name[:-1] , 2):
                        
                            string_1=f"""{tuple(group_name[:-number])}""".replace('()','').replace("(","").replace(")","").replace("'",'"')
                            string_2= f"""{tuple([f' NULL as "{group_name[-number:][ty]}"  ,'  for ty in range(len(group_name[-number:])) ])}"""[1:-1].replace("', '",'').replace("'",'')
                            list_duplicates.append(string_1+string_2)
                    
                    temp_str += f""" {temp_tuple}  """.replace("'",'"').replace(",,",',').replace(",)",')')
         
                if list_dis_assemble:
                        
                        for list_dis in list_dis_assemble:
                            if len(list_dis)==1:
                                temp_str+= f' NULL as {list_dis[-1]} ,'
                            else:
                                for dis in list_dis:
                                    temp_str+= f' NULL as {dis} ,'
                if break_flag:
                            break


                query_BIG += temp_str
                temp_list_str=''

                if not self.bool_access_merge:
                # if True:
                    for n , mini_val in enumerate(group_names_asemble):

                        if n != name_number:

                            temp_list_str+= f""" {tuple(mini_val)}"""+""",""".replace("(",'').replace(")",'').replace(",,",',').replace(",)", ")").replace("'",'"')
                else:

                    for n , mini_val in enumerate(group_names_asemble):

                            if mini_val[-1] not in self.analytics_merge :

                                temp_list_str+= f""" {tuple(mini_val)}"""+""",""".replace("(",'').replace(")",'').replace(",,",',').replace(",)", ")").replace("'",'"')

                            if mini_val ==  group_names_asemble[name_number] : 

                                temp_list_str+= f""" {tuple(mini_val)}"""+""",""".replace("(",'').replace(")",'').replace(",,",',').replace(",)", ")").replace("'",'"')

                temp_list_str=temp_list_str[:-1]
                rec = 'Корень' if enumerate_number==-1 else group_data_column
                
                if name_number ==0 :
                    create_index_strung= f' CREATE  INDEX idx_cube_{self.cube_id} ON {cube_cube_id_data_temp}  {tuple(group_names_all)}   ; '.replace("'",'"')
                    
                # для Корня
                if not self.bool_access_merge:
                
                    if rec== 'Корень':
                
                        if last_analytic :#and rec != 'Корень': # условие абсурд я знаю 
                
                            for number, i in enumerate(list_duplicates):
                
                                string_where= self.create_where_for_last(cube_cube_id_data_temp=cube_cube_id_data_temp,group_names_asemble=group_names_asemble[name_number], number=number)
                
                                if number==0:
                
                                    temp=query_BIG + f'''   SUM("{group_data_column}") AS "{rec}"  FROM {cube_cube_id_data_temp}  ''' 
                                    temp=temp.replace('" "', '"').replace("'",'"').replace(');', ';').replace(',)', ')')  # .replace("'",'"')
                                    temp=temp+ f'WHERE {string_where} '.replace('()','')
                                    temp=temp+f''' GROUP BY  {temp_list_str}  ,  {tuple(group_names_asemble[name_number][:-1])}  '''.replace('" "', '"').replace("'",'"').replace(');', ';').replace(',)', ')').replace(',  ()','')  # .replace("'",'"')
                                     
                                    list_query.append(temp.replace(',   WHERE','  WHERE '))
                
                                else:
                                    
                                    temp=query_BIG + f'''   SUM("{group_data_column}") AS "{rec}"  FROM {cube_cube_id_data_temp} '''  
                                    temp=temp.replace(list_duplicates[0].replace("'",'"'),list_duplicates[number])
                                    temp=temp.replace('" "', '"').replace("'",'"').replace(');', ';').replace(',)', ')') # .replace("'",'"')
                                    # if number!=2:
                                    temp=temp+f'WHERE {string_where} '.replace('()','').replace('()','').replace(',   WHERE','  WHERE ')
                                    temp=temp+f'''GROUP BY  {temp_list_str}  ,  {tuple(group_names_asemble[name_number][:-(number+1)])} '''.replace('" "', '"').replace("'",'"').replace(');', ';').replace(',)', ')').replace(',  ()','')
                                    list_query.append(temp.replace(',   WHERE','  WHERE '))
                                
                        elif name_number==0: 
                
                            try:
                                query_BIG+= f'''   SUM("{group_data_column}") AS "{rec}"  FROM {cube_cube_id_data_temp}   GROUP BY  {temp_list_str}  ,  ROLLUP {tuple(group_names_asemble[name_number][:-1])} );''' 
                            except:
                                query_BIG+= f'''   SUM("{group_data_column}") AS "{rec}"   FROM {cube_cube_id_data_temp}   GROUP BY  {temp_list_str}    ; '''
                        # для всех остальных 
                        else: 
                
                            try:
                                query_BIG+= f'''   SUM("{group_data_column}") AS "{rec}"   FROM {cube_cube_id_data_temp}   GROUP BY  {temp_list_str} ,  ROLLUP {tuple(group_names_asemble[name_number][:-1])}   ; '''
                            except:
                                query_BIG+= f'''   SUM("{group_data_column}") AS "{rec}"   FROM {cube_cube_id_data_temp}   GROUP BY  {temp_list_str}    ; '''
                            
                    else:   
                
                        if last_analytic: 
                
                            for number, i in enumerate(list_duplicates):
                
                                string_where= self.create_where_for_last(cube_cube_id_data_temp=cube_cube_id_data_temp,group_names_asemble=group_names_asemble[name_number], number=number)
                
                                if number==0:
                
                                    temp=query_BIG + f'''   {all_columns_Data_to_Group_By[1:]}   FROM {cube_cube_id_data_temp} ''' 
                                     
                                    temp=temp.replace('" "', '"').replace("'",'"').replace(');', ';').replace(',)', ')')  # .replace("'",'"')
                                    temp=temp+f'WHERE {string_where} '.replace('()','').replace('()','').replace(',   WHERE','  WHERE ').replace(',  ()','')
                                    temp=temp+f''' GROUP BY  {temp_list_str} ,   {tuple(group_names_asemble[name_number][:-1])}   '''.replace('" "', '"').replace("'",'"').replace(');', ';').replace(',)', ')').replace(',  ()','')
                                    list_query.append(temp.replace(',   WHERE','  WHERE '))
                
                                else:
                
                                    temp=query_BIG +  f'''   {all_columns_Data_to_Group_By[1:]}   FROM {cube_cube_id_data_temp} '''  
                                    
                                    temp=temp.replace(list_duplicates[0].replace("'",'"'),list_duplicates[number])
                                    temp=temp.replace('" "', '"').replace("'",'"').replace(');', ';').replace(',)', ')') # .replace("'",'"')
                                    # if number!=2:
                                    #     print('тут новое')
                                    temp=temp+f'WHERE {string_where}   '.replace('()','').replace('()','').replace(',   WHERE','  WHERE ').replace(',  ()','')
                                    temp=temp+f''' GROUP BY  {temp_list_str} ,    {tuple(group_names_asemble[name_number][:-(number+1)])}  '''.replace('" "', '"').replace("'",'"').replace(');', ';').replace(',)', ')').replace(',  ()','')
                                    list_query.append(temp.replace(',   WHERE','  WHERE '))
                                
                        else:
                            query_BIG+= f'''   {all_columns_Data_to_Group_By[1:]}   FROM {cube_cube_id_data_temp}   GROUP BY  {temp_list_str} ,  ROLLUP {tuple(group_names_asemble[name_number][:-1])}   ; '''

                else:# тут меняется только название табилцы 
                
                    flag_union_all=True 
                
                    if rec== 'Корень':
                
                        query_BIG+= f'''   SUM("{group_data_column}") AS "{rec}"  FROM {cube_cube_id_analytics_merge}   GROUP BY  {temp_list_str}  ,  ROLLUP {tuple(group_names_asemble[name_number][:-1])}   ; '''
                
                    else: 
                
                         query_BIG+= f'''   {all_columns_Data_to_Group_By[1:]}  FROM {cube_cube_id_analytics_merge}   GROUP BY  {temp_list_str}  ,  ROLLUP {tuple(group_names_asemble[name_number][:-1])}   ; '''



                query_BIG=query_BIG.replace('" "', '"').replace("'",'"').replace(');', ';').replace(',)', ')').replace(', (""), ("")', '').replace('NULL as "х"  , ','').replace(', ("х")', '').replace(', ("х")','').replace('"х"  ,', '').replace('NULL as "х",','').replace('NULL as   "х",','').replace(' "х",','')
                query_BIG=query_BIG.replace('"Розничное страхование",     NULL as   "Банкострах",     NULL as   "нефтян отр",       "Авиационная отрасль"  ,',' NULL as "Розничное страхование",     NULL as   "Банкострах",     NULL as   "нефтян отр",       "Авиационная отрасль"  ,')
                query_BIG=query_BIG.replace('NULL as    NULL', 'NULL' )
                
                if not last_analytic: 
                
                    list_query.append(query_BIG)
                
                last_analytic=False
                
                if not self.bool_access_merge:
                
                    query_BIG= f''' INSERT INTO {cube_cube_id_data_temp}   SELECT '''
                
                else:
                
                    query_BIG= f''' INSERT INTO {cube_cube_id_data_temp}   SELECT '''

                if self.bool_access_merge:
                
                    temp_a+=1
                    self.bool_access_merge=False
                    # break
            

            if flag_union_all: # cube_cube_id_analytics_merge    cube_cube_id_data_temp
                
                # union_all= f''' INSERT INTO {cube_cube_id_data_temp}   SELECT * FROM {cube_cube_id_analytics_merge}  '''
                # ttt= f''' 
                #                         INSERT INTO cube_113_data_temp  
                #                         SELECT  "Филиал Хайпирион",  
                #                         "Ответственный Руководитель Хайпи",  
                #                             "Линия Бизнеса",   "Компания",   "Профильная Программа Хайпирион",  
                #                             "Страховой Продукт Хайпирион",   "статья",     NULL as   "Андеррайтинг спец рисков",   
                #                                 NULL as   "Дир по розн банкострах",     NULL as   "Корп продажи рег сети",   
                #                                     NULL as   "Нефтяная отрасль",      NULL as  "Гос компании"  ,     SUM("{group_data_column}") AS "{rec}"
                #                                         FROM cube_113_analytics_merge   
                #                                         GROUP BY   ("Филиал Хайпирион"), ("Ответственный Руководитель Хайпи"),
                #                                         ("Линия Бизнеса"), ("Компания"), ("Профильная Программа Хайпирион"),
                #                                             ("Страховой Продукт Хайпирион"), ("статья")    
                                        

                #                         '''
                # list_query.append(ttt)
                pass
            # после составления агрегированных данных делаем следующее
            temp_str=''
            for group_name, group_column in zip(self.group_names, self.group_columns[:-1]):
                temp_tuple=f"{tuple(group_name)},".replace("(","").replace(")","")
                temp_str+= f"""  COALESCE{tuple(group_name[::-1])} AS "{group_column}", """
                temp_str=temp_str.replace("'",'"').replace(",,",',').replace(",)",')')
            temp_str=temp_str[:-2]
            # промежуточная таблица в которой будут хранится оригинальные индексы  -> data_table_temp_index
                # ПРИМЕР           таблица которая получилась выше->    | x3 | x2 | x1 | -> получится так | x  |  это и есть "промежуточная таблица"
                #                                                       | 02 | 01 | 07 |                  | 07 |
                #                                                       | 02 | 01 | 02 |                  | 02 |
                #                                                       | 02 | 01 |NAN |                  | 01 |
                #                                                       | 02 |NAN |NAN |                  | 02 |
                #                                                       |NAN |NAN |NAN |                  | 00 | -> дефолтное значение
                # COALESCE(LPAD( "{group_column}",{lenght}, '0') ,'{lenght*"0"}'),  
                # COALESCE   -> выбирает первое не NAN значение , если все NAN то самое первое знчение которое мы ставим по дефолту 
                # LPAD -> добавляет нули слева до тех пор пока не будет нужной длины 
                #'CREATE TABLE IF NOT EXISTS temp_81_index AS (SELECT  DISTINCT    COALESCE("Подразделение 1го уровня", "Основное подразделение", "department") AS "Основное подразделение_1",   COALESCE("Куратор", "name_user_id_access") AS "Куратор_1",   COALESCE("Дата") AS "Дата ",   COALESCE("Территория") AS "Территория ",   "НГД"  FROM cube_81_data_temp )',
            data_table_temp_index= f"temp_{self.cube_id}_index" 
            list_query.append(f""" DROP TABLE IF EXISTS  {data_table_temp_index}""")
            if rec=='Корень':
                query_create_temp_index= f"""CREATE UNLOGGED TABLE IF NOT EXISTS {data_table_temp_index} AS (SELECT  DISTINCT  {temp_str} , "{rec}"  FROM {cube_cube_id_data_temp} )"""
            else:
                query_create_temp_index= f"""CREATE UNLOGGED TABLE IF NOT EXISTS {data_table_temp_index} AS (SELECT  DISTINCT  {temp_str}  {all_columns_Data_to_itterable_columns}  FROM {cube_cube_id_data_temp} )"""
             
            list_query.append(query_create_temp_index)
            
            temp_list_rollup=''
            distinc_on=''

            # COALESCE(LPAD( "{group_column}",{lenght}, '0') ,'{lenght*"0"}'),  
            # COALESCE   -> выбирает первое не NAN значение , если все NAN то самое первое знчение которое мы ставим по дефолту 
            # LPAD -> добавляет нули слева до тех пор пока не будет нужной длины 
            #   ' INSERT INTO  cube_81_clearcube (SELECT DISTINCT ON ( "Основное подразделение_1" , "Куратор_1" , "Дата " , "Территория " )  concat_ws( \'\' ,   COALESCE(LPAD( "Основное подразделение_1",5, \'0\') ,\'00000\'),    COALESCE(LPAD( "Куратор_1",4, \'0\') ,\'0000\'),    COALESCE(LPAD( "Дата ",4, \'0\') ,\'0000\'),    COALESCE(LPAD( "Территория ",3, \'0\') ,\'000\')  ,\'002\') AS index, "НГД" AS value FROM temp_81_index        );',
            for group_names_join_node, lenght, group_column  in zip(self.group_names_join_nodes[:-1], self.group_lenghts[:-1] ,self.group_columns[:-1]):
                temp_list_rollup+=f"""   COALESCE(LPAD( "{group_column}",{lenght}, '0') ,'{lenght*"0"}'), """
                distinc_on+=f""" "{group_column}" ,"""
            distinc_on=distinc_on[:-1]
            temp_list_name_anal=''
             # это вред не использется , было раньше
            for n , name_anal in zip(self.group_names_join_nodes[:-1], self.group_columns[:-1]):
                temp_list_name_anal+=f'''  LEFT JOIN cube_{self.cube_id}_nodes_2 {n} ON {data_table_temp_index}."{name_anal}" ={n}.name and  {n}.axis={n[1:]} '''
            # это создаются непосредственно индексы 
            

            if not self.reassemble:
                
                if enumerate_number==0:   
                    
                    list_query.append(f'''  DROP TABLE IF EXISTS  {cube_cube_id_clearcube} ''')
                    list_query.append(f'''  CREATE UNLOGGED TABLE  IF NOT EXISTS  {cube_cube_id_clearcube}
                                                                (
                                                                    index  VARCHAR(512) PRIMARY KEY,
                                                                    value FLOAT 
                                                                )
                                                                ''')
                    list_query.append(f'''  DROP TABLE  IF  EXISTS  {cube_cube_id_clearcube}_{str(enumerate_number)}        ''')
                    
                    list_query.append(f'''  CREATE UNLOGGED TABLE  IF NOT EXISTS  {cube_cube_id_clearcube}_{str(enumerate_number)}
                                                                (
                                                                    index  VARCHAR(512) PRIMARY KEY,
                                                                    value FLOAT 
                                                                )
                                                                ''')
                    query_BIG=f''' insert into {cube_cube_id_clearcube}_{str(enumerate_number)}  
                    ( SELECT DISTINCT ON ({distinc_on}) concat_ws(  '' ,{temp_list_rollup[:-2]}  ,
                                    '{(int(self.group_lenghts[-1])-1)*'0'+str(enumerate_number)}') AS index, {'Корень'} AS value  '''
                    query_BIG+=f''' FROM {data_table_temp_index}    ''' # {temp_list_name_anal}
                    query_BIG+="    );" 
                    list_query.append(query_BIG)
                    list_query.append(f'''  ALTER TABLE {cube_cube_id_clearcube}_{str(enumerate_number)} INHERIT  {cube_cube_id_clearcube}  ''')
            
                else:  
                    for name_all_col in self.group_data_columns[1:] : 
                        
                        list_query.append(f'''  DROP TABLE  IF  EXISTS  {cube_cube_id_clearcube}_{str(dict_name_col_and_index[name_all_col])}        ''')
                    
                        list_query.append(f'''  CREATE UNLOGGED TABLE  IF NOT EXISTS  {cube_cube_id_clearcube}_{str(dict_name_col_and_index[name_all_col])}
                                                                (
                                                                    index  VARCHAR(512) PRIMARY KEY,
                                                                    value FLOAT 
                                                                )
                                                                ''')
                        
                        query_BIG=f''' INSERT INTO  {cube_cube_id_clearcube}_{str(dict_name_col_and_index[name_all_col])} 
                        (
                            SELECT DISTINCT ON ({distinc_on})  
                                concat_ws( '' ,{temp_list_rollup[:-2]}  ,
                '{  ( int(self.group_lenghts[-1]) -len( str(dict_name_col_and_index[name_all_col]) ) ) *'0'+str(dict_name_col_and_index[name_all_col])  }') AS index,
                                    "{name_all_col}" AS value'''
                        query_BIG+=f''' FROM {data_table_temp_index}    ''' # {temp_list_name_anal}
                        query_BIG+="    );" 
                        list_query.append(query_BIG)
                        list_query.append(f'''  ALTER TABLE {cube_cube_id_clearcube}_{str(dict_name_col_and_index[name_all_col])} INHERIT  {cube_cube_id_clearcube}  ''')
            
            else: 
                list_query= self.reassemble_del_copys(list_query, distinc_on, temp_list_rollup, group_data_column, enumerate_number )
                
            # делаем столбец PK
            if enumerate_number==0 and   not self.reassemble : 
                # list_query.append(f'''ALTER TABLE {cube_cube_id_clearcube} ADD PRIMARY KEY (index) ''')
                pass
                
        # тут убираем ROLLUP если сука аналитик  выглядит [x1]
        for i in range(len(list_query)):
            list_query[i]=list_query[i].replace('""', '"').replace('" "', '"').replace("0", '0').replace(",,", ',').replace(',  ROLLUP ()',  '   ')


        name_dict_df_nodes_and_axis={ i['name']:i['id'] for i in self.structure['axis']}


        if self.reassemble and not self.without_root: 
            cube_cube_id_reassemble_template=f'cube_{self.cube_id}_reassemble_template'  # арифмет операц
            cube_cube_id_reassemble=f'cube_{self.cube_id}_reassemble'    # арифмет операц
            value3=f'cube_cube_{self.cube_id}_reassemble_value3' # арифмет операц
            if self.list_name_last_analytic:
                query_BIG=f''' INSERT INTO  {cube_cube_id_clearcube} 
                                ( 
                
                                SELECT DISTINCT  
                                
                                    COALESCE(  {value3}.index,  {cube_cube_id_reassemble}.index,  {cube_cube_id_reassemble_template}.index  ) as index  ,
                                    
                                        ( COALESCE({value3}.value::float,0) - COALESCE({cube_cube_id_reassemble}.value::float,0) + COALESCE({cube_cube_id_reassemble_template}.value::float,0) )  as value 
                                        
                                            FROM {cube_cube_id_reassemble_template} 
                                                LEFT JOIN  {cube_cube_id_reassemble}  ON {cube_cube_id_reassemble_template}.index  =  {cube_cube_id_reassemble}.index
                                
                                                LEFT JOIN  {value3}  ON {cube_cube_id_reassemble_template}.index  =  {value3}.index 
                                                
                                                    WHERE   {value3}.index  LIKE '00000000000000000000%'   or  
                                                            {cube_cube_id_reassemble}.index   LIKE '00000000000000000000%'   or  
                                                            {cube_cube_id_reassemble_template}.index   LIKE '00000000000000000000%'   
                                )
                                
                                '''
                list_query.append(query_BIG)
                query_BIG=f''' INSERT INTO  {cube_cube_id_clearcube}  
                                (
                                    SELECT DISTINCT
                                                    {cube_cube_id_reassemble_template}.index   as index  ,
                                                    (  COALESCE(   {cube_cube_id_reassemble_template}.value::float,0  )   ) as value 
                                                    
                                                    FROM {cube_cube_id_reassemble_template} 
                                                    
                                                        WHERE {cube_cube_id_reassemble_template}.index   NOT  LIKE '00000000000000000000%'  
                                )
                                '''
                list_query.append(query_BIG)
            else:
                query_BIG=f''' INSERT INTO  {cube_cube_id_clearcube}
                
                            ( 
                                    SELECT DISTINCT
                                    
                                            COALESCE({value3}.index,    {cube_cube_id_reassemble}.index,  {cube_cube_id_reassemble_template}.index  ) as index  ,
                                    
                                            ( COALESCE({value3}.value::float, 0 ) - COALESCE({cube_cube_id_reassemble}.value::float, 0 ) + COALESCE( {cube_cube_id_reassemble_template}.value::float, 0  )   )  as value 
                                    
                                                FROM {cube_cube_id_reassemble_template} 
                                                    
                                                    LEFT JOIN  {cube_cube_id_reassemble}  ON {cube_cube_id_reassemble_template}.index={cube_cube_id_reassemble}.index
                                                    
                                                    LEFT JOIN  {value3}  ON {cube_cube_id_reassemble_template}.index={value3}.index 
                              
                            )
                                '''
                list_query.append(query_BIG)
                


        if self.without_root:
            cube_cube_id_reassemble_template=f'cube_{self.cube_id}_reassemble_template'  # арифмет операц
            cube_cube_id_reassemble=f'cube_{self.cube_id}_reassemble'    # арифмет операц
            value3=f'cube_cube_{self.cube_id}_reassemble_value3' # арифмет операц
            query_BIG=f''' 
                            INSERT INTO  {cube_cube_id_clearcube}
                            ( 
                                    SELECT DISTINCT    
                                    
                                        {cube_cube_id_reassemble_template}.index  as index  ,
                                    
                                        COALESCE( {cube_cube_id_reassemble_template}.value::float, 0 )  as value 
                                    
                                    FROM {cube_cube_id_reassemble_template} 
                            )                             '''
            list_query.append(query_BIG)
            
            query_BIG=f'''  DELETE FROM {cube_cube_id_reassemble_template} '''
            list_query.append(query_BIG)

        # в конце удаляем промежутоные табилцы которые раньше хранились в перменной nodes_df, да и щас хранятся , они нцжны для того чтобы заменить значения аналитиков на инедксы 
        if  drop_axis:
            list_query.append(f'''  DROP TABLE IF  EXISTS  {cube_cube_id_analytics_merge} ''')
            list_query.append(f'''  DROP TABLE IF  EXISTS  cube_cube_{self.cube_id}_reassemble_value3 ''')
            list_query.append(f'''  DROP TABLE IF  EXISTS  cube_{self.cube_id}_reassemble ''')
            list_query.append(f'''  DROP TABLE IF  EXISTS  cube_{self.cube_id}_reassemble_template''')   
            list_query.append(f'''  DROP TABLE IF  EXISTS   {data_table_temp_index}''')     
            list_query.append(f'''  DROP TABLE IF  EXISTS   {cube_cube_id_data_temp}''')      
            list_query.append(f'''  DROP TABLE IF  EXISTS   temp_{self.cube_id}_index''')      
            list_query.append(f'''  DROP TABLE IF  EXISTS    cube_{self.cube_id}_data_assemble_index  ''')      
            list_query.append(f'''  DROP TABLE IF  EXISTS   cube_{self.cube_id}_data_assemble    ''')        
            list_query.append(f'''  DROP TABLE IF  EXISTS   {cube_cube_id_analytics_merge}    ''')        
            for group_column  , group_name in zip(self.group_columns[:-1], self.group_names ):
                list_query.append(f'''  DROP TABLE IF  EXISTS  cube_{self.cube_id}_nodes_axis_{name_dict_df_nodes_and_axis[group_column]}    ''')
            
        return list_query

""" 

ВСЁ
༼ つ ಥ_ಥ ༽つ

"""



# def main_function(self,  df,group_combinations_df, structure,
#                     group_names,  group_columns, nodes_df_list, 
#                     data_columns_aggregation, original_data_columns,
#                     data_columns_operations,  month_columns, cube_id, 
#                     cube_name, start_time_aggregate, engine, user_id , df_list_name_columns_after_function_index   , list_name_origin_df , reassemble=False   , data_columns_preoperations=False  ):
    
def main_function(self, engine , user_id, cube_id, group_columns=None, group_names=None, without_root=True,reassemble=True, return_query=False ):



# DB.query(query=  f'''    UPDATE  test_index_cube_test_today SET index = concat_ws('',left(index, -3), '_' ,right(index, 3) )              '''  ,engine=DB.e, return_df=False)
    percent=60
    a =25
    
    if not group_names:
        structure_response = galileo.cubes.get_structure(   cube_id=cube_id, 
                                                        engine=engine, 
                                                        convert=True, 
                                                        old_format = False, 
                                                        user_id = None)
        group_names = structure_response['data']['group_names']
        
    if not group_columns:
        
         
        structure_response = galileo.cubes.get_structure(   cube_id=cube_id, 
                                                        engine=engine, 
                                                        convert=True, 
                                                        old_format = False, 
                                                        user_id = None)
        structure = structure_response['data']['structure']
     
        group_columns = []
        for group in structure['axis']: group_columns.append(group['columns'])
        
        
    
    temp=Sql_cube_created(  engine= engine, 
                            user_id= user_id, 
                            cube_id= cube_id, 
                            group_columns= group_columns, 
                            group_names= group_names,
                            reassemble=reassemble,
                            without_root=without_root  )
    try:
        list_query = temp.create_main_querys()
    except Exception as e:
        asdas= traceback.format_exc()
        return {'code': 0 , 'message': f'{str(e)}', 'asdas': asdas}
    if return_query: return     {'code': 1 , 'message': f'Тестовая сборка для вывода списка запросов', 'list_query': list_query}
    # return {'code':1,'user_id' : user_id, 
    #                         'message' : 'Тестовая сборка локально',
    #                         'cube_id':cube_id, 
    #                         'group_columns': group_columns, 
    #                         'group_names' : group_names,
    #                         'reassemble':reassemble,
    #                         'list_query':list_query }
    # return {'code':1,'list_query':list_query } # можно раскоментить эту строку и посмотреть какие запросы SQL составились 
    galileo.cubes.log.set_cube_status(  cube_id=cube_id, 
                                        status=f'Агрегация куба   without_root = {without_root}', 
                                        engine=engine, 
                                        user_id = user_id, 
                                        in_assemble = True , 
                                        percent=percent )
    # websocket.send( name='cube_status', data= {'id':cube_id, 'status': f'Агрегация куба'  , 'percent': percent } , to=[user_id] )
    # херачим запросы 
    # if cube_id ==1:
    #     list_query=list_query[70:-31]
    for number,i in  enumerate(list_query):

        try:
            DB.query(query=i, engine=engine)
        except Exception as e:
            return {'code':0, 'message' : 'Ошибка при создании КУБА', 'query':i, 'error': str(e) , 'list_query':list_query }
        
        if  int(number*100/len(list_query))==a:
            a+=25
            percent+=10
            galileo.cubes.log(  cube_id=cube_id,
                            action=f'assemble',  # assemble
                            date = galileo.db.timestamp(engine),
                            value = f'Выполнено {"="*int(percent/2)}>{percent}% из 100%',
                            user_id = user_id,
                            engine = engine )
        galileo.cubes.log.set_cube_status(  cube_id=cube_id, 
                                            status=f'Расчет {number} из {len(list_query)}', 
                                            engine=engine, 
                                            user_id = user_id, 
                                            in_assemble = True , 
                                            percent=percent )
        # websocket.send( name='cube_status', data= {'id':cube_id, 'status': f'Расчет {number} из {len(list_query)}'  , 'percent': percent } , to=[user_id] )
    if len(DB.query(query=f""" SELECT * FROM cube_{cube_id}_clearcube LIMIT 2   """, engine=engine, return_df=True))==0:
        return {'code':0, 
                'message' : ' КУБ пустой, данная ошибка связана с аналитиками и их уровнями , какой то из них может быть полностью пустым',   
                'list_query':list_query }
    return {'code':1, 'mesage': 'Успешная сборка куба', 'list_query':list_query }