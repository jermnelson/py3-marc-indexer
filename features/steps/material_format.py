"""
 :mod:`material_format` Steps for determing the material format from 
 MARC21 record using the `Behave module <http://packages.python.org/behave>`_
"""
__author__ = "Jeremy Nelson"

from behave import *

@given("we have a MARC record")
def set_marc_record(context,marc_record=None):
    """
    Sets MARC record in World for format testing
    
    :param marc_record: MARC record
    """
    if context.marc_record is None:
        context.marc_record = marc_record
    context.passed_rules = []

@when('"<code>" field "<position>" is "<value>"')
def check_field_value_position(context,field,position,value):
    """
    Function checks if the MARC field at a position is a value

    :param context: Context 
    :param field: MARC Field or Leader
    :param position: Zero-index integer
    :param value: Expected value
    """
    if field == 'LDR':
        field = context.marc_record.leader
    else:
        field = context.marc_record[field]
    if field is not None:
        extracted_value = field[position]
        if extracted_value == value:
            context.passed_rule.append(True)
        else:
            context.passed_rule.append(False)
    else:
        context.passed_rule.append(False)
    
@when("{field} position {position} not {value}")
def check_field_not_value_position(context,field,position,value):
    """
    Function checks if the MARC field at a position is not a value

    :param context: Context
    :param field: MARC Field or Leader
    :param position: Zero-index integer
    :param value: Expected value
    """
    if field == 'LDR':
        field = context.marc_record.leader
    else:
        field = context.marc_record[field]
    if field is not None:
        extracted_value = field[position]
        if extracted_value != value:
            context.passed_rule.append(True)
        else:
            context.passed_rule.append(False)
    else:
        context.passed_rule.append(False)
 

