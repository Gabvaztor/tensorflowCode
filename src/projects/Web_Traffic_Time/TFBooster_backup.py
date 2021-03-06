# -*- coding: utf-8 -*-
"""
Author: @gabvaztor
StartDate: 04/03/2017

This file contains the next information:
    - Libraries to import with installation comment and reason.
    - Data Mining Algorithm.
    - Sets (train,validation and test) information.
    - ANN Arquitectures.
    - A lot of utils methods which you'll get useful advantage


The code's structure is:
    - Imports
    - Global Variables
    - Interface
    - Reading data algorithms
    - Data Mining
    - Training and test
    - Show final conclusions

Style: "Google Python Style Guide" 
https://google.github.io/styleguide/pyguide.html

Notes:
    * This file use TensorFlow version >1.0.
"""

"""
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
"""

'''LOCAL IMPORTS
* UtilsFunctions is a library that contains a lot of functions which will help us
to code expressively, clearly and efficiently.
* TensorFlowGUI's library contains all GUI's methods. Contains EasyGUI.
Here you can download the library: https://pypi.python.org/pypi/easygui#downloads
It had been used the version: 0.98.1
'''

import TFBoost.TFReader as tfr
from TFBoost.TFEncoder import Dictionary
from UsefulTools.UtilsFunctions import *
import TFBoost.TFModels as models
from src import SettingsObject

''' TensorFlow: https://www.tensorflow.org/
To upgrade TensorFlow to last version:
*CPU: pip3 install --upgrade tensorflow
*GPU: pip3 install --upgrade tensorflow-gpu
'''
import tensorflow as tf
print("TensorFlow: " + tf.__version__)


''' Numpy is an extension to the Python programming language, adding support for large,
multi-dimensional arrays and matrices, along with a large library of high-level
mathematical functions to operate on these arrays.
It is mandatory to install 'Numpy+MKL' before scipy.
Install 'Numpy+MKL' from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
http://www.numpy.org/
https://en.wikipedia.org/wiki/NumPy '''

'''
# You need to install the 64bit version of Scipy, at least on Windows.
# It is mandatory to install 'Numpy+MKL' before scipy.
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
# We can find scipi in the url: http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy'''

''' Matlab URL: http://matplotlib.org/users/installing.html
python -m pip3 install matplotlib'''

''' TFLearn library. License MIT.
Git Clone : https://github.com/tflearn/tflearn.git
    To install: pip install tflearn'''
'''
 Sklearn(scikit-learn): Simple and efficient tools for data mining and data analysis
 To install: pip3 install -U scikit-learn
'''
"""
To install pandas: pip3 install pandas
"""
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ---- GLOBAL VARIABLES ----
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
"""

"""
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ---- USER INTERFACE ----
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
"""Creating user interface
#properties = eg.EasyGui()
#uf.pt("Typos GUI",properties.types)

"""
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ---- READING DATA ----
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


# Setting object
setting_object_web_traffic = SettingsObject.Settings(Dictionary.string_settings_web_traffic)
# Option problem
option_problem_web_traffic = Dictionary.string_option_web_traffic_problem
# Number of classes
number_of_classes_web_traffic = 1
# Path Train: Must be a list
path_train_validation_test_sets_web_traffic  = [setting_object_web_traffic.train_path,
                                                setting_object_web_traffic.test_path,
                                                setting_object_web_traffic.model_path,
                                                setting_object_web_traffic.submission_path]
# Labels_set
labels_set_web_traffic = None
# Sets_Percentages
percentages_sets_web_traffic = [0.7,0.2,0.1]
# Is unique
is_an_unique_csv_web_traffic = False  # If this variable is true, then only one CSV file will be passed and it will be treated like
# trainSet, validationSet(if necessary) and testSet
known_data_type_web_traffic = None  # Contains the type of data if the data file contains an unique type of data. Examples: # Number

tf_reader_web_traffic = tfr.Reader(delimiter=Dictionary.string_char_comma,
                                   paths_to_read=path_train_validation_test_sets_web_traffic,
                                   number_of_classes=number_of_classes_web_traffic,
                                   labels_set=labels_set_web_traffic,
                                   is_unique_file=is_an_unique_csv_web_traffic,
                                   known_data_type=known_data_type_web_traffic,
                                   percentages_sets=percentages_sets_web_traffic,
                                   type_problem=option_problem_web_traffic)  # Reader Object with all information

validation_set_web_traffic = tf_reader_web_traffic.validation_set  # Test Set
train_set_web_traffic  = tf_reader_web_traffic.train_set  # Train Set

del tf_reader_web_traffic

names_of_data = ["input_data", "validation_data", "inputs_labels", "validation_labels"]
names_of_data_updated = ["input_data_updated", "validation_data_updated", "inputs_labels", "validation_labels"]
names_dictionaries = ["input_validation_dictionary"]
# Load input, validation and labels from updated arrays where inputs are [number, float] where number is
# the page id and float is the visits' number

input_data, validation, input_labels, validation_labels = \
    load_numpy_arrays_generic(path_to_load=setting_object_web_traffic.accuracies_losses_path,
                              names=names_of_data_updated)
models_zillow_price = models.TFModels(input_data=input_data,
                                      input_labels=input_labels,
                                      validation=validation,
                                      validation_labels=validation_labels,
                                      number_of_classes=number_of_classes_web_traffic,
                                      setting_object=setting_object_web_traffic,
                                      option_problem=option_problem_web_traffic,
                                      load_model_configuration=False)
#with tf.device('/gpu:0'):
models_zillow_price.rnn_lstm_web_traffic_time()

