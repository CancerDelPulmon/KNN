This document describes a project to build a KNN image classifier application in Python.  Here's a breakdown of the key elements to help you prioritize your work over the next two days:

**1. Core Functionality:**

* **KNN Algorithm Implementation:** This is the heart of the project. Make sure you understand the five steps of the KNN algorithm and implement it generically.
* **Metric Selection and Calculation:**  This is arguably the most crucial and challenging part. You *must* choose *three* metrics to represent the images in 3D space.  Focus on metrics that are:
    * Simple to calculate.
    * Disperse data points well for different classes.
    * Independent of each other.
    * Ideally, invariant to translation, rotation, and scaling.
    * Ideally, normalized to a known range.  Think about things like area, perimeter, compactness, aspect ratio, number of corners (if you can detect them efficiently).  Do *not* use all the pixels.
* **Data Loading and Access:**  Ensure you can connect to the PostgreSQL database and retrieve the image data using the provided functions.  Familiarize yourself with the database structure.
* **Classification Process:** Implement the logic to load a test image, calculate its metrics, apply the KNN algorithm, and display the classification result.

**2. User Interface:**

* **Essential UI Elements:** Prioritize the mandatory UI elements: 3D scatter plot, data set selection, image selection, classification button, K parameter input, and the "About" dialog.  A well-designed UI can save you debugging time later.
* **Data Viewer Widget (Provided):**  Use the `KlustRDataSourceViewWidget`!  It's already built and will help you immensely in understanding the data and for testing.

**3. Optimization and Refinement:**

* **Dimensionality Reduction:** This is taken care of by the requirement to use only three metrics.
* **Performance:** Aim for reasonable performance. Consider data structures and algorithms that won't slow down the classification process too much.
* **Complex Datasets:** Start with the simpler datasets (ABC, Mouse, Squirrel) to test your implementation.  Move on to the more complex ones only if you have time.

**4. Report and "About" Dialog:**

* **Follow the Template:**  Use the provided text for the "About" dialog and report, filling in the placeholders.  Don't underestimate this; it's an easy way to gain points.

**Key Considerations for Time Management:**

* **Focus on the Core:** Get the KNN implementation and metric calculation working first.  A basic UI is more important than a polished one.
* **Modular Design:** Break down the project into smaller, manageable tasks.  This will help you track your progress and make debugging easier.
* **Test Early and Often:**  Test your code frequently to identify and fix bugs early on.
* **Consult the Provided Code:** The `klustr_utils` and the data viewer widget are there to help you!  Use them.

If you're working in a team, divide the tasks effectively based on individual strengths.  Good communication is essential.

Good luck with your project! Let me know if you have more specific questions as you work through it.
