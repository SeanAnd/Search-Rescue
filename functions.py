import cv2
import numpy as np

# Utility Functions
def normalize_image(image):
    """Normalizes an infrared image to the range 0-255 for display."""
    normalized = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    rescaled = (normalized * 255).astype(np.uint8)
    return rescaled

def invert_brightness_weight(image, intensity_threshold=10, smoothing_factor=1):
    """Suppress bright pixels and amplify dim ones via compressive weighting."""
    image = image.astype(np.float32)
    filtered_image = np.where(
        image > intensity_threshold,
        image / ((image + smoothing_factor)**2),
        0
    )
    filtered_image = cv2.normalize(filtered_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return filtered_image

def clean_artifacts(image, min_area=50, fill_holes=True):
    """
    Remove noise artifacts and fill gaps using connected component analysis.

    Unlike morphological filtering, this preserves original pixel values in the
    subject by operating on a binary mask rather than the grayscale data directly.

    Parameters:
    - min_area: components smaller than this (in pixels) are treated as noise
    - fill_holes: if True, fills interior holes in the largest components
    """
    _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)

    mask = np.zeros_like(binary)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            mask[labels == i] = 255

    if fill_holes:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(mask, contours, -1, 255, thickness=cv2.FILLED)

    result = cv2.bitwise_and(image, mask)
    return result

def threshold_brightness(image, threshold=155, dim_factor=0.5, boost_factor=1.25):
    """
    Separate bright subjects from dark background by pushing them apart.

    Pixels below the threshold are dimmed, pixels above are boosted.
    The result is normalized back to 0-255.

    Parameters:
    - threshold: intensity cutoff (0-255)
    - dim_factor: multiplier for pixels below threshold (< 1.0 darkens)
    - boost_factor: multiplier for pixels above threshold (> 1.0 brightens)
    """
    img = image.astype(np.float32)
    result = np.where(img < threshold, img * dim_factor, img * boost_factor)
    return np.clip(result, 0, 255).astype(np.uint8)

def fsr_upscale(image, scale=1, sharpness=0.8, noise_sensitivity=40.0):
    """
    FSR 1.0-inspired spatial upscaling with contrast-adaptive sharpening.

    EASU pass: Lanczos interpolation preserves edges better than bilinear/bicubic.
    RCAS pass: sharpens detail while suppressing amplification in noisy/flat regions
    by weighting the unsharp mask inversely with local standard deviation.

    Parameters:
    - scale: upscale factor (e.g. 2 = double resolution)
    - sharpness: strength of the RCAS sharpening pass (0.0-2.0)
    - noise_sensitivity: higher values reduce sharpening in noisy regions
    """
    upscaled = cv2.resize(image, None, fx=scale, fy=scale,
                          interpolation=cv2.INTER_LANCZOS4)

    img_min, img_max = int(upscaled.min()), int(upscaled.max())
    if img_min == img_max:
        return upscaled
    if img_max - img_min < 128:
        upscaled = cv2.normalize(upscaled, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    upscaled_f = upscaled.astype(np.float32)
    lowpass = cv2.GaussianBlur(upscaled_f, (3, 3), 0)
    detail = upscaled_f - lowpass

    local_variance = cv2.GaussianBlur(detail ** 2, (7, 7), 0)
    local_std = np.sqrt(np.maximum(local_variance, 0))
    weight = sharpness / (1.0 + local_std / noise_sensitivity)

    sharpened = np.clip(upscaled_f + detail * weight, 0, 255)
    return sharpened.astype(np.uint8)
