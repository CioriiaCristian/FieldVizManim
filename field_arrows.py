from manim import *
from manim.opengl import *
from config import Config
import numpy as np

u_res = Config.u_resolution
v_res = Config.v_resolution
init_cond = Config.initial_conditions
freq = Config.frequency
arrow_size = Config.field_tip_scale_factor
full_phase_rotations = Config.full_phase_number
camera_rotation_rate = Config.ambient_camera_rotation_rate


def get_sphere_faces_centers(u_resolution, v_resolution):
    
    # u_values stand for phi values
    # v_values stand for theta values
    # phi and theta are defined as in https://en.wikipedia.org/wiki/Spherical_coordinate_system#Integration_and_differentiation_in_spherical_coordinates
    
    u_values = np.linspace(0,TAU,u_resolution+1)
    v_values = np.linspace(0, PI, v_resolution+1)
    u_centers = [np.mean(u_values[i:i+2]) for i in range(u_resolution)]
    v_centers = [np.mean(v_values[i:i+2]) for i in range(v_resolution)]
    centers_list = np.transpose([np.tile(u_centers, len(v_centers)), np.repeat(v_centers, len(u_centers))])          
    return centers_list


class FieldArrows(ThreeDScene):
    def construct(self):
        
        # DEFINE THE 3D axes and show them in the Scene
        axes = ThreeDAxes()
        sphere = Sphere(resolution=[u_res, v_res], fill_opacity = 1)
        self.add(axes,sphere)
        self.set_camera_orientation(phi = 45*DEGREES, theta = 60*DEGREES)
        
        # COMPUTE SPHERE POLYGON CENTER POSITIONS
        faces_centers = get_sphere_faces_centers(u_resolution=u_res, v_resolution=v_res)
        value_trackers_list = [ValueTracker(init_cond[i]) for i in range(u_res*v_res)]

        # STORE OBJECTS TO ANIMATE LATER
        center_dots = []
        field_tip_dots = []
        arrows = []

        # CREATE ANIMATION OBJECTS 
        for idx, _center in enumerate(faces_centers):
            _u,_v = _center
            # GET r,theta,phi spherical coord unit vectors
            # _u stands for phi, _v stands for theta. phi varies between [0,2*PI], theta varies between [0,PI]
            # _u is the azimuthal angle, _v is the latitude
            r_vector_direction = np.array([
                np.cos(_u)*np.sin(_v), np.sin(_u)*np.sin(_v), np.cos(_v)
            ])
            theta_vector_direction = np.array([
                np.cos(_u)*np.cos(_v), np.sin(_u)*np.cos(_v), -np.sin(_v)
            ])
            phi_vector_direction = np.array([
                -np.sin(_u), np.cos(_u), 0
            ])
            center_dots.append(
                Dot(r_vector_direction, color = random_bright_color().get_hex(), fill_opacity = 0)
                .rotate(axis=phi_vector_direction, angle=_v)
                )
            self.add(center_dots[idx])
            
            
            field_tip_dots.append(always_redraw(
                lambda idx = idx, 
                        r_hat = r_vector_direction, 
                        theta_hat = theta_vector_direction, 
                        phi_hat = phi_vector_direction, 
                        _v = _v, 
                        _u = _u : 
                        Dot(point = center_dots[idx].get_center(), fill_opacity=0)
                        .rotate(axis=phi_hat, angle=_v)
                        .shift(arrow_size*(np.cos(freq*TAU*value_trackers_list[idx].get_value())*theta_hat + np.sin(freq*TAU*value_trackers_list[idx].get_value())*phi_hat))
            ))
            self.add(field_tip_dots[idx])

            arrows.append(always_redraw( 
                    lambda idx=idx: Arrow(start = center_dots[idx].get_center(), end = field_tip_dots[idx].get_center(), stroke_color = RED, stroke_width=4)
                )
            )
            self.add(arrows[idx])

        
        
        self.begin_ambient_camera_rotation(rate=camera_rotation_rate)
        self.play(AnimationGroup(*[k.animate.set_value(full_phase_rotations) for k in value_trackers_list]), run_time = 5)
        self.play(Uncreate(sphere), run_time = 2)
        self.wait(2)
        self.stop_ambient_camera_rotation()
        self.wait(3)

        #Enable interactive mode if you want to interact with the 3D Scene via mouse
        #self.interactive_embed()

