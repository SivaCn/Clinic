
import time

## ----------- sqlalchemy DataTypes ------------ ##
from sqlalchemy import create_engine, MetaData

## ----------- sqlalchemy Table Properties ------------ ##
from sqlalchemy import Table, Column, Integer, String, DATETIME

## ----------- sqlalchemy Constraints ------------ ##
from sqlalchemy import ForeignKey

## ----------- sqlalchemy CRUD imports ------------ ##
from sqlalchemy import select


class PreSet(object):
    """
    """
    engine = create_engine('mysql+mysqldb://root:root@localhost/clinic')
    metadata = MetaData(engine)


class TableNames(object):
    """
    """
    user_table_name = 'USERS'
    roles_table_name = 'ROLES'


class Defaults(object):
    """
    """
    def __init__(self):
        """
        """
        pass

    def date_time(self, **kwargs):
        """
        """
        if 'CRT_DT' not in kwargs:
            kwargs['CRT_DT'] = time.strftime('%Y-%m-%d %H:%M:%S')
        return kwargs


class Dependents(PreSet, TableNames, Defaults):
    """
    """
    def __init__(self):
        """
        """
        pass


class Users(Dependents):
    """
    """
    ## def __init__(self):
    ##     """
    ##     """
    ##     pass

    users = Table(TableNames.user_table_name,
               PreSet.metadata,
               Column('USER_ID', Integer, primary_key=True),
               Column('UNAME', String(50)),
               Column('ROLE', ForeignKey(TableNames.roles_table_name + '.ROLE')),
               Column('HASH', String(256), nullable=False),
               Column('EMAIL', String(100)),
               Column('ACTIVE', String(1)),
               Column('DESCRIPTION', String(150)),
               Column('CRT_DT', DATETIME, nullable=False),
               Column('UPD_DT', DATETIME, nullable=False, default=time.strftime('%Y-%m-%d %H:%M:%S')),
               Column('LAST_LOGIN', DATETIME, nullable=True),
               extend_existing=True
               )

    def __repr__(self):
        """
        """
        _str = "USERS(USER_ID, UNAME, ROLE, EMAIL, ACTIVE, DESCRIPTION, LAST_LOGIN)"
        return _str


class Roles(Dependents):
    """
    """
    ## def __init__(self):
    ##     """
    ##     """
    ##     pass

    roles = Table(TableNames.roles_table_name,
               PreSet.metadata,
               Column('ROLE', String(20), primary_key=True),
               Column('LEVEL', Integer, nullable=False),
               Column('ACTIVE', String(1), nullable=False),
               Column('CRT_DT', DATETIME, nullable=False),
               Column('UPD_DT', DATETIME, nullable=False),
               extend_existing=True
               )

    def __repr__(self):
        """
        """
        _str = "ROLES(ROLE, LEVEL, ACTIVE)"
        return _str


class Tbl(Users, Roles):
    """
        A common Interface for all the Available Tables.
    """
    users = Users.users
    roles = Roles.roles





obj = Users()

_dict = {
     'UNAME': 'aaa',
     'ROLE': 'xxx',
     'HASH': '12334435',
     'EMAIL': 'aa@ss.com',
     'ACTIVE': 'Y',
     'DESCRIPTION': 'adsafdsa',
     'CRT_DT': time.strftime('%Y-%m-%d %H:%M:%S'),
     }

import pdb; pdb.set_trace() # BREAKPOINT
table = Tbl

import pdb; pdb.set_trace() # BREAKPOINT

print ""
