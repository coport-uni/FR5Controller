import time
import logging
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

            return 0
        else:
            self.logger.error(input_error)
            raise Exception("CommError")
    
    def run_gripper_movement(self, target_gripper_position, target_gripper_speed = 100, target_gripper_power = 50):
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
    
    def run_joint_movement(self, target_joint_list : list, target_gripper_position : int, target_joint_speed = 30):
        '''
        Docstring for run_joint_movement
        
        :param self: Description
        :param list_joint: Description
        :type list_joint: list
        '''
        error = self.robot.MoveJ(joint_pos=target_joint_list, tool = 1, user = 0, vel = target_joint_speed)
        self.run_error_analyze(error)

        self.run_gripper_movement(target_gripper_position)
        
        self.logger.info("JointPositionReached")
        
        return 0
    
    def get_joint_position(self):
        '''
        Docstring for get_joint_position
        
        :param self: Description
        '''
        error, current_joint_list = self.robot.GetActualJointPosDegree()
        self.run_error_analyze(error)
        time.sleep(1)

        return current_joint_list

def main():
    '''
    Docstring for main
    '''
    fc = FR5Controller("192.168.58.2")

    example_joint_1 = [0, -99.66753387451172, 117.4729995727539, -108.61497497558594, -91.7260513305664, 74.25582885742188]
    example_joint_2 = [90, -99.66753387451172, 117.4729995727539, -108.61497497558594, -91.7260513305664, 74.25582885742188]
    for i in range(10):
        fc.run_joint_movement(example_joint_1, 100, 100)
        fc.run_joint_movement(example_joint_2, 0, 100)
        # print(fc.get_joint_position())
        # fc.run_gripper_movement(100)
        # fc.run_gripper_movement(0)

if __name__ == "__main__":
    main()


def move(self):
    j1 = [-11.904, -99.669, 117.473, -108.616, -91.726, 74.256]
    # j1 = [0, 0, 0, 0, 0, 0]
    j2 = [-45.615, -106.172, 124.296, -107.151, -91.282, 74.255]
    j3 = [-29.777, -84.536, 109.275, -114.075, -86.655, 74.257]
    j4 = [-31.154, -95.317, 94.276, -88.079, -89.740, 74.256]
    desc_pos1 = [-419.524, -13.000, 351.569, -178.118, 0.314, 3.833]
    desc_pos2 = [-321.222, 185.189, 335.520, -179.030, -1.284, -29.869]
    desc_pos3 = [-487.434, 154.362, 308.576, 176.600, 0.268, -14.061]
    desc_pos4 = [-443.165, 147.881, 480.951, 179.511, -0.775, -15.409]
    offset_pos = [0.0] * 6
    epos = [0.0] * 4

    tool = 1
    user = 0

    self.robot.SetSpeed(20)

    # result = self.robot.MoveJ(joint_pos=j1, tool=tool, user=user, vel=vel, acc=acc, ovl=ovl, exaxis_pos=epos, blendT=blendT, offset_flag=flag, offset_pos=offset_pos)
    result = self.robot.MoveJ(joint_pos=j1, tool=tool, user=user)
    print(result)
    # self.robot.MoveL(desc_pos=desc_pos2, tool=tool, user=user, vel=vel, acc=acc, ovl=ovl, blendR=blendR, blendMode=blendMode, exaxis_pos=epos, search=search, offset_flag=flag, offset_pos=offset_pos,
    #                   oacc=oacc, velAccParamMode=velAccMode)

    # self.robot.MoveC(desc_pos_p=desc_pos3, tool_p=tool, user_p=user, vel_p=vel, acc_p=acc, exaxis_pos_p=epos, offset_flag_p=flag, offset_pos_p=offset_pos, desc_pos_t=desc_pos4, tool_t=tool, user_t=user, vel_t=vel,
    #                   acc_t=acc, exaxis_pos_t=epos, offset_flag_t=flag, offset_pos_t=offset_pos, ovl=ovl, blendR=blendR, oacc=oacc, velAccParamMode=velAccMode)

    # self.robot.Circle(desc_pos_p=desc_pos3, tool_p=tool, user_p=user, vel_p=vel, acc_p=acc, exaxis_pos_p=epos, desc_pos_t=desc_pos1, tool_t=tool, user_t=user, vel_t=vel, acc_t=acc, exaxis_pos_t=epos, ovl=ovl,
    #                    offset_flag=flag, offset_pos=offset_pos, oacc=oacc, blendR=-1, velAccParamMode=velAccMode)

    # self.robot.MoveCart(desc_pos=desc_pos4, tool=tool, user=user, vel=vel, acc=acc,ovl=ovl, blendT=blendT, config=-1)

    self.robot.CloseRPC()