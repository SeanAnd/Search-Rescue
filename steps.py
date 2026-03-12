

# Step Functions
from functions import clean_artifacts, fsr_upscale, invert_brightness_weight, normalize_image, threshold_brightness


def step_normalize(image):
    """Normalize the image to 0-255."""
    return normalize_image(image)


def step_invert_brightness_weight(image, intensity_threshold=155, smoothing_factor=1):
    """Suppress bright pixels and amplify dim ones via compressive weighting."""
    return invert_brightness_weight(image, intensity_threshold=intensity_threshold, smoothing_factor=smoothing_factor)

def step_clean_artifacts(image, min_area=50, fill_holes=True):
    """Remove noise dots and fill gaps in subject silhouettes."""
    return clean_artifacts(image, min_area=min_area, fill_holes=fill_holes)

def step_threshold_brightness(image, threshold=128, dim_factor=0.5, boost_factor=1.5):
    """Dim pixels below threshold and boost pixels above it."""
    return threshold_brightness(image, threshold=threshold, dim_factor=dim_factor, boost_factor=boost_factor)

def step_fsr_upscale(image, scale=2, sharpness=0.8, noise_sensitivity=25.0):
    """Upscale and sharpen using FSR 1.0-inspired spatial upscaling."""
    return fsr_upscale(image, scale=scale, sharpness=sharpness, noise_sensitivity=noise_sensitivity)
