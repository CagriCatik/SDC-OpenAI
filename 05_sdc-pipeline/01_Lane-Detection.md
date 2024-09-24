# Lane Detection Pipeline

The goal of the lane detection pipeline is to identify and model lane boundaries within a given state image. The process is divided into three main steps: edge detection, edge assignment, and spline fitting. Each step contributes to detecting lane boundaries, assigning detected edges to lanes, and fitting splines to model lane curvature. Finally, testing is conducted to validate the pipeline's functionality.

You can find the class template in `lane_detection.py` and use `test_lane_detection.py` for testing and validation.

## **1. Edge Detection**

Edge detection is the first step, aiming to identify potential lane boundary candidates in the image.

### a. Grayscale Conversion and Cropping

- **Objective**: Convert the input image (likely in RGB) to grayscale and focus on the relevant region for lane detection.
- **Implementation**:
  - In the function `LaneDetection.cut_gray()`, implement the following:
    1. Convert the RGB image to grayscale (e.g., using OpenCV’s `cv2.cvtColor()` or `PIL.Image.convert()`).
    2. Crop the image to remove unnecessary portions, such as the sky or distant objects, by adjusting the crop height.
- **Rationale**: Reducing irrelevant information will improve computational efficiency and enhance detection accuracy.

### b. Gradient Calculation

- **Objective**: Detect significant intensity changes (edges) in the image, typically corresponding to lane markings.
- **Implementation**:
  - In `LaneDetection.edge_detection()`, compute the image gradient using Sobel, Prewitt, or Scharr operators to detect edges along both horizontal and vertical axes.
  - Apply thresholding to filter out minor changes and focus only on prominent edges by setting small gradients to zero.
- **Rationale**: This step highlights potential lane boundaries characterized by abrupt intensity changes.

### c. Maxima Detection (Peak Finding)

- **Objective**: Identify the most prominent edges (maxima) in each row of pixels to locate lane markings.
- **Implementation**:
  - Use a peak-finding algorithm (e.g., `scipy.signal.find_peaks()`) to detect the highest intensity changes within each row of the image.
  - Tune peak detection parameters (such as height and prominence) to ensure the algorithm accurately identifies lane markings while ignoring noise.
- **Rationale**: This step isolates the exact pixel locations corresponding to lane boundaries.

## **2. Assigning Edges to Lane Boundaries**

After detecting edges, the next step is to assign these edges to their respective lane boundaries (left and right).

### a. Initial Edge Detection Near the Car

- **Objective**: Identify lane boundaries close to the car, where they are most visible and reliable.
- **Implementation**:
  - Use `LaneDetection.find_maxima_gradient_rowwise()` to detect edges in the row closest to the car, which typically has the least distortion and provides a reliable starting point.
- **Rationale**: Accurately identifying lane boundaries near the car is crucial for tracking them as they extend further into the image.

### b. Edge Assignment Using Nearest Neighbor Search

- **Objective**: Assign detected edges to the correct lane boundary using a nearest-neighbor search approach.
- **Implementation**:
  - Start from the initial detected maxima and, row by row, assign edges to either the left or right lane based on their proximity.
  - Implement the nearest-neighbor search using basic distance calculations or a more advanced algorithm, as needed.
  - Complete the missing sections of code in `LaneDetection.lane_detection()` to handle this edge assignment process.
- **Rationale**: Correctly classifying edges ensures that the detected lane boundaries can be consistently tracked across the image, even when the lane curves or moves further away.

## **3. Spline Fitting**

Once edges are assigned to lane boundaries, splines are fitted to model the curvature of the lanes.

### a. Spline Fitting to Lane Boundaries

- **Objective**: Fit smooth parametric splines to the detected lane boundaries.
- **Implementation**:
  - In `LaneDetection.lane_detection()`, fit a parametric spline to each lane boundary using a method like the one outlined in [1].
  - The spline should smoothly represent the lane boundary's curvature, ensuring continuity.
  - Experiment with spline parameters (such as smoothness and tension) to achieve the most accurate fit.
- **Rationale**: Fitting a spline provides a continuous, smooth representation of the lane boundary, essential for tasks like path planning and vehicle control.

## **4. Testing and Validation**

After implementing the core steps of the pipeline, thorough testing ensures that the system functions correctly.

### a. Test Execution

- **Objective**: Validate the accuracy and robustness of the lane detection pipeline.
- **Implementation**:
  - Run `test_lane_detection.py` and use the arrow keys to drive the vehicle while observing the lane detection results in real-time.
  - Test under various conditions, such as sharp curves, different lighting environments, and potential obstructions (e.g., other vehicles).
- **Rationale**: Real-world testing highlights areas for improvement and ensures the lane detection system is reliable in diverse scenarios.

### b. Refinement Suggestions

- **Cropping**: Experiment with different crop heights to focus on the most relevant part of the image.
- **Gradient Threshold**: Fine-tune the threshold values to balance edge detection sensitivity and noise reduction.
- **Spline Smoothness**: Adjust the spline parameters to improve the balance between model accuracy and stability when modeling the lane boundaries.

By following these steps, you will develop a robust lane detection system capable of detecting and modeling lane boundaries accurately. Ensure to iterate and test your implementation thoroughly to handle various real-world conditions effectively.
