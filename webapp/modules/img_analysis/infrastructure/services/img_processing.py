import os
from datetime import datetime

from cv2 import (
    rectangle as draw_rectangle,
    putText as put_text,
    imread as read_img_file,
    imwrite as write_img_file,
)
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

    return read_img_file(input_file_path)


def _build_output_img_file(
    file_id: str, tracking_message: ImageAnalysisUpdateSchema, output_folder_path: str
) -> str:
    object_label = tracking_message.object_label
    analysis_type = tracking_message.analysis_type.value
    current_dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder_path = f"{output_folder_path}/{analysis_type}"

    os.makedirs(output_folder_path, exist_ok=True)

    return f"{output_folder_path}/{file_id}_bb_{object_label}_{current_dt}.png"


def draw_bounding_boxes(
    file_id: str,
    image_data: MatLike,
    tracking_messages: list[ImageAnalysisUpdateSchema],
    color_map: Scalar = (0, 255, 0),
    output_folder_path: str = OUTPUT_FOLDER_PATH,
):
    """Draw bounding boxes on an image.

    file_id: the ID that identifies the image file in Google Drive.
    image_data: image data in numpy array format
    tracking_messages: list of parsed tracking messages from JSON, filtered by object
    color_map: Bounding box color candidates, list of RGB tuples.
    outpur_folder_path: output image folder path
    """

    if not image_data.shape:
        logger.warning("Empty image file. Nothing to be done.")
        return

    for msg in tracking_messages:
        img_height, img_width, _ = image_data.shape
        thickness = int((img_height + img_width) // 900)

        lower_point = (int(msg.x_min_bb), int(msg.y_min_bb))
        upper_point = (int(msg.x_max_bb), int(msg.y_max_bb))

        draw_rectangle(image_data, lower_point, upper_point, color_map, thickness)

        label = f"{msg.object_label}@{msg.region_label}"
        label_coords = (int(msg.x_min_bb), int(msg.y_min_bb) - 12)

        put_text(
            image_data,
            label,
            label_coords,
            0,
            1e-3 * img_height,
            color_map,
            thickness // 3,
        )

    output_file_path = _build_output_img_file(
        file_id, tracking_messages[0], output_folder_path
    )

    logger.warning(f"Writing bounding boxed to file {output_file_path}...")

    write_img_file(output_file_path, image_data)
