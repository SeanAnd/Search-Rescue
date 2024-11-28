import cv2

def process_infrared_image(image_path, processing_steps, background_image=None):
    """
    Processes an infrared image using a custom sequence of steps.
    
    Parameters:
    - image_path (str): Path to the infrared image.
    - processing_steps (list): A list of functions to apply sequentially to the image.
    - background_image (numpy.ndarray, optional): Optional background image for subtraction.

    Returns:
    - numpy.ndarray: Processed image after applying all steps.
    """
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image at {image_path} could not be loaded.")

    # Apply each step sequentially
    for step in processing_steps:
        if callable(step):
            image = step(image)
        else:
            raise ValueError(f"Step {step} is not callable.")
    
    return image
