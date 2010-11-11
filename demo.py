## $Id: demo.py,v c9e97604c73e 2008/07/30 11:26:55 vsevolod $

import decoroute
    
app = decoroute.App(prefix='')
    
# pure WSGI
@app.expose('/wsgi/<id:\d+>')
@decoroute.wsgi('path.kw')
def wsgi_app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return environ['path.kw']
    
# pass variables into **kw
def render_response(status = '200 OK', content_type = 'text/plain', add_headers = [], **context):
    return status, [('Content-Type', content_type)] + add_headers, context
    
@app.expose('/node', id = '1')
@app.expose('/node/<id:\d+>')
def node(env, id):
    return render_response(id = id)
    
@app.expose('/url_for')
def url_for(env):
    return render_response(url = app.url_for(node, id = 666))
    
@app.expose('/404')
def not_found(env):
    raise decoroute.NotFound()
    
@app.not_found
def not_found_handler(env):
    return render_response(status = '404 NF', **env)
    
@app.render
def render(env, (status, headers, context)):
    context['site_uri'] = '%s://%s' % (env['wsgi.url_scheme'], env['HTTP_HOST'])
    return status, headers, ['%s=%s\n' %(k, context[k]) for k in context.keys()] # fake templating
    
from wsgiref.simple_server import make_server
    
make_server('', 6666, app).serve_forever()
