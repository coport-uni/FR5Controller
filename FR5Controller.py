import time
import logging
import math
from fairino import Robot
from ctypes import sizeof

class FR5Controller():
    def __init__(self, ip_address):
        '''
        Docstring for __init__
        
        :param self: Description
        '''
        self.robot = Robot.RPC(ip_address)
        self.setup_debugger("info")
        self.setup_gripper()

        self.robot.ResetAllError()
    
    def setup_debugger(self, debug_level):
        '''
        Docstring for setup_debugger
        
        :param self: Description
        '''
        self.logger = logging.getLogger()
        if debug_level == "info":
            self.logger.setLevel(logging.INFO)
            
        elif debug_level == "error":
            self.logger.setLevel(logging.ERROR)

        else:
            raise Exception("DebugLevelError")
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def setup_gripper(self):
        '''
        Docstring for setup_gripper
        
        :param self: Description
        '''
        # Initialize GripperConfig. 1-Robotiq, 2-Huiling, 3-Tianji, 4-Dahuan, 5-Knowledge
        error = self.robot.SetGripperConfig(company=4,device=0)
        self.run_error_analyze(error)
        time.sleep(1)

        error,gripperconfig = self.robot.GetGripperConfig()
        print("SettingStatus：", gripperconfig)
        self.run_error_analyze(error)
        time.sleep(1)

        # Initialize GripperConfig. 0-reset, 1=activate
        error = self.robot.ActGripper(index=1,action=0)
        self.run_error_analyze(error)
        time.sleep(1)

        error = self.robot.ActGripper(index=1, action=1)
        self.run_error_analyze(error)
        time.sleep(1)

    def run_error_analyze(self, input_error):
        '''
        Docstring for run_error_analyze
        
        :param self: Description
        :param input_error: Description
        '''
        if input_error == 0:
            self.logger.info("OK")

        else:
            self.logger.error(input_error)
            raise Exception("CommError")
    
    def run_gripper_movement(self, target_gripper_position, target_gripper_speed : int, target_gripper_power : int):
        '''
        Docstring for run_gripper_movement
        
        :param self: Description
        :param position_gripper: Description
        '''
        current_position = self.get_gripper_position()

        while target_gripper_position is not current_position:
            error = self.robot.MoveGripper(index = 1, pos = target_gripper_position, vel = target_gripper_speed, force = target_gripper_power, maxtime = 30000,
                              block = 0, type = 0, rotNum = 0, rotVel = 0, rotTorque = 0)
            self.run_error_analyze(error)
            time.sleep(1)

            current_position = self.get_gripper_position()

        self.logger.info("GripperPositionReached")
        
        return 0
    
    def get_gripper_position(self):
        '''
        Docstring for get_gripper_position
        
        :param self: Description
        '''
        # Initialize GripperConfig. 0-reset, 1-activate
        error, fault, position = self.robot.GetGripperCurPosition()
        self.run_error_analyze(error)

        return position
    
    def run_joint_movement(self, target_joint_list : list, target_gripper_position : int, target_gripper_speed = 100, target_gripper_power = 50, target_joint_speed = 30):
        '''
        Docstring for run_joint_movement
        
        :param self: Description
        :param list_joint: Description
        :type list_joint: list
        '''
        # 0-joint, 1-eef
        self.robot.SingularAvoidStart(0)

        error = self.robot.MoveJ(joint_pos=target_joint_list, tool = 1, user = 0, vel = target_joint_speed)
        self.run_error_analyze(error)

        self.run_gripper_movement(target_gripper_position, target_gripper_speed, target_gripper_power)

        self.robot.SingularAvoidEnd()
        
        self.logger.info("JointPositionReached")

    def get_joint_position(self):
        '''
        Docstring for get_joint_position
        
        :param self: Description
        '''
        error, current_joint_list = self.robot.GetActualJointPosDegree()
        self.run_error_analyze(error)
        time.sleep(1)

        return current_joint_list

    def run_eef_movement_ptp(self, target_eef_list : list, target_gripper_position : int, target_gripper_speed = 100, target_gripper_power = 50, target_eef_speed = 30):
        # 0-joint, 1-eef
        self.robot.SingularAvoidStart(1)
        
        error = self.robot.MoveCart(desc_pos=target_eef_list, tool = 1, user = 0, vel = target_eef_speed)
        self.run_error_analyze(error)

        self.run_gripper_movement(target_gripper_position, target_gripper_speed, target_gripper_power)

        self.robot.SingularAvoidEnd()
        
        self.logger.info("EEF_PTP_PositionReached")
    
    def get_eef_position(self):
        error, current_eef_list = self.robot.GetActualTCPPose()
        self.run_error_analyze(error)
        time.sleep(1)

        return current_eef_list

def main():
    '''
    Docstring for main
    '''
    fc = FR5Controller("192.168.58.2")

    movement_range = 200
    movement_speed = 100
    movement_test = 50

    example_joint_1 = [0, -99.66753387451172, 117.4729995727539, -108.61497497558594, -91.7260513305664, 74.25582885742188]
    example_joint_2 = [90, -99.66753387451172, 117.4729995727539, -108.61497497558594, -91.7260513305664, 74.25582885742188]

    example_eef_1 = [-310.64605712890625, 167.83993530273438, 237.2095184326172, 179.6305694580078, -0.00029896487831138074, 45.72968292236328]
    example_eef_2 = [-310.64605712890625 + (movement_range / math.sqrt(2)), 167.83993530273438 + (movement_range / math.sqrt(2)), 237.2095184326172, 179.6305694580078, -0.00029896487831138074, 45.72968292236328]
    example_eef_3 = [-310.64605712890625 + (movement_range / math.sqrt(2)), 167.83993530273438 + (movement_range / math.sqrt(2)), 237.2095184326172 - movement_range, 179.6305694580078, -0.00029896487831138074, 45.72968292236328]
    example_eef_4 = [-310.64605712890625, 167.83993530273438, 237.2095184326172 - movement_range, 179.6305694580078, -0.00029896487831138074, 45.72968292236328]

    example_eef_5 = [74.24925994873047, 322.0446472167969, 90, -179.36241149902344, 3.5878381729125977, 42.54720687866211]
    example_eef_6 = [74.24925994873047 - (movement_test / math.sqrt(2)), 322.0446472167969 + (movement_test /  math.sqrt(2)), 90, -179.36241149902344, 3.5878381729125977, 42.54720687866211]

    
    # print(fc.get_eef_position())

    fc.run_eef_movement_ptp(example_eef_5, 100, target_eef_speed = movement_speed)
    time.sleep(3)
    fc.run_eef_movement_ptp(example_eef_6, 100, target_eef_speed = movement_speed)
    time.sleep(3)
    
    # for i in range(3):
    #     fc.run_eef_movement_ptp(example_eef_1, 100, target_eef_speed = movement_speed)
    #     fc.run_eef_movement_ptp(example_eef_2, 0, target_eef_speed = movement_speed)
    #     fc.run_eef_movement_ptp(example_eef_3, 100, target_eef_speed = movement_speed)
    #     fc.run_eef_movement_ptp(example_eef_4, 0, target_eef_speed = movement_speed)
    #     fc.run_eef_movement_ptp(example_eef_1, 100, target_eef_speed = movement_speed)

        # fc.run_joint_movement(example_joint_1, 100, target_joint_speed = movement_speed)
        # print(fc.get_joint_position())
        # fc.run_joint_movement(example_joint_2, 0, target_joint_speed = movement_speed)
        # print(fc.get_joint_position())

        # fc.run_gripper_movement(100)
        # fc.run_gripper_movement(0)
    
    fc.robot.CloseRPC()

if __name__ == "__main__":
    main()