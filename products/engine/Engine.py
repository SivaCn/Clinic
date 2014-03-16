

import bottle

from products.db.ponyApi import Users, Roles, Patient, Medical, Images, BaseDB


class CodeInfo(object):
    """."""
    def __init__(self):
        self.params = {
                       'patient_id': '',
                       'fname': '',
                       'mname': '',
                       'lname': '',
                       'address': '',
                       'dob': '',
                       'age': '',
                       #'gender': 'Male',
                       'religion': '',
                       'country': '',
                       'occupation': '',
                       #'maritial_status': 'Single',
                       'photo':'',
                       'email': '',
                       'mobile': '',
                       'telephone': '',
                       'gname': '',
                       'gphone': '',
                       'notes': ''
                       }


class Engine(CodeInfo):
    """."""
    def __init__(self):
        """."""
        super(Engine, self).__init__()

    def __call__(self, str_method='', fresh=True):
        """."""
        try:
            if str_method:
                func = getattr(self, str_method)
            self.params.update({'fresh':fresh})
            return func(**self.params)
        except AttributeError:
            return "<h1>Page Not Found</h1>"

    def __generate_patient_id(self):
        """."""
        return '123456'

    def patient(self, **params):
        """."""
        fresh = params.get('fresh')
        if fresh:
            params['patient_id'] = ''  # """ID: {0}""".format(self.__generate_patient_id())
            return bottle.template('patient.html', **params)

        ## if not fresh fetech from DB

        request_params = bottle.request.params
        
        _params_dict = dict()

        for key, value in request_params.items():
            _params_dict[key] = value

        _params_dict['patient_id'] = """ID: {0}""".format(self.__generate_patient_id())

        self.params.update(_params_dict)

        import pdb; pdb.set_trace() # BREAKPOINT
        return bottle.template('patient.html', **self.params)
