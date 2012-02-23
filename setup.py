from distutils.core import setup
import os

root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

data_files = []
for dirpath, dirnames, filenames in os.walk('selectfilter'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        continue
    elif filenames:
        for f in filenames:
            data_files.append(os.path.join(dirpath[21:], f))

version = "%s.%s" % __import__('selectfilter').VERSION[:2]

setup(name='django-selectfilter',
      version=version,
      description='improved Django many to many widgets',
      author='Francesco Banconi, Marcel Dancak, Ivan Mincik',
      url='https://github.com/gista/django-selectfilter',
      package_dir={'selectfilter': 'selectfilter'},
      packages=['selectfilter', 'selectfilter.forms'],
      package_data={'selectfilter': data_files},
      classifiers=['Development Status :: 4 - Beta',
                   'Framework :: Django',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
