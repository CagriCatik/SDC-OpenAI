# Path Planning

This guide outlines how to plan the optimal path for a vehicle by calculating road center waypoints and adjusting speed based on path curvature. Each task is broken down into detailed steps for implementation, testing, and optimization.

## **1. Road Center Waypoints Prediction**

The first task in path planning is to predict the car's path by generating waypoints along the road's center. These waypoints guide the vehicle to stay centered in its lane.

### **Objective**

Implement the function `waypoint_prediction()` in `waypoint_prediction.py` to output **N waypoints** along the road's center, using lane boundary splines.

### **Steps**

1. **Generate Lane Boundary Points**
   - **Task**: Using lane boundary splines (from lane detection), generate lane boundary points for **6 equidistant spline parameter values**.
   - **Spline Parameter Values**: Ensure these values cover the visible lane length, starting at a spline parameter value of **0** (closest to the vehicle).
   - **Hint**: Experiment with how far the spline parameters should extend to ensure a smooth path.

2. **Calculate the Lane Center**
   - **Task**: For each spline parameter value, compute the **midpoint** between the left and right lane boundary points. These midpoints represent the road's center for each distance.
   - **Result**: These midpoints become the **road center waypoints** that guide the car to stay centered.

3. **Output N Waypoints**
   - **Task**: Ensure that `waypoint_prediction()` outputs **N waypoints**, evenly spaced along the road length.
   - **Hint**: The value of **N** depends on how many spline parameters are chosen and should cover a reasonable distance ahead of the vehicle.

4. **Testing**
   - **Task**: Use `test_waypoint_prediction.py` to test your implementation.
   - **Edge Cases**: Pay attention to scenarios where predictions may fail, such as:
     - Abrupt lane width changes
     - Occluded or missing lane markings
     - Sharp turns

   **Goal**: Refine the implementation to handle diverse road conditions effectively.

## **2. Path Smoothing**

To optimize vehicle performance, the predicted path must not only follow the lane center but also be smoothed to avoid sharp turns and allow for more efficient navigation, such as cutting corners when appropriate.

### **Objective**

Adjust the waypoints to minimize an objective function that balances following the road's center with minimizing sharp turns.

### **Steps**

1. **Minimization Objective**
   - The function to be minimized is:

   \[
   \text{argmin}_{x_1, \dots, x_N} \sum_{i} |y_i - x_i|^2 - \beta \sum_{n} \frac{(x_{n+1} - x_n) \cdot (x_n - x_{n-1})}{|x_{n+1} - x_n||x_n - x_{n-1}|}
   \]

   Where:
   - \( x_i \in \mathbb{R}^2 \) are the **waypoints** to adjust.
   - \( y_i \in \mathbb{R}^2 \) are the **road center waypoints** computed in part 1.
   - \( \beta \) is a smoothing parameter balancing path smoothness and adherence to the center.

2. **Understanding the Terms**
   - **First Term** \( \sum_{i} |y_i - x_i|^2 \):
     - Keeps the adjusted waypoints \( x_i \) close to the center waypoints \( y_i \), ensuring the car remains near the road's center.

   - **Second Term** \( \sum_{n} \frac{(x_{n+1} - x_n) \cdot (x_n - x_{n-1})}{|x_{n+1} - x_n||x_n - x_{n-1}|} \):
     - Penalizes sharp direction changes between consecutive waypoints, favoring smoother transitions for more stable navigation.

3. **Implementation**
   - Implement the second term of the objective function in the `curvature()` function.
   - Adjust the smoothing parameter \( \beta \) to balance the curvature smoothness with path accuracy.

4. **Fine-tuning**
   - **Task**: Experiment with different values of \( \beta \) to optimize the trade-off between staying near the center and smoothing sharp turns.
   - **Goal**: Ensure smooth transitions on straight roads, bends, and sharp curves.

## **3. Target Speed Prediction**

After determining and smoothing the path, the next task is to predict the vehicle's speed along the path. The speed should vary based on the path's curvature, slowing down in sharp turns to maintain stability and accelerating on smoother sections.

### **Objective**

Implement the function `target_speed_prediction()` to calculate the car's target speed based on the curvature of the predicted path.

### **Steps**

1. **Formula for Target Speed**
   The target speed \( v_{\text{target}} \) is computed as:

   \[
   v_{\text{target}}(x_1, \dots, x_N) = (v_{\max} - v_{\min}) \exp \left[-K_v \cdot \left(N - 2 - \sum_n \frac{(x_{n+1} - x_n) \cdot (x_n - x_{n-1})}{|x_{n+1} - x_n||x_n - x_{n-1}|}\right)\right] + v_{\min}
   \]

   Where:
   - \( v_{\max} = 60 \): Maximum speed for smooth paths.
   - \( v_{\min} = 30 \): Minimum speed for sharp turns.
   - \( K_v = 4.5 \): Curvature penalty factor that controls how much the car slows in sharp curves.

2. **Understanding the Formula**
   - The **exponential function** modulates the speed, slowing the car exponentially as the path becomes more curved.
   - The **curvature term** \( \sum_n \frac{(x_{n+1} - x_n) \cdot (x_n - x_{n-1})}{|x_{n+1} - x_n||x_n - x_{n-1}|} \):
     - Measures the smoothness of the path.
     - Low curvature (straight path) results in higher speeds, while high curvature (sharp turns) results in lower speeds for stability.

   - **Adjusting \( K_v \)**: A larger \( K_v \) reduces speed more in sharp curves, while a smaller \( K_v \) allows faster cornering.

3. **Implementation**
   - Implement `target_speed_prediction()` to compute the target speed based on the curvature of the smoothed waypoints \( x_1, \dots, x_N \).
   - Use the curvature to adjust the vehicle's speed between \( v_{\min} \) and \( v_{\max} \).

4. **Fine-tuning and Testing**
   - **Test Cases**: Test the speed prediction on straight roads, slight bends, and sharp corners.
   - **Parameter Tuning**: Fine-tune parameters like \( v_{\max} \), \( v_{\min} \), and \( K_v \) for optimal performance.

   **Goal**: Ensure the car maintains stability while navigating curves efficiently.

### Summary

1. **Road Center Waypoints**: Implement `waypoint_prediction()` to generate a set of N waypoints based on lane boundary splines.
2. **Path Smoothing**: Minimize the objective function to balance staying near the road's center and reducing sharp turns.
3. **Target Speed Prediction**: Calculate the target speed based on the path's curvature, allowing for efficient and stable driving.

By following this detailed guide, you'll implement a robust path planning system that ensures smooth, stable, and efficient driving for the vehicle, with speed adjustments based on the road's curvature.
