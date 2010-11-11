# -*- shell-script -*-
# Arch Linux package build script
#
# Contributor: Vsevolod Balashov <vsevolod@balashov.name>
#
# $Id: PKGBUILD,v 870e0d9d07c9 2009/10/28 07:27:50 vsevolod $

name=decoroute
pkgname=python-$name-hg
pkgver=45
pkgrel=1
pkgdesc="Pattern-matching based WSGI-compliant URL routing tool"
arch=(any)
url="http://pypi.python.org/pypi/$name"
license=('LGPL2')
depends=('python')
makedepends=('setuptools' 'mercurial')

_hgroot="http://bitbucket.org/sevkin/"
_hgrepo=decoroute

build() {
  cd "$srcdir/$name"
  python setup.py install --prefix=/usr --root=$startdir/pkg || return 1
}
