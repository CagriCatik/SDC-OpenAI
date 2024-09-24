# Lane Detection Pipeline

The lane detection pipeline aims to identify the lane boundaries in the given state image, assign edges to these boundaries, and fit splines to model the lane boundaries' curvature. The process is divided into three key steps: edge detection, edge assignment to lane boundaries, and spline fitting. A testing phase follows the implementation to ensure proper functionality. Below is a detailed explanation of each step, including suggestions and hints for implementation.

You will find the class template in `lane_detection.py` and use `test_lane_detection.py` for testing and validation.

---

## **a) Edge Detection:**

The first task is to detect edges in the grayscale image, which serve as potential lane boundary candidates.

1. **Grayscale Conversion and Cropping:**
   - **Goal**: Convert the input state image (which is likely in RGB) to a grayscale image, focusing only on the part of the image that is relevant for lane detection.
   - **Implementation**: Implement the function `LaneDetection.cut_gray()`.
     - This function should:
       1. Convert the input image into a grayscale format using appropriate libraries (e.g., OpenCV’s `cv2.cvtColor()` or `PIL.Image.convert()`).
       2. Crop out the portion of the image that is above the car’s perspective, as this area typically contains irrelevant background information (sky, trees, etc.). You may want to experiment with the crop height to find the most effective area to focus on.
   - **Why**: This will reduce the noise in the data and enhance computational efficiency.

2. **Gradient Calculation**:
   - **Goal**: Identify areas in the image where there is a significant change in intensity (edges), which likely correspond to lane markings.
   - **Implementation**: In `LaneDetection.edge_detection()`, compute the gradient of the grayscale image.
     - Use gradient operators such as Sobel, Prewitt, or Scharr to calculate the intensity change along both horizontal and vertical axes.
     - **Thresholding**: To reduce noise and only focus on prominent edges, set a threshold that eliminates small gradients (e.g., gradients below a certain magnitude should be set to zero). You can experiment with different threshold values to achieve optimal results.
   - **Why**: This step isolates potential lane boundaries, which are characterized by abrupt changes in pixel intensity.

3. **Maxima Detection (Peak Finding)**:
   - **Goal**: Identify the most prominent edges (maxima) in each row of the image, as these are likely to correspond to lane markings.
   - **Implementation**: Write a function that detects the maxima in the thresholded gradient for each row of pixels.
     - Use `scipy.signal.find_peaks()` or a similar method to locate the highest gradient values within each row. Peaks represent strong changes in intensity, which are indicators of lane boundaries.
     - Ensure the peaks correspond to actual lane edges and not noise or irrelevant features (e.g., experiment with the peak height and prominence parameters to fine-tune the detection).
   - **Why**: This step helps pinpoint the exact location of lane boundaries in the image.

---

## **b) Assigning Edges to Lane Boundaries:**

Once the edges have been detected, the next step is to assign these detected maxima to the correct lane boundaries (left and right lanes).

1. **Initial Edge Detection Near the Car**:
   - **Goal**: Begin by identifying the lane boundaries near the car, as this is typically the most reliable and visible area.
   - **Implementation**: Use `LaneDetection.find_maxima_gradient_rowwise()` to detect the first set of maxima (edges) in the row of pixels closest to the car.
     - This row provides the best visibility and is often least distorted by perspective effects, making it a good starting point for lane detection.
   - **Why**: Reliable detection in this region provides a strong foundation for tracking the lane as it extends further away from the vehicle.

2. **Edge Assignment Using Nearest Neighbor Search**:
   - **Goal**: Assign the detected maxima in other rows to either the left or right lane boundary.
   - **Implementation**: Use a nearest-neighbor approach to search for edges along each lane boundary.
     - Starting from the detected initial maxima, search row-by-row, finding the nearest edge in each subsequent row. Continue this process until all edges in the image have been assigned to one of the lane boundaries.
     - The nearest-neighbor search can be implemented using basic distance calculations or more advanced algorithms if needed.
     - In `LaneDetection.lane_detection()`, complete the missing sections of code to handle this edge assignment process. Feel free to improve upon the suggested approach for greater accuracy or efficiency.
   - **Why**: This step ensures that all detected edges are correctly classified as belonging to either the left or right lane boundary, even as the lane curves or moves away from the car.

---

## **c) Spline Fitting:**

Once the edges have been assigned to lane boundaries, the final step is to model these boundaries using parametric splines.

1. **Goal**: Fit smooth splines to the detected lane boundaries to model their curvature accurately.
   - **Implementation**: In `LaneDetection.lane_detection()`, implement the spline fitting for each lane boundary.
     - Parametric splines allow you to create a smooth curve that can be sampled at various points, making them ideal for modeling the continuous nature of lane boundaries.
     - Use a parametric spline that takes a single parameter representing the length of the curve and outputs the corresponding points on the lane boundary.
     - The method documented in [1] can guide the implementation. Experiment with different spline parameters (e.g., smoothness, tension) to find the best fit for your detected lane boundaries.
   - **Why**: A spline-based representation of the lane boundaries is critical for applications such as vehicle path planning, where the car must follow a smooth trajectory between the lanes.

---

## **d) Testing and Validation:**

After completing the edge detection, edge assignment, and spline fitting, it’s essential to test your implementation thoroughly.

1. **Test Execution**:
   - **Goal**: Validate the accuracy and robustness of the lane detection pipeline by running `test_lane_detection.py`.
   - **Implementation**:
     - Use the arrow keys to drive the vehicle and observe how well the lane boundaries are detected and modeled in the additional window.
     - Check for edge cases and failure scenarios. For example, how well does the algorithm handle sharp curves, varying lighting conditions, or other vehicles on the road?

2. **Refinement Suggestions**:
   - Experiment with different parameters for:
     - **Cropping**: Find the optimal area of the image to focus on. A good crop minimizes distractions and focuses on the lanes.
     - **Gradient Threshold**: Tune the gradient threshold to avoid missing subtle but important lane markings while filtering out noise.
     - **Spline Smoothness**: Adjust the smoothness of the spline to balance accuracy and stability in lane boundary modeling.
