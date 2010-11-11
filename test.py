#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:et
# $Id: test.py,v 6357de52402e 2008/06/30 05:59:15 vsevolod $
#

from nose.tools import raises
import decoroute

class TestRE:
    
    def test_make_url_for(self):
        assert decoroute.make_url_for('/') == '/'
        assert decoroute.make_url_for('/node') == '/node'
        assert decoroute.make_url_for('/node<id:\d+>') == '/node%(id)s'
        decoroute.make_url_for('/node<id:\d+>/<name:[^>]+>') == '/node%(id)s/%(name)s'
    
    def test_make_variables(self):
        assert decoroute.make_variables('/') == []
        assert decoroute.make_variables('/node') == []
        assert decoroute.make_variables('/node<id:\d+>') == ['id']
        assert decoroute.make_variables('/node<id:\d+>/<name:[^/]+>') == ['id', 'name']
    
    def test_make_selector_fragment(self):
        assert decoroute.make_selector_fragment('/') == '\\/'
        assert decoroute.make_selector_fragment('/node') == '\\/node'
        assert decoroute.make_selector_fragment('/node<id:\d+>') == '\\/node(?:\\d+)'
        assert decoroute.make_selector_fragment('/node<id:\d+>/<name:[^/]+>') == '\\/node(?:\\d+)\\/(?:[^/]+)'
    
    def test_make_selector(self):
        assert decoroute.make_selector(['/']) == '(^\\/$)'
        assert decoroute.make_selector(['/', '/node']) == '(^\\/$)|(^\\/node$)'
        assert decoroute.make_selector(['/', '/node', '/node<id:\d+>']) == '(^\\/$)|(^\\/node$)|(^\\/node(?:\\d+)$)'

class TestUrlMap:
    
    def setUp(self):
        self.map = decoroute.UrlMap()
    
    def test_route(self):
        def p(cid, pid):
            pass
        self.map.add('/category_<cid:\d+>.html', p, pid = '1')
        self.map.add('/category_<cid:\d+>/page_<pid:\d+>.html', p)
        
        assert (p, dict(cid='1', pid='1')) == self.map.route('/category_1.html')
        assert (p, dict(cid='1', pid='1')) == self.map.route('/category_1/page_1.html')
        assert (p, dict(cid='1', pid='2')) == self.map.route('/category_1/page_2.html')
    
    def test_url_for(self):
        def p(cid, pid):
            pass
        self.map.add('/category_<cid:\d+>.html', p, pid = '1')
        self.map.add('/category_<cid:\d+>/page_<pid:\d+>.html', p)
        
        assert '/category_1.html' == self.map.url_for(p, cid='1')
        assert '/category_1.html' == self.map.url_for(p, cid='1', pid='1')
        assert '/category_1/page_2.html' == self.map.url_for(p, cid='1', pid='2')
    
    @raises(Exception)
    def test_param_defaults_subset(self):
        def ab(a, b):
            pass
        self.map.add('/a_<a:\d+>/b_<b:\d+>', ab)
        self.map.add('/static', ab, a=1, b=2)
        try:
            self.map.add('/a/b_<b:\d+>', ab, b=2)
        except Exception, e:
            assert e.args[2] == dict(b=2) and e.args[3] == dict(a=1, b=2)
            raise
    
    @raises(Exception)
    def test_param_defaults_superset(self):
        def ab(a, b):
            pass
        self.map.add('/a_<a:\d+>/b_<b:\d+>', ab)
        self.map.add('/a/b_<b:\d+>', ab, b=2)
        try:
            self.map.add('/static', ab, a=1, b=2)
        except Exception, e:
            assert e.args[2] == dict(a=1, b=2) and e.args[3] == dict(b=2)
            raise

class TestApp:
    pass

class TestRequestMethod:
    pass
