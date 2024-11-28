import cv2
from process import process_infrared_image
from steps import step_contrast_enhancement, step_inverse_square_brightness, step_normalize, step_polarization_filter, step_spectral_filter, step_subtract_background


if __name__ == "__main__":
    # Provide the path to your infrared image
    image_path = "./images/field.jpg"

    # Define the custom steps
    custom_steps = [
        step_normalize,
        # step_subtract_background,
        # step_spectral_filter,
        # step_polarization_filter,
        # step_contrast_enhancement,
        step_inverse_square_brightness
    ]
    
    try:
        # Process the image with the custom steps
        processed_image = process_infrared_image(image_path, processing_steps=custom_steps)
        
        # Display the final processed image
        cv2.imshow('Processed Infrared Image', processed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Invalid step configuration: {e}")
