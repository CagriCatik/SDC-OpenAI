# Longitudinal Control of a Vehicle

In this section, the focus is on implementing a **longitudinal control** system that manages the speed of the vehicle through a **PID controller**. This control system adjusts the throttle (gas) and braking inputs to track a desired target speed, which has been calculated in prior sections.

The process is divided into two major parts:

1. Implementing the **PID Controller** to follow the target speed.
2. Tuning the **PID Parameters** to optimize the system's performance.

---

### a) PID Controller

The goal of the longitudinal control system is to minimize the difference between the vehicle's actual speed \( v(t) \) and the desired or target speed \( v_{\text{target}} \). The PID controller adjusts the control input \( u(t) \), which governs the gas or brake commands to the vehicle.

#### Control Law

The PID controller in its discretized form is expressed as:

\[
e(t) = v_{\text{target}} - v(t)
\]

Where:

- \( e(t) \) is the speed error at time \( t \), representing the difference between the target speed and the actual speed of the vehicle.

The control signal \( u(t) \), which dictates whether to apply throttle or braking, is calculated by the following equation:

\[
u(t) = K_p \cdot e(t) + K_d \cdot \left[ e(t) - e(t-1) \right] + K_i \cdot \left[ \sum_{l=0}^{t} e(l) \right]
\]

Where:

- \( K_p \): Proportional gain, which adjusts the control signal in proportion to the current error \( e(t) \).
- \( K_d \): Derivative gain, which adjusts the control signal based on the rate of change of the error (i.e., how fast the error is changing).
- \( K_i \): Integral gain, which adjusts the control signal based on the accumulation of past errors, helping to eliminate steady-state error.

#### Control Signal Interpretation

- If \( u(t) > 0 \), the vehicle should accelerate by applying throttle.
- If \( u(t) < 0 \), the vehicle should decelerate by applying the brakes.

This logic is implemented as:

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

#### Key Control Concepts

- **Proportional Control \( K_p \)**: The proportional term provides a control signal proportional to the current error. A higher \( K_p \) will cause the vehicle to respond more aggressively to deviations from the target speed. However, too high of a value can cause oscillations or overshoot.
  
- **Integral Control \( K_i \)**: The integral term sums past errors to eliminate steady-state errors, ensuring the vehicle maintains the desired speed over time. However, excessive accumulation (also known as **integral windup**) can cause large overshoots, especially if the error accumulates over a long period without correction.

- **Derivative Control \( K_d \)**: The derivative term helps predict the future trend of the error by considering how fast the error is changing. This reduces overshoot and helps the system dampen oscillations by reacting to rapid error changes.

#### Avoiding Integral Windup

The integral term can lead to an issue known as **integral windup**, where the error accumulates to such an extent that it causes the system to overshoot the target speed significantly. To prevent this, it is necessary to limit the maximum value of the integral term or reset it when the system achieves the desired speed. This can be done by:

- **Clamping the integral sum**: Setting a maximum limit on the cumulative error sum.
- **Anti-windup techniques**: Implement mechanisms that halt or reset the accumulation of the integral term when certain conditions are met, such as when the error becomes zero.

---

### b) PID Parameter Tuning

Tuning the PID controller parameters \( K_p \), \( K_d \), and \( K_i \) is an essential step in achieving a well-behaved control system. The goal is to find the right balance between responsiveness (reducing the error quickly) and stability (avoiding overshoot or oscillations).

#### General Approach to PID Tuning

1. **Start with Proportional Control**:
   - Set \( K_d = 0 \) and \( K_i = 0 \), and tune only \( K_p \).
   - Slowly increase \( K_p \) until the system responds adequately to changes in speed but without causing oscillations or overshoot.
   - A good starting point is to observe how quickly the vehicle accelerates toward the target speed.

2. **Add Derivative Control**:
   - Once the proportional control is satisfactory, start tuning \( K_d \).
   - The derivative term helps to smooth out the response, especially when the system is prone to overshoot or rapid changes in error.
   - Increase \( K_d \) gradually until the system’s response becomes smoother and less oscillatory.

3. **Add Integral Control**:
   - Finally, tune the integral gain \( K_i \).
   - The integral term helps eliminate steady-state errors, ensuring that the vehicle can maintain the desired speed over time.
   - Increase \( K_i \) slowly, but keep an eye on the possibility of integral windup. Implement an anti-windup mechanism if necessary.

#### Parameter Search

Finding the correct values of \( K_p \), \( K_d \), and \( K_i \) is largely empirical and requires extensive testing. In particular, attention should be paid to:

- The maximum and minimum speeds of the vehicle.
- The responsiveness of the system to both acceleration and deceleration.
- The impact of different road conditions (e.g., slopes, friction) on the control system.

The recommended approach for parameter tuning is to:

1. Use the **plots** of the target speed and the actual speed generated by `test.longitudinal_control.py` to observe the system's behavior.
2. Start with tuning the proportional term \( K_p \), as it has the most immediate and significant effect on the control system.
3. Adjust the derivative term \( K_d \) to dampen any oscillations or overshoot caused by proportional control.
4. Lastly, introduce the integral term \( K_i \) to correct steady-state errors while avoiding integral windup.

---

### Summary and Conclusion

The longitudinal control of the vehicle is managed using a **PID controller**, which adjusts the throttle and brake commands to track a desired target speed. The control law is based on minimizing the speed error using proportional, integral, and derivative components, each contributing to the overall system performance in different ways:

- **Proportional control** adjusts the response based on the current error.
- **Integral control** eliminates steady-state errors but can lead to integral windup if not managed properly.
- **Derivative control** predicts error trends to reduce overshoot and stabilize the system.

From a control engineering perspective, tuning the PID controller parameters \( K_p \), \( K_d \), and \( K_i \) is crucial for achieving the desired balance between responsiveness and stability. Through empirical testing and observation, an optimal set of parameters can be found to ensure that the vehicle accelerates and decelerates smoothly and tracks the desired speed effectively. Anti-windup techniques must be employed to avoid excessive integral action, which can destabilize the system.

Overall, the PID-based longitudinal control system forms a robust framework for maintaining a desired vehicle speed in a variety of driving conditions.
