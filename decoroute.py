#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# $Id: decoroute.py,v 7027370799fe 2009/10/28 07:01:52 vsevolod $
#
# Pattern Matching based WSGI-enabled URL routing tool.
#
# Actual version on http://pypi.python.org/pypi/decoroute
#
# (C) 2008, 2009 by Vsevolod S. Balashov <vsevolod@balashov.name>
# under terms of GNU LGPL v2.1 http://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt

__author__  = "Vsevolod Balashov"
__email__   = "vsevolod@balashov.name"
__version__ = "0.8.1"

import re
from collections import defaultdict

__all__ = ['NotFound', 'App', 'wsgi']

class NotFound(Exception):
    pass

_pattern_re = re.compile(r'''
    ([^<]+)                     # static rule data
    (?:<
        ([a-zA-Z][a-zA-Z0-9_]*) # variable name
        \:
        ([^>]+)                 # regexp constraint
    >)?
''', re.VERBOSE)

def pattern2regexp(pattern, f, s = lambda x: re.escape(x)):
    def parser():
        for t in _pattern_re.findall(pattern):
            yield s(t[0])
            if t[1] != '':
                yield f(t[1], t[2])
    return parser()

make_url_for = lambda p: ''.join(pattern2regexp(p, lambda v, r: '%%(%s)s' % v, lambda s: s))
make_variables = lambda p: filter(lambda x: x, pattern2regexp(p, lambda v, r: v, lambda s: None))
make_pattern = lambda p: r''.join(pattern2regexp(p, lambda v, r: r'(?P<%s>%s)' % (v, r)))
make_selector_fragment = lambda p: r''.join(pattern2regexp(p, lambda v, r: r'(?:%s)' % r))
make_selector = lambda i: r'(^%s$)' % r'$)|(^'.join(map(make_selector_fragment, i))

class UrlMap(object):
    "if you understand it - you are python jedi, else - just use it"
    
    def __init__(self):
        self._endpoints = {}
        self._defaults = defaultdict(lambda:{})
        self._patterns = {}
        self._pattern_selector = re.compile(make_selector(self._patterns.iterkeys()))
    
    def add(self, pattern, endpoint, **kw):
        if self._patterns.has_key(pattern):
            raise Exception('duplicate pattern', pattern)
        self._endpoints[(endpoint, frozenset(make_variables(pattern)))] = make_url_for(pattern)
        keyvalues = frozenset([(k, v) for k,v in kw.iteritems()])
        if keyvalues != frozenset():
            if self._defaults[endpoint].has_key(keyvalues):
                raise Exception('duplicate defaults for endpoint', endpoint, kw)
            for key in self._defaults[endpoint].keys():
                if keyvalues.issuperset(key) or keyvalues.issubset(key):
                    raise Exception('defaults for endpoint already exist in route', endpoint, \
                      kw, dict([c for c in key]))
            self._defaults[endpoint][keyvalues] = set(kw.keys())
        self._patterns[pattern] = (re.compile(make_pattern(pattern)), endpoint, kw)
        self._pattern_selector = re.compile(make_selector(self._patterns.iterkeys()))
    
    def route(self, url):
        """return (endpoint, kw)
            kw = parsed from url + defaults for this url
        """
        try:
            p = self._patterns.values()[re.match(self._pattern_selector, url).lastindex - 1]
            m = p[0].match(url)
            d = m.groupdict().copy()
            d.update(p[2])
            # l = list(m.groups()) ## http://wsgi.org/wsgi/Specifications/routing_args#example
            # e = url[m.end():]
            return p[1], d #, l, e
        except Exception, e:
            raise NotFound('route not found', url)
    
    def url_for(self, endpoint, **kw):
        keyvalues = frozenset([(k, v) for k,v in kw.iteritems()])
        keys = set(kw.keys())
        for defaults in self._defaults[endpoint].keys():
            if defaults.issubset(keyvalues):
                keys -= self._defaults[endpoint][defaults]
                #TODO what if find another?
                break
        return self._endpoints[(endpoint, frozenset(keys))] % kw

class App(object):
    def __init__(self, prefix = '', key = 'decoroute.app'):
        self.map = UrlMap()
        self._prefix = (prefix, re.compile(r'^%s' % re.escape(prefix)))
        self._key = key
        self._not_found = lambda e: ('404 NOT FOUND', [("Content-Type", "text/plain")], [''])
        self._render = lambda e, r: r
    
    def route(self, env):
        env[self._key] = self
        path, n = self._prefix[1].subn('', env['PATH_INFO'])
        if n == 1:
            endpoint, kw = self.map.route(path)
        else:
            raise NotFound()
        return endpoint(env, **kw)
    
    def url_for(self, endpoint, **kw):
        return self._prefix[0] + self.map.url_for(endpoint, **kw)
    
    def __call__(self, env, start_response):
        def helper((response, headers, body)):
            start_response(response, headers)
            return body
        try:
            return helper(self._render(env, self.route(env)))
        except NotFound:
            return helper(self._render(env, self._not_found(env)))
    
    def expose(self, pattern, **kw):
        def decorate(f):
            self.map.add(pattern, f, **kw)
            return f
        return decorate
    
    def not_found(self, f):
        self._not_found = f
        return f
    
    def render(self, f):
        self._render = f
        return f

class Response(object):
    def __call__(self, status, headers):
        self.status = status
        self.headers = headers

def wsgi(key_name):
    "put kw into env[key_name] and make endpoint wsgi-compliant"
    def decorate(f):
        def fun(env, **kw):
            response = Response()
            env[key_name]=kw
            body=f(env, response)
            return response.status, response.headers, body
        return fun
    return decorate

def request_method(*a):
    "not implemented"
    def decorate(f):
        s = frozenset(a)
        def proxy(env, **kw):
            assert s.issuperset(frozenset([env['REQUEST_METHOD']]))
            return f(env, **kw)
        return proxy # , s
    return decorate
