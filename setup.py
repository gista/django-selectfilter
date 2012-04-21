import os
from distutils.core import setup

# classifiers
classifiers = [
	'Development Status :: 4 - Beta',
	'Framework :: Django',
	'Environment :: Web Environment',
	'Intended Audience :: Developers',
	'License :: OSI Approved :: MIT License',
	'Operating System :: OS Independent',
	'Programming Language :: Python',
	'Topic :: Utilities',
]

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
package_root_dir = 'selectfilter'
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
	os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk(package_root_dir):
	# Ignore dirnames that start with '.'
	for i, dirname in enumerate(dirnames):
		if dirname.startswith('.'): del dirnames[i]
	if '__init__.py' in filenames:
		pkg = dirpath.replace(os.path.sep, '.')
		if os.path.altsep:
			pkg = pkg.replace(os.path.altsep, '.')
		packages.append(pkg)
	elif filenames:
		prefix = dirpath[len(package_root_dir)+1:] # Strip "package_root_dir/" from path
		for f in filenames:
			data_files.append(os.path.join(prefix, f))

# setup
setup(name='django-selectfilter',
	version="%s.%s.%s" % __import__('selectfilter').VERSION[:3],
	description='improved Django many to many widgets',
	author='Francesco Banconi, Marcel Dancak, Ivan Mincik',
	author_email='francesco.banconi@gmail.com, marcel.dancak@gista.sk, ivan.mincik@gista.sk',
	url='https://github.com/gista/django-selectfilter',
	package_dir={'selectfilter': 'selectfilter'},
	packages=packages,
	package_data={'selectfilter': data_files},
	classifiers=classifiers,
)
