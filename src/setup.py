from setuptools import find_packages
from setuptools import setup

setup(
    name='deepin-talk',
    version=1.0,
    description='Talk for Linux Deepin',
    long_description='Talk for Linux Deepin',
    author='LinuxDeepin',
    author_email='deepin@gmail.com',
    url='http://github.com/linuxdeepin/deepin-talk/',
    include_package_data=True,
    packages=['dtalk',
	      'dtalk.cache',
	      'dtalk.conf',
	      'dtalk.controls',
	      'dtalk.core',
	      'dtalk.dispatch',
	      'dtalk.gui',
	      'dtalk.gui.plugins',
	      'dtalk.keybinder',
	      'dtalk.models',
	      'dtalk.utils',
	      'dtalk.views',
	      'dtalk.views.expression',
	      'dtalk.views.widgets',
	      'dtalk.xmpp',
    ],
    package_data={
	      'dtalk.views.expression': ['dtalk/views/expression/QQexpression/*.gif'],
	      'dtalk.views': [
			'dtalk/views/images/*/*.png',
			'dtalk/views/qml/*.qml',
			'dtalk/views/qml/*/*.qml',
			'dtalk/views/qml/scripts/*.js',
			'dtalk/views/qss/dtalk.css']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
	'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
	'Topic :: Communications :: Chat',
    ],
    scripts = ['dtalk.py'],
)
