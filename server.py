#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject, GLib

Gst.init(None)

class RTSPServer(GstRtspServer.RTSPServer):
    def __init__(self):
        super(RTSPServer, self).__init__()
        # Set a custom port (you can adjust as needed).
        self.set_service("8563")
        
        self.factory = GstRtspServer.RTSPMediaFactory()
        # Updated pipeline with compression (downscale resolution) and 30 fps limit.
        self.factory.set_launch(
            "( v4l2src device=/dev/video2 ! videoconvert ! videoscale ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! x264enc tune=zerolatency bitrate=500 speed-preset=ultrafast ! rtph264pay config-interval=1 name=pay0 pt=96 )"
        )
        self.factory.set_shared(True)
        # Mount the pipeline at the /test URL.
        self.get_mount_points().add_factory("/test", self.factory)
        self.attach(None)
        print("RTSP Server is listening on rtsp://129.97.181.180:8564/test")

def media_configure_callback(factory, media):
    element = media.get_element()
    appsrc = element.get_by_name("source")
    print("Appsrc configured successfully.")

# Create and attach the media-configure callback.
server = RTSPServer()
server.factory.connect("media-configure", media_configure_callback)

loop = GObject.MainLoop()
loop.run()
