


#coding: utf-8

import bottle

 
@bottle.route('/')
@bottle.route('/index.html')
def index():
    #return '<a href="/hello">Go to Hello World page</a>'
    return bottle.template('first.html')
 
@bottle.route('/hello')
def hello():
    return '<h1>HELLO WOLRD</h1>'
 
@bottle.route('/hello/:name')
def hello_name(name):
    page = bottle.request.GET.get('page', '1')
    return '<h1>HELLO %s <br/>(%s)</h1>' % (name, page)
 
@bottle.route('/static/:filename')
def serve_static(filename):
    return bottle.static_file(filename, root='/home/arthur/workspace/my_python_codes/src/')
 
@bottle.route('/raise_error')
def raise_error():
    bottle.abort(404, "error...")
 
@bottle.route('/redirect')
def redirect_to_hello():
    bottle.redirect('/hello')
 
@bottle.route('/ajax')
def ajax_response():
    return {'dictionary': 'you will see ajax response right? Content-Type will be "application/json"'}
 
@bottle.error(404)
def error404(error):
    return '404 error !!!!!'
 
@bottle.get('/upload')
def upload_view():
    return """
        <form action="/upload" method="post" enctype="multipart/form-data">
          <input type="text" name="name" />
          <input type="file" name="data" />
          <input type="submit" name="submit" value="upload now" />
        </form>
        """    
 
@bottle.post('/upload')
def do_upload():
    name = bottle.request.forms.get('name')
    data = bottle.request.files.get('data')
    if name is not None and data is not None:
        raw = data.file.read() # small files =.=
        filename = data.filename
        return "Hello %s! You uploaded %s (%d bytes)." % (name, filename, len(raw))
    return "You missed a field."
 
@bottle.route('/tpl')
def tpl():
    return template('test')
 
# Static pages

@bottle.route('/login')
@bottle.view('login_form')
def login_form():
    """Serve login form"""
    return {}

@bottle.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'

@bottle.get('/<filename:re:.*\.(tpl|html)>')
def templates(filename):
    return bottle.static_file(filename, root='views')

@bottle.get('/<filename:re:.*\.js>')
def javascripts(filename):
    return bottle.static_file(filename, root='static/js')

@bottle.get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return bottle.static_file(filename, root='static/css')

@bottle.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return bottle.static_file(filename, root='static/images')

##  Web application main  # #
def main():

    # Start the Bottle webapp
    bottle.debug(True)
    bottle.run(host='localhost', port=8000, reloader=True)

if __name__ == "__main__":
    main()
