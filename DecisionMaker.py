from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory
from threading import Thread
import keys
import time
import threading
import random


class DecisionMaker(threading.Thread):
    
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = keys.pubnunb_subscribe_key
    pnconfig.publish_key = keys.pubnub_publish_key
    pnconfig.ssl = False
    pubnub = PubNub(pnconfig)
    
    class SACListener(SubscribeCallback):
        
        def publish_callback(self,result,status):
            pass
            
        def message(self, pubnub, message):
            channel = message.channel
            message = message.message
            print(message)
            #When the data is received process and send the temprature back
            if(channel == 'Temperature_Data_Channel_ML'):
                temp = message['temperature']
                humid = message['humidity']
             #get ml data, make decision
                new_temp = random.randint(16,26)
                message = {
                        'Request':'Change_Temp',
                       'ml_temperature' : new_temp
                    }
                pubnub.publish().channel('Temperature_Command_Channel_ML').message(message).async(self.publish_callback) 
                message = {'eon':
                        {'ml_temperature': new_temp
                        }}
                pubnub.publish().channel('Temperature_Real_Time_Channel_ML').message(message).async(self.publish_callback) 
                   
                
        def presence(self, pubnub, presence):
            pass
        
    
    def publish_callback(self,result,status):
        pass
        
    def request_data(self):
        message={
            'Request':'Get_Data_ML'}
        print(message)
        self.pubnub.publish().channel('Temperature_Command_Channel_ML').message(message).async(self.publish_callback) 
                
    
    def listen(self):
        listener = self.SACListener()
        self.pubnub.add_listener(listener)
        self.pubnub.subscribe().channels('Temperature_Data_Channel_ML').execute()
        
        while(True):
            self.request_data()
            time.sleep(30)
        
            
    def run(self):
        self.listen()
        
