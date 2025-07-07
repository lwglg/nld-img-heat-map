import os
import json
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from multiprocessing import cpu_count
from typing import Any

from loguru import logger

from webapp.modules.img_analysis.domain.attributes import ImageAnalysisType
from webapp.modules.img_analysis.domain.schemas.img_analysis import (
    ImageAnalysisUpdateSchema,
)
from webapp.common.constants import INPUT_FOLDER_PATH
from webapp.common.utils.parsing import is_empty_no_side_effects


def load_json_from_file(
    file_id: str, input_folder_path: str = INPUT_FOLDER_PATH
) -> dict[str, Any] | None:
    """Load JSON data given a valid file ID."""

    json_path = f"{input_folder_path}/elasticsearch/{file_id}.json"

    if not os.path.exists(json_path):
        return None

    logger.info(f"Loading data from JSON '{json_path}'...")

    with open(json_path) as json_file:
        data = json.load(json_file)

        return data


def extract_values(json_object: dict[str, Any], target_key: str):
    """Filter recursively a JSON by a given key."""

    if isinstance(json_object, dict):
        for key, value in json_object.items():
            if key == target_key:
                yield value

            yield from extract_values(value, target_key)
    elif isinstance(json_object, list):
        for item in json_object:
            yield from extract_values(item, target_key)


def extract_tracking_data(
    json_data: dict[str, Any], tracking_data_obj_key: str = "deepstream-msg"
) -> list[str] | None:
    """Extract the flattened list of tracking message data from the loaded JSON."""

    logger.info(f"Filtering JSON data by key '{tracking_data_obj_key}'...")

    filtered = extract_values(json_data, tracking_data_obj_key)

    if not is_empty_no_side_effects(filtered)[1]:
        raw_tracking_data = list(filtered)

        return [item for sublist in raw_tracking_data for item in sublist]


def _filtering_task(tracking_msg: str, object_label: str) -> bool:
    """Check if given object label is substring from message."""

    return object_label.strip().lower() in tracking_msg


def parse_tracking_msg_to_model(
    tracking_msg: str,
    analysis_type: ImageAnalysisType,
    img_file_id: str,
    separator: str = "|",
) -> ImageAnalysisUpdateSchema:
    """Split the tracking message and parses it into a model object."""

    tracking_id, x_min, x_max, y_min, y_max, object_label, region_label = (
        tracking_msg.split(separator)
    )

    tracking_id = int(tracking_id)
    x_min, x_max = float(x_min), float(x_max)
    y_min, y_max = float(y_min), float(y_max)

    x_centroid = (x_max + x_min) / 2.0
    y_centroid = (y_max + y_min) / 2.0

    return ImageAnalysisUpdateSchema(
        tracking_id=tracking_id,
        x_min_bb=x_min,
        y_min_bb=y_min,
        x_max_bb=x_max,
        y_max_bb=y_max,
        x_centroid_bb=x_centroid,
        y_centroid_bb=y_centroid,
        object_label=object_label.strip().lower(),
        region_label=region_label.strip(),
        analysis_type=analysis_type,
        image_path=f"{INPUT_FOLDER_PATH}/images/{img_file_id}.png",
    )


def filter_tracking_data_by_object(
    tracking_data: list[str],
    object_label: str,
    analysis_type: ImageAnalysisType,
    img_file_id: str,
) -> list[ImageAnalysisUpdateSchema] | None:
    """Filter all tracking messages by an object label."""

    if len(tracking_data) == 0:
        return tracking_data

    apply_task_with_object_label = partial(_filtering_task, object_label=object_label)

    with ProcessPoolExecutor(max_workers=cpu_count()) as ppe:
        object_tracking_data = [
            parse_tracking_msg_to_model(tmsg, analysis_type.value, img_file_id)
            for tmsg, is_from_object in zip(
                tracking_data, ppe.map(apply_task_with_object_label, tracking_data)
            )
            if is_from_object
        ]

    return object_tracking_data
