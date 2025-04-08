import cv2
import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import av
import aiohttp_cors

# Set to store RTCPeerConnection connections
pcs = set()

class CameraStream(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera.")

    async def recv(self):
        pts, time_base = await self.next_timestamp()

        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read from camera")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    await pc.setRemoteDescription(offer)

    if any(t.kind == "video" and t.direction in ["recvonly", "sendrecv"] for t in pc.getTransceivers()):
        pc.addTrack(CameraStream())

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })

async def on_shutdown(app):
    print("Shutting down...")
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

def create_webrtc_app():
    app = web.Application()
    app.on_shutdown.append(on_shutdown)

    # Enable CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # Add route with CORS
    resource = cors.add(app.router.add_resource("/offer"))
    cors.add(resource.add_route("POST", offer))
    
    return app

def run_server(port=8080):
    app = create_webrtc_app()
    web.run_app(app, port=port)

# To allow the script to be run directly or be imported as a module
if __name__ == "__main__":
    # This code will only run if you run this file directly
    run_server()
