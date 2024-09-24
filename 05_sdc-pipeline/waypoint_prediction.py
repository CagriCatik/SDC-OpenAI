import numpy as np
from scipy.interpolate import splev
from scipy.optimize import minimize

def normalize(v):
    norm = np.linalg.norm(v, axis=0) + 1e-10  # Avoid division by zero
    return v / norm

def curvature(waypoints):
    '''
    Compute the curvature term for path smoothing and speed prediction.

    args:
        waypoints: [2, num_waypoints]
    '''
    delta_waypoints = waypoints[:, 1:] - waypoints[:, :-1]  # Shape: [2, N-1]
    delta_waypoints_normalized = normalize(delta_waypoints)  # Shape: [2, N-1]
    
    # Compute dot products between consecutive normalized vectors
    dots = np.sum(delta_waypoints_normalized[:, :-1] * delta_waypoints_normalized[:, 1:], axis=0)
    
    # Curvature term as per the objective function
    curvature = np.sum(dots)
    return curvature

def smoothing_objective(waypoints_flat, waypoints_center_flat, beta=30):
    '''
    Objective function for path smoothing.

    args:
        waypoints_flat: [2 * num_waypoints] flattened waypoints array to optimize
        waypoints_center_flat: [2 * num_waypoints] flattened center waypoints array
        beta: smoothing parameter
    '''
    num_waypoints = waypoints_center_flat.shape[0] // 2
    waypoints = waypoints_flat.reshape(2, num_waypoints)
    waypoints_center = waypoints_center_flat.reshape(2, num_waypoints)

    # First term: Sum of squared differences between waypoints and center waypoints
    ls_tocenter = np.sum((waypoints - waypoints_center) ** 2)

    # Second term: Curvature term
    curv = curvature(waypoints)

    # Objective function: Minimize the first term and maximize the curvature term
    objective = ls_tocenter - beta * curv
    return objective

def waypoint_prediction(roadside1_spline, roadside2_spline, num_waypoints=6, way_type="smooth"):
    '''
    Predict waypoints via two different methods:
    - "center": Directly use the midpoints between lane boundaries
    - "smooth": Smooth the path by optimizing the waypoints

    args:
        roadside1_spline: Spline representation of the first roadside
        roadside2_spline: Spline representation of the second roadside
        num_waypoints: Number of waypoints to generate (default=6)
        way_type: "center" or "smooth" (default="smooth")
    '''
    # Create spline parameter values from 0 to a value less than or equal to 1
    u = np.linspace(0, 1, num_waypoints)

    # Derive roadside points from splines
    roadside1_points = np.array(splev(u, roadside1_spline))  # Shape: [2, num_waypoints]
    roadside2_points = np.array(splev(u, roadside2_spline))  # Shape: [2, num_waypoints]

    # Calculate the midpoints between corresponding roadside points
    waypoints_center = (roadside1_points + roadside2_points) / 2  # Shape: [2, num_waypoints]

    if way_type == "center":
        # Output waypoints with shape (2 x num_waypoints)
        return waypoints_center

    elif way_type == "smooth":
        # Flatten the waypoints for optimization
        waypoints_center_flat = waypoints_center.flatten()

        # Optimization to smooth the path
        result = minimize(
            smoothing_objective,
            waypoints_center_flat,
            args=(waypoints_center_flat),
            method='L-BFGS-B'
        )

        # Retrieve the optimized waypoints
        waypoints_smoothed_flat = result.x
        waypoints_smoothed = waypoints_smoothed_flat.reshape(2, num_waypoints)

        return waypoints_smoothed

def target_speed_prediction(waypoints, num_waypoints_used=4,
                            max_speed=30, min_speed=15, K_v=2.5):
    '''
    Predict target speed given waypoints using curvature.

    args:
        waypoints: [2, num_waypoints]
        num_waypoints_used: Number of waypoints to consider (default=5)
        max_speed: Maximum possible speed (default=60)
        min_speed: Minimum possible speed (default=30)
        K_v: Curvature penalty factor (default=4.5)

    output:
        target_speed (float)
    '''
    # Use the specified number of waypoints
    waypoints_used = waypoints[:, :num_waypoints_used]

    # Compute curvature term for speed prediction
    delta_waypoints = waypoints_used[:, 1:] - waypoints_used[:, :-1]  # Shape: [2, N-1]
    delta_waypoints_normalized = normalize(delta_waypoints)
    dots = np.sum(
        delta_waypoints_normalized[:, :-1] * delta_waypoints_normalized[:, 1:], axis=0
    )
    curvature_term = np.sum(1 - dots)

    # Apply the target speed formula
    exponent = -K_v * curvature_term
    target_speed = (max_speed - min_speed) * np.exp(exponent) + min_speed
    target_speed = max(target_speed, 0)  # Ensure non-negative speed

    return target_speed

