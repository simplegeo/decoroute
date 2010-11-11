#
# $Id: Makefile,v e834a419882a 2009/10/28 08:02:52 vsevolod $
#

all: build

arch:
	cp -f PKGBUILD PKGBUILD.local
	sed -i -e 's/_hgroot=.*/_hgroot=../' PKGBUILD.local
	makepkg -p PKGBUILD.local

build:
	python setup.py sdist

pypi:
	python setup.py register

pypiup:
	# can`t work via proxy ?
	python setup.py sdist upload

clean:
	rm -rf build dist *.egg-info *.pyc *.tar.gz *.orig *~ pkg src PKGBUILD.local
