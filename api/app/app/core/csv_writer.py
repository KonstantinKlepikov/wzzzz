import csv
from typing import Any
from aiocsv import AsyncDictWriter
from aiofiles.threadpool.text import AsyncTextIOWrapper
from app.schemas import Vacancy


async def get_vacancy_csv(
    data: list[dict[str, Any]],
    file: AsyncTextIOWrapper
        ) -> AsyncTextIOWrapper:
    """Get csv file

    Args:
        data (Vacancies_): data to write
        file (AsyncTextIOWrapper): temporal csv file

    Returns:
       (AsyncTextIOWrapper) csv temporal file
    """
    writer = AsyncDictWriter(
        file,
        Vacancy.__fields__.keys(),
        restval="NULL",
        quoting=csv.QUOTE_ALL
            )
    await writer.writeheader()
    await writer.writerows(data)
    await file.seek(0)
    return file
