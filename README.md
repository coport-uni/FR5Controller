# FR5Controller

A Python controller library for the Fairino FR5 collaborative robot, providing simplified interfaces for robot control, gripper operations, and motion planning.

## Overview

FR5Controller is a high-level wrapper around the Fairino Python SDK that provides intuitive methods for controlling the FR5 robot arm. It simplifies common operations such as joint movements, end-effector (EEF) positioning, and gripper control with built-in error handling and logging.

## Features

- **Robot Initialization**: Automatic connection setup and error reset
- **Gripper Control**: Support for Dahuan gripper with activation and positioning
- **Joint Movement**: Control robot joints with configurable speed and position
- **End-Effector Control**: Point-to-point (PTP) Cartesian movements
- **Error Handling**: Comprehensive error analysis and logging
- **Debug Modes**: Configurable logging levels (info/error)
- **Singular Avoidance**: Built-in singularity avoidance for safe movements

## Requirements

- Python 3.12 
- Fairino Python SDK (Which is included)
- Network connection to FR5 robot controller (Double check wiring with given manual)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/coport-uni/FR5Controller.git
cd FR5Controller
```

2. Ensure the Fairino SDK is available in the `fairino` directory

3. Check robot status to "autonomous mode". which is usually blue lighted. 

## Usage

### Basic Setup

```python
from FR5Controller import FR5Controller

# Initialize controller with robot IP address
fc = FR5Controller("192.168.58.2")
```

### Joint Movement

```python
# Define target joint positions (in degrees)
target_joints = [0, -99.67, 117.47, -108.61, -91.73, 74.26]

# Move to position with gripper at 100% open, speed 30%
fc.run_joint_movement(target_joints, target_gripper_position=100, target_joint_speed=30)

# Get current joint positions
current_joints = fc.get_joint_position()
```

### End-Effector Movement (Cartesian)

```python
# Define target EEF pose [x, y, z, rx, ry, rz]
target_eef = [-310.65, 167.84, 237.21, 179.63, -0.0003, 45.73]

# Move to position with gripper closed (0%), speed 30%
fc.run_eef_movement_ptp(target_eef, target_gripper_position=0, target_eef_speed=30)

# Get current EEF pose
current_eef = fc.get_eef_position()
```

### Gripper Control

```python
# Open gripper (100% open)
fc.run_gripper_movement(target_gripper_position=100,
                        target_gripper_speed=100,
                        target_gripper_power=50)

# Close gripper (0% open / fully closed)
fc.run_gripper_movement(target_gripper_position=0,
                        target_gripper_speed=100,
                        target_gripper_power=50)

# Get current gripper position
position = fc.get_gripper_position()
```

### Closing Connection

```python
# Always close the connection when done
fc.robot.CloseRPC()
```

## API Reference

### FR5Controller Class

#### `__init__(self, ip_address: str)`
Initialize connection to the FR5 robot controller.

- **Parameters**: `ip_address` - IP address of the robot controller (e.g., "192.168.58.2")

#### `run_joint_movement(target_joint_list, target_gripper_position, target_gripper_speed=100, target_gripper_power=50, target_joint_speed=30)`
Execute joint movement with gripper control.

- **Parameters**:
  - `target_joint_list` (list): Target joint angles in degrees [J1, J2, J3, J4, J5, J6]
  - `target_gripper_position` (int): Gripper position (0-100%)
  - `target_gripper_speed` (int): Gripper speed (0-100%, default: 100)
  - `target_gripper_power` (int): Gripper force (0-100%, default: 50)
  - `target_joint_speed` (int): Joint movement speed (0-100%, default: 30)

#### `run_eef_movement_ptp(target_eef_list, target_gripper_position, target_gripper_speed=100, target_gripper_power=50, target_eef_speed=30)`
Execute Cartesian point-to-point movement with gripper control.

- **Parameters**:
  - `target_eef_list` (list): Target pose [x, y, z, rx, ry, rz]
  - `target_gripper_position` (int): Gripper position (0-100%)
  - `target_gripper_speed` (int): Gripper speed (0-100%, default: 100)
  - `target_gripper_power` (int): Gripper force (0-100%, default: 50)
  - `target_eef_speed` (int): Cartesian movement speed (0-100%, default: 30)

#### `run_gripper_movement(target_gripper_position, target_gripper_speed, target_gripper_power)`
Control gripper independently.

- **Parameters**:
  - `target_gripper_position` (int): Target position (0-100%)
  - `target_gripper_speed` (int): Movement speed (0-100%)
  - `target_gripper_power` (int): Gripping force (0-100%)

#### `get_joint_position()`
Get current joint angles.

- **Returns**: list - Current joint positions in degrees

#### `get_eef_position()`
Get current end-effector pose.

- **Returns**: list - Current EEF pose [x, y, z, rx, ry, rz]

#### `get_gripper_position()`
Get current gripper position.

- **Returns**: int - Current gripper position (0-100%)

#### `setup_debugger(debug_level: str)`
Configure logging level.

- **Parameters**: `debug_level` - "info" or "error"

## Example Application

See [Main.py](Main.py) for a complete example demonstrating:
- Robot initialization
- Sequential EEF movements
- Gripper control integration
- Multiple movement patterns

## Error Handling

The controller includes built-in error handling for common scenarios:
- **Error Code 0**: Operation successful
- **Error Code 14**: Robot motion error (requires error reset)
- **Other errors**: Communication errors (may require reboot)

All errors are logged and raise exceptions with descriptive messages.

## Gripper Configuration

Currently configured for Dahuan gripper (company code: 4). To use a different gripper, modify the `setup_gripper()` method:
- 1: Robotiq
- 2: Huiling
- 3: Tianji
- 4: Dahuan (default)
- 5: Knowledge

## License

Please refer to the Fairino SDK license for usage terms.

## Documentation

For more information about the Fairino Python SDK, see:
- [Fairino Python SDK Documentation](https://fair-documentation.readthedocs.io/en/latest/SDKManual/python_intro.html)

## Contributing

Contributions are welcome! Please ensure all changes maintain backward compatibility and include appropriate error handling.
