
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

class PreSet(object):
    """
    """
    engine = create_engine('mysql+mysqldb://root:root@localhost/clinic')
    metadata = MetaData(engine)


class Users(PreSet):
    """
    """
    users = Table('users', PreSet.metadata,
                      Column('user_id', Integer, primary_key=True),
                      Column('name', String(40)),
                      Column('age', Integer),
                      Column('password', String),
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

    def select(self):
        """
        """
        pass


obj = Users()
obj.insert({'name': 'aaaa', 'age': 28})
