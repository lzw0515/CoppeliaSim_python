# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time
import math

print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
#print(clientID)#0

stop = sim.simxStopSimulation(
    clientID, sim.simx_opmode_blocking)
time.sleep(4)
print("!!")
start = sim.simxStartSimulation(
    clientID, sim.simx_opmode_blocking)
print("Resetting Simulation. Stop Code: {} Start Code: {}".format(stop, start))

#sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot)
#sim.simxFinish(clientID)

#ret, QuadObj = sim.simxGetObjectHandle(clientID, 'Quadricopter', sim.simx_opmode_blocking)
#sim.simxSetObjectPosition(clientID, QuadObj,-1,(-24,-24, 1), sim.simx_opmode_blocking)
#sim.simxSetObjectOrientation(clientID, QuadObj, -1, [0, 0, 0], sim.simx_opmode_blocking)
#time.sleep(0.5)
#sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot)
#time.sleep(0.5)
#sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot)
#sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot)

if clientID != -1:
    print ('Connected to remote API server')


    # Now try to retrieve data in a blocking fashion (i.e. a service call):
    res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
    #print(res)#0
    #print(objs)#0
    if res==sim.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
    else:
        print ('Remote API function call returned with error code: ',res)
    
    

    ret, targetObj = sim.simxGetObjectHandle(clientID, 'Quadricopter_target', sim.simx_opmode_blocking)
    if ret != sim.simx_return_ok:
        print("!!!")

    ret, arr = sim.simxGetObjectPosition(clientID, targetObj, -1, sim.simx_opmode_blocking)
    if ret==sim.simx_return_ok:
        print (arr)
    
    #sim.simxSetObjectPosition(clientID, targetObj,-1,(arr[0],arr[1] + 0.1,arr[2]), sim.simx_opmode_blocking)
    '''
    propellerScripts=[-1,-1,-1,-1]
    for i in range(4):
        ret, propellerScripts[i]=sim.simxGetObjectHandle(clientID, 'Quadricopter_propeller_respondable' + str(i + 1), sim.simx_opmode_blocking)
    '''
    '''
    ret, targetObj2 = sim.simxGetObjectHandle(clientID, 'Quadricopter_target', sim.simx_opmode_blocking)
    if ret != sim.simx_return_ok:
        print("!!!")
    '''
    
    time.sleep(1)

    # Now retrieve streaming data (i.e. in a non-blocking fashion):
    startTime=time.time()
    #sim.simxGetIntegerParameter(clientID,sim.sim_intparam_mouse_x,sim.simx_opmode_streaming) # Initialize streaming
    while time.time()-startTime < 5:
        
        #returnCode,data=sim.simxGetIntegerParameter(clientID,sim.sim_intparam_mouse_x,sim.simx_opmode_buffer) # Try to retrieve the streamed data
        '''
        if returnCode==sim.simx_return_ok: # After initialization of streaming, it will take a few ms before the first value arrives, so check the return code
            print ('Mouse position x,y: ',data) # Mouse position x is actualized when the cursor is over CoppeliaSim's window
        '''
        
        #sim.setObjectParent(targetObj,-1,true)

        #d=sim.getObjectHandle('Quadricopter_base')
        '''
        ret, arr = sim.simxGetStringSignal(clientID, sim.sim_objfloatparam_abs_x_velocity, sim.simx_opmode_buffer)
        if ret==sim.simx_return_ok:
            print (arr)
        '''
        #ret = sim.simxClearFloatSignal(clientID, 'propeller1Vel', sim.simx_opmode_blocking)
        #ret = sim.simxSetFloatSignal(clientID, 'propeller1Vel', 1, sim.simx_opmode_blocking)
        #ret = sim.simxSetFloatSignal(clientID, 'propeller2Vel', 1, sim.simx_opmode_blocking)
        #ret = sim.simxSetFloatSignal(clientID, 'propeller3Vel', 1, sim.simx_opmode_blocking)
        #ret = sim.simxSetFloatSignal(clientID, 'propeller4Vel', 1, sim.simx_opmode_blocking)

        
        ret, arr = sim.simxGetObjectPosition(clientID, targetObj, -1, sim.simx_opmode_blocking)
        if ret==sim.simx_return_ok:
            print (arr)
        

        sim.simxSetObjectPosition(clientID, targetObj,-1,(arr[0],arr[1] + 0.5,arr[2]), sim.simx_opmode_blocking)

        #成功的
        #t= time.time()-startTime
        #sim.simxSetObjectPosition(clientID, targetObj,-1,{ (math.cos(t*math.pi/2))/2, (math.sin(t*math.pi/2))/2, 1}, sim.simx_opmode_blocking)

        time.sleep(0.5)

    # Now send some data to CoppeliaSim in a non-blocking fashion:
    #sim.simxAddStatusbarMessage(clientID,'Hello CoppeliaSim!',sim.simx_opmode_oneshot)

    # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(clientID)

    sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot)

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
