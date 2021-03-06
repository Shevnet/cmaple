#!/usr/bin/env python
"""
****UNDER DEVELOPMENT NOT READY FOR PRACTICAL USE****
Created on May 20, 2018

@author: rhindere@cisco.com

ssh.py implements Cisco iptables specific REST functionality.  Generic
REST functionality is inherited by sub classing RestBase.

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

from cmaple.text_base import TextBase
import sys
import os
import re
import cmaple.tree_helpers as tree_helpers
from cmaple.tree_helpers import set_default as sd
import cmaple.iptables.iptables_helpers as iptables_helpers
import cmaple.input_validations as input_validations
import cmaple.output_transforms as output_transforms
import json
import urllib3
from pprint import pprint, pformat
import logging
from autologging import logged, traced
from autologging import TRACE
import time
from objectpath import *
from collections import OrderedDict
import _pickle

#Define global variables...

# Create a logger tree.iptables...
logger = logging.getLogger(re.sub('\.[^.]+$','',__name__))

@logged(logger)
@traced(logger)
class IPT(TextBase):
    """
    This class defines the API interface for the iptables.

    Inherits generic REST functionality from RestBase.

    Overrides methods in RestBase where necessary.

    Method names not beginning with "_" are made available to cmaple_cli.py for use in operations config files.

    """

    def __init__(self, **kwargs):

        """__init__ receives a kwargs dict to define parameters.  This allows __init__ to pass these parameters
        to the superclass.

        Returns an iptables leaf object.

        *Parameters*

        iptables_rules_file: string, keyword, default=None
            The file path for the iptables rule file
        iptables_config_file: string, keyword, default=None
            The file path for the iptables config file
        iptables_interface_file: string, keyword, default=None
            The file path for the iptables interface file
        persist_responses: boolean, keyword, default=True
            If True, responses will be pickle persisted by url into the leaf's working directory.
        restore_responses: boolean, keyword, default=False
            If True, pickled persistent responses will be restored prior to all other operations.
        leaf_dir: string, keyword, default=None
            Provided by CMapleTree when this leaf type is instantiated.  Contains the directory where working files
            for the leaf instance are stored.
        """

        kwarg_defaults = {'iptables_rules_file_name': None, 'iptables_config_file': None, 'iptables_interface_file': None,
                          'persist_responses': True, 'restore_responses': False, 'leaf_dir': None}

        for key, val in kwargs.items():
            kwarg_defaults[key] = val

        self.__dict__.update(kwarg_defaults)

        super(IPT, self).__init__()

        #Attributes inherited from leaf_base to override in this class

        #Validate critical attributes
        self.iptables_rules_file = input_validations.validate_file_open_for_read(self.iptables_rules_file_name)
        #self.iptables_config_file = input_validations.validate_file_open_for_read(self.iptables_config_file)
        #self.iptables_interface_file = input_validations.validate_file_open_for_read(self.iptables_interface_file)
        
        #Add class specific attributes
        if self.restore_responses:
            response_url = list(self.responses_dict.keys())[0]

    #Methods inherited from leaf_base to override in this class
    ##############################################################################################################

    #Begin class specific methods
    ################################################################################################################
    def parse_iptables_rules(self):

        # for line in self.iptables_rules_file.readlines():
        #     print(line)

        # open file
        fd = self.iptables_rules_file

        # file length
        len = self.file_len(self.iptables_rules_file_name)

        # import parser
        import cmaple.iptables.IpTablesYacc as _parse_kit

        # clear state and dictionary values
        _parse_kit.init(self.iptables_rules_file_name)

        t0 = time.time()  # start timer
        count, ctr = 0, 0

        for line in fd:
            _parse_kit.update()
            ctr += 1
            try:
                _parse_kit.parser.parse(line, _parse_kit.lexer, debug=1)
            except:
                print('Error while parsing line: %s' % line, ctr)
                # raise SyntaxError
            count += 1

        _parse_kit.finish()
        fd.close()

        print()
        time.time() - t0

        print(_parse_kit.get_firewall())
        firewall = _parse_kit.get_firewall()[0]
        print(firewall.to_string())

    def file_len(self, fname):
        """Return the number of line in the file"""
        i = 0
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

