import httpx
from fastapi import HTTPException, Response


class ImageService:
    async def proxy_image(self, url: str):
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(url, timeout=10.0)

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code, detail="Could not fetch image"
                    )

                return Response(
                    content=response.content,
                    media_type=response.headers.get("Content-Type", "image/jpeg"),
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Proxy error: {str(e)}")
