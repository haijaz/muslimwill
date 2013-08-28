import time
import BaseHTTPServer
import datetime
import subprocess
import os


HOST_NAME = 'localhost'
PORT_NUMBER = 9000

TEAM = raw_input("Enter three letter code for home team: ")
QUALITY = raw_input("Enter quality(800,1200,1600,3200)")
SERVC = raw_input("Enter three digit server number")

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "application/vnd.apple.mpegurl")
        s.end_headers()
        os.environ['TZ'] = 'GMT'
        time.tzset()
        offset = -40
        team = TEAM
        ptime = str(int(time.time()))[:-1] + "0"
        print ptime
        start_time = 1368059400
        quality = QUALITY
        s.wfile.write("#EXTM3U\n")
        s.wfile.write("#EXT-X-TARGETDURATION:10\n")
        s.wfile.write("#EXT-X-MEDIA-SEQUENCE:" + str((int(ptime) - start_time) / 10) + "\n")
        i = 0
        while (i >= -20):
            s.wfile.write("#EXTINF:10,\n")
            s.wfile.write("http://nlds"+SERVC+".cdnak.neulion.com/nldsdvr/nba/"+team+"/as/live/"+team+"_hd_"+str(quality)+"_"+datetime.datetime.fromtimestamp(int(ptime) + (offset - i) * 10).strftime("%Y%m%d%H%M%S")+".ts\n")
            i-=1

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    #subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC','http://localhost:9000','--http-continuous','--quiet'])
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)