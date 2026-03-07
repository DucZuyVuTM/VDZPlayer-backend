from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import httpx
import yt_dlp


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_video_info(url: str):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "source": info.get('extractor_key'),
                "videoUrl": info.get('url'),
                "thumbnail": info.get('thumbnail'),
                "title": info.get('title'),
            }
        except Exception as e:
            print(f"Error: {e}")
            return None


@app.get("/api/extract")
async def extract(url: str = Query(
    ...,
    description="Video URL from supported platforms"
)):
    data = get_video_info(url)
    if not data:
        raise HTTPException(status_code=400, detail="Platform not supported or URL is invalid.")
    return data


@app.get("/api/proxy-image")
async def proxy_image(url: str = Query(
    ...,
    description="Link to original image to be proxied"
)):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, timeout=10.0)

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Could not fetch image")

            return Response(
                content=response.content, 
                media_type=response.headers.get("Content-Type", "image/jpeg")
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Proxy error: {str(e)}")


@app.get("/api/stream-video")
async def stream_video(url: str = Query(
    ...,
    description="Link to original video to be streamed"
)):
    if not url or url == "undefined" or not url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL không hợp lệ")

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
