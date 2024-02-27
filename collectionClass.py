from typing import Any, Mapping
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import flask
import functions_framework
import json
import re



class newHireData:
  def __init__ (self, first, last, dealership, department, hiringManager, status):
    self.first = first
    self.last = last
    self.dealership = dealership
    self.department = department
    self.hiringManager = hiringManager
    self.status = status
  
  @staticmethod
  def from_dict(source):
    if not all (["first", "last", "dealership", "department", "hiringManger", "status"] in source.keys()):
      raise ValueError("Missing required fields for newHireData!")
    return newHireData(source["first"], source["last"], source["dealership"], source["department"], source["hiringManager"], source["status"])
  
  def to_dict(self):
    return {"first": self.first, "last": self.last, "dealership": self.dealership, "department": self.department, "hiringManager": self.hiringManager, "status": self.status}
  
  def __repr__(self):
    return f"newHireData(\
        first = {self.first}, \
        last = {self.last}, \
        dealership = {self.dealership}, \
        department = {self.department}, \
        hiringManager = {self.hiringManager}, \
        status = {self.status}\
    )"
    
class access:
  def __init__(self, access1, access2, access3):
    self.access1 = access1
    self.access2 = access2
    self.access3 = access3
  
  @staticmethod
  def from_dict(source):
    if not all (["access1", "access2", "access3"] in source.keys()):
      raise ValueError("Missing required fields for access!")
    return access(source["access1"], source["access2"], source["access3"])
  
  def to_dict(self):
    return {"access1": self.access1, "access2": self.access2, "access3": self.access3}
  
  def __repr__(self):
    return f"access(\
        access1 = {self.access1}, \
        access2 = {self.access2}, \
        access3 = {self.access3} \
    )"
    
