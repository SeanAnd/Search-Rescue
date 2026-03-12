import cv2
from process import process_infrared_image
from steps import step_clean_artifacts, step_fsr_upscale, step_invert_brightness_weight, step_normalize, step_threshold_brightness


if __name__ == "__main__":
    # Provide the path to your infrared image
    image_path = "./images/lake.jpg"

    # Define the custom steps
    custom_steps = [
        # upscale the image using FSR (this is kludgey but it works)
        step_fsr_upscale,
        # normalize the image to 0-255 (makes it a bit easier to calculate the threshold and brightness)
        step_normalize,
        # make the bright subjects brighter and the dark background darker to separate them.
        # Basically, since we don't have distance data for the inverse square law 
        # we need to use a threshold to separate the subjects from the background.
        # (optional as this kinda whitewashes the image but helps the invert step if done right)
        step_threshold_brightness,
        # suppress bright pixels and amplify dim ones. This is a simple way to separate the subjects from the background.
        step_invert_brightness_weight,
        # clean the image from artifacts like random noise and small objects
        step_clean_artifacts, 
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
