
import time
import bottle

from products.db.ponyApi import Users, Roles, Patient, Medical, Images, BaseDB


class CodeInfo(object):
    """."""
    def __init__(self):
        self.patient_schema = (
                     ## ((Front End name, Actual column in DB), Default Value)
                     (('patient_id', 'id'), ''),
                     (('fname', 'first_name'), ''),
                     (('mname', 'middle_name'), ''),
                     (('lname', 'last_name'), ''),
                     (('address', 'address'), ''),
                     (('dob', 'dob'), ''),
                     (('age', 'age'), ''),
                     (('gender', 'gender'),  ''),
                     (('religion', 'religion'), ''),
                     (('country', 'country'), ''),
                     (('occupation', 'occupation'), ''),
                     (('maritial_status', 'maritial_status'), ''),
                     (('photo', 'photo'),  ''),
                     (('email', 'email'), ''),
                     (('mobile', 'mobile'), ''),
                     (('telephone', 'telephone'), ''),
                     (('gname', 'guardian_name'), ''),
                     (('gphone', 'guardian_con_no'), ''),
                     (('notes', 'notes'), ''),
                    )


class Engine(CodeInfo):
    """."""
    def __init__(self):
        """."""
        super(Engine, self).__init__()

        self.mapped_dict_to_db = { db_col: default
                                   for (ui_col, db_col), default in self.patient_schema }

    def __call__(self, str_method='', save=False):
        """."""
        try:
            if str_method:
                func = getattr(self, str_method)
            self.mapped_dict_to_db.update({ 'save': save })
            return func(**self.mapped_dict_to_db)
        except AttributeError:
            return "<h1>Page Not Found</h1>"

    def __generate_patient_id(self):
        """."""
        return '123456'

    def patient(self, **kwargs):
        """."""
        save = kwargs.get('save', False)
        del kwargs['save']

        if not save:
            ## Fetch contents from DB and render them.

            max_id = BaseDB().select_by_sql(Patient,
                      'select id from patient order by id')[-1].id

            res = BaseDB().select_by_sql(Patient,
                      'select * from patient where id = {0}'.format(max_id))[0]

            _d = {key: res._vals_[value] for key, value in res._adict_.items()}

            params = {ui_col: _d[db_col] for (ui_col, db_col), _ in self.patient_schema}

            import pdb; pdb.set_trace() # BREAKPOINT
            #return bottle.template('patient.html', **params)
            #return bottle.redirect('/engine/get/patient')

            return "<h1>fdsafgdsag</h1>"

        else:
            ## Fresh Insert into Database.

            request_params = bottle.request.params

            _params = {}
            _extra_params = {'active': 'Y',
                             'crt_dt': time.ctime(time.time()),
                             'upd_dt': time.ctime(time.time())}

            for req_ui_col, data in request_params.items():
                _d = { db_col: data
                       for (ui_col, db_col), default in self.patient_schema
                       if ui_col == req_ui_col }

                if _d: _params.update(_d)

            _params.update(_extra_params)

            BaseDB().insert(Patient, **_params)

            ## Render back the inserted data.
            self.patient(save=False)


class Fresh(CodeInfo):
    """Render the Fresh Template files with necessary population."""
    def __init__(self):
        """."""
        super(Fresh, self).__init__()

    def __call__(self, str_method='', fresh=True):
        """."""
        try:
            if str_method:
                func = getattr(self, str_method)
            return func()
        except AttributeError:
            return "<h1>Page Not Found</h1>"

    def patient(self):
        """."""
        self.patient_fresh_params = { ui_col: default
                                      for (ui_col, db_col), default in self.patient_schema }

        _extra_params = {'photo_src': ''}

        self.patient_fresh_params.update(_extra_params)

        return bottle.template('patient.html', **self.patient_fresh_params)

