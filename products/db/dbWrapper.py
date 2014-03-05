
import time
import datetime


#from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, \
        DATETIME, ForeignKey



#Base = declarative_base()


class PreSet(object):
    """
    """
    engine = create_engine('mysql+mysqldb://root:root@localhost/clinic')
    metadata = MetaData(engine)


class Generator(object):
    """
    """
    def __init__(self):
        """
        """
        ## Internal mapper for the JOIN portion
        self.mapper = (
                       ## COLUMNS FROM USERS TABLE ##
                       ## TABLE, COLUMN, ISPRIMARY, FOREIGN
                       ('USERS', 'USER_ID', 'YES', 'NO'),
                       ('USERS', 'UNAME', 'NO', 'NO'),
                       ('USERS', 'ROLE', 'NO', 'NO'),

                       ## INFO OF ROLES TABLE ##
                       ## TABLE, COLUMN, ISPRIMARY
                       ('ROLES', 'ROLE', 'NO', 'YES'),
                       ('ROLES', 'LEVEL', 'NO', 'NO'),
                      )

        self.template_general = """
        SELECT
            %(colnames)s
        FROM
            %(table_or_join)s
        %(where_cond)s"""

    def __joiner(self, select, _tables):
        """
        """
        join_template = """%(T1)s INNER JOIN %(T2)s ON %(cond)s"""

        _dict = {'T1': '', 'T2': '', 'cond': 'T1.A = T2.B'}

        joined_str = []

        for i in xrange(len(_tables) - 1):
            child_table, parent_table = _tables[i], _tables[i + 1]
            if i == 0:
                _dict['T1'] = child_table
            else:
                _dict['T1'] = ''

            _dict['T2'] = parent_table

            ## build condition part on join
            col_name =  [ele[1]
                         for ele in self.mapper \
                         if ele[0] == parent_table and ele[3] == 'YES']

            print col_name

            try:
                ## Place the Table name as alias name to avoid the column ambiguous.
                _idx = select.index(col_name[0])
                select[_idx] = """{0}.{1}""".format(child_table, col_name[0])
                print select, ">>>>"

                col_name = col_name[0]
                _dict['cond'] = """{0}.{2} = {1}.{2}""".format(child_table, parent_table, col_name)

                joined_str.append(join_template % (_dict))
            except ValueError:
                pass
            except IndexError:
                pass

        return select, '\n'.join(joined_str)

    def generate_where_clause(self, **kwargs):
        """
        """
        return 'WHERE DUMMY GENERATED'

    def query(self, select=None, table=None, where=None):
        """
        """
        if not select or not table:
            print "Argument select or table is must"
            return False

        _dict = {'colnames': '',
                 'table_or_join': '',
                 'where_cond': ''
                 }

        #_dict['colnames'] = ', '.join(select)
        if isinstance(table, list):
            if len(table) > 1:

                select, joined_str = self.__joiner(select, table)
                _dict['colnames'] = ', '.join(select)

                _dict['table_or_join'] = joined_str
            else:
                _dict['table_or_join'] = table[0].upper()
        else:
            _dict['table_or_join'] = table.upper()

        print self.template_general % (_dict)

        #if where:


obj = Generator()
obj.query(select=['ROLE', 'UNAME', 'EMAIL'],
          table=['USERS', 'ROLES', 'TEST', 'test2'],
          )



class Dependents(Generator): #Base):
    """
    """
    pass


class TableNames(object):
    """
    """
    user_table_name = 'USERS'
    roles_table_name = 'ROLES'


class Users(PreSet, TableNames, Dependents):
    """
    """
    tn = TableNames

    users = Table(tn.user_table_name, PreSet.metadata,
                Column('USER_ID', Integer, primary_key=True),
                Column('UNAME', String(50)),
                Column('ROLE', ForeignKey(tn.roles_table_name + '.ROLE')),
                Column('HASH', String(256), nullable=False),
                Column('EMAIL', String(100)),
                Column('ACTIVE', String(1)),
                Column('DESCRIPTION', String(150)),
                Column('CRT_DT', DATETIME, nullable=False),
                Column('UPD_DT', DATETIME, nullable=False, default=time.strftime('%Y-%m-%d %H:%M:%S')),
                Column('LAST_LOGIN', DATETIME, nullable=True)
            )

    def __init__(self):
        """
        """
        super(PreSet, self).__init__()

    def insert(self, *args, **kwargs):
        """
        """
        if args:
            self.users.insert().execute(*args)
        if kwargs:
            self.users.insert().execute(**kwargs)

    def select(self, **kwargs):
        """
        """
        

    def update(self, *args, **kwargs):
        """
        """
        pass

    def active(self, *args, **kwargs):
        """
        """
        pass


class Roles(PreSet, TableNames, Dependents):
    """
    """
    tn = TableNames

    roles = Table(tn.roles_table_name, PreSet.metadata,
                Column('ROLE', String(20), primary_key=True),
                Column('LEVEL', Integer, nullable=False),
                Column('ACTIVE', String(1), nullable=False),
                Column('CRT_DT', DATETIME, nullable=False),
                Column('UPD_DT', DATETIME, nullable=False)
                )

    def __init__(self):
        """
        """
        super(PreSet, self).__init__()

    def insert(self, *args, **kwargs):
        """
        """
        pass

    def select(self):
        """
        """
        pass

    def update(self, *args, **kwargs):
        """
        """
        pass

    def active(self, *args, **kwargs):
        """
        """
        pass


## obj = Users()
## 
## _dict = {
##      'UNAME': 'aaa',
##      'ROLE': 'xxx',
##      'HASH': '12334435',
##      'EMAIL': 'aa@ss.com',
##      'ACTIVE': 'Y',
##      'DESCRIPTION': 'adsafdsa',
##      'CRT_DT': time.strftime('%Y-%m-%d %H:%M:%S'),
##      }
## 
## obj.insert(**_dict)
