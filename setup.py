import os
from posixpath import curdir, sep, pardir, join, abspath, commonprefix
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

# package_data files
package = 'selectfilter'
package_data_dirs = ('selectfilter/locale', 'selectfilter/static')
package_data_files = []

def relpath(path, start=curdir):
	"""Return a relative version of a path (missing in Python <=2.5)."""
	if not path:
		raise ValueError("no path specified")
	start_list = abspath(start).split(sep)
	path_list = abspath(path).split(sep)
	i = len(commonprefix([start_list, path_list]))
	rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
	if not rel_list:
		return curdir
	return join(*rel_list)

for data_dir in package_data_dirs:
	filelist = []
	for dirpath, dirnames, filenames in os.walk(data_dir):
		for filename in filenames:
			if os.path.isfile(os.path.join(dirpath, filename)):
				filelist.append(relpath(os.path.join(dirpath, filename), package))
	package_data_files.extend(filelist)

# version
version = "%s.%s.%s" % __import__('selectfilter').VERSION[:3]
print version

# setup
setup(name='django-selectfilter',
      version=version,
      description='improved Django many to many widgets',
      author='Francesco Banconi, Marcel Dancak, Ivan Mincik',
      url='https://github.com/gista/django-selectfilter',
      package_dir={'django-selectfilter': '.'},
      packages=['selectfilter', 'selectfilter.forms'],
      package_data={'selectfilter': package_data_files},
      classifiers=classifiers,
      )
