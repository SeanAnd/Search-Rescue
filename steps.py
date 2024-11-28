

# Step Functions
from functions import enhance_contrast, inverse_square_brightness, normalize_image, polarization_filter, spectral_filter, subtract_background


def step_normalize(image):
    """Normalize the image to 0-255."""
    return normalize_image(image)

def step_subtract_background(image, background_image=None, width=21, height=21):
    """Subtract the background using a Gaussian blur or a reference image."""
    return subtract_background(image, background_image, width, height)

def step_spectral_filter(image, lower_percentile=5, upper_percentile=95):
    """Apply a spectral filter to isolate intensity ranges."""
    return spectral_filter(image, lower_percentile=lower_percentile, upper_percentile=upper_percentile)

def step_polarization_filter(image, blur_ksize=(5, 5), percentile=95):
    """Suppress glare using a polarization filter."""
    return polarization_filter(image, blur_ksize=blur_ksize, percentile=percentile)

def step_contrast_enhancement(image, method="clahe", clip_limit=2.0, tile_grid_size=(8, 8)):
    """Enhance contrast using histogram equalization or CLAHE."""
    return enhance_contrast(image, method=method, clip_limit=clip_limit, tile_grid_size=tile_grid_size)

def step_inverse_square_brightness(image, intensity_threshold=155, smoothing_factor=1):
    """Apply the inverse square law to suppress dark pixels."""
    return inverse_square_brightness(image, intensity_threshold=intensity_threshold, smoothing_factor=smoothing_factor)
