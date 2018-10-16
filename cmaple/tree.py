#!/usr/bin/env python
"""
Created on May 20, 2018

@author: rhindere@cisco.com

tree.py is the top level script for MAPLE
(Multi-purpose API Programming Language Extension).  Defines the main
class CMapleTree which serves as the overarching control point for
MAPLE leafs.  Leafs implement the specific functionality for a
given products API.  CMapleTree also provides leaf management functions.

Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied."""

__author__ = "Ron Hinderer (rhindere@cisco.com)"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates."
__license__ = "Cisco DEVNET"

import logging
from autologging import logged, traced

import sys
import os
import re

# Create and configure a logger for cmaple...
logger = logging.getLogger(re.sub('\.[^.]+$','',__name__))
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(funcName)s:%(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

@logged(logger)
@traced(logger)
class CMapleTree():
    """This class defines the top level object for MAPLE; the 'tree' object.

    The tree object provides methods to instantiate and manage MAPLE 'leaf' objects.
    """
    def __init__(self,name=None,tree_dir=None,logging_config_dict={},logging_level='INFO',log_file_mode='w'):

        """__init__ receives a kwargs dict to define parameters.  This allows __init__ to pass these parameters
        to the superclass.

        Returns a tree object.

        *Parameters*

        name: string, keyword, default=None
            The name of this MAPLE tree.  The name is required and will be used to create a working directory
            for the tree object.
        tree_dir: string, keyword, default=None
            The path to the desired location for the tree's working directory.  Together with the tree name, will
            be used to create the tree's working directory (e.g. leaf_dir/name)
        logging_level: string, keyword, default=None
            The desired logging level for the tree object (inherited by all leaf objects
        log_file_mode: string, keyword, default='w'
            The file mode for the log file.  Default is 'w' for write mode.
        """

        # Setup the tree working directory
        if not name:
            logger.error('tree_name argument is None.  Tree must have a name...exiting')
            sys.exit()

        if not tree_dir:
            tree_dir = '.'
            logger.warning('tree_dir argument is None.  Using current directory...')
        else:
            if not os.path.isdir(tree_dir):
                try:
                    os.mkdir(tree_dir)
                except Exception as err:
                    logger.error("Error creating cmaple working directory, error message--> " + str(err))
                    sys.exit(str(err))

        # Create the tree directory named 'tree_name'
        maple_tree_dir = os.path.join(tree_dir, name)
        if not os.path.isdir(maple_tree_dir):
            try:
                os.mkdir(maple_tree_dir)
            except Exception as err:
                logger.error("Error creating tree working directory, error message--> " + str(err))
                sys.exit(str(err))

        if logging_config_dict:
            logger.config.dictConfig(logging_config_dict)
        logger.setLevel(logging.getLevelName(logging_level))
        file_handler = logging.FileHandler(os.path.join(maple_tree_dir,'cmaple.log'), mode=log_file_mode)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info('Starting new cmaple session...')
        
        self.name = name
        self.leaf_modules ={}
        self.leaf_instances = {}
        self.logging_config_dict = logging_config_dict
        self.logging_level = logging_level
        self.log_file_mode = log_file_mode
        self.maple_tree_dir = maple_tree_dir

    def add_leaf_instance(self,leaf_type=None,**kwargs):

        """Initializes a leaf instance.

        Returns a leaf object.

        *Parameters*

        leaf_type: string, keyword, default=None
            The leaf type to initialize.
        kwargs: dictionary
            kwargs dictionary containing keyword: value pairs pass to the leaf's __init__ method
        """

        kwargs['maple_parent'] = self

        leaf = leaf_type.lower()
        
        # Create a working directory for the new leaf...
        if not 'name' in kwargs:
            logger.error('name argument is None. %s leaf must have a name...exiting' % (leaf))
            sys.exit()
        else:
            logger.info('Initializing new leaf instance type %s and name %s' % (leaf, kwargs['name']))
        # Create the leaf working directory
        leaf_dir = os.path.join(self.maple_tree_dir, kwargs['name'])
        if not os.path.isdir(leaf_dir):
            try:
                os.mkdir(leaf_dir)
            except Exception as err:
                logger.error("Error creating %s name %s working directory, error message--> %s" % (leaf_type, kwargs['name'], str(err)))
                sys.exit(str(err))

        if leaf == 'fmc':
            import cmaple.fmc.fmc
            self.leaf_modules[leaf] = cmaple.fmc.fmc

        if leaf == 'amp':
            import cmaple.amp.amp
            self.leaf_modules[leaf] = cmaple.amp.amp

        if leaf == 'tg':
            import cmaple.threatgrid.threatgrid
            self.leaf_modules[leaf] = cmaple.threatgrid.threatgrid

        if leaf == 'html_leaf':
            import cmaple.under_construction.html_leaf.HTML_leaf
            self.leaf_modules[leaf] = cmaple.under_construction.html_leaf.HTML_leaf

        if leaf not in self.leaf_instances:
            self.leaf_instances[leaf] = []
        leaf_class = getattr(self.leaf_modules[leaf], leaf.upper())
        self.leaf_instances[leaf].append(leaf_class(**kwargs, leaf_dir=leaf_dir))
        
        return self.leaf_instances[leaf][-1]
