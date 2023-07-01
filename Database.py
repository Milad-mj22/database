
import mysql.connector
from mysql.connector import Error



CONNECTION_ERROR = 'Connection error'
SUCCESSFULL = 'True'
DEFAULT_SCHEMA = False   

NULL = 'NULL'
NOT_NULL = 'NOT NULL'
AUTO_INCREMENT = 'AUTO_INCREMENT'
INT = 'INT'
VARCHAR = 'VARCHAR(255)'
FLOAT = 'FLOAT'
DEFAULT = 'DEFAULT '

NOTHING = 0   # Print nothing
INFO = 1      # Only print errors
WARNING = 2   # Print All messages 



Error_auto_increment = 'AUTO INCREMENT Only can set on INT type'

class dataBase:
    def __init__(self,username,password,host,database_name,logger_obj=None,log_level=1):
        pass
        self.user_name=username
        self.password=password
        self.host=host
        self.data_base_name=database_name
        self.logger_obj = logger_obj
        self.log_level=log_level
        self.check_connection()
        



    def set_log_level(self,num):
        """this function used to set level of logging

        Args:
            num (int): 0,1 for logging info or warning
        """
        self.log_level = num


    def connect(self):
        """this function used to connect mysql with init parms

        Returns:
            object: connection of mysql
        """


        connection = mysql.connector.connect(host=self.host,
                                            database=self.data_base_name,
                                            user=self.user_name,
                                            password=self.password,
                                            auth_plugin='mysql_native_password')  
        cursor = connection.cursor()
        self.cursor, self.connection = cursor, connection  
        return cursor,connection     


    def check_connection(self):
        """
        this function is used to check if the connection to databse can be esablished and set self parms for connecting

        Inputs: None

        Returns: a boolean value determining if the connecton is stablished or not
        """

        flag=False

        try:
            cursor, connection = self.connect() # connect to database
            self.cursor, self.connection = cursor, connection  
            #
            flag=True
            #
            if connection.is_connected():
                db_Info = connection.get_server_info() # get informations of database
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchall()
                #
                return True

        except Exception as e:
            self.show_message('Error while connecting to MySQL')
            return False


    def execute_quary(self, quary , need_data=False, close=False):
        """
        this function is used to execute a query on database

        Inputs:
            quary: the input query to execute
            cursor:
            connection:
            need_data: a bolean value
            close:
        
        Returns: None
        """
        if need_data:
            self.cursor.execute(quary, data)

        else:
            self.cursor.execute(quary)

        # connection.commit()
        if close:
            self.cursor.close()
        else:
            return self.cursor


    def add_record(self,table_name , data):
        """this function is used to add a new record to table

        Inputs:
            table_name : name of table
            data: data that want to add to the database
        
        Returns: Flag of doing query
        """
        parametrs = self.get_col_name(table_name=table_name,without_auto_incresment=True)
        len_parameters = len(parametrs)
        cols =''
        for parm in parametrs:
            cols+=parm+','
        cols = cols[:-1]
        cols = '(' + cols + ')'
        parametrs = cols
        s ='%s,'*len_parameters
        s = s[:-1]
        s = '(' + s + ')'

        try:

            if self.check_connection():
                mySql_insert_query = """INSERT INTO {} {} 
                                    VALUES 
                                    {} """.format(table_name,parametrs,s)
                self.cursor.execute(mySql_insert_query,data)
                self.connection.commit()
                self.cursor.close()
                return True

            else:
                return False

        except Exception as e:
            self.show_message(e)
            return False


    def update_record(self,table_name,col_name,value,id_name,id_value):
        """this function used to update a row with input parms

        Args:
            table_name (str): name of that table we want to change data
            col_name (str): column name of table
            value (str): new vlaue
            id_name (str): name of column for selecting the row 
            id_value (str): Row specifier
        """
       
        try:
            if self.check_connection():
                mySql_insert_query = """UPDATE {} 
                                        SET {} = {}
                                        WHERE {} ={} """.format(table_name,col_name,("'"+value+"'"),id_name,("'"+id_value+"'"))
                self.cursor.execute(mySql_insert_query)
                self.connection.commit()
                self.show_message((self.cursor.rowcount, "Record Updated successfully "),level=1)
                self.cursor.close()
                return True
            else:
                return False
            
        except mysql.connector.Error as e:
            self.show_message(("Error Update Record ", e))
            


    def remove_record(self, table_name , col_name, value ):
        """
        this function is used to remove a record from table acourding to specified column value

        Inputs:
            col_name: name of the column to check for (in string)
            value: value of the column (in string)
            table_name: name of the table (in string)
        
        Returns:
            results: a boolean determining if the record is removed or not
        """
        
        try:
            if self.check_connection():
                mySql_delete_query = """DELETE FROM {} WHERE {}={};""".format(table_name,col_name,"'"+value+"'")

                self.execute_quary(mySql_delete_query)
                self.connection.commit()
                self.cursor.close()
                self.show_message((self.cursor.rowcount, "Remove successfully from table {}".format(table_name)))
                return True
            
            else:
                return False
            
        except Exception as e:
            self.show_message(e)
            return False



    def search(self, table_name, col_name, value):
        """this function is used to search in table

        :param table_name: table name
        :type table_name: str
        :param param_name: column names to search
        :type param_name: list or strs
        :param values: column values to search
        :type values: list
        :param int_type:
        :type int_type:
        
        :return:
            result: boolean to determine result
            table_content: list of dicts containing table records, if count==True: count of table
        :rtype: _type_
        """
        value = str(value)
        int_type=False
        if value.isnumeric():
            int_type = True


        # try:
        if self.check_connection():
            if int_type:
                sql_select_Query = "SELECT * FROM {} WHERE {} = {};".format(table_name,col_name,str(value))
                cursor=self.execute_quary(sql_select_Query)
            else:

                sql_select_Query = """SELECT * FROM {} WHERE {} = {} """.format(table_name,col_name,("'"+str(value)+"'"))
                cursor=self.execute_quary(sql_select_Query)

            records = cursor.fetchall()
            
            field_names = [col[0] for col in cursor.description]
            res = []

            for record in records:
                record_dict = {}
                for i in range( len(field_names) ):
                    record_dict[ field_names[i] ] = record[i]
                # print('record_dict',record_dict)
                
                res.append( record_dict )
            
            return res

        else:
            self.show_message('Error in connection')
            return []

        # except Exception as e:
        #     return e, []


    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------

    def delete_table(self,table_name):
        """delete selected table

        Args:
            table_name (str): name of table
        """
        try:
            if self.check_connection():
                sql_Delete_table = "DROP TABLE {};".format(table_name)
                cursor=self.execute_quary(sql_Delete_table)                                    
        except Exception as e:
            self.show_message(e)
    # #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------

    def delete_column(self,table_name,col_name):
        """delete column of table

        Args:
            table_name (str): name of table
            col_name (str): name of column

        Returns:
            _type_: bool
        """
        self.check_connection()
        if self.check_column_exist(table_name=table_name,col_name=col_name):
            try:
                if self.check_connection():
                    query = "ALTER TABLE {} DROP COLUMN {};".format(table_name,col_name)
                    self.execute_quary(quary=query)
                    self.show_message('Column Deleted',level=1)
                    return True
                else:
                    return False

            except mysql.connector.Error as e:
                self.show_message(("Error Drop Column ", e))
        else:
            self.show_message('Column Not Exist for Drop')


    def get_col_name(self,table_name,without_auto_incresment=False):

        """get name of column

        Args:
            table_name (str): name of table
            without_auto_incresment (bool): get all of column name or columns withoit incresment

        Returns:
            _type_: _description_
        """
        try:
            if self.check_connection():
                cursor=self.execute_quary("select * from {}".format(table_name))
                records = cursor.fetchall()
                field_names = [col[0] for col in cursor.description]

                if without_auto_incresment:
                    col_name = list(self.get_auto_increment_col_name(table_name=table_name))
                    res = []
                    for name in field_names:
                        if name not in col_name:
                            res.append(name)

                    return res


            return field_names
        except mysql.connector.Error as e:
            self.show_message(e)


    def get_auto_increment_col_name(self,table_name):
        """this function used to get column name which that auto increment feature 

        Args:
            table_name (str): name of table

        Returns:
            _type_: list of column names
        """
        if self.check_connection():
            cursor=self.execute_quary("select COLUMN_NAME from information_schema.columns where TABLE_SCHEMA='test2' and TABLE_NAME='users' and EXTRA like '%auto_increment%';")
            records = cursor.fetchall()
            if records:
                records=records[0]
            return records


    def get_all_content(self,table_name, limit=False, limit_size=20, offset=0, reverse_order=False,column_order = 'id'):
        """this function is used to get all content of a table
        :param table_name: table name
        :type table_name: str
        :param limit: boolean determining whether to return part of table, defaults to False
        :type limit: bool, optional
        :param limit_size: conut of table rows to reurn, defaults to 20
        :type limit_size: int, optional
        :param offset: starting row index to return n next roes, defaults to 0
        :type offset: int, optional
        :param reverse_order: boolean to reverse sorting the table, defaults to False
        :type reverse_order: bool, optional
        :return:
            result: boolean to determine result
            table_content: list of dicts containing table records, if count==True: count of table
        :rtype: _type_
        """
        
        sort_order = 'DESC' if reverse_order else 'ASC'
        try:
            if self.check_connection():
                if not limit:
                    sql_select_Query = "select * from {} ORDER BY {} {}".format(table_name,column_order, sort_order)
                else:
                    sql_select_Query = "select * from {} ORDER BY {} {} LIMIT {} OFFSET {}".format(table_name,column_order, sort_order, limit_size, offset)
                    
                cursor=self.execute_quary(sql_select_Query)
                records = cursor.fetchall()
                field_names = [col[0] for col in cursor.description]
                cursor.close()
                res = []
                for record in records:
                        record_dict = {}
                        for i in range( len(field_names) ):
                            record_dict[ field_names[i] ] = record[i]
                        res.append( record_dict )
                return res
            else:
                return []

        except Exception as e:
            self.show_message(e)
            return []


    def check_table_exist(self,table_name):
        """this function used to check table exist or not 

        Args:
            table_name (str): name of table

        Returns:
            _type_: bool of exist table
        """
        try:
            sql_check_table = "SELECT * FROM {}.{};".format(self.data_base_name,table_name)
            self.execute_quary(sql_check_table)        
            return True                              
        except mysql.connector.Error as e:
            self.show_message(("Error reading data from MySQL table", e))
            return False


    def create_table(self,table_name):
        """this function used to create table

        Args:
            table_name (str): name of table

        Returns:
            _type_: bool of create table
        """
        try:
            if self.check_connection():
                query = "CREATE TABLE IF NOT EXISTS {} (id INT NOT NULL PRIMARY KEY);".format(table_name)
                self.execute_quary(quary=query)
                return True
            else:
                return False
        except mysql.connector.Error as e:
            self.show_message(("Error Create Table ", e))


    def check_column_exist(self,table_name,col_name):
        """this function used check column of table exist or not

        Args:
            table_name (str): name of table

        Returns:
            bool: list of column names
        """

        try:
            query = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}'".format(table_name)
            cursor=self.execute_quary(quary=query)
            schemas = cursor.fetchall()
            for col in schemas:
                if col_name == col[3]:
                    self.show_message('Column Exist')
                    return True
            return False
        except:
            return False



    def add_column(self,table_name,col_name,type,len=255,Null=NULL,AI=False,default=''):
        """this function used to add column to specefic table with args

        Args:
            table_name (str): name of table
            col_name (str): column of table
            type (KEY): type of column like STR,INT,...
            len (int, optional): if type is str you can set len 
            Null (_type_, optional): set column can be null or not
            AI (str, optional): set for auto incresment column
            default (str, optional): _description_. Defaults to ''.

        Returns:
            _type_: _description_
        """
        
        if not AI:
            AI=''
        else:
            AI=AUTO_INCREMENT

        self.create_table(table_name=table_name)

        if type == VARCHAR:
            type='VARCHAR({})'.format(len)

        if default!= '':
            print(isinstance(default,str))
            if isinstance(default,str):
                default = DEFAULT+"'"+default+"'"
            else:
                default = DEFAULT+str(default)

           


        if type !=INT and AI==AUTO_INCREMENT:
            self.show_message((' Error Add Column {}'.format(Error_auto_increment)))
            return False

        if not self.check_column_exist(table_name=table_name,col_name=col_name):

            try:
                if self.check_connection():
                    query = "ALTER TABLE  {} ADD {} {} {} {} {};".format(table_name,col_name,type,Null,AI,default)
                    self.execute_quary(quary=query)
                    return True
                else:
                    return False

            except mysql.connector.Error as e:
                self.show_message(("Error Add Column ", e))

        else:
            return False


    def create_schema(self,schema_name):
        """this function used to create schema 

        Args:
            schema_name (str): name of schema

        Returns:
            bool: if query work retuen True else return False
        """
        try:
            if self.check_connection():
                query = "CREATE SCHEMA IF NOT EXISTS {};".format(schema_name)
                self.execute_quary(quary=query)
                return True
            else:
                return False
        except mysql.connector.Error as e:
            print("Error create schema ", e)


    def get_all_schemas(self):
        """get name all of schemas

        Returns:
            list: list of all schemas
        """
        try:
            self.connect()
            query = "show schemas"
            cursor=self.execute_quary(quary=query)
            schemas = cursor.fetchall()
            return schemas
        except mysql.connector.Error as e:
            print("Error Get schema names ", e)


    def show_message(self,error,level=0):
        """this function print errors or messages

        Args:
            error (_type_): _description_
            level (int, optional): _description_. Defaults to 0.
        """
        if self.log_level==1:
            print(error)







if __name__ == "__main__":
    db=dataBase('root','Dorsa-1400','localhost','test222')
    db.create_table('users')   # you can dont create table
    a=db.get_all_schemas()
    db.add_column(table_name='users',col_name='first_name',type=VARCHAR,len=80,Null=NOT_NULL)
    db.add_column(table_name='users',col_name='last_name',type=VARCHAR,len=80,Null=NOT_NULL)
    db.add_column(table_name='users',col_name='email',type=VARCHAR,len=80,Null=NOT_NULL)

    content=db.get_all_content('asdw2')

    col_name=db.get_col_name('asdw')

    db.delete_column('users','id')

    data = ('milad','moltaji','m.moltaji')
    for _ in range(50):
        ret =db.add_record('users',data='__YOUR_DATA__')

    db.get_auto_increment_col_name('users')

    db.update_record(table_name='asdw2',col_name='test4',value='11',id_name='id',id_value='1')

    db.remove_record(table_name='users',col_name='first_name',value='m')
    
    r = db.get_all_content(table_name='users',limit=True,column_order='email')
    
    a=db.search(table_name='users',col_name='first_name',value='m')




