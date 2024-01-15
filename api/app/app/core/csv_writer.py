import csv
from typing import Any
from aiocsv import AsyncDictWriter
from aiofiles.threadpool.text import AsyncTextIOWrapper
from app.schemas.scheme_vacancy import VacancyOut


async def get_vacancy_csv(
    vac: list[dict[str, Any]],
    file: AsyncTextIOWrapper
        ) -> AsyncTextIOWrapper:
    """Get csv file

    Args:
        vac (list[dict[str, Any]]): data to write
        file (AsyncTextIOWrapper): temporal csv file

    Returns:
       (AsyncTextIOWrapper) csv temporal file
    """
    writer = AsyncDictWriter(
        file,
        VacancyOut.model_fields.keys(),
        restval="NULL",
        quoting=csv.QUOTE_ALL
            )
    await writer.writeheader()
    await writer.writerows(vac)
    await file.seek(0)
    return file
