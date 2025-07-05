from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from starlette import status

from src.application.container import Container
from src.modules.imganalysis.usecase import router
from src.modules.imganalysis.usecase.new_heat_map.impl import NewImageHeatMapUseCase

from .impl import NewImageHeatMapCommand


@router.post("/heatmap", name="Heat Map Generation", status_code=status.HTTP_201_CREATED)
@inject
async def new_heat_map(command: NewImageHeatMapCommand, uc: NewImageHeatMapUseCase = Depends(Provide[Container.new_img_heat_map_use_case])):
    """Create a new record of an image heat map in the DB."""
    img_analysis = await uc.invoke(command)

    return img_analysis.id
