
import time
import bottle

from pony.orm import *

from products.db.ponyApi import Users, Roles, Patient, Medical, Images, BaseDB


class CodeInfo(object):
    """."""
    def __init__(self):
        self.fs_found_patient_template = """
        <fieldset><legend>&nbsp;&nbsp;FOUND PATIENTS&nbsp;&nbsp;</legend>
        <br>
            <table border=0>
                <tr>
                    <td>&nbsp;&nbsp;</td>
                    <td>
                        <select name="load_patient" id="load_patient" size=8 style="width: 300px;  border: none;">
                            %(option_values_found_patients)s
                        </select>
                    </td>
                </tr>
            </table>
                <p align=center><br><br>
                    <input type="submit" name="load" value="Look Up"></input>
                </p>
        </fieldset>"""

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

        self.patient_search_schema = (
                                     # ((form_field_name, DB_ Col_name), default_value)
                                       (('search_by_email', 'email'), '-- Email --'),
                                       (('search_by_gname', 'gname'), '-- Guardian Name --'),
                                       (('search_by_patient_id', 'id'), '-- Patient ID --'),
                                       (('search_by_patient_name', ['first_name',
                                                                    'middle_name',
                                                                    'last_name']), '-- Patient Name --'),
                                       (('search_result', ''), '')
                                     )

        self.patient_extra_params = {'photo_src': 'photo_default.jpg',
                                     'method_name': 'post',
                                     'main_submit_button': 'Create',
                                     'msg_with_patient_id': ''
                                     }


class Engine(CodeInfo):
    """."""
    def __init__(self):
        """."""
        super(Engine, self).__init__()

        self.mapped_dict_to_db = { db_col: default
                                   for (ui_col, db_col), default in self.patient_schema }

    def __call__(self, str_method='', **kwargs):
        """."""
        try:
            if str_method:
                func = getattr(self, str_method)
            self.mapped_dict_to_db.update( kwargs )
            return func(**self.mapped_dict_to_db)
        except AttributeError:
            return "<h1>Page Not Found</h1>"

    def patient(self, **kwargs):
        """."""

        _welcome_msg = ""

        save = kwargs.get('save', False)
        if save:
            del kwargs['save']

        ## search = kwargs.get('search', False)
        ## if search:
        ##     ## ------------------------------------------------------------- ##
        ##     ## Search for any Patient with the specified identity fields.
        ##     ## ------------------------------------------------------------- ##
        ##     del kwargs['search']


        if not save:
            ## ------------------------------------------------------------- ##
            ## Fetch contents from DB and render them.
            ## ------------------------------------------------------------- ##

            given_patient_id = kwargs.get('patient_id', False)

            ## load patient for given patient id
            if not given_patient_id:
                patient_id = BaseDB().select_by_sql(Patient,
                             'select id from patient order by id')[-1].id

                _welcome_msg = """<font color="blue">Patient Added Successfully with ID: {0}</font>"""

            else:
                patient_id = given_patient_id
                _welcome_msg = """<font color="blue"> Details loaded for Patient ID: {0}</font>"""

            if kwargs.get('msg_with_patient_id', ''):
                self.patient_extra_params['msg_with_patient_id'] = kwargs.get('msg_with_patient_id')
            else:
                self.patient_extra_params['msg_with_patient_id'] = _welcome_msg.format( patient_id )

            res = BaseDB().select_by_sql(Patient,
                      'select * from patient where id = {0}'.format(patient_id))[0]

            _d = {key: res._vals_[value] for key, value in res._adict_.items()}

            params = {ui_col: _d[db_col] for (ui_col, db_col), _ in self.patient_schema}

            _extra_params = {ui_col: default
                             for (ui_col, db_col), default in self.patient_search_schema}

            self.patient_extra_params['main_submit_button'] = 'Update'
            self.patient_extra_params['method_name'] = 'update'

            params.update(self.patient_extra_params)
            params.update(_extra_params)

            ## Update or retain the previous Searched patients
            params.update( {'search_result': kwargs.get('prev_found_recs', '')} )

            return bottle.template('patient.html', **params)

        else:
            ## ------------------------------------------------------------- ##
            ## Fresh Insert into Database.
            ## ------------------------------------------------------------- ##

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
            return self.patient(save=False)


class Search(CodeInfo):
    """Search for information with given key fields."""
    def __init__(self):
        """."""
        super(Search, self).__init__()

    def __call__(self, str_method=''):
        """."""
        try:
            if str_method:
                func = getattr(self, str_method)
            return func()
        except AttributeError:
            return "<h1>Page Not Found</h1>"

    @db_session
    def patient(self):
        """."""
        self.patient_page_params = { ui_col: default
                                      for (ui_col, db_col), default in self.patient_schema }

        req_params = bottle.request.params

        _default_list = [ui_col for (ui_col, db_col), default in self.patient_search_schema
                         if default]

        sql_where = ''
        ## list for sql where clause without name list
        _sql_where = ["{0} = {1}".format( db_col, "'"+req_params[ui_col]+"'" if isinstance(req_params[ui_col], str) else req_params[ui_col] )
                      for (ui_col, db_col), default in self.patient_search_schema
                      if ui_col not in ['search_result', 'search_by_patient_name']
                      ]

        sql_where = """{}""".format( ' AND '.join([ele for ele in _sql_where if '--' not in ele]) )

        sql_where = """( {} )""".format(sql_where) if sql_where else ''

        _sql_where = ''

        if not req_params['search_by_patient_name'].startswith('--'):
            _sql_where = ["""{} like '%{}%'""".format( ele, req_params['search_by_patient_name'] )
                          for ele in ['first_name', 'middle_name', 'last_name']]

        if _sql_where:
            _sql_where = """( {} )""".format( ' OR '.join(_sql_where) )

            sql_where = """{} {} {}""".format( sql_where,
                                               'AND' if sql_where else '',
                                               _sql_where ).strip()

        if not sql_where:
            return bottle.redirect('/engine/fresh/patient')

        _temp = """
                SELECT
                    id,
                    first_name,
                    middle_name,
                    last_name
                FROM
                    patient
                WHERE
                    %(where_clause)s"""

        res = BaseDB().select_by_sql( Patient, _temp % ( {'where_clause': sql_where} ) )

        self.patient_page_params.update( self.patient_extra_params )

        _search_window = {ui_col: default for (ui_col, db_col), default in self.patient_search_schema }
        self.patient_page_params.update( _search_window )

        _options = []
        _option_temp = """<option value="{}">{}</option>"""

        for eachrec in res:
            _formatted_name = """{} {} {} ({})""".format( eachrec.first_name,
                                                          eachrec.middle_name,
                                                          eachrec.last_name,
                                                          str(eachrec.id) )

            _options.append( _option_temp.format( eachrec.id, _formatted_name ) )

        self.patient_extra_params['search_result'] = self.fs_found_patient_template % ({'option_values_found_patients': ' '.join(_options)})

        self.patient_page_params.update(self.patient_extra_params)

        return bottle.template('patient.html', **self.patient_page_params)


class Update(CodeInfo):
    """Update or overwrite the Records."""
    def __init__(self):
        """."""
        super(Update, self).__init__()

    def __call__(self, str_method, **kwargs):
        """."""
        try:
            if str_method:
                func = getattr(self, str_method)
            return func()
        except AttributeError:
            return "<h1>Page Not Found</h1>"

    @db_session
    def patient(self, **kwargs):
        """."""
        request_params = bottle.request.params
        patient_id = request_params.get('hidden_patient_id', 0)

        if patient_id == 0:
            return "<h1>Invalid Patient ID</h1>"

        _params = {}
        _extra_params = {'upd_dt': time.ctime(time.time())}

        for req_ui_col, data in request_params.items():
            _d = { db_col: data
                   for (ui_col, db_col), default in self.patient_schema
                   if ui_col == req_ui_col }

            if _d: _params.update(_d)

        _params.update(_extra_params)

        Patient.get(id=int(patient_id)).set(**_params)

        _welcome_msg = """<font color="blue"> Patient Details were updated for ID: {0}</font>"""
        msg_with_patient_id = _welcome_msg.format( patient_id )

        ## Render back the Updated data.
        return Engine().patient(patient_id=int(patient_id),
                                msg_with_patient_id=msg_with_patient_id,
                                save=False)

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

        self.patient_fresh_params.update(self.patient_extra_params)

        _search_window = {ui_col: default for (ui_col, db_col), default in self.patient_search_schema}
        self.patient_fresh_params.update( _search_window )

        return bottle.template('patient.html', **self.patient_fresh_params)

