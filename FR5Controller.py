import time
import logging
import math
from fairino import Robot
from ctypes import sizeof

class FR5Controller():
    def __init__(self, ip_address):
        '''
        This function initalize connection between pc and controller
        
        Input: str
        '''
        self.robot = Robot.RPC(ip_address)
        self.setup_debugger("info")
        self.setup_gripper()

        self.robot.ResetAllError()
    
    def setup_debugger(self, debug_level):
        '''
        This function select mode between debug and production level.
        
        Input: str
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
        This function initialize gripper setup
        
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
        This function compare known error codes and raise exception with helpful message.
        
        Input: int
        '''
        if input_error == 0:
            self.logger.info("OK")

        if input_error == 14:
            self.logger.error(input_error)
            raise Exception("RobotMotionError. Clear Error!")

        else:
            self.logger.error(input_error)
            raise Exception("CommError. Reboot!")
    
    def run_gripper_movement(self, target_gripper_position : int, target_gripper_speed : int, target_gripper_power : int):
        '''
        This function run gripper with given parameters. it is usually integrated with joint or eef functions. Every variables are percentage-based.
        
        Input: int, int, int
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
        This function get current gripper postion.

        Output: int
        '''
        # Initialize GripperConfig. 0-reset, 1-activate
        error, fault, position = self.robot.GetGripperCurPosition()
        self.run_error_analyze(error)

        return position
    
    def run_joint_movement(self, target_joint_list : list, target_gripper_position : int, target_gripper_speed = 100, target_gripper_power = 50, target_joint_speed = 30):
        '''
        This function run joint operation with given parameters. Every variables are percentage-based except list. Default values are recommended values from docs.
        
        Input: list, int, int, int, int
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
        This function get current joint postion.

        Output: list
        '''
        error, current_joint_list = self.robot.GetActualJointPosDegree()
        self.run_error_analyze(error)
        time.sleep(1)

        return current_joint_list

    def run_eef_movement_ptp(self, target_eef_list : list, target_gripper_position : int, target_gripper_speed = 100, target_gripper_power = 50, target_eef_speed = 30):
        '''
        This function run eef operation with given parameters. Every variables are percentage-based except list. Default values are recommended values from docs.
        
        Input: list, int, int, int, int
        '''
        # 0-joint, 1-eef
        self.robot.SingularAvoidStart(1)
        
        error = self.robot.MoveCart(desc_pos=target_eef_list, tool = 1, user = 0, vel = target_eef_speed)
        self.run_error_analyze(error)

        self.run_gripper_movement(target_gripper_position, target_gripper_speed, target_gripper_power)

        self.robot.SingularAvoidEnd()
        
        self.logger.info("EEF_PTP_PositionReached")
    
    def get_eef_position(self):
        '''
        This function get current eef postion.

        Output: list
        '''
        error, current_eef_list = self.robot.GetActualTCPPose()
        self.run_error_analyze(error)
        time.sleep(1)

        return current_eef_list
        