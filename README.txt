decoroute
=========

.. contents:

Decorator style and pattern-matching based url routing library. No framework!
Very compact. Core logic less 100 lines of code. WSGI compliant. No additional API required.

Complete example
----------------

::

    import decoroute
    
    app = decoroute.App(prefix='')
    
    # pure WSGI
    @app.expose('/wsgi/<id:\d+>')
    @decoroute.wsgi('wsgiorg.routing_args')
    def wsgi_app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return environ['wsgiorg.routing_args']
    
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

Tips
----

If you place your views (Django term. in ror - controller) in another modules, organize code like
`werkzeug <http://dev.pocoo.org/hg/werkzeug-main/file/tip/examples/shorty/>`_.

::

    # utils.py
    
    import decoroute
    app = decoroute.App()

::

    # view.py and anoter
    
    from utils import *
    
    @app.render
    def render(env, ...)
        # returns of your endpoints pass to render handler
        # in render use your prefered template engine and return triple
        # status, generator of response headers, generator of response body
        # ( generator / iterator / list - any )
        # if you use default render endpoints must be return triple
    
    @app.not_found
        # no route enpoint
        # it also pass to render handler
    
    @app.expose('/node', id = '1')
    @app.expose('/node/<id:\d+>')
    def node(env, id):
        # endpoint passed some variables
        # env is a wsgi environ
        # id = '1' default value of parameter
        #   all parameters must be <type 'str'>
        # <id:\d+> parameter pattern;
        #   \d+ specify regexp constraint of parameter (required)

::

    # manage.py - main module
    
    from utils import app
    import view # and all other
    
    if __name__ == '__main__':
        # serve app here

Legal
-----

decoroute distributed under terms of
`GNU LGPL v.2.1 <http://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt>`_.

Copyright 2008, 2009 `Vsevolod Balashov <http://vsevolod.balashov.name/>`_.

Links
-----

Source code of `decoroute <http://bitbucket.org/sevkin/decoroute/>`_.
Arch Linux `PKGBUILD <http://aur.archlinux.org/packages.php?ID=31564>`_.
