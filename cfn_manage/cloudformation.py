#!/usr/bin/env python
'''cloudformation

This module contains cloudformation helper classes

Created by: Michael West
Date 2017-May-07

'''
from __future__ import absolute_import, division, print_function, unicode_literals
import boto3
import logging

__version__ = '0.7.1'
# adding null handler sends all logs to /dev/null
# it is the clients responsibility to add handelers they need
logging.getLogger(__name__).addHandler(logging.NullHandler())


class CfnStack:
    '''CfnStack represents a cloudformation stack

    Attributes:

        name (str): Stack name
        template_url: (str): location of template
        iam (boolean): does this stack effect permissions?
        tags (list if dicts): tags for stack
        capability (list): iam capabilities stack requires
        parameters (list of dicts): Parameters and Values to pass to the cloudformation stack
        create_response (dict): response from calling create stack
        update_response (dict): response from calling update stack
        delete_response (dict): response from calling delete stack

    '''
    # static class logger property for static methods
    # don't see a way to dynamically get the class name from here
    # I think I should use the fully qualified name here
    _log = logging.getLogger(__name__)

    # constructor
    def __init__(self, name, template_url, iam=False, **kwargs):
        '''Initialize CfnStack

        Args:
            name (str): Stack name
            template_url: (str): location of template
            iam (boolean): does this stack effect permissions?  Default False
            **kwargs: Parameters and Values to pass to the cloudformation stack

        '''

        self._log = logging.getLogger(__name__)
        self._log.debug('Initializing CfnStack')
        # in python just assign, don't define attributes
        # have to use self everywhere
        self.name = name
        self.template_url = template_url
        self.iam = iam
        self.capability = []
        if (self.iam):
            self.capability.append('CAPABILITY_IAM')

        self.parameters = []
        self.tags = []
        # set tags and parameters
        for key in kwargs:
            self._log.debug('kwarg key {0} has value {1}'.format(key, kwargs[key]))
            self.parameters.append(
                {
                    'ParameterKey': key,
                    'ParameterValue': kwargs[key]
                }
            )
            # pull out three standard tags if they exist
            if key in ['owner', 'product', 'environment']:
                self.tags.append(
                    {
                        'Key': key,
                        'Value': kwargs[key]
                    }
                )
        self._log.debug('initialized object is: {0}'.format(self))

    def create_stack(self):
        '''create cloudformation stack'''
        self._log.debug('BEGIN create_stack')

        cfn = boto3.client('cloudformation')

        self.create_response = cfn.create_stack(
            StackName=self.name,
            TimeoutInMinutes=30,
            OnFailure='ROLLBACK',
            Capabilities=self.capability,
            TemplateURL=self.template_url,
            Parameters=self.parameters,
            Tags=self.tags
        )

        self._log.debug('END create_stack')

    def update_stack(self):
        '''update cloudformation stack'''
        self._log.debug('BEGIN update_stack')

        cfn = boto3.client('cloudformation')

        self.update_response = cfn.update_stack(
            StackName=self.name,
            Capabilities=self.capability,
            TemplateURL=self.template_url,
            Parameters=self.parameters
        )
        self._log.debug('END update_stack')

    def delete_stack(self):
        '''delete cloudformation stack'''
        self._log.debug('BEGIN delete_stack')

        cfn = boto3.client('cloudformation')
        cfClient = boto3.client('cloudformation')
        waiter = cfClient.get_waiter('stack_delete_complete')

        self.delete_response = cfn.delete_stack(StackName=self.name)

        waiter.wait(StackName=self.name)
        self._log.debug('END delete_stack')

    def __repr__(self):
        '''String representation of object

        Returns:
            String representation of object

        '''
        return '{0}(name={1}, template_url={2}, iam={3}, tags={4}, parameters={4})'.format(
            self.__class__,
            self.name,
            self.template_url,
            self.iam,
            self.tags,
            self.parameters
        )
