import numpy as np

class Config:
    
    u_resolution = 5
    v_resolution = 5
    frequency = 1
    initial_conditions = np.zeros(shape =u_resolution*v_resolution)
    field_tip_scale_factor = .2
    full_phase_number = 2
    ambient_camera_rotation_rate = np.pi/8
    animation_time = 10
    

