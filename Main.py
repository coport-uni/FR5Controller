from FR5Controller import FR5Controller
import time, math

def main():
    '''
    This function run eef scenario with given parameters. exmaple with 2 FR5 robots    
    '''
    fc1 = FR5Controller("192.168.58.2")
    fc2 = FR5Controller("192.168.59.2")

    movement_range = 200
    movement_speed = 100
    movement_test = 50

    example_joint_1 = [0, -99.66753387451172, 117.4729995727539, -108.61497497558594, -91.7260513305664, 74.25582885742188]
    example_joint_2 = [90, -99.66753387451172, 117.4729995727539, -108.61497497558594, -91.7260513305664, 74.25582885742188]

    example_eef_1 = [-310.64605712890625, 167.83993530273438, 237.2095184326172, 179.6305694580078, -0.00029896487831138074, 45.72968292236328]
    example_eef_2 = [-310.64605712890625 + (movement_range / math.sqrt(2)), 167.83993530273438 + (movement_range / math.sqrt(2)), 237.2095184326172, 179.6305694580078, -0.00029896487831138074, 45.72968292236328]
    example_eef_3 = [-310.64605712890625 + (movement_range / math.sqrt(2)), 167.83993530273438 + (movement_range / math.sqrt(2)), 237.2095184326172 - movement_range, 179.6305694580078, -0.00029896487831138074, 45.72968292236328]
    example_eef_4 = [-310.64605712890625, 167.83993530273438, 237.2095184326172 - movement_range, 179.6305694580078, -0.00029896487831138074, 45.72968292236328]

    example_eef_5 = [74.24925994873047, 322.0446472167969, 90, -179.36241149902344, 3.35878381729125977, 42.54720687866211]
    example_eef_6 = [74.24925994873047 - (movement_test / math.sqrt(2)), 322.0446472167969 + (movement_test /  math.sqrt(2)), 90, -179.36241149902344, 3.5878381729125977, 42.54720687866211]

    for i in range(3):
        fc1.run_eef_movement_ptp(example_eef_1, 100, target_eef_speed = movement_speed)
        fc2.run_eef_movement_ptp(example_eef_1, 100, target_eef_speed = movement_speed)

        fc1.run_eef_movement_ptp(example_eef_2, 0, target_eef_speed = movement_speed)
        fc2.run_eef_movement_ptp(example_eef_2, 0, target_eef_speed = movement_speed)

        fc1.run_eef_movement_ptp(example_eef_3, 100, target_eef_speed = movement_speed)
        fc2.run_eef_movement_ptp(example_eef_3, 100, target_eef_speed = movement_speed)

        fc1.run_eef_movement_ptp(example_eef_4, 0, target_eef_speed = movement_speed)
        fc2.run_eef_movement_ptp(example_eef_4, 0, target_eef_speed = movement_speed)

        fc1.run_eef_movement_ptp(example_eef_1, 100, target_eef_speed = movement_speed)
        fc2.run_eef_movement_ptp(example_eef_1, 100, target_eef_speed = movement_speed)


    fc1.robot.CloseRPC()
    fc2.robot.CloseRPC()

if __name__ == "__main__":
    main()