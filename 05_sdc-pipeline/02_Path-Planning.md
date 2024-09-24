### Path Planning: Detailed Implementation Guide

This section covers how to plan the path for a vehicle by calculating the optimal road center waypoints and setting the appropriate speed based on the path's curvature. Below, each task is broken down into more detailed steps, providing guidance for implementation, testing, and optimization.

---

#### **a) Road Center Waypoints Prediction:**

The first step in path planning is predicting the car's path by determining waypoints along the center of the road. These waypoints will guide the vehicle to follow the center of the lane accurately.

##### **Objective**:
To implement a function `waypoint_prediction()` that outputs **N waypoints** along the center of the road, based on the lane boundary splines, in `waypoint_prediction.py`.

##### **Steps**:

1. **Generate Lane Boundary Points**:
   - Using the lane boundary splines (previously calculated in the lane detection module), derive the lane boundary points corresponding to **6 equidistant spline parameter values**.
   - **Spline Parameter Values**: These values should cover the length of the visible lane. The points generated for each spline parameter will represent the lane boundaries at various distances from the vehicle.
   
   **Hint**: For best results, ensure that the first waypoint (closest to the vehicle) has a spline parameter value of **0**, meaning that the first boundary points should be as close to the vehicle as possible. You may want to experiment with how far the spline parameters should extend to generate smooth, usable paths.

2. **Calculate Center of Lane**:
   - For each of the spline parameter values, compute the **midpoint** between the left and right lane boundary points. This midpoint represents the center of the lane for that specific parameter.
   - These midpoints will serve as the **road center waypoints**, which the car will follow to stay centered in the lane.

3. **N Waypoints**:
   - Ensure that your `waypoint_prediction()` function outputs **N waypoints** representing the center of the road, evenly spaced along the lane's length.
   
   **N**: The number of waypoints will depend on the total number of spline parameter values and should cover a reasonable length of the road ahead of the vehicle.

4. **Testing**:
   - Test your implementation using the provided script `test_waypoint_prediction.py`.
   - **Edge Cases**: While testing, pay close attention to situations where the prediction fails, such as:
     - When the lane width changes abruptly.
     - When lane markings are occluded or missing.
     - Sharp turns or bends in the road.
   
   These failure cases can help you refine your cropping, boundary detection, and spline fitting steps to handle a wider variety of road conditions.

---

#### **b) Path Smoothing:**

To create a high-performance racing car, the predicted path should not just follow the center of the lane; it should also be smoothed to optimize the car's movement along the road, such as cutting corners when appropriate. This involves adjusting the waypoints by minimizing an objective function that accounts for both path accuracy and smoothness.

##### **Objective**:
Smooth the path by adjusting the waypoints to minimize an objective function that balances staying close to the road's center with reducing sharp turns.

##### **Steps**:

1. **Minimization Objective**:
   The objective function to be minimized is given by:

   \[
   \text{argmin}_{x_1, \dots, x_N} \sum_{i} |y_i - x_i|^2 - \beta \sum_{n} \frac{(x_{n+1} - x_n) \cdot (x_n - x_{n-1})}{|x_{n+1} - x_n||x_n - x_{n-1}|}
   \]
   
   Where:
   - \( x_i \in \mathbb{R}^2 \) are the **waypoints** that you will adjust to minimize the objective.
   - \( y_i \in \mathbb{R}^2 \) are the **road center waypoints** (computed in part a) that represent the estimated center path.
   - \( \beta \) is a smoothing parameter that controls the trade-off between staying close to the center and reducing sharp turns.

2. **Understanding the Two Terms**:
   - **First Term** \( \sum_{i} |y_i - x_i|^2 \):
     - This term ensures that the smoothed path \( x_i \) stays as close as possible to the original road center waypoints \( y_i \). In essence, this prevents the car from straying too far from the center of the road.
   
   - **Second Term** \( \sum_{n} \frac{(x_{n+1} - x_n) \cdot (x_n - x_{n-1})}{|x_{n+1} - x_n||x_n - x_{n-1}|} \):
     - This term measures the **change in direction** between consecutive waypoints. The objective here is to penalize sharp changes in direction, encouraging smoother transitions from one waypoint to the next.
     - **Interpretation**: It’s a curvature-based smoothing term, where smoother paths (with less drastic changes in direction) are favored. This is especially important for high-speed racing where jerky movements can result in instability.

3. **Implementation**:
   - Implement the **second term** of the objective function in the `curvature()` function. You will need to calculate the change in direction between consecutive waypoints and adjust the smoothing parameter \( \beta \) to balance curvature smoothness with path accuracy.
   
   **Hint**: Refer to section 8.1 of [2] for more details on path smoothing.

4. **Fine-tuning**:
   - Experiment with different values of \( \beta \) to find the optimal trade-off between staying close to the center of the road and minimizing sharp turns.
   - Test how the smoothing behaves in sharp curves, straight roads, and varying road conditions.

---

#### **c) Target Speed Prediction:**

Once the path has been determined and smoothed, the next critical task is to determine the speed at which the car should drive along the predicted path. This speed should depend on the path’s curvature: the car should accelerate when the path is smooth and decelerate in sharp turns to avoid instability.

##### **Objective**:
Implement the function `target_speed_prediction()` to calculate the car's target speed based on the curvature of the predicted path.

##### **Steps**:

1. **Formula for Target Speed**:
   The target speed \( v_{\text{target}} \) is computed as:

   \[
   v_{\text{target}}(x_1, \dots, x_N) = (v_{\max} - v_{\min}) \exp \left[-K_v \cdot \left(N - 2 - \sum_n \frac{(x_{n+1} - x_n) \cdot (x_n - x_{n-1})}{|x_{n+1} - x_n||x_n - x_{n-1}|}\right)\right] + v_{\min}
   \]
   
   Where:
   - \( v_{\max} = 60 \): Maximum possible speed in smooth paths.
   - \( v_{\min} = 30 \): Minimum possible speed for sharper curves.
   - \( K_v = 4.5 \): Curvature penalty factor, which adjusts how much the car slows down for sharper curves.

2. **Understanding the Formula**:
   - The **exponential function** ensures that the speed decreases exponentially as the path becomes more curved.
   - The **curvature term** \( \sum_n \frac{(x_{n+1} - x_n) \cdot (x_n - x_{n-1})}{|x_{n+1} - x_n||x_n - x_{n-1}|} \) measures the smoothness of the path:
     - When the path is straight (low curvature), this term is small, resulting in higher speeds.
     - When the path is curvy (high curvature), this term becomes larger, leading to a lower speed to maintain stability.
   
   - \( K_v \) controls how aggressively the speed is reduced for high curvature. A larger \( K_v \) would make the car slow down more in sharp turns, while a smaller \( K_v \) would allow for faster cornering.

3. **Implementation**:
   - Implement the function `target_speed_prediction()` to compute the target speed based on the predicted path and curvature.
   - Use the curvature of the waypoints \( x_1, \dots, x_N \) to modulate the car’s speed between \( v_{\min} \) and \( v_{\max} \).

4. **Fine-tuning and Testing**:
   - **Test Cases**: Ensure your speed prediction works well on straight roads, slight bends, and sharp corners.
   - **Parameter Tuning**: You can experiment with the following parameters to optimize performance:
     - \( v_{\max} \) and \( v_{\min} \) for speed limits.
     - \( K_v \) for curvature sensitivity.
   
   **Goal**: Achieve a balance between fast cornering and maintaining vehicle stability.

---

### Summary:

1. **Road Center**: Implement `waypoint_prediction()` to generate a set of N center waypoints based on lane boundary splines.
2. **Path Smoothing**: Smooth the path by minimizing the objective function that balances staying close to the center and reducing sharp turns.
3. **Target Speed Prediction**: Use the curvature of the smoothed path to compute the optimal target speed for the vehicle.

By following these detailed steps, you can ensure that the

 vehicle follows a smooth, stable, and efficient path, adapting its speed based on the curvature of the road ahead.