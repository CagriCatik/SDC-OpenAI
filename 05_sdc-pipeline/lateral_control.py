import numpy as np

class LateralController:
    '''
    Lateral control using the Stanley controller

    functions:
        stanley 

    init:
        gain_constant (default=5)
        damping_constant (default=0.5)
    '''

    def __init__(self, gain_constant=0.025, damping_constant=0.0125):
        self.gain_constant = gain_constant
        self.damping_constant = damping_constant
        self.previous_steering_angle = 0

    def stanley(self, waypoints, speed):
        '''
        One step of the Stanley controller with damping.
        Args:
            waypoints (np.array): Shape [2, num_waypoints], the waypoints in vehicle coordinates.
            speed (float): The current speed of the vehicle.
        '''
        # Prevent division by zero by adding a small epsilon
        epsilon = 1e-6  # Small value to prevent division by zero

        # Vehicle's position and heading (assumed to be at the origin and along the x-axis)
        vehicle_position = np.array([0.0, 0.0])
        vehicle_heading = 0.0  # Heading along the x-axis

        # Derive orientation error as the angle of the first path segment to the car orientation
        if waypoints.shape[1] >= 2:
            dx = waypoints[0, 1] - waypoints[0, 0]
            dy = waypoints[1, 1] - waypoints[1, 0]
            path_heading = np.arctan2(dy, dx)
        else:
            path_heading = 0.0  # Default to zero if not enough waypoints

        psi_t = path_heading - vehicle_heading
        # Normalize psi_t to the range [-pi, pi]
        psi_t = (psi_t + np.pi) % (2 * np.pi) - np.pi

        # Derive cross-track error as distance between the first waypoint and the car position
        dx_error = waypoints[0, 0] - vehicle_position[0]
        dy_error = waypoints[1, 0] - vehicle_position[1]
        d_t = np.hypot(dx_error, dy_error)

        # Determine the sign of the cross-track error
        cross_track_vector = np.array([dx_error, dy_error])
        cross_track_error_sign = np.sign(cross_track_vector[1])  # Sign based on y-component
        d_t = d_t * cross_track_error_sign  # Signed cross-track error

        # Derive Stanley control law
        delta_sc = psi_t + np.arctan2(self.gain_constant * d_t, speed + epsilon)

        # Derive damping term
        delta = delta_sc - self.damping_constant * (delta_sc - self.previous_steering_angle)

        # Update the previous steering angle
        self.previous_steering_angle = delta

        steering_angle = delta
        # Clip to the maximum steering angle (0.4 radians) and rescale the steering action space
        return np.clip(steering_angle, -0.4, 0.4) / 0.4
