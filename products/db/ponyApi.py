

## ----------- pony Imports ------------ ##
from pony.orm import *

db = Database('mysql',
              host="localhost",
              #port=3306,
              user="root",
              passwd="root",
              db="clinic"
              )


class Users(db.Entity):
    """Users Schema.
    """
    user_id = Required(int)
    uname = Required(unicode)
    role = Required(unicode)
    passwd = Required(unicode)
    email = Required(unicode)
    active = Required(unicode, 1)
    description = Required(unicode)
    crt_dt = Required(unicode)
    upd_dt = Required(unicode)
    last_login = Required(unicode)


class Roles(db.Entity):
    """Roles Schema.
    """
    role = Required(unicode)
    level = Required(int)
    active = Required(unicode, 1)
    crt_dt = Required(unicode)
    upd_dt = Optional(unicode)


class Patient(db.Entity):
    """Patient Schema.
    """
    patient_id = Required(unicode)
    first_name = Required(unicode)
    middle_name = Optional(unicode)
    last_name = Optional(unicode)
    address = Required(unicode)
    mobile_list = Required(unicode)
    telephone_list = Optional(unicode)
    age = Required(int)
    gender = Required(unicode)
    dob = Required(unicode)  # time.ctime(time.time()) stripped format only date
    active = Required(unicode, 1)
    email = Optional(unicode)
    guardian_name = Optional(unicode)
    guardian_con_no = Optional(unicode)
    maritial_status = Required(unicode)
    occupation = Required(unicode)
    religion = Required(unicode)
    country = Required(unicode)
    crt_dt = Required(unicode)
    upd_dt = Optional(unicode)


class Medical(db.Entity):
    """
    """
    patient_id = Required(unicode)
    active = Required(unicode, 1)
    medical_id = Required(unicode)
    last_visit = Optional(unicode)
    next_visit= Required(unicode)
    food = Required(unicode)
    complaints = Optional(unicode)
    signs_symptoms = Required(unicode)
    problem_area = Required(unicode)
    treatment_details = Required(unicode)
    any_improvement = Required(unicode)
    pathiyas = Required(unicode)
    sleep = Required(unicode)
    crt_dt = Required(unicode)
    upd_dt = Optional(unicode)


class Images(db.Entity):
    """
    """
    patient_id = Required(unicode)
    active = Required(unicode, 1)
    photo_id = Required(unicode)
    scan_reports_list = Required(unicode)
    medical_reports_list = Required(unicode)
    crt_dt = Required(unicode)
    upd_dt = Optional(unicode)


class BaseDB(object):
    """
    """
    @db_session
    def commit(self):
        """Commit on Demand.
        """
        commit()

    def get_id(self, table_cls, **kwargs):
        """Get an id of a record.
        """
        try:
            return table_cls.select(**kwargs).id
        except MultipleObjectsFoundError:
            print "Found Many rows"

    @db_session
    def select(self, table_cls):
        """
        """
        return table_cls.select()

    @db_session
    def select_by_id(self, table_cls, _id):
        """
        """
        pass

    @db_session
    def insert(self, table_cls, auto_commit=False, **kwargs):
        """Insert a new record to the specified Table.
        """
        obj = table_cls(**kwargs)

        if auto_commit:
            self.commit()

    @db_session
    def deactivate(self, table_cls, _id, auto_commit=False):
        """Delete an item.
        """
        table_cls.get(id=_id).set(active='N')
        if auto_commit:
            self.commit()

    @db_session
    def update(self, table_cls, auto_commit=False, **kwargs):
        """Update a Record of given Table.
        """
        if '_id' in kwargs:
            obj = table_cls.get(id=kwargs['_id'])
            ## Remove Unmapped table fields.
            del kwargs['_id']
            obj.set(**kwargs)
        if auto_commit:
            self.commit()


import pdb; pdb.set_trace() # BREAKPOINT
db.generate_mapping(create_tables=True)
#db.generate_mapping()

_dict = {'user_id':4, 'uname':'AA', 'role':'SDF', 'passwd':'AAA', 'email':'SS@SS.COM',
         'active':'y', 'description':'desc', 'crt_dt':'DFSFDS', 'upd_dt':'DFSDF',
         'last_login':'DSAFDS'}
 
#BaseDB().post(Users, **_dict)

#BaseDB().update(Users, uname='YYYY', _id=3)

BaseDB().select(Users)
import pdb; pdb.set_trace() # BREAKPOINT
print ""
