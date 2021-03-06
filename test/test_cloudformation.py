from __future__ import absolute_import, division, print_function, unicode_literals
import six
import json
import boto3
import pytest
from moto import mock_s3, mock_cloudformation
from cfn_manage.cloudformation import CfnStack

# note that some tests use multiple asserts but will fail on the first error
# a possible solution is to use the pytest_expect module but it failed when I tried it

# START GLOBALS #

# moto only supports json templates
template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "Test Stack",
    "Resources": {},
}
template_json = json.dumps(template)
s3_bucket = 'test_cloudformation'


# END  GLOBALS #


# START FIXTURES #


@pytest.fixture
@mock_s3
def template_to_s3():
    '''put template in s3 and return url'''
    # note when mocking moto in a fixure to not mock again in the test
    # or the setup gets cleared
    template_name = 'template.json'
    s3 = boto3.resource('s3', region_name='us-west-2')
    # s3client = boto3.client('s3')
    s3.create_bucket(Bucket=s3_bucket)

    s3.Object(s3_bucket, template_name).put(Body=template_json)
    # response = s3client.list_objects_v2(Bucket=s3_bucket)
    # when run from tox the ETag value changes every run.
    # when run from pytest it is the same every run
    # assert response[u'Contents'][0][u'ETag'] == '"75f753b3d9c0b5b0bb3c0252e2e1503c"'
    return 'https://{0}.s3-us-west-2.amazonaws.com/{1}'.format(s3_bucket, 'template.json')


# START TESTS  #


def testSimpleInitialization():
    '''test that properties are initialized correctly for simple stack'''
    initSimpleCfnStack = CfnStack(name='simpleStack', template_url='simpleUrl')
    # tests with multiple asserts stop at the first failure
    assert initSimpleCfnStack.name == 'simpleStack'
    assert initSimpleCfnStack.template_url == 'simpleUrl'
    assert initSimpleCfnStack.iam is False
    assert initSimpleCfnStack.capability == []
    assert initSimpleCfnStack.tags == []
    assert initSimpleCfnStack.parameters == []


def testCompleteInitialization():
    '''test that properties are initialized correctly for complete stack'''
    initCompleteCfnStack = CfnStack(
        name='completeStack',
        template_url='completeUrl',
        iam=True,
        owner='owner',
        product='product',
        additional='additional'
    )
    assert initCompleteCfnStack.name == 'completeStack'
    assert initCompleteCfnStack.template_url == 'completeUrl'
    assert initCompleteCfnStack.iam is True
    assert initCompleteCfnStack.capability == ['CAPABILITY_IAM']
    assert {'Key': 'owner', 'Value': 'owner'} in initCompleteCfnStack.tags
    assert {'Key': 'product', 'Value': 'product'} in initCompleteCfnStack.tags
    # assert initCompleteCfnStack.parameters == [{'ParameterKey': 'owner', 'ParameterValue': 'owner'},
    assert {'ParameterKey': 'owner', 'ParameterValue': 'owner'} in initCompleteCfnStack.parameters
    assert {'ParameterKey': 'product', 'ParameterValue': 'product'} in initCompleteCfnStack.parameters
    assert {'ParameterKey': 'additional', 'ParameterValue': 'additional'} in initCompleteCfnStack.parameters


def testNoIamInitialization():
    '''test that Iam default it set when iam is not passed to init'''
    initNoIamCfnStack = CfnStack(
        name='noIamStack',
        template_url='noIamUrl',
        key1='value1',
        key2='value2'
    )
    assert initNoIamCfnStack.name == 'noIamStack'
    assert initNoIamCfnStack.template_url == 'noIamUrl'
    assert initNoIamCfnStack.iam is False
    assert initNoIamCfnStack.capability == []
    assert initNoIamCfnStack.tags == []
    assert {'ParameterKey': 'key2', 'ParameterValue': 'value2'} in initNoIamCfnStack.parameters
    assert {'ParameterKey': 'key1', 'ParameterValue': 'value1'} in initNoIamCfnStack.parameters


def testFailInitialization():
    '''test that initialization fails when missing required parameters'''
    # may also use @pytest.mark.xfail annotation to mark test as expected to fail.
    # I do not understand the tradeoffs of the two methods.
    with pytest.raises(TypeError, message='expecting TypeError') as excinfo:
        CfnStack()
    if six.PY2:
        excinfo.match('takes at least 3 arguments')
    if six.PY3:
        excinfo.match('missing 2 required positional arguments')


@mock_cloudformation
def testCreateStack(template_to_s3):
    stack = CfnStack(
        name='testStack',
        # moto requires virtual hosted style urls, path style not supported
        template_url=template_to_s3
    )
    stack.create_stack()
    # moto does not appear to support template_url for update
    # stack.update_stack()


@pytest.mark.skip(reason='bug - moto does not support updating a stack from a template stored in s3')
@mock_cloudformation
def testUpdateStack(template_to_s3):
    '''placeholder'''


@mock_cloudformation
def testDeleteStack(template_to_s3):
    stack = CfnStack(
        name='testStack',
        # moto requires virtual hosted style urls, path style not supported
        template_url=template_to_s3
    )
    stack.create_stack()
    stack.delete_stack()

# END TESTS  #
