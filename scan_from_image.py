import sys
from PIL import Image, ImageFilter
from pyzbar import pyzbar
import PIL.ExifTags
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

help_str = """
1st argument is image to parse
outputs details and image of scanned codes
"""

def main(argv):
    supported_ext = ['png','jpg','jpeg']
    img_file = argv[1]
    print("Input IMG: %s"%img_file)
    if (img_file.split('.')[-1]).lower() not in supported_ext:
        print("Not supported img type: %s"%supported_ext)
    img = Image.open(sys.argv[1])
    exif = img._getexif()
    #print(exif)
    print(get_img_gps(img))
    bcloc = pyzbar.decode(img)
    print(bcloc)
    get_img_barcodes(img)

def get_img_info(img):
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }
    return exif

def get_img_gps(img):
    deg= u'\N{DEGREE SIGN}'
    gpsif = get_img_info(img)['GPSInfo']
    gps_google_str = str(gpsif[2][0][0]) + deg + str(gpsif[2][1][0]) + "\'" \
                + "%.4f"%(gpsif[2][2][0]/gpsif[2][2][1]) + "\"" \
                + gpsif[1] + "+" \
                + str(gpsif[4][0][0]) + deg \
                + str(gpsif[4][1][0]) + "'" \
                + "%.4f"%(gpsif[4][2][0]/gpsif[4][2][1]) + "\"" \
                + gpsif[3]
    html_str = "<a href=https://google.com/maps/place/" + gps_google_str + ">" + gps_google_str + "</a>"
    return html_str

def get_img_barcodes(A):
    img = np.array(A, dtype=np.uint8)
    codes = []
    # Converts to grayscale
    npimg = 0.2989 * img[:,:,0] + 0.5870 * img[:,:,1] + 0.1140 * img[:,:,2]
    mpimg = npimg
    while True:
        bcloc = pyzbar.decode(npimg)
        if len(bcloc) == 0:
            print(bcloc)
            return codes
        codes.append(bcloc)
        r = bcloc[0].rect
        dx,dy = int(img.shape[0]*0.02), int(img.shape[1]*0.02)
        for x in range(r.left-dx,r.left+r.width+dx):
            for y in range(r.top-dy,r.top+r.height+dy):
                npimg[y,x] = 0
        print(codes[-1])


if __name__ == "__main__":
    if len(sys.argv)<2:
        print(help_str)
    main(sys.argv)







