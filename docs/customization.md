# Software Customizations

## Ardupilot

- much less customization than for the previous version, which had to accommodate a winch for vertical control & negative buoyancy
- lots of the work done for ROV4 has been removed, replaced with something closer to standard ardupilot
- main difference is the implementation of an "anchoring mode", and a new driver for the 

### Custom Frames
Custom frames for Anchorbot & AnchorbotMini (a bluerov)
http://www.ardusub.com/developers/developers.html#making-a-custom-configuration

``` cpp
// ardupilot/AP_Motors/AP_Motors6DOF.cpp

    case SUB_FRAME_ANCHORBOT:
        _frame_class_string = "ANCHORBOT";

    /*
    ANCHORBOT is ROV5, motors are arranged in an x configuration, with two
    vertical thrusters for depth control.

    Motor arrangement:
        1       6
            ^
          3 | 4
            |
        2       5

    */
        add_motor_raw_6dof(AP_MOTORS_MOT_1,     0.0f,            0.0f,           1.0f,           0.0f,               1.0f,               1.0f,           1);
        add_motor_raw_6dof(AP_MOTORS_MOT_2,     0.0f,            0.0f,           1.0f,           0.0f,               1.0f,               -1.0f,          2);
        add_motor_raw_6dof(AP_MOTORS_MOT_3,     0.0f,            0.0f,           0.0f,           2.0f,               0.0f,               0.0f,           3);
        add_motor_raw_6dof(AP_MOTORS_MOT_4,     0.0f,            0.0f,           0.0f,           2.0f,               0.0f,               0.0f,           4);
        add_motor_raw_6dof(AP_MOTORS_MOT_5,     0.0f,            0.0f,           1.0f,           0.0f,               -1.0f,              -1.0f,          5);
        add_motor_raw_6dof(AP_MOTORS_MOT_6,     0.0f,            0.0f,           1.0f,           0.0f,               -1.0f,              1.0f,           6);
        break;

    case SUB_FRAME_ANCHORBOTMINI:
        _frame_class_string = "ANCHORBOTMINI";
    /*
    AnchorbotMini is the original prototype, a bluerov2 with the thrusters
    extended on little arms. It's the same motor arrangement as the bluerov2, but
    the escs are numbered differently to make wiring easier

    Motor arrangement:
        2       1
            ^
          6 | 5
            |
        4       3

    */

//                         Motor #              Roll Factor     Pitch Factor    Yaw Factor      Throttle Factor     Forward Factor      Lateral Factor  Testing Order
        add_motor_raw_6dof(AP_MOTORS_MOT_1,     1.0f,           -1.0f,          1.0f,           0,                  -1.0f,              1.0f,           1);
        add_motor_raw_6dof(AP_MOTORS_MOT_2,     -1.0f,          -1.0f,          -1.0f,          0,                  -1.0f,              -1.0f,          2);
        add_motor_raw_6dof(AP_MOTORS_MOT_3,     1.0f,           1.0f,           -1.0f,          0,                  1.0f,               1.0f,           3);
        add_motor_raw_6dof(AP_MOTORS_MOT_4,     -1.0f,          1.0f,           1.0f,           0,                  1.0f,               -1.0f,          4);
        add_motor_raw_6dof(AP_MOTORS_MOT_5,     0.0f,           0,              0,              -1.0f,              0,                  0,              5);
        add_motor_raw_6dof(AP_MOTORS_MOT_6,     0.0f,           0,              0,              -1.0f,              0,                  0,              6);
        break;
```

### Anchoring Controller

- Take a look through `ardupilot/ArduAnchorbot/libraries/AA_AnchorControl` for more details. The controller corrects for any wobble during install to guarantee the anchor is correctly installed.

#### Current state:
- [x] Stabilizes a vertical anchor install only, can't handle major currents.
- [x] Tunable using the "Anchoring Control Parameters" settings page in AnchorbotQGroundControl

#### Future work:
- [ ] Stabilize around a non-vertical axis
- [ ] Implement world-frame controller for current compensation
- [ ] Constant yaw rate automatic install.
- [ ] Extend Lua scripting for missions.
- [ ] Integration with the rangefinder for automatic operation.

Quick explanation of how the controller works:
- Install axis is defined (currently hard-coded, can be included in a mission waypoint for off-vertical installs later)
- Controller compares current vertical axis to the target, gets error as angle off vertical (acos of the dot product), feeds this into a hand-tuned PID loop.
- Gets the body-frame direction of thrust by projecting the target vector onto the roll & pitch axes & normalizing to get a unit vector pointing in the direction


### Additional Customization

- [x] New CAN BMS driver `AP_BattMonitor_VESC`
- [x] Different channels for servo 1-2-3 in `joystick.cpp`
- [ ] VESC ESC CAN driver, get ESC temperature, control output over canbus
- [ ] Better logging for tuning `AA_AnchorControl`

# QGroundControl