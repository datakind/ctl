#
#   Copyright (c) 2010-2013, MIT Probabilistic Computing Project
#
#   Lead Developers: Dan Lovell and Jay Baxter
#   Authors: Dan Lovell, Baxter Eaves, Jay Baxter, Vikash Mansinghka
#   Research Leads: Vikash Mansinghka, Patrick Shafto
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import cPickle
import gzip
import os
#
import pandas


def is_gz(filename):
    ext = os.path.splitext(filename)[-1]
    return ext == '.gz'

def my_open(filename):
    opener = open
    if is_gz(filename):
        opener = gzip.open
    return opener

def pickle(variable, filename, dir=''):
    full_filename = os.path.join(dir, filename)
    opener = my_open(full_filename)
    with opener(full_filename, 'wb') as fh:
        cPickle.dump(variable, fh)

def unpickle(filename, dir=''):
    full_filename = os.path.join(dir, filename)
    opener = my_open(full_filename)
    with opener(full_filename, 'rb') as fh:
        variable = cPickle.load(fh)
    return variable

def process_or_unpickle(filename, func):
    pkl_filename = filename + '.pkl'
    if os.path.isfile(pkl_filename):
        print 'using pickled file: %s' % pkl_filename
        ret_var = unpickle(pkl_filename)
    else:
        print 'processing and pickling %s' % filename
        ret_var = func(filename)
        pickle(ret_var, pkl_filename)
    return ret_var


def process_or_read_hdf(filename, func, key):
    h5_filename = filename + '.h5'
    ret_F = None
    if os.path.isfile(h5_filename):
        print 'using h5 file: %s' % h5_filename
        ret_F = pandas.read_hdf(h5_filename, key)
    else:
        print 'processing and storing %s' % filename
        ret_F = func(filename)
        ret_F.to_hdf(h5_filename, key)
    return ret_F
