#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: @gabvaztor
StartDate: 04/03/2017

This file contains samples and overrides deep learning algorithms.

Style: "Google Python Style Guide"
https://google.github.io/styleguide/pyguide.html

"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
"""

'''LOCAL IMPORTS'''
import src.config.GlobalSettings as GS
import src.utils.Inputs as inputs
import src.utils.UtilsFunctions as utils
import src.utils.Jsons as jsons
import src.utils.Folders as folders

from src.utils.Errors import Errors
from src.utils.Constants import Constant
from src.utils.Dictionary import Dictionary
from src.utils.Prints import pt
import src.utils.Prints as prints
from src.config.Projects import Projects
from src.config.GlobalDecorators import DecoratorClass
from src.utils.AsynchronousThreading import execute_asynchronous_thread
from src.utils.Logger import Logger

LOGGER = GS.LOGGER if GS.LOGGER else Logger()

# noinspection PyUnresolvedReferences
print("CModel Executed")

''' Numpy is an extension to the Python programming language, adding support for large,
multi-dimensional arrays and matrices, along with a large library of high-level
mathematical functions to operate on these arrays.
It is mandatory to install 'Numpy+MKL' before scipy.
Install 'Numpy+MKL' from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
http://www.numpy.org/
https://en.wikipedia.org/wiki/NumPy '''
import numpy as np

if not GS.MINIMUM_IMPORTS:
    ''' Matlab URL: http://matplotlib.org/users/installing.html'''
    import matplotlib.pyplot as plt

''' Pillow URL: https://pillow.readthedocs.io/en/5.1.x/
Problem with OpenCV on Raspbian. Installed Pillow. '''

import PIL.Image
import PIL

''' TFLearn library. License MIT.
Git Clone : https://github.com/tflearn/tflearn.git
To install: pip3 install tflearn'''

'''"Best image library"
pip3 install opencv-python
Imported by petition (variable flag) because of problem on raspberry. Used PILLOW instead'''
# import cv2

"""Python libraries"""
""" Random to shuffle lists """
import random

""" Time """
import time
""" Datetime"""
import datetime

""" To serialize object"""

""" To print stacktrace"""
import traceback

""" To work with numbers"""

""" To work with types"""

""" To recollect python rash"""
import gc

import os

import tensorflow as tf

""" GLOBAL VARIABLES"""
global GLOBAL_FUNCTION
global GLOBAL_METADATA
INPUT_VALUE = ""
CONSOLE_WORDS_OPTION = ["WAIT -t", "SAVE", "CODE 'a condition'", "STOP", "HELP"]



if not GS.GPU_TO_TRAIN:
    os.environ["NUM_CUDA_VISIBLE_DEVICES"] = "0"
else:
    pt("Cuda visible from CModels:",2)

class CModels():
    """
    Long Docs ...
    """
    # TODO (@gabvaztor) Docs
    def __init__(self, setting_object=None, option_problem=None, input_data=None, test=None, input_labels=None,
                 test_labels=None, number_of_classes=None , type=None, validation=None, validation_labels=None,
                 predict_flag=False, execute_background_process=False):
        global LOGGER
        LOGGER = GS.LOGGER
        # TODO (@gabvaztor) Show and save graphs during all training asking before
        # TODO (@gabvaztor) Run some operations in other python execution or multiprocessing
        # NOTE: IF YOU LOAD_MODEL_CONFIGURATION AND CHANGE SOME TENSORFLOW ATTRIBUTE AS NEURONS, THE TRAIN WILL START
        # AGAIN
        self._input = input_data
        self._validation = validation
        self._test = test
        self._input_labels = input_labels
        self._validation_labels = validation_labels
        self._test_labels = test_labels
        self._number_of_classes = number_of_classes
        self._settings_object = setting_object  # Setting object represent a kaggle configuration
        self._input_batch = None
        self._label_batch = None
        # Parallel processes
        self._processes = []
        # CONFIGURATION VARIABLES
        self._debug_level = 0 # TODO (@gabvaztor) Explain debug levels
        self._restore_model = False # Labels and logits info. Load only to continue training.
        self._restore_model_configuration = self.restore_model  # By defect, use restore_model value. This, load variables from configuration file.
        self._restore_to_predict = predict_flag  # Load pretrained model to do a prediction. Restrictive
        self._save_model_information = False  # If must to save model or not
        self._ask_to_save_model_information = False  # If True and 'save_model' is true, ask to save model each time
        # TODO (@gabvaztor) Create a flag variable with which you can change a variable value before load and, if
        # the value change, the changed value is priority
        # 'should_save'
        self._show_when_save_information = False  # If True then you will see printed in console when during training
        # the information.json has been saved.
        self._ask_to_continue_creating_model_without_exist = False  # If True and 'restore_model' is True,
        # ask to continues save model at first if there isn't a model to restore
        self._show_advanced_info = False  # Labels and logits info.
        self._show_images = False  # If True show images when show_info is True
        self._save_model_configuration = False  # If True, then all attributes will be saved in a settings_object path.
        self._shuffle_data = False  # If True, then the train and validation data will be shuffled separately.
        self._generate_predictions = False  # If true, it tries to generate a prediction
        self._save_graphs_images = False  # If True, then save graphs images from statistical values. NOTE that this will
        # decrease the performance during training. Although this is true or false, for each time an epoch has finished,
        # the framework will save a graph
        # TRAIN MODEL VARIABLES
        self._input_rows_numbers = option_problem[2] if option_problem else None  # For example, in german problem, number of row pixels
        self._input_columns_numbers = option_problem[3] if option_problem else None  # For example, in german problem, number of column pixels
        self._epoch_numbers = 20  # Epochs number
        self._batch_size = 10  # Batch size
        if self.input is not None and not self.restore_to_predict:  # Change if necessary
            self._input_size = self.input.shape[0]  # Change if necessary
            self._trains = int(self.input_size / self.batch_size) + 1  # Total number of trains for epoch
        else:
            self._input_size = None  # Change if necessary
            self._trains = None  # Total number of trains per epoch
        if self.validation is not None:
            self._validation_size = validation.shape[0] # Change if necessary
        else:
            self._validation_size = None
        if self.test is not None:
            self._test_size = len(test) # Change if necessary
        else:
            self._test_size = None
        self._train_dropout = 0.5  # Keep probably to dropout to avoid overfitting
        # TODO (@gabvaztor) Transform neurons variable to a list
        self._first_label_neurons = 8
        self._second_label_neurons = 16
        self._third_label_neurons = 16
        self._fourth_label_neurons = 32
        # TODO (@gabvaztor) Crate lists of kernels
        self._kernel_size = [7, 7]  # Kernel patch size
        self._learning_rate = 1e-4  # Learning rate
        self._number_epoch_to_change_learning_rate = 60  #You can choose a number to change the learning rate. Number
        # represent the number of epochs before be changed.
        self._print_information = 200  # How many trains are needed to print information
        # INFORMATION VARIABLES
        self._index_buffer_data = 0  # The index for mini_batches during training. Start at zero.
        self._num_trains_count = 1  # Start at one
        self._num_epochs_count = 1  # Start at one
        self._train_accuracy = None
        self._validation_accuracy = None
        self._test_accuracy = None
        self._train_loss = None
        self._validation_loss = None
        self._test_loss = None
        self._problem_information = "Accuracy represent error. Low is better"
        self._delta_time = 0
        self._saves_information = []
        # TODO (@gabvaztor) Add mean accuracy by epoch in list (will can see a graph with evolution)
        self._train_accuracy_sum = 0.  # Sum of all train accuracies of a epoch
        self._num_actual_trains = 0
        # TODO (@gabvaztor) Create a parallel function which could save with an input() anytime.
        # OPTIONS
        # Options represent a list with this structure:
        #               - First position: "string_option" --> unique string to represent problem in question
        #               - Others positions: all variables you need to process each input and label elements
        self._options = option_problem
        # RESTART TRAINING
        self._save_and_restart = False  # All history and metadata will be saved in a different folder and the execution
        # will be restarted
        if self.save_and_restart and not self.restore_to_predict:
            # TODO (@gabvaztor) Get path from project path logic
            #utils.save_and_restart(GS.MODELS_PATH + GS.PROBLEM_ID + "Models")
            utils.save_and_restart(self.settings_object.model_path)
        # SAVE AND LOAD MODEL
        # If load_model_configuration is True, then it will load a configuration from settings_object method
        # TODO (@gabvaztor) Check when temp file exists and, if timestamp is more actual, load it.
        if self.restore_model_configuration and not self.restore_to_predict:
            # And restore time too.
            if self.restore_model:
                # input("You will load model configuration but no restore the tensorflow model, do you want to continue?")
                pt("Loading model configuration", self.settings_object.configuration_path)
                self._load_model_configuration(self.settings_object.load_actual_configuration())
        #COMRPOBAR DE DONDE GUARDAR Y COMPRUEBA LOS DATOS, DEL INFORMATION O CONFIGURATION
        if self.save_model_configuration and not self.restore_to_predict:
            # TODO (@gabvaztor) First, save a temporal file to avoid corrupts files.
            # Save model configuration in a json file
            self._save_json_configuration(Constant.attributes_to_delete_configuration)
        # TODO (@gabvaztor) Explote this feature
        # Execute input function asynchronously to force_save or wait process
        if not self.restore_to_predict and execute_background_process:
            execute_asynchronous_thread(input_while)

    @property
    def problem_information(self):
        return self._problem_information

    @problem_information.setter
    def problem_information(self, value):
        self._problem_information = value

    @property
    def validation_size(self):
        return self._validation_size

    @validation_size.setter
    def validation_size(self, value):
        self._validation_size = value

    @property
    def print_information(self):
        return self._print_information

    @print_information.setter
    def print_information(self, value):
        self._print_information = value

    @property
    def validation(self):
        return self._validation

    @validation.setter
    def validation(self, value):
        self._validation = value

    @property
    def validation_labels(self):
        return self._validation_labels

    @validation_labels.setter
    def validation_labels(self, value):
        self._validation_labels = value

    @property
    def show_when_save_information(self):
        return self._show_when_save_information

    @show_when_save_information.setter
    def show_when_save_information(self, value):
        self._show_when_save_information = value

    @property
    def ask_to_continue_creating_model_without_exist(self):
        return self._ask_to_continue_creating_model_without_exist

    @ask_to_continue_creating_model_without_exist.setter
    def ask_to_continue_creating_model_without_exist(self, value):
        self._ask_to_continue_creating_model_without_exist = value

    @property
    def number_epoch_to_change_learning_rate(self):
        return self._number_epoch_to_change_learning_rate

    @number_epoch_to_change_learning_rate.setter
    def number_epoch_to_change_learning_rate(self, value):
        self._number_epoch_to_change_learning_rate = value

    @property
    def save_and_restart(self):
        return self._save_and_restart

    @save_and_restart.setter
    def save_and_restart(self, value):
        self._save_and_restart = value

    @property
    def num_epochs_count(self):
        return self._num_epochs_count

    @num_epochs_count.setter
    def num_epochs_count(self, value):
        self._num_epochs_count = value

    @property
    def save_graphs_images(self):
        return self._save_graphs_images

    @save_graphs_images.setter
    def save_graphs_images(self, value):
        self._save_graphs_images = value

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    @property
    def input_batch(self):
        return self._input_batch

    @input_batch.setter
    def input_batch(self, value):
        self._input_batch = value

    @property
    def label_batch(self):
        return self._label_batch

    @label_batch.setter
    def label_batch(self, value):
        self._label_batch = value

    @property
    def show_advanced_info(self):
        return self._show_advanced_info

    @show_advanced_info.setter
    def show_advanced_info(self, value):
        self._show_advanced_info = value

    @property
    def save_model_information(self):
        return self._save_model_information

    @save_model_information.setter
    def save_model_information(self, value):
        self._save_model_information = value

    @property
    def save_model_configuration(self):
        return self._save_model_configuration

    @save_model_configuration.setter
    def save_model_configuration(self, value):
        self._save_model_configuration = value

    @property
    def ask_to_save_model_information(self):
        if self._save_model_information:
            return self._ask_to_save_model_information
        else:
            return False

    @ask_to_save_model_information.setter
    def ask_to_save_model_information(self, value):
        self._ask_to_save_model_information = value

    @property
    def restore_model(self):
        return self._restore_model

    @restore_model.setter
    def restore_model(self, value):
        self._restore_model = value

    @property
    def train_accuracy(self):
        return self._train_accuracy

    @train_accuracy.setter
    def train_accuracy(self, value):
        self._train_accuracy = value

    @property
    def test_accuracy(self):
        return self._test_accuracy

    @test_accuracy.setter
    def test_accuracy(self, value):
        self._test_accuracy = value

    @property
    def validation_accuracy(self):
        return self._validation_accuracy

    @validation_accuracy.setter
    def validation_accuracy(self, value):
        self._validation_accuracy = value

    @property
    def settings_object(self):
        return self._settings_object

    @settings_object.setter
    def settings_object(self, value):
        self._settings_object = value

    @property
    def learning_rate(self):
        return float("{0:.64f}".format(self._learning_rate))

    @learning_rate.setter
    def learning_rate(self, value):
        self._learning_rate = value

    @property
    def show_images(self):
        return self._show_images

    @show_images.setter
    def show_images(self, value):
        self._show_images = value

    @property
    def shuffle_data(self):
        return self._shuffle_data

    @shuffle_data.setter
    def shuffle_data(self, value):
        self._shuffle_data = value

    @property
    def input_rows_numbers(self):
        return self._input_rows_numbers

    @input_rows_numbers.setter
    def input_rows_numbers(self, value):
        self._input_rows_numbers = value

    @property
    def input_columns_numbers(self):
        return self._input_columns_numbers

    @input_columns_numbers.setter
    def input_columns_numbers(self, value):
        self._input_columns_numbers = value

    @property
    def input_columns_after_reshape(self):
        return self.input_rows_numbers * self.input_columns_numbers

    @input_columns_after_reshape.setter
    def input_columns_after_reshape(self, value):
        self.input_columns_after_reshape = value

    @property
    def input_rows_columns_array(self):
        return [self.input_rows_numbers, self.input_columns_numbers]

    @input_rows_columns_array.setter
    def input_rows_columns_array(self, value):
        self.input_rows_columns_array = value

    @property
    def kernel_size(self):
        return self._kernel_size

    @kernel_size.setter
    def kernel_size(self, value):
        self._kernel_size = value

    @property
    def input_size(self):
        return self._input_size

    @input_size.setter
    def input_size(self, value):
        self._input_size = value

    @property
    def test_size(self):
        return self._test_size

    @test_size.setter
    def test_size(self, value):
        self._test_size = value

    @property
    def batch_size(self):
        return self._batch_size

    @batch_size.setter
    def batch_size(self, value):
        self._batch_size = value

    @property
    def train_dropout(self):
        return self._train_dropout

    @train_dropout.setter
    def train_dropout(self, value):
        self._train_dropout = value

    @property
    def index_buffer_data(self):
        return self._index_buffer_data

    @index_buffer_data.setter
    def index_buffer_data(self, value):
        self._index_buffer_data = value

    @property
    def first_label_neurons(self):
        return self._first_label_neurons

    @first_label_neurons.setter
    def first_label_neurons(self, value):
        self._first_label_neurons = value

    @property
    def second_label_neurons(self):
        return self._second_label_neurons

    @second_label_neurons.setter
    def second_label_neurons(self, value):
        self._second_label_neurons = value

    @property
    def third_label_neurons(self):
        return self._third_label_neurons

    @third_label_neurons.setter
    def third_label_neurons(self, value):
        self._third_label_neurons = value

    @property
    def fourth_label_neurons(self):
        return self._fourth_label_neurons

    @fourth_label_neurons.setter
    def fourth_label_neurons(self, value):
        self._fourth_label_neurons = value

    @property
    def trains(self):
        return self._trains

    @trains.setter
    def trains(self, value):
        self._trains = value

    @property
    def num_trains_count(self):
        return self._num_trains_count

    @num_trains_count.setter
    def num_trains_count(self, value):
        self._num_trains_count = value

    @property
    def number_of_classes(self):
        return self._number_of_classes

    @number_of_classes.setter
    def number_of_classes(self, value):
        self._number_of_classes = value

    @property
    def input_labels(self):
        return self._input_labels

    @input_labels.setter
    def input_labels(self, value):
        self._input_labels = value

    @property
    def test_labels(self):
        return self._test_labels

    @test_labels.setter
    def test_labels(self, value):
        self._test_labels = value

    @property
    def epoch_numbers(self):
        return self._epoch_numbers

    @epoch_numbers.setter
    def epoch_numbers(self, value):
        self._epoch_numbers = value

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = value

    @property
    def test(self):
        return self._test

    @test.setter
    def test(self, value):
        self._test = value

    @property
    def restore_to_predict(self):
        return self._restore_to_predict

    @restore_to_predict.setter
    def restore_to_predict(self, value):
        self._restore_to_predict = value

    @property
    def debug_level(self):
        return self._debug_level

    @debug_level.setter
    def debug_level(self, value):
        self._debug_level = value

    @property
    def train_loss(self):
        return self._train_loss

    @train_loss.setter
    def train_loss(self, value):
        self._train_loss = value

    @property
    def validation_loss(self):
        return self._validation_loss

    @validation_loss.setter
    def validation_loss(self, value):
        self._validation_loss = value

    @property
    def test_loss(self):
        return self._test_loss

    @test_loss.setter
    def test_loss(self, value):
        self._test_loss = value

    @property
    def restore_model_configuration(self):
        return self._restore_model_configuration

    @restore_model_configuration.setter
    def restore_model_configuration(self, value):
        self._restore_model_configuration = value

    @property
    def delta_time(self):
        return self._delta_time

    @delta_time.setter
    def delta_time(self, value):
        self._delta_time = value

    @property
    def saves_information(self):
        return self._saves_information

    @saves_information.setter
    def saves_information(self, value):
        self._saves_information = value

    @property
    def train_accuracy_sum(self):
        return self._train_accuracy_sum

    @train_accuracy_sum.setter
    def train_accuracy_sum(self, value):
        self._train_accuracy_sum = value

    @property
    def num_actual_trains(self):
        return self._num_actual_trains

    @num_actual_trains.setter
    def num_actual_trains(self, value):
        self._num_actual_trains = value

    def _save_json_configuration(self, attributes_to_delete_configuration, save_type=None):
        try:
            save_path = self.settings_object.configuration_path
            if save_type == 2:
                save_path = utils.get_temp_file_from_fullpath(save_path)
            execute_asynchronous_thread(functions=self._save_model_to_json,
                                        arguments=(save_path,
                                                   attributes_to_delete_configuration,),
                                        kwargs={"type_file": "Configuration"})

            """
            self._save_model_to_json(self.settings_object.configuration_path,
                                     attributes_to_delete_configuration,
                                     type_file="Configuration")
            
            f = self._save_model_to_json(self.settings_object.configuration_path,
                                                   attributes_to_delete_configuration,
                                                   type_file="Configuration")
                                                   """
            """
            p = multiprocessing.Process(target=self._save_model_to_json, args=(self.settings_object.configuration_path,
                                                                           attributes_to_delete_configuration,
                                                                           "Configuration"))
            
            #import Asynchronous
            #Asynchronous.execte_asynchronous_process(functions=f, arguments=None)

            global global_function
            global global_metadata
            global_function = self._save_model_to_json
            global_metadata = (self.settings_object.configuration_path, attributes_to_delete_configuration, "Configuration")
            global_metadata = (self)

            import Asynchronous
            pass
            """
        except Exception as e:
            pt(Errors.error, e)
            traceback.print_exc()
            pass
    def convolution_model_image_v2(self):
        import importlib
        package = "src.projects." + GS.PROBLEM_ID + ".modeling"
        module_name = ".Models"
        models = importlib.import_module(name=module_name, package=package)
        models.main(self)

    def execute_model_v2(self, model, config):
        # Print actual configuration
        self.print_current_configuration(config=config)

        # Batching values and labels from input and labels (with batch size)
        if not self.restore_to_predict:
            # TODO (@gabvaztor) When restore model and don't change train size, it must to keep the same order of
            # train set.
            self.update_batch(create_dataset_flag=False)
            # To restore model
            if self.restore_model:
                #self.load_and_restore_model_v2()
                pass
            # Besides this, when test/validation set requires check its accuracy but its size is very long to save
            # in memory, it has to update all files during training to get the exact precision.

            self.train_current_model(model=model, config=config)
        else:
            #self.prediction(x_input=x_input, y_prediction=y_prediction, keep_probably=keep_probably, sess=sess)
            pass

    def train_current_model(self, model: tf.keras.Sequential, config, **kwargs):
        """

        Args:
            model: Model to be trained
            config: Current configuration

        Returns:

        """
        global INPUT_VALUE
        #DEBUG_MODE = kwargs['DEBUG']
        self.update_batch(create_dataset_flag=False)  # Generate first train batch
        self.update_batch(is_test=True)  # Generate test batch

        # TRAIN VARIABLES
        start_time = time.time()  # Start time
        actual_delta = self.delta_time  # Last delta time if exists
        # TO STATISTICS
        # To load accuracies and losses
        accuracies_train, accuracies_test, loss_train, loss_test = utils.load_accuracies_and_losses(
            self.settings_object.accuracies_losses_path, self.restore_model)
        """
        # Graph
        x_vec = np.linspace(0,1,100+1)[0:-1]
        y_vec = np.zeros(len(x_vec))
        line1 = []
        # use ggplot style for more sophisticated visuals
        plt.style.use('ggplot')

        def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.01):
            if line1==[]:
                # this is the call to matplotlib that allows dynamic plotting
                plt.ion()
                fig = plt.figure(figsize=(13,6))
                ax = fig.add_subplot(111)
                # create a variable for the line so we can later update it
                line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)
                #update plot label/title
                plt.ylabel('Y Label')
                plt.title('Title: {}'.format(identifier))
                plt.show()

            # after the figure, axis, and line are created, we only need to update the y-data
            line1.set_ydata(y1_data)
            # adjust limits if new data goes beyond bounds
            if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
                plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
            # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
            plt.pause(pause_time)

            # return line so we can update it again in the next iteration
            return line1

        y_vec[-1] = self.train_accuracy
        line1 = live_plotter(x_vec, y_vec, line1)
        y_vec = np.append(y_vec[1:],0.0)
        """
        # Folders and file where information and configuration files will be saved.
        filepath_save = None
        # Update real self.num_actual_trains:
        if self.index_buffer_data == 0:
            self.num_actual_trains = 0
        elif self.num_actual_trains == 0: # 1188
            self.num_actual_trains = int(self.num_trains_count % self.trains)  # This case only can happen when
        # you restore a model and num_actual_trains2 fails to load. Otherwise, num_actual_trains contains rigth value.
        is_new_epoch_flag = False  # Represent if training come into a new epoch. With this, a graph will be saved each
        # new epoch
        pt("Training model...")
        pt("metrics_names", model.metrics_names)
        # START  TRAINING
        for epoch in range(self.num_epochs_count, self.epoch_numbers):  # Start with load value or 0
            if is_new_epoch_flag:
                self.index_buffer_data = 0  # When it starts new epoch, index of data will be 0 again. This does not
                # happen when restore model
                self.train_accuracy_sum = 0.  # Restart train_accuracy_sum for new epoch.
                is_new_epoch_flag = False
                self.num_actual_trains = 0
                # Update batches values (because index_buffer_data restarted)
                self.update_batch()
            for num_train in range(self.num_actual_trains, self.trains):  # Start with load value or 0
                # Setting values
                #self.train_loss, self.train_accuracy = model.train_on_batch(x=self.input_batch, y=self.label_batch)
                train_metrics = model.train_on_batch(x=self.input_batch, y=self.label_batch)


                # TODO(@gabvaztor) Add validation_accuracy to training when necessary
                #self.test_loss, self.test_accuracy = model.evaluate(self.x_test, self.y_test, verbose=0)
                test_metrics = model.evaluate(self.x_test, self.y_test, verbose=0)

                test_labels_predicted = np.argmax(np.array(model(self.x_test, training=False)), axis=1)
                train_labels_predicted = np.argmax(np.array(model(self.input_batch, training=False)), axis=1)

                pt("test_labels_predicted", test_labels_predicted)
                pt("self.y_test", np.argmax(self.y_test, axis=-1))
                pt("train_labels_predicted", train_labels_predicted)
                pt("self.label_batch", np.argmax(self.label_batch, axis=-1))
                [pt("train_" + model.metrics_names[i], train_metrics[i]) for i in range(len(train_metrics))]
                [pt("test_" + model.metrics_names[i], test_metrics[i]) for i in range(len(test_metrics))]

                self.train_loss = train_metrics[0]
                self.test_loss = test_metrics[0]
                self.train_accuracy = train_metrics[1]
                self.test_accuracy = test_metrics[1]

                pt("Train loss", self.train_loss)
                pt("Train accuracy", str(self.train_accuracy * 100) + "%")

                self.train_accuracy_sum += self.train_accuracy
                # To generate statistics
                accuracies_train.append(self.train_accuracy)
                accuracies_test.append(self.test_accuracy)
                loss_train.append(self.train_loss)
                loss_test.append(self.test_loss)

                # TODO (@gabvaztor) Each X time, do a backup and continue training.

                # Update time
                delta = actual_delta + (time.time() - start_time)
                self.delta_time = delta
                day = str(int(time.strftime("%d", time.gmtime(delta))) - 1)
                to_append = "Time: " + str(time.strftime(day + " Days - %Hh%Mm%Ss", time.gmtime(delta))) + \
                            " || Train loss: " + str(self.train_loss) + " || Test loss: " + str(self.test_loss) + \
                            " || train_accuracy: " + str(self.train_accuracy) + " || test_accuracy: " + \
                            str(self.test_accuracy) + " || Trains: " + str(self.num_trains_count) + " || Epoch: " + \
                            str(epoch)

                prints.show_percent_by_total(total=self.input_size, count_number=self.index_buffer_data,
                                             to_append=to_append)
                with tf.device('/cpu:0'):
                    numpy_arrays = [accuracies_train, accuracies_test, loss_train, loss_test]
                    numpy_names = ["accuracies_train", "accuracies_test", "loss_train", "loss_test"]
                    execute_asynchronous_thread(functions=utils.save_numpy_arrays_generic,
                                                arguments=(self.settings_object.accuracies_losses_path,
                                                           numpy_arrays,
                                                           numpy_names),
                                                kwargs=None)


                #y_pre = y_prediction.eval(feed_dict_train_100)
                #prediction_ = np.argmax(y_pre, axis=1)
                #p = tf.argmax(y_prediction, axis=1).eval(feed_dict_train_100)



                # Update actual
                if num_train % self.print_information == 0 or INPUT_VALUE != "" :
                    #pt("y_pre", y_pre)
                    #pt("y_pre_sum", y_pre.sum())
                    #pt("prediction_", prediction_)
                    #pt("p", p)
                    pt("saves_information", self.saves_information)
                    percent_advance = "{0:.3f}".format(float(num_train * 100 / self.trains))
                    day = str(int(time.strftime("%d", time.gmtime(delta))) - 1)
                    pt('Time', str(time.strftime(day + " Days - %Hh%Mm%Ss", time.gmtime(delta))))
                    pt('TRAIN NUMBER: ' + str(self.num_trains_count) + ' | Percent Epoch ' +
                       str(epoch) + ": " + percent_advance + '%' + " | Trains number of actual epoch: " + str(num_train))
                    pt('train_accuracy', self.train_accuracy)
                    pt('cross_entropy_train', self.train_loss)
                    pt('test_accuracy', self.test_accuracy)
                    pt('index_buffer_data', self.index_buffer_data)
                    #pt('Mean train accuracy (actual epoch)', self.train_accuracy_sum / num_train)
                    pt('WORDS: ', str(CONSOLE_WORDS_OPTION))

                # Update indexes
                # Update num_epochs_counts
                if num_train + 1 == self.trains:  # +1 because start in 0
                    self.num_epochs_count += 1
                    is_new_epoch_flag = True
                # To decrement learning rate during training
                if self.num_epochs_count % self.number_epoch_to_change_learning_rate == 0 \
                        and self.num_epochs_count != 1 and self.index_buffer_data == 0:
                    self.learning_rate = float(self.learning_rate / 10.)
                #save_type = self.should_save(check_loss_train=True, if_is_equal=False)
                save_type = 0
                if (num_train % self.print_information == 0) and num_train >= self.print_information:
                    save_type = 1
                if save_type > 0:  # 0, not save | 1, train save | 2, force save
                    filepath_save_ = self.save_actual_model(model, save_type=save_type, config=config)
                    #fullpath_save = self.settings_object.model_path + "my_model.h5"
                    #model.save(fullpath_save)
                    pt("Model saved")
                if self.show_advanced_info:
                    #self.show_advanced_information(y_labels=y_labels, y_prediction=y_prediction,
                    #                              feed_dict=feed_dict_train_100)
                    pass
                """
                with tf.device('/cpu:0'):
                    if (self.save_graphs_images and filepath_save) or (is_new_epoch_flag):
                        if not filepath_save:
                            filepath_save = self.settings_object.configuration_path
                        self.show_save_statistics(accuracies_train=accuracies_train, accuracies_test=accuracies_test,
                                                  loss_train=loss_train, loss_test=loss_test,
                                                  folder_to_save=filepath_save, show_graphs=False,
                                                  is_new_epoch_flag=is_new_epoch_flag)
                """
                # Update num_trains_count and yo
                self.num_trains_count += 1
                self.num_actual_trains = num_train
                if self.save_model_configuration:
                    # Save configuration
                    self._save_json_configuration(Constant.attributes_to_delete_configuration, save_type=save_type)
                if INPUT_VALUE == "STOP":
                    pt("PAUSING Training...","")
                    time.sleep(3)  # 3 Seconds to save configuration
                    pt("Training PAUSED", "You can now stop process without problems.")
                    exit()
                    break
                else:
                    # Collect trash
                    if self.num_trains_count % 100 == 0:
                        gc.collect()
                    # TODO (@gabvaztor) Check update batch when it is the last train of epoch
                    # Update batches values
                    self.update_batch()

        pt('END TRAINING ')
        # Actual epoch is epoch_number
        self.actual_epoch = self.epoch_numbers
        if self.save_model_configuration:
            # Save configuration to that results
            self._save_json_configuration(Constant.attributes_to_delete_configuration)
        self.show_save_statistics(accuracies_train=accuracies_train, accuracies_test=accuracies_test,
                                  loss_train=loss_train, loss_test=loss_test, folder_to_save=filepath_save)
        self.make_predictions()


    def test_prediction(self, sess, x_input_tensor, y_prediction, x_input_pred, keep_probably, real_label=None,
                        input_path=None):
        start_time_load_model = datetime.datetime.now()
        # Restore model
        self.load_and_restore_model(session=sess)
        pt('Time to load model', (datetime.datetime.now()- start_time_load_model).total_seconds())
        if self.debug_level > 0:
            pt("x_input", x_input_tensor)
            pt("x_input.shape", x_input_tensor.shape)
            pt("x_input_pred", x_input_pred)
            pt("x_input_pred", x_input_pred.shape)
        x_input_pred = np.asarray([x_input_pred])
        feed_dict_prediction = {x_input_tensor: x_input_pred, keep_probably: 1.0}
        i = 0
        prediction = None
        if x_input_pred is not None:
            while i < 1:
                start_datetime_ = datetime.datetime.now()
                prediction = y_prediction.eval(feed_dict=feed_dict_prediction)
                pt("Prediction " + str(i), np.argmax(prediction))
                if real_label:
                    pt("Real Label", real_label)
                delta = datetime.datetime.now() - start_datetime_
                pt("Time to do inference " + str(i), delta.total_seconds())
                i += 1
            path_saved = None
            information = self.options[0]
            try:
                prediction_class = prediction.ImagePrediction(information=information, real_label=real_label,
                                                image_fullpath=input_path,
                                                prediction_label=int(np.argmax(prediction)))
                prediction_class.save_json(save_fullpath=self.settings_object.submission_path)
            except Exception as e:
                pt(Errors.error, e)
                raise ValueError("Can not save prediction json")
        else:
            raise ValueError("Can not predict the test")
        return path_saved

    def update_inputs_and_labels_shuffling(self, inputs, inputs_labels):
        """
        Update inputs_processed and labels_processed variables with an inputs and inputs_labels shuffled
        :param inputs: Represent input data
        :param inputs_labels:  Represent labels data
        """
        c = list(zip(inputs, inputs_labels))
        random.shuffle(c)
        self.inputs_processed, self.labels_processed = zip(*c)

    def shuffle_dataset(self, x, y):
        x, y = get_inputs_and_labels_shuffled(x, y)
        return x, y


    def data_buffer_generic_class(self, inputs, inputs_labels, shuffle_data=False, batch_size=None, is_test=False,
                                  options=None, create_dataset_flag=False):
        """
        Create a data buffer having necessaries class attributes (inputs,labels,...)
        Args:
            inputs: Inputs
            inputs_labels: Inputs labels
            shuffle_data: If it is necessary shuffle data.
            batch_size: The batch size.
            is_test: if the inputs are the test set.
            options: options
            create_dataset_flag: Two numpy arrays (x_batch and y_batch) with input data and input labels data batch_size like shape.

        Returns: x and y batch (can be for train, test or validation)
        """
        x_batch = []
        y_batch = []
        if is_test:
            # TODO (@gabvaztor) Create process set to create new datasets
            x_batch, y_batch = process_test_set(inputs, inputs_labels, options, create_dataset_flag=create_dataset_flag)
        else:
            if shuffle_data and self.index_buffer_data == 0:
                self.input, self.input_labels = get_inputs_and_labels_shuffled(self.input, self.input_labels)
            else:
                self.input, self.input_labels = self.input, self.input_labels  # To modify if is out class
            batch_size, out_range = self.get_out_range_and_batch()  # out_range will be True if
            # next batch is out of range
            for _ in range(batch_size):
                x, y = process_input_unity_generic(self.input[self.index_buffer_data],
                                                   self.input_labels[self.index_buffer_data],
                                                   options)
                x_batch.append(x)
                y_batch.append(y)
                self.index_buffer_data += 1
            x_batch = np.array(x_batch)
            y_batch = np.array(y_batch)
            if out_range:  # Reset index_buffer_data
                pt("index_buffer_data OUT OF RANGE")
                self.index_buffer_data = 0
        return x_batch, y_batch

    def get_out_range_and_batch(self):
        """
        Return out_range flag and new batch_size if necessary. It is necessary when batch is bigger than input rest of
        self.index_buffer_data
        :return: out_range (True or False), batch_size (int)
        """
        out_range = False
        batch_size = self.batch_size
        if self.input_size - self.index_buffer_data == 0:  # When is all inputs
            out_range = True
        elif self.input_size - self.index_buffer_data < self.batch_size:
            batch_size = self.input_size - self.index_buffer_data
            out_range = True
        return batch_size, out_range

    def should_save(self, check_loss_train=False, if_is_equal=True):
        """
        Check if must save from validation/test accuracy/error

        :return: if should save
        """
        # TODO (@gabvaztor) Save a temp file to continue training when X hours or input console
        global INPUT_VALUE
        should_save = 0
        if INPUT_VALUE != "":
            if INPUT_VALUE == "HELP":
                pt("WORDS", CONSOLE_WORDS_OPTION)
                pt("STOP", "Stop current training")
                pt("WAIT -t", "If you write WAIT, the training will be paused for 10 seconds. If you write a -t time "
                              "(WAIT -20), the training will be paused for 't' time.")
                pt("SAVE", "Force save in the actual train step")
                pt("CODE 'a condition'",
                   "With CODE you can write a python code (self.trains > 1000) and, if True, will "
                   "activate a variable that save the actual model")
                pt("HELP", "Show this message for 10 seconds")
                INPUT_VALUE = "WAIT"
            if "WAIT" in INPUT_VALUE:
                time_to_sleep = 10
                if INPUT_VALUE != "WAIT":
                    try:
                        time_to_sleep = int(INPUT_VALUE[6:])
                        if time_to_sleep <= 0:  # Must be higher than 0
                            raise ()  # Provoke error
                    except Exception:
                        pt("Bad line code of WAIT. Format: 'WAIT -10'")
                # TODO (@gabvaztor) Do sleep showing how seconds rest dinamically
                pt("WAITING " + str(time_to_sleep) + " SECONDS...")
                time.sleep(time_to_sleep)  # To sleep
                pt("Continue Training...")
            if INPUT_VALUE == "SAVE":
                should_save = 2
                # STOP training because, it is probably that index_buffer_data change value
                INPUT_VALUE = "STOP"
            if "CODE" in INPUT_VALUE:
                try:
                    condition = exec(INPUT_VALUE)
                    pt(INPUT_VALUE)
                    pt("Condition", condition)
                    if condition:
                        should_save = 1
                except Exception:
                    pt("Bad line code as condition. Format: 'self.train_loss < 0.2'")
            if INPUT_VALUE != "STOP":
                INPUT_VALUE = ""
        save_for_information = True
        # TODO (@gabvaztor) Detect when stop learning. From 60% to 10% validation/test
        if self.saves_information:
            if self.saves_information.count(1) / 2 >= 25:
                save_for_information = False
            if len(self.saves_information) >= 50:
                del self.saves_information[0]
        if should_save:  # This happens when force save for input or condition = True
            pt("FORCE SAVE...")
        else:
            if self.save_model_information and save_for_information:
                actual_information = self.settings_object.load_actual_information()
                if actual_information:
                    last_train_accuracy = actual_information._train_accuracy
                    last_test_accuracy = actual_information._test_accuracy
                    last_validation_accuracy = actual_information._validation_accuracy
                    last_train_loss = actual_information._train_loss
                    if last_train_accuracy and last_validation_accuracy and not self.ask_to_save_model_information:
                        # TODO(@gabvaztor) Check when, randomly, gradient descent obtain high accuracy
                        if self.validation_accuracy and last_validation_accuracy:
                            if if_is_equal:
                                if self.validation_accuracy >= last_validation_accuracy:  # Save checking validation
                                    #  accuracies in this moment
                                    should_save = 1
                            elif self.validation_accuracy > last_validation_accuracy:
                                should_save = 1
                    elif last_train_accuracy and last_test_accuracy and not self.ask_to_save_model_information:
                        # TODO(@gabvaztor) Check when, randomly, gradient descent obtain high accuracy
                        if self.test_accuracy and last_test_accuracy:
                            if if_is_equal:
                                # TODO (@gabvaztor) Sometimes, gradient break and always obtain same test. Fix it. (restart
                                # learning)
                                if self.test_accuracy >= last_test_accuracy:  # Save checking test
                                    #  accuracies in this moment
                                    should_save = 1
                            elif self.test_accuracy > last_test_accuracy:
                                    should_save = 1
                    else:
                        if self.ask_to_save_model_information:
                            pt("last_train_accuracy", last_train_accuracy)
                            pt("last_test_accuracy", last_test_accuracy)
                            pt("last_validation_accuracy", last_validation_accuracy)
                            pt("actual_train_accuracy", self.train_accuracy)
                            pt("actual_test_accuracy", self.test_accuracy)
                            pt("actual_validation_accuracy", self.validation_accuracy)
                            option_choosed = inputs.recurrent_ask_to_save_model()
                        else:
                            option_choosed = True
                        if option_choosed:
                            should_save = 1
                    if check_loss_train:
                        # TODO (@gabvaztor) module number parametrizable
                        if self.train_loss <= last_train_loss and (last_test_accuracy <= self.test_accuracy):
                            should_save = 1
                else:
                    should_save = 1
        if should_save:
            self.saves_information.append(1)
        else:
            self.saves_information.append(0)
        return should_save

    def _load_model_configuration(self, configuration):
        """
        Load previous configuration to class Model (self).

        This will update all class' attributes with the configuration in a json file.

        If configuration is None, the file will be created after this method if save_configuration attribute is True
        :param configuration: the json class
        """
        if configuration:
            try:
                # TODO Add to docs WHEN it is necessary to add more attributes = Do documentation
                if not self.restore_model:
                    self.restore_model = configuration._restore_model
                if configuration._epoch_numbers != self.epoch_numbers:
                    # It has preferency the actual epoch numbers.
                    if self.epoch_numbers < configuration._epoch_numbers:
                        raise ValueError("Epoch number can't be lower than last configuration. Please, put a higher "
                                         "epoch_number")
                    self.epoch_numbers = self.epoch_numbers
                self.save_model = configuration._save_model_information
                self.ask_to_save_model = configuration._ask_to_save_model_information
                self.show_info = configuration._show_advanced_info
                self.show_images = configuration._show_images
                self.save_model_configuration = configuration._save_model_configuration
                self.save_model_information = configuration._save_model_information
                self.shuffle_data = configuration._shuffle_data
                self.input_rows_numbers = configuration._input_rows_numbers
                self.input_columns_numbers = configuration._input_columns_numbers
                self.kernel_size = configuration._kernel_size
                self.batch_size = configuration._batch_size
                self.input_size = configuration._input_size
                self.test_size = configuration._test_size
                self.train_dropout = configuration._train_dropout
                self.first_label_neurons = configuration._first_label_neurons
                self.second_label_neurons = configuration._second_label_neurons
                self.third_label_neurons = configuration._third_label_neurons
                self.learning_rate = configuration._learning_rate
                self.trains = configuration._trains
                self.number_epoch_to_change_learning_rate = configuration._number_epoch_to_change_learning_rate
                self.save_graphs_images = configuration._save_graphs_images
                self.ask_to_continue_creating_model_without_exist = \
                    configuration._ask_to_continue_creating_model_without_exist
                self.ask_to_save_model_information = configuration._ask_to_save_model_information
                self.show_when_save_information = configuration._show_when_save_information
                self.print_information = configuration._print_information
                self.validation_size = configuration._validation_size
                self.problem_information = configuration._problem_information
                self.restore_to_predict = configuration._restore_to_predict
                self.debug_level = configuration._debug_level
                self.fourth_label_neurons = configuration._fourth_label_neurons
                self.restore_model_configuration = configuration._restore_model_configuration
                self.train_loss = configuration._train_loss
                self.test_loss = configuration._test_loss
                self.validation_loss = configuration._validation_loss
                self.saves_information = configuration._saves_information
                self.train_accuracy_sum = configuration._train_accuracy_sum
                self.num_actual_trains = configuration._num_actual_trains
                # If you don't restore model then you won't load train number and epochs number
                if self.restore_model:
                    self.num_trains_count = configuration._num_trains_count
                    self.num_epochs_count = configuration._num_epochs_count
                    self.index_buffer_data = configuration._index_buffer_data
                    self.delta_time = configuration._delta_time
                pt("Loaded model configuration")
            except Exception as e:
                raise ValueError("Error during load configuration", e)

    def _save_model_to_json(self, fullpath, attributes_to_delete=None, *args, **kwargs):
        """
        Save actual model configuration (with some attributes) in a json file.
        :param attributes_to_delete: represent witch attributes set must not be save in json file.
        """
        type_file = kwargs["type_file"]
        accuracy = ""
        if "accuracy" in kwargs:
            accuracy = kwargs["accuracy"]
        filepath = ""
        try:
            pt("Saving model " + type_file + " ... DO NOT STOP PYTHON PROCESS")
            json = jsons.object_to_json(object=self, attributes_to_delete=attributes_to_delete)
            folders.write_string_to_pathfile(json, fullpath)
            filepath = utils.create_historic_folder(fullpath, type_file, accuracy)
            folders.write_string_to_pathfile(json, filepath)
            pt("Model " + type_file + " has been saved")
        except Exception as e:
            pt("Can not get json from class to save " + type_file + " file.")
            pt("Do you have float32? (Probably you need numpy float64 or int) Be careful with data types.")
            pt(Errors.error, e)
            traceback.print_exc()
        return filepath

    def load_and_restore_model(self, session):
        """
        Restore a tensorflow model from a model_path checking if model_path exists and create if not.
        :param session: Tensorflow session
        """
        # TODO (@gabvaztor) Get path from project path logic
        # utils.save_and_restart(GS.MODELS_PATH + GS.PROBLEM_ID + "Models")
        if self.settings_object.model_path:
            pt("Restoring model...", self.settings_object.model_path)
            try:
                # TODO (@gabvaztor) Do Generic possibles models
                # TODO (@gabvaztor) Get path from project path logic
                # utils.save_and_restart(GS.MODELS_PATH + GS.PROBLEM_ID + "Models")
                model_possible_1 = self.settings_object.model_path + "model" + Dictionary.string_ckpt_extension
                model_possible_2 = model_possible_1 + Dictionary.string_meta_extension
                model_possible_3 = model_possible_1 + Dictionary.string_ckpt_extension
                model_possible_4 = model_possible_3 + Dictionary.string_meta_extension
                possibles_models = [model_possible_1, model_possible_2, model_possible_3, model_possible_4]
                model = [x for x in possibles_models if folders.file_exists_in_path_or_create_path(x)]
                if model:
                    saver = tf.train.import_meta_graph(model[0])
                    # Restore variables from disk.
                    saver.restore(session, model_possible_1)
                    pt("Model restored without problems")
                else:
                    if self.ask_to_continue_creating_model_without_exist:
                        response = inputs.recurrent_ask_to_continue_without_load_model()
                        if not response:
                            raise Exception()
                    else:
                        pt("The model won't load because it doesn't exist",
                           "You chose 'continue_creating_model_without_exist")
            except Exception as e:
                pt(Errors.error, e)
                raise Exception(Errors.error + " " + Errors.can_not_restore_model)

    def show_advanced_information(self, y_labels, y_prediction, feed_dict):
        y__ = y_labels.eval(feed_dict)
        pt("y_pred", y__[0])
        #argmax_labels_y_ = [np.argmax(m) for m in y__]
        #pt('y_labels_shape', y__.shape)
        #pt('argmax_labels_y__', argmax_labels_y_)
        #pt('y__[-1]', y__[-1])
        #pt("y_labels",y__)
        y__prediction = y_prediction.eval(feed_dict)
        #argmax_labels_y_convolutional = [np.argmax(m) for m in y__prediction]
        #pt('argmax_y_conv', argmax_labels_y_convolutional)
        #pt('y_pred_shape', y__prediction.shape)
        #pt("y_pred", y__prediction[0])
        pt("y_pred", y__prediction[0])
       #pt('index_buffer_data', self.index_buffer_data)
        #pt("SMAPE", smape(y__, y__prediction).eval(feed_dict))

    def save_actual_model(self, model: tf.keras.Sequential, save_type, config):
        # Save variables to disk.
        # TODO (@gabvaztor) Get path from project path logic
        # utils.save_and_restart(GS.MODELS_PATH + GS.PROBLEM_ID + "Models")
        if self.settings_object.model_path:
            try:
                # TODO (@gabvaztor) Get path from project path logic
                # utils.save_and_restart(GS.MODELS_PATH + GS.PROBLEM_ID + "Models")
                fullpath_save = self.settings_object.model_path + config.model_name_saved
                pt("fullpath_save", fullpath_save)
                if save_type == 2:  # Force save, temp save
                    fullpath_save = utils.get_temp_file_from_fullpath(fullpath_save)
                    pt("Saving TEMP model... DO NOT STOP PYTHON PROCESS")
                else:
                    pt("Saving model... DO NOT STOP PYTHON PROCESS")
                arguments = fullpath_save
                #execute_asynchronous_thread(functions=model.save,
                #                            arguments=arguments)
                model.save(fullpath_save)
                #saver.save(session, self.settings_object.model_path + Dictionary.string_ckpt_extension)
                pt("Model saved without problem")
                if self.show_when_save_information:
                    pt("Saving model information...")
                if self.save_model_information:
                    accuracy = None
                    if self.validation_accuracy:
                        accuracy = self.validation_accuracy
                    elif self.test_accuracy:
                        accuracy = self.test_accuracy
                    information_path = self.settings_object.information_path
                    if save_type == 2:
                        information_path = utils.get_temp_file_from_fullpath(information_path)
                    filepath = self._save_model_to_json(
                        fullpath=information_path,
                        attributes_to_delete=Constant.attributes_to_delete_information,
                        type_file="Information", accuracy=accuracy)
                else:
                    filepath = self.settings_object.history_information_path
                if self.show_when_save_information:
                    pt("Model information has been saved")
                return filepath
            except Exception as e:
                pt(Errors.error, e)
        else:
            pt(Errors.error, Errors.model_path_bad_configuration)

    def show_save_statistics(self, accuracies_train, accuracies_validation=None, accuracies_test=None,
                             loss_train=None, loss_validation=None, loss_test=None,
                             folder_to_save=None, show_graphs=None, is_new_epoch_flag=False):
        """
        Show all necessary visual and text information.
        """
        if is_new_epoch_flag:
            accuracies_train, accuracies_validation, accuracies_test, \
            loss_train, loss_validation, loss_test = utils.preprocess_lists([accuracies_train, accuracies_validation,
                                                                       accuracies_test, loss_train, loss_validation,
                                                                       loss_test], index_to_eliminate=2)

        accuracy_plot = plt.figure(0)
        plt.title(str(self.options[0]))
        plt.xlabel("ITERATIONS | Batch Size=" + str(self.batch_size) + " | Trains for epoch: " + str(self.trains))
        plt.ylabel("ACCURACY (BLUE = Train | RED = Validation | GREEN = Test)")
        plt.plot(accuracies_train, 'b')
        if accuracies_validation:
            plt.plot(accuracies_validation, 'r')
        if accuracies_test:
            plt.plot(accuracies_test, 'g')
        if folder_to_save:
            folder = folders.get_directory_from_filepath(folder_to_save)
            complete_name = folder + "\\graph_accuracy" + Dictionary.string_extension_png
            if self.save_graphs_images or is_new_epoch_flag:
                plt.savefig(complete_name)
        if (accuracies_train or accuracies_validation or accuracies_test) and show_graphs:
            accuracy_plot.show()
        loss_plot = plt.figure(1)
        plt.title("LOSS")
        plt.xlabel("ITERATIONS | Batch Size=" + str(self.batch_size) + " | Trains for epoch: " + str(self.trains))
        plt.ylabel("LOSS (BLUE = Train | RED = Validation | GREEN = Test)")
        plt.plot(loss_train, 'b')
        if loss_validation:
            plt.plot(loss_validation, 'r')
        if loss_test:
            plt.plot(loss_test, 'g')
        if (loss_train or loss_validation or loss_test) and show_graphs:
            loss_plot.show()
        if folder_to_save:
            folder = folders.get_directory_from_filepath(folder_to_save)
            complete_name = folder + "\\graph_loss" + Dictionary.string_extension_png
            if self.save_graphs_images or is_new_epoch_flag:
                plt.savefig(complete_name)

    def print_current_configuration(self, config):
        """
        Print all attributes to console
        """
        pt('first_label_neurons', self.first_label_neurons)
        pt('second_label_neurons', self.second_label_neurons)
        pt('third_label_neurons', self.third_label_neurons)
        pt('fourth_label_neurons',self._fourth_label_neurons)
        pt('input_size', self.input_size)
        pt('batch_size', self.batch_size)


    def update_batch(self, is_test=False, create_dataset_flag=False):
        if not is_test:
            #pt("Updating input batch")
            #pt("Updating input batch", str(self.index_buffer_data) + "/" + str(self.input_size), same_line=False)
            self.input_batch, self.label_batch = self.data_buffer_generic_class(inputs=self.input,
                                                                                inputs_labels=self.input_labels,
                                                                                shuffle_data=self.shuffle_data,
                                                                                batch_size=self.batch_size,
                                                                                is_test=False,
                                                                                options=self.options,
                                                                                create_dataset_flag=create_dataset_flag)
            return self.input_batch, self.label_batch
        elif is_test:
            pt("Creating test inputs...")
            self.x_test, self.y_test = self.data_buffer_generic_class(inputs=self.test,
                                                                      inputs_labels=self.test_labels,
                                                                      shuffle_data=self.shuffle_data,
                                                                      batch_size=None,
                                                                      is_test=True,
                                                                      options=self.options,
                                                                      create_dataset_flag=create_dataset_flag)
            return self.x_test, self.y_test

    @DecoratorClass.global_decorator(timed_flag=True)
    def batch_generator(self, is_test=False):
        """

        Returns: a part of inputs and labels.

        """
        is_new_epoch_flag = False
        for num_train in range(self.num_actual_trains, self.trains):
            if is_new_epoch_flag:
                self.index_buffer_data = 0  # When it starts new epoch, index of data will be 0 again. This does not
                # happen when restore model
                self.train_accuracy_sum = 0.  # Restart train_accuracy_sum for new epoch.
                is_new_epoch_flag = False
                self.num_actual_trains = 0
                # Update batches values (because index_buffer_data restarted)
                self.update_batch()
            self.update_batch()
            if num_train + 1 == self.trains:  # +1 because start in 0
                self.num_epochs_count += 1
                is_new_epoch_flag = True
            # Update num_trains_count
            self.num_trains_count += 1
            self.num_actual_trains = num_train
            if is_test:
                yield [self.input_batch, self.label_batch]
            else:
                yield [self.x_test, self.y_test]

    def batch_generator_v2(self, shape, is_test=False):
        from src.utils.DataGenerator import DataGenerator
        return DataGenerator(CMODELS=self, shape=shape, is_test=is_test)

    def make_predictions(self, model: tf.keras.Sequential):
        start_time_load_model = datetime.datetime.now()
        """
        # Load model
        fullpath_save = self.settings_object.model_path + "modelckpt_" + "my_model.h5"
        model = tf.keras.models.load_model(fullpath_save)
        delta = datetime.datetime.now() - start_time_load_model
        pt("Time to load model ", delta.total_seconds())
        """
        pt(1)
        self.update_batch(is_test=True)
        pt(2)
        start_datetime_ = datetime.datetime.now()
        pt(3)
        to_predict = self.x_test
        pt(4)
        pt("shape ", to_predict.shape)
        # Use `convert_image_dtype` to convert to floats in the [0,1] range.
        #to_predict = tf.image.convert_image_dtype(to_predict, tf.float32)
        pt("shape2 ", to_predict.shape)
        #to_predict = np.resize(to_predict, [720, 1280, 1])
        pt("shape3 ", to_predict.shape)
        try:
            predictions = model.predict(x=to_predict/255.0, verbose=2, use_multiprocessing=True,
                                        batch_size=15)
            pt(str(predictions))
        except Exception as e:
            pt(Errors.error, e)
        delta = datetime.datetime.now() - start_datetime_
        pt("Time to do inference ", delta.total_seconds())
        pt("predictions", predictions)
        path_saved = None
        information = self.options[0]
        try:
            prediction_class = prediction.ImagePrediction(information=information, real_label=real_label,
                                                          image_fullpath=input_path,
                                                          prediction_label=int(np.argmax(prediction)))
            prediction_class.save_json(save_fullpath=self.settings_object.submission_path)
        except Exception as e:
            pt(Errors.error, e)
            raise ValueError("Can not save prediction json")

        return path_saved
        # TODO (@gabvaztor) Finish method



"""
STATIC METHODS: Not need "self" :argument
"""

def get_inputs_and_labels_shuffled(inputs, inputs_labels):
    """
    Get inputs_processed and labels_processed variables with an inputs and inputs_labels shuffled
    :param inputs: Represent input data
    :param inputs_labels:  Represent labels data
    :returns inputs_processed, labels_processed
    """
    c = list(zip(inputs, inputs_labels))
    random.shuffle(c)
    inputs_processed, labels_processed = zip(*c)
    inputs_processed, labels_processed = np.array(inputs_processed), np.array(labels_processed)
    return inputs_processed, labels_processed


def image_process_retinopathy(image, image_type, height, width, is_test=False, cv2_flag=False, debug_mode=False,
                              to_save=False, to_predict=False):
    fullpath_image = image
    if not cv2_flag and not debug_mode:
        if image_type == 0:  # GrayScale
            image = PIL.Image.open(image).convert('L')
        else:
            image = PIL.Image.open(image)
        #pil_image_resized_antialias = np.array(image.resize((height, width), PIL.Image.ANTIALIAS))
        # Save resized
        if to_save or to_predict:
            #  TODO(@gabvaztor) Delete width black pixels, resize and save to x,y resolution
            # Resize image and modify
            #image_array = np.array(image)[:, 140:-127, :]
            image_array = np.array(image)
            image = PIL.Image.fromarray(image_array)
            width2, height2 = image.size
            to_write = "BEFORE RESIZE:\nwidth: " + str(width2) + " || height: " + str(height2)
            LOGGER.write_to_logger(to_write)
            pt("width2", width2)
            pt("height2", height2)
            image = np.array(image.resize((width, height)))
            to_write = "AFTER RESIZE:\nwidth: " + str(width) + " || height: " + str(height) + " || " + \
                       "image.shape: " + str(image.shape)
            LOGGER.write_to_logger(to_write)
            pt("image", image.shape)
            # We delete the last dimension if there is 4 instead 3. (transparency)
            if image.shape[2] == 4:
                image = image[:,:,:3]
                to_write = "AFTER REMOVE ALPHA:\nwidth: " + str(width) + " || height: " + str(height) + " || " + \
                           "image.shape: " + str(image.shape)
                LOGGER.write_to_logger(to_write)
            if to_save:
                # TODO (@gabvaztor) Create new place in SETTINGS to save new datasets
                # Image path
                path_to_save = os.path.dirname(fullpath_image)
                filename = os.path.basename(fullpath_image)[:-5]
                if is_test:
                    folder = "\\test\\"
                    pass  # We have already save test images
                else:
                    folder = "\\train\\"
                fullpath_to_save = path_to_save + folder + filename
                folders.create_directory_from_fullpath(fullpath=fullpath_to_save)
                PIL.Image.fromarray(image).save(fullpath_to_save + ".jpeg")
        else:
            image = np.array(image)
        #pt("image2", type(image))
        return image/255.


def process_input_unity_generic(x_input, y_label=None, options=None, is_test=False, to_save=False, to_predict=False):
    """
    Generic method that process input and label across a if else statement witch contains a string that represent
    the option (option = how process data)
    :param x_input: A single input
    :param y_label: A single input label
    :param options: All attributes to process data. First position must to be the option.
    :param is_test: Sometimes you don't want to do some operation to test set.
    :return: x_input and y_label processed
    """

    if options:
        option = options[0]  # Option selected
        if option == Projects.signals_images_problem_id:
            x_input = process_image_signals_problem(x_input, options[1], options[2],
                                                    options[3], is_test=is_test)
        if option == Projects.german_prizes_problem_id:
            x_input = process_german_prizes_csv(x_input, is_test=is_test)
        if option == Projects.retinopathy_k_problem_id:
            x_input = image_process_retinopathy(image=x_input, image_type=options[1], height=options[2],
                                                width=options[3], is_test=is_test, to_save=to_save,
                                                cv2_flag=False, debug_mode=False, to_predict=to_predict)
    return x_input, y_label

# noinspection PyUnresolvedReferences
def process_image_signals_problem(image, image_type, height, width, is_test=False, cv2_flag=False, debug_mode=False):
    """
    Process signal image
    :param image: The image to change
    :param image_type: Gray Scale, RGB, HSV
    :param height: image height
    :param width: image width
    :param is_test: flag with True if image is in test set
    :return:
    """
    # TODO (@gabvaztor) Doc method
    if not cv2_flag and not debug_mode:
        image = Image.open(image).convert('L')
        image = np.array(image.resize((height, width)))
        pt("image", image)
        pt("image", image.size)
        #pil_image_resized_antialias = np.array(image.resize((height, width), PIL.Image.ANTIALIAS))

    elif not cv2_flag and debug_mode:
        import cv2
        image_ = cv2.imread(image, image_type)
        image_2 = cv2.resize(image_, (height, width))

        cv_image = np.array(image_)
        cv_image_resized = np.array(image_2)

        image = Image.open(image).convert('L')

        pil_image = np.array(image)
        pil_image_resized = np.array(image.resize((height, width)))
        pil_image_resized_antialias = np.array(image.resize((height, width), PIL.Image.ANTIALIAS))

        pt("image_shape", pil_image.shape)
        pt("image_shape", pil_image_resized.shape)
        pt("image", pil_image_resized_antialias.shape)

        cv_image_sum = np.sum(cv_image_resized, axis=1)
        pil_image_sum = np.sum(pil_image, axis=1)
        pil_image_resized_sum = np.sum(pil_image_resized, axis=1)
        pil_image_resized_antialias_sum = np.sum(pil_image_resized_antialias, axis=1)

        pt("cv_image_sum", cv_image_sum)
        pt("pil_image_sum", pil_image_sum)
        pt("pil_image_resized_sum", pil_image_resized_sum)
        pt("pil_image_resized_antialias_sum", pil_image_resized_antialias_sum)

        pt("cv_image_resized", np.sum(cv_image_resized))
        pt("pil_image_resized_sum", np.sum(pil_image_resized_sum))
        pt("pil_image_resized_antialias_sum", np.sum(pil_image_resized_antialias_sum))

        if np.array_equal(cv_image, pil_image):
            pt("YES")
        if np.array_equal(cv_image_resized, pil_image_resized):
            pt("YES")
        if np.array_equal(cv_image_resized, pil_image_resized_antialias):
            pt("YES")

        pt("image", pil_image)
        pt("image", pil_image_resized)
        pt("image", pil_image_resized_antialias)

    else:
        # 1- Get image in GrayScale
        # 2- Modify intensity and contrast
        # 3- Transform to gray scale
        # 4- Return image
        import cv2
        image = cv2.imread(image, image_type)
        image = cv2.resize(image, (height, width))
        #image = cv2.equalizeHist(image)

        if not is_test:
            random_percentage = random.randint(3, 20)
            to_crop_height = int((random_percentage * height) / 100)
            to_crop_width = int((random_percentage * width) / 100)
            image = image[to_crop_height:height - to_crop_height, to_crop_width:width - to_crop_width]
            image = cv2.copyMakeBorder(image, top=to_crop_height,
                                       bottom=to_crop_height,
                                       left=to_crop_width,
                                       right=to_crop_width,
                                       borderType=cv2.BORDER_CONSTANT)

        #image = image.reshape(-1)
        #cv2.imshow('image', image)
        #cv2.waitKey(0)  # Wait until press key to destroy image
    return image

def process_test_set(test, test_labels, options, create_dataset_flag=False):
    """
    Process test set and return it
    :param test: Test set
    :param test_labels: Test labels set
    :param options: All attributes to process data. First position must to be the option.
    :return: x_test and y_test
    """
    x_test = []
    y_test = []
    for i in range(len(test)):
        # TODO (@gabvaztor) Number parametrizable
        if i % 350 == 0:
            x, y = process_input_unity_generic(test[i], test_labels[i], options, is_test=True,
                                               to_save=create_dataset_flag)
            if not create_dataset_flag:
                x_test.append(x)
                y_test.append(y)
    x_test = np.asarray(x_test)
    y_test = np.asarray(y_test)
    return x_test, y_test

def process_german_prizes_csv(x_input, is_test=False):
    return x_input

def call_method(method):
    method()

def input_while():
    global INPUT_VALUE
    while True:
        INPUT_VALUE = input()

def data_treatment_generic_problem(input, inputs_labels, options=None, to_predict=False):
    """

    Args:
        input:
        inputs_labels:
        options:

    Returns:

    """
    x_batch = []
    y_batch = []
    x, y = process_input_unity_generic(input, inputs_labels, options, to_predict=to_predict)
    x_batch.append(x)
    y_batch.append(y)
    x_batch = np.array(x_batch)
    y_batch = np.array(y_batch)

    return x_batch, y_batch