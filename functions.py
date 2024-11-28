import cv2
import numpy as np

# Utility Functions
def normalize_image(image):
    """Normalizes an infrared image to the range 0-255 for display."""
    normalized = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    rescaled = (normalized * 255).astype(np.uint8)
    return rescaled

def enhance_contrast(image, method="histogram", clip_limit=2.0, tile_grid_size=(8, 8)):
    """Enhances the contrast of the image using the specified method."""
    if method == "histogram":
        return cv2.equalizeHist(image)
    elif method == "clahe":
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        return clahe.apply(image)
    else:
        raise ValueError(f"Invalid method '{method}'. Choose 'histogram' or 'clahe'.")

def subtract_background(image, background_image=None, width=15, height=15):
    """Subtract the background using a Gaussian blur or a reference image."""
    if background_image is not None:
        return np.clip(image - background_image, 0, None)
    else:
        smoothed_background = cv2.GaussianBlur(image, (width, height), 0)
        return np.clip(image - smoothed_background, 0, None)

def spectral_filter(image, lower_percentile=5, upper_percentile=95):
    """Filters the image to keep only a specific range of intensities."""
    lower_bound = np.percentile(image, lower_percentile)
    upper_bound = np.percentile(image, upper_percentile)
    filtered_image = np.where((image >= lower_bound) & (image <= upper_bound), image, 0)
    normalized = cv2.normalize(filtered_image, None, 0, 255, cv2.NORM_MINMAX)
    return 255 - normalized

def polarization_filter(image, percentile=95, blur_ksize=(5, 5)):
    """Suppress glare dynamically based on intensity percentiles."""
    threshold = np.percentile(image, percentile)
    suppressed = np.where(image > threshold, threshold, image)
    blurred = cv2.GaussianBlur(suppressed.astype(np.float32), blur_ksize, 0)
    return blurred.astype(np.uint8)

def inverse_square_brightness(image, intensity_threshold=10, smoothing_factor=1):
    """Apply the inverse square law to pixel brightness."""
    image = image.astype(np.float32)
    filtered_image = np.where(
        image > intensity_threshold,
        image / ((image + smoothing_factor)**2),
        0
    )
    filtered_image = cv2.normalize(filtered_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return filtered_image
