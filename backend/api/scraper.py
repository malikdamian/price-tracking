import subprocess

from fastapi import APIRouter, HTTPException, status

from backend.schemas import ScraperRequest

router = APIRouter(tags=["Tracked Product"])


@router.post(
    "/start-scraper",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
    summary="Start Scraper",
)
def start_scraper(request: ScraperRequest):
    """Starts the scraper async with the given URL and search text."""
    url = request.url
    search_text = request.search_text

    # Run scraper asynchronously in a separate process
    command = f'python ./scraper/__init__.py {url} "{search_text}" /results'
    try:
        subprocess.Popen(command, shell=True)
    except subprocess.SubprocessError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start scraper: {e}",
        )

    return {"message": "Scraper started successfully"}
