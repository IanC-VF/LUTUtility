# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:22:17 2020

@author: iancloutier
"""


import time
import numpy as np
import threading
from opcua import Client
from opcua import ua
class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """

    def __init__(self,value):
        self.PassedObj=value
        pass

    def datachange_notification(self, node, val, data):
        #print("Python: New data change event", node, val)
        self.PassedObj=val
        

    def event_notification(self, event):
        print("Python: New event", event)
class BNRopcuaTag:
    def __init__(self, client,VarName,period,Sub=0):
       self.Node=client.get_node(VarName)
       self.Variable=self.Node.get_value()
       self.type=Sub
       if Sub==1:
           self.VarHandler=SubHandler(self.Variable)
           self.VariableSub=client.create_subscription(period,self.VarHandler)
           self.SubHandle=self.VariableSub.subscribe_data_change(self.Node)
    def getValue(self):
        if self.type==1:
            return self.VarHandler.PassedObj
        else:
            return self.Node.get_value()
    def setValue(self, val):
        if self.type==1:
            print('Variable not Settable\n')
        else:
            typ=self.Node.get_value()
            if type(val)==type(typ):
                if isinstance(val,bool):
                    self.Node.set_value(ua.DataValue(ua.Variant(val,ua.VariantType.Boolean)))
                if isinstance(val,int):
                    vartype=self.Node.get_data_type_as_variant_type()
                    self.Node.set_value(ua.DataValue(ua.Variant(int(val),vartype)))
                if isinstance(val,float):
                    self.Node.set_value(ua.DataValue(ua.Variant(val,ua.VariantType.Float)))
            else:
                print('Invalid Data Type\n')
                        
    def __del__(self):
        if self.type==1:
            self.VariableSub.delete()
                    
                    
                    
           
        
            
        