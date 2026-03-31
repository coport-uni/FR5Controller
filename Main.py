from FR5Controller import FR5Controller
import time, math

def main():
    '''
    This function run eef scenario with given parameters. exmaple with 2 FR5 robots    
    '''
    fc1 = FR5Controller("192.168.58.2")
    # fc2 = FR5Controller("192.168.59.2")

    movement_range = 200
    movement_speed = 100
    movement_test = 50

    example_joint_1 = [-135, -25, -150, -30, 90, 0]
    example_joint_2 = [-135 + 45, -25, -150, -30, 90, 0]

    for i in range(3):
        fc1.run_joint_movement(example_joint_1, 0)
        fc1.run_joint_movement(example_joint_2, 100)


    fc1.robot.CloseRPC()
    # fc2.robot.CloseRPC()

if __name__ == "__main__":
    main()