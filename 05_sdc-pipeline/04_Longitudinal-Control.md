# Longitudinal Control of a Vehicle

This section focuses on designing and implementing a **longitudinal control** system that regulates the vehicle's speed using a **PID controller**. The controller adjusts the throttle (acceleration) and braking inputs to ensure the vehicle tracks a target speed, calculated from previous sections.

The implementation is divided into two parts:

1. Implementing the **PID Controller** for speed regulation.
2. Tuning the **PID Parameters** to optimize control performance.

## **1. PID Controller**

The PID controller's goal is to minimize the error between the vehicle's actual speed \( v(t) \) and the target speed \( v_{\text{target}} \). It adjusts the control input \( u(t) \), which manages throttle or brake commands.

### Control Law

The speed error is defined as:

\[
e(t) = v_{\text{target}} - v(t)
\]

Where:

- \( e(t) \) is the error between the target speed and the actual speed at time \( t \).

The control signal \( u(t) \) is then calculated as:

\[
u(t) = K_p \cdot e(t) + K_d \cdot \left[ e(t) - e(t-1) \right] + K_i \cdot \left[ \sum_{l=0}^{t} e(l) \right]
\]

Where:

- \( K_p \): Proportional gain, which scales the control input based on the current error.
- \( K_d \): Derivative gain, which adjusts the input based on the rate of change of the error.
- \( K_i \): Integral gain, which sums past errors to correct long-term drift and eliminate steady-state error.

### Control Signal Interpretation

- If \( u(t) > 0 \), throttle is applied to increase the vehicle's speed.
- If \( u(t) < 0 \), braking is applied to reduce the speed.

The corresponding logic is:

\[
a_{\text{gas}}(t) =
\begin{cases}
0 & u(t) < 0 \\
u(t) & u(t) \geq 0
\end{cases}
\]
\[
a_{\text{brake}}(t) =
\begin{cases}
-u(t) & u(t) < 0 \\
0 & u(t) \geq 0
\end{cases}
\]

### Key Control Concepts

1. **Proportional Control \( K_p \)**:
   - Responds to the current speed error. A higher \( K_p \) increases responsiveness but can cause oscillations or overshoot if too high.

2. **Integral Control \( K_i \)**:
   - Accumulates past errors to eliminate steady-state error. Overuse can lead to **integral windup**, causing large overshoots due to accumulated error.

3. **Derivative Control \( K_d \)**:
   - Reacts to the rate of change of the error. It helps dampen oscillations by predicting future error trends, preventing overshoot.

### Avoiding Integral Windup

Integral windup occurs when the integral term accumulates excessively, causing large overshoots. To prevent this:

1. **Clamp the integral sum**: Limit the maximum value of the integral term.
2. **Anti-windup techniques**: Halt or reset the integral accumulation when the system reaches the desired speed.

## **2. PID Parameter Tuning**

Tuning the PID controller parameters \( K_p \), \( K_d \), and \( K_i \) is crucial to achieve optimal system performance. The goal is to balance responsiveness and stability, minimizing error while avoiding oscillations or overshoot.

### General Approach to PID Tuning

1. **Start with Proportional Control**:
   - Set \( K_d = 0 \) and \( K_i = 0 \), and focus on tuning \( K_p \).
   - Gradually increase \( K_p \) until the vehicle responds effectively to speed changes without excessive oscillations.
   - Observe the system’s initial behavior in reaching the target speed.

2. **Introduce Derivative Control**:
   - Once the proportional control is satisfactory, start tuning \( K_d \).
   - Derivative control helps smooth the response, particularly reducing oscillations caused by the proportional term.
   - Gradually increase \( K_d \) to achieve a smoother, less oscillatory response.

3. **Add Integral Control**:
   - Finally, introduce \( K_i \) to address any remaining steady-state error.
   - Slowly increase \( K_i \), but be cautious of integral windup. Implement anti-windup measures to prevent excessive accumulation.

### Parameter Search Process

Tuning the PID parameters requires empirical testing to find the best balance. Key considerations include:

- **Vehicle Speed Range**: The system must work across the vehicle's full speed range.
- **Responsiveness**: How quickly the system reacts to speed changes (acceleration and deceleration).
- **Road Conditions**: Consider the impact of road conditions like slopes or varying friction.

To guide the tuning process:

1. Use plots of the actual speed versus the target speed (available in `test.longitudinal_control.py`) to monitor system behavior.
2. Focus on \( K_p \) first, as it has the most immediate impact on the control system’s performance.
3. Adjust \( K_d \) to dampen oscillations and improve stability.
4. Finally, tune \( K_i \) to eliminate any steady-state error, while keeping an eye on potential windup.

## **Summary and Conclusion**

The longitudinal control system uses a **PID controller** to adjust throttle and braking commands, ensuring the vehicle tracks a desired target speed. The controller is designed to minimize speed error through three components:

1. **Proportional Control**: Adjusts based on current error, offering immediate responsiveness.
2. **Integral Control**: Accumulates past errors to eliminate long-term deviation from the target, but requires careful tuning to avoid windup.
3. **Derivative Control**: Responds to error rate changes, reducing overshoot and stabilizing the system.

From a control engineering perspective, tuning \( K_p \), \( K_d \), and \( K_i \) is essential to achieving the desired balance between fast response and stable behavior. Proper tuning ensures the vehicle smoothly accelerates and decelerates, maintaining the target speed under various driving conditions. Anti-windup techniques are necessary to prevent excessive integral action from destabilizing the system.

The PID-based longitudinal control system forms a solid framework for maintaining consistent vehicle speed and can be adapted for various road conditions, providing a robust foundation for effective speed management.
