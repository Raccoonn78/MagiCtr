self.group_columns ['X', 'Y', 'Данные']
self.group_names  [['x_1', 'x_2', 'x_3'], ['y_1', 'y_2', 'y_3']]
self.group_data_columns ['COALESCE("Значения", 0 ) ', 'Значения']

self.structure {'last_update': '2025-05-21 11:18:52', 'cube_name': 'Тестовое создание куба', 'data_columns_aggregation': 0, 
'created_by': 'mironov.dmitry.s@sogaz.ru', 'data_columns_preoperations': [], 'data_columns_operations': [], 'analytics_merge': [],
 'data_columns': [{'name': 'Значения', 'visible': True, 'aggregation': [{'analytics': 'X', 'aggregation_id': 0}, {'analytics': 'Y', 'aggregation_id': 0}]}], 
'axis': [{'name': 'X', 'id': 0, 'columns': ['x_1', 'x_2', 'x_3'], 'mapping': None, 'root_id': 0, 'id_length': 2,
 'indexing': None, 'id_position': 2, 'access': False, 'rewrite': True}, {'name': 'Y', 'id': 1, 'columns': ['y_1', 'y_2', 'y_3'], 
'mapping': None, 'root_id': 0, 'id_length': 2, 'indexing': None, 'id_position': 1, 'access': False, 'rewrite': False}, {'name': 'Данные', 'id': 2,
 'columns': ['Столбец данных'], 'mapping': None, 'root_id': 0, 'id_length': 3, 'indexing': None, 'id_position': 0, 'access': False, 'rewrite': False}],
 'max_filter_index': 2, 'data_columns_order': [{'name': 'Значения', 'mock': False, 'order': 0, 'id': 1744567412161}], 'cubes_chain': {}, 'needs_assemble': True}


query= '''
 CREATE UNLOGGED TABLE IF NOT EXISTS  cube_120_data_assemble_index AS 
    (  
        SELECT distinct on(     
                            cube_120_data_assemble."x_1",  cube_120_data_assemble."x_2",  cube_120_data_assemble."x_3",
                            cube_120_data_assemble."y_1",  cube_120_data_assemble."y_2",  cube_120_data_assemble."y_3"
                            )     
            cube_120_data_assemble."Значения",   
            n0.index AS "x_1",  
            n1.index AS "x_2",  
            n2.index AS "x_3",  
            n3.index AS "y_1",  
            n4.index AS "y_2",  
            n5.index AS "y_3" 
                
        FROM  cube_120_data_assemble 

    LEFT OUTER JOIN  cube_120_nodes_axis_0 n2 USING(  "x_1", "x_2", "x_3" ) 
    LEFT OUTER JOIN  cube_120_nodes_axis_0 n1 USING(  "x_1", "x_2" ) 
    LEFT OUTER JOIN  cube_120_nodes_axis_0 n0 USING(  "x_1" ) 
    LEFT OUTER JOIN  cube_120_nodes_axis_1 n5 USING(  "y_1", "y_2", "y_3" ) 
    LEFT OUTER JOIN  cube_120_nodes_axis_1 n4 USING(  "y_1", "y_2" ) 
    LEFT OUTER JOIN  cube_120_nodes_axis_1 n3 USING(  "y_1" ) 
    WHERE ( cube_120_data_assemble."x_1"= n0."name"   and  n0."x_2" is NULL  and  n0."x_3" is NULL   )  and 
        ( cube_120_data_assemble."x_2"= n1."name"   and  n1."x_3" is NULL   )  and 
        ( cube_120_data_assemble."x_3"= n2."name"    )  and 
        ( cube_120_data_assemble."y_1"= n3."name"   and  n3."y_2" is NULL  and  n3."y_3" is NULL   )  and 
        ( cube_120_data_assemble."y_2"= n4."name"   and  n4."y_3" is NULL   )  and 
        ( cube_120_data_assemble."y_3"= n5."name"    )   
    );
'''