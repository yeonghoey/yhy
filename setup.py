import ast
import re
from setuptools import find_packages, setup


def extract_version(content):
    m = re.search(r'__version__\s+=\s+(.*)', content)
    s = m.group(1)
    return str(ast.literal_eval(s))


with open('yhy/__init__.py', 'rb') as f:
    content = f.read().decode('utf-8')
    version = extract_version(content)


setup(
    name='yhy',
    version=version,
    description='Personalized CLI',
    keywords='automation cli anki',
    url='https://github.com/yeonghoey/yhy',

    author='Yeongho Kim',
    author_email='yeonghoey@gmail.com',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'yhy=yhy.__main__:cli',
        ]
    },

    install_requires=[
        'Click',
        'pillow',
        'pyperclip',
        'requests'
    ],

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],
)
