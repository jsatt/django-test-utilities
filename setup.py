#!/usr/bin/env python
#
# Copyright 2013 Consumers Unified LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from setuptools import setup


setup(
    name='django-test-utilities',
    version='0.5.1',
    author='Jeremy Satterfield',
    author_email='jsatt0@gmail.com',
    description='Additional test functionality useful within Django',
    license='Apache License 2.0',
    url='https://github.com/jsatt/django-test-utilities',
    packages=['test_utilities'],
    install_requires=['Django>=1.2'],
    long_description=(
        'Additional test case methods which are useful within Django'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
