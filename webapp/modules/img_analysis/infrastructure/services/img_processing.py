import os

import cv2
import numpy as np
from cv2.typing import MatLike, Scalar
from loguru import logger

from webapp.modules.img_analysis.domain.schemas.img_analysis import (
    ImageAnalysisUpdateSchema,
)
from webapp.common.constants import INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH


def load_image_data(
    file_id: str, input_folder_path: str = INPUT_FOLDER_PATH
) -> MatLike | None:
    """Load image file into a matrix."""

    input_file_path = f"{input_folder_path}/images/{file_id}.png"
    logger.info(f"Loading image frm '{input_file_path}'...")

    if not os.path.exists(input_file_path):
        return None

    return cv2.imread(input_file_path)


def build_output_img_file(
    file_id: str,
    object_label: str,
    analysis_type: str,
    output_folder_path: str = OUTPUT_FOLDER_PATH,
) -> str:
    """Automates output image folder and file path creation."""

    output_folder_path = f"{output_folder_path}/{analysis_type}"
    os.makedirs(output_folder_path, exist_ok=True)

    return f"{output_folder_path}/{analysis_type}_{object_label}_{file_id}.png"


def draw_bounding_boxes(
    file_id: str,
    image_data: MatLike,
    tracking_messages: list[ImageAnalysisUpdateSchema],
    color_map: Scalar = (0, 255, 0),
):
    """Draw bounding boxes on an image, given its geometric parameters from the tracking messages."""

    if not image_data.shape:
        logger.warning("Empty image file. Nothing to be done.")
        return

    for msg in tracking_messages:
        img_height, img_width, _ = image_data.shape
        thickness = int((img_height + img_width) // 900)

        lower_point = (int(msg.x_min_bb), int(msg.y_min_bb))
        upper_point = (int(msg.x_max_bb), int(msg.y_max_bb))

        cv2.rectangle(image_data, lower_point, upper_point, color_map, thickness)

        label = f"{msg.object_label}@{msg.region_label}"
        label_coords = (int(msg.x_min_bb), int(msg.y_min_bb) - 12)

        cv2.putText(
            image_data,
            label,
            label_coords,
            0,
            1e-3 * img_height,
            color_map,
            thickness // 3,
        )

        cv2.circle(
            image_data,
            (int(msg.x_centroid_bb), int(msg.y_centroid_bb)),
            radius=1,
            color=(0, 0, 255),
            thickness=2,
        )

    output_file_path = build_output_img_file(
        file_id,
        tracking_messages[0].object_label,
        tracking_messages[0].analysis_type.value,
    )

    logger.warning(f"Drawing bounding boxes on file '{output_file_path}'...")

    cv2.imwrite(output_file_path, image_data)


def generate_img_heat_map(
    file_id: str,
    image_data: MatLike,
    tracking_messages: list[ImageAnalysisUpdateSchema],
):
    """Apply heat map on incoming image data, given the bounding boxes positions."""

    img_height, img_width, _ = image_data.shape
    heatmap_image = np.zeros((img_height, img_width, 1), np.uint8)

    for msg in tracking_messages:
        x = int(msg.x_centroid_bb)
        y = int(msg.y_centroid_bb)

        if 0 < x < img_width and 0 < y < img_height:
            cv2.circle(heatmap_image, (x, y), 100, 255, -1)

    # Apply distance transform
    heatmap_image = cv2.distanceTransform(heatmap_image, cv2.DIST_L2, 5)

    # Normalize and apply colormap
    heatmap_image = cv2.normalize(
        heatmap_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
    )
    heatmap_image = cv2.applyColorMap(heatmap_image, cv2.COLORMAP_JET)

    # Overlay the heatmap
    overlayed_image = cv2.addWeighted(image_data, 0.7, heatmap_image, 0.3, 0)

    output_file_path = build_output_img_file(
        file_id,
        tracking_messages[0].object_label,
        tracking_messages[0].analysis_type.value,
    )

    logger.warning(f"Generating heat map on file '{output_file_path}'...")

    cv2.imwrite(output_file_path, overlayed_image)
