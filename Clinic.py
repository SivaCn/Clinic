


"""
"""

# -*- coding: utf-8 -*-

## ------------ Begin Default Imports ------------ ##
from defaults import *
## ------------ End Default Imports ------------ ##


## ------------ Begin Exposed Methods ------------ ##

## ------------ Begin Session Manager ------------ ##
#session_manager = bottlesession.PickleSession()
session_manager = bottlesession.CookieSession()
valid_user = bottlesession.authenticator(session_manager)

@route('/')
@valid_user()
def main():
    import pdb; pdb.set_trace()  # BREAKPOINT
    return jinjaEngine.Jinja().renderTemplate(r'templates', 'login.html')

@route('/login')
def login():
    db = Sqlite()
    session = session_manager.get_session()
    session['valid'] = True
    session_manager.save(session)
    bottle.redirect(bottle.request.cookies.get('validuserloginredirect', '/'))

@route('/logout')
def logout():
   session = session_manager.get_session()
   session['valid'] = False
   session_manager.save(session)
   bottle.redirect('/login')
## ------------ End Session Manager ------------ ##

## --------- Begin Error Handling --------- ##

@error(404)
def error404(error):
    """
    """
    return '404 error !!!!!'

## --------- End Error Handling --------- ##


## --------- Begin File Handling --------- ##

@get('/upload')
def upload_view():
    """
    """
    return """
        <form action="/upload" method="post" enctype="multipart/form-data">
          <input type="text" name="name" />
          <input type="file" name="data" />
          <input type="submit" name="submit" value="upload now" />
        </form>
        """

@post('/upload')
def do_upload():
    """
    """
    name = request.forms.get('name')
    data = request.files.get('data')
    if name is not None and data is not None:
        raw = data.file.read() # small files =.=
        filename = data.filename
        return "Hello %s! You uploaded %s (%d bytes)." % (name, filename, len(raw))
    return "You missed a field."

## --------- End File Handling --------- ##

## ------------ End Exposed Methods ------------ ##

if __name__ == "__main__":
    """
    """
    app = app()
    debug(True)
    run(app=app, host='localhost', port=8000, reloader=True)
