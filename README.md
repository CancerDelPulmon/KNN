# KNN
l'interpreteur a choisir est dans le repository github, select : .venv/bin/python (je crois)
comme lien vers l'interpreteur

pour verifier l'installation des differents modules : pip list

Research :
1. Normalized Area (Invariance to Scaling)
- Description: The area of the black shape (number of pixels) normalized by the total area of the image. This feature is useful because it remains constant under transformations like translation and reflection, and it scales proportionally under scaling.

- Why it's useful: It can help identify shapes with similar coverage area, regardless of their position or scale.

- Formula:
Normalized Area = Number of black pixels in the shape / Total number of pixels in the image

- implementation: Count the number of black pixels (0s) in the image array and divide by the total number of pixels.


2. Aspect Ratio (Width-to-Height Ratio)
- Description: Measures the ratio of the width to the height of the bounding box around the object in the image. This feature is invariant to translation but changes under scaling and reflection, providing insight into the shape's proportions.

- Why it's useful: It helps differentiate between shapes that are elongated in one direction versus more compact shapes (e.g., a tall rectangle vs. a square).

- Formula:
Aspect Ratio = Width of Bounding Box / Height of Bounding Box

- Implementation: Compute the bounding box dimensions based on the non-zero (black) pixels in the image.

3. Hu Moments (Invariant to Scaling, Translation, and Rotation)
- Description: Hu Moments are a set of 7 mathematical features that describe the shape of an object and are invariant to translation, scaling, and rotation. They capture information about the spatial distribution of the pixels in a shape.

- Why it's useful: Hu Moments are specifically designed to be invariant to transformations like translation, scaling, and rotation, making them ideal for your case where the objects undergo these transformations.

- Formula: The first Hu moment is given by:

Hu1 = η20 + η02
where ηij are normalized central moments of the image.

- Implementation: Use cv2.HuMoments() if OpenCV is available or calculate them using NumPy for a manual implementation.

Why These Features?
- Normalized Area: Robust to scaling, invariant to translation, useful to capture size and coverage.

- Aspect Ratio: Simple, invariant to translation, captures proportional information of the shape.

- Hu Moments: Invariant to translation, scaling, and rotation, making them ideal for handling geometric transformations.

Next Steps
- Extract Features for All Images: Implement these feature extractions on all your images and store the results as a feature matrix.

- Input Features to KNN: Use the extracted features as input to the KNN algorithm for classification.

- Visualize in 3D: Use the three features as x, y, and z coordinates for a 3D scatter plot to visualize your data.
