import httpx
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from app.utils.extractor import get_video_info


class VideoService:

    async def get_info(self, url: str):
        data = get_video_info(url)
        if not data:
            raise HTTPException(status_code=400, detail="Invalid URL")
        return data
    
    async def stream_video(self, url: str):
        if not url or url == "undefined" or not url.startswith("http"):
            raise HTTPException(status_code=400, detail="URL is invalid")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://www.facebook.com/",
            "Accept": "*/*",
        }
        
        async def video_generator():
            async with httpx.AsyncClient(
                headers=headers,
                follow_redirects=True,
                timeout=None
            ) as client:
                try:
                    async with client.stream("GET", url) as response:
                        if response.status_code >= 400:
                            return
                        async for chunk in response.aiter_bytes(chunk_size=256*1024):
                            yield chunk
                except Exception as e:
                    print(f"Streaming error: {e}")

        return StreamingResponse(video_generator(), media_type="video/mp4")
