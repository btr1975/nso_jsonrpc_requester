from setuptools import setup
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = [
    'nso_jsonrpc_requester'
]

install_requires = [
    'requests ~= 2.23.0',
    'PyYAML ~= 5.3.1',
]

tests_require = [
    'pytest',
]

setup(
    name='nso_jsonrpc_requester',
    version='1.0.3',
    python_requires='>=3.3',
    description='This is a library used to manipulate data in Cisco NSO',
    long_description=long_description,
    long_description_content_type='text/restructuredtext',
    keywords='cisco nso json rpc network engineer',
    # url='https://nso_jsonrpc_requester.readthedocs.io',
    project_urls={
        # 'Documentation': 'https://nso_jsonrpc_requester.readthedocs.io/en/latest/',
        'Source': 'https://github.com/btr1975/nso_jsonrpc_requester',
        'Tracker': 'https://github.com/btr1975/nso_jsonrpc_requester/issues',
    },
    author='Benjamin P. Trachtenberg',
    author_email='e_ben_75-python@yahoo.com',
    license='MIT',
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    test_suite='pytest',
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
