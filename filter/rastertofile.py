#! /usr/bin/env python3

import sys, os
from collections import namedtuple
from struct import unpack
from PIL import Image, ImageOps


ESC = b'\x1b'
GS  = b'\x1d'

CupsRas3 = namedtuple(
    # Documentation at https://www.cups.org/doc/spec-raster.html
    'CupsRas3',
    'MediaClass MediaColor MediaType OutputType AdvanceDistance AdvanceMedia Collate CutMedia Duplex HWResolutionH '
    'HWResolutionV ImagingBoundingBoxL ImagingBoundingBoxB ImagingBoundingBoxR ImagingBoundingBoxT '
    'InsertSheet Jog LeadingEdge MarginsL MarginsB ManualFeed MediaPosition MediaWeight MirrorPrint '
    'NegativePrint NumCopies Orientation OutputFaceUp PageSizeW PageSizeH Separations TraySwitch Tumble cupsWidth '
    'cupsHeight cupsMediaType cupsBitsPerColor cupsBitsPerPixel cupsBitsPerLine cupsColorOrder cupsColorSpace '
    'cupsCompression cupsRowCount cupsRowFeed cupsRowStep cupsNumColors cupsBorderlessScalingFactor cupsPageSizeW '
    'cupsPageSizeH cupsImagingBBoxL cupsImagingBBoxB cupsImagingBBoxR cupsImagingBBoxT cupsInteger1 cupsInteger2 '
    'cupsInteger3 cupsInteger4 cupsInteger5 cupsInteger6 cupsInteger7 cupsInteger8 cupsInteger9 cupsInteger10 '
    'cupsInteger11 cupsInteger12 cupsInteger13 cupsInteger14 cupsInteger15 cupsInteger16 cupsReal1 cupsReal2 '
    'cupsReal3 cupsReal4 cupsReal5 cupsReal6 cupsReal7 cupsReal8 cupsReal9 cupsReal10 cupsReal11 cupsReal12 '
    'cupsReal13 cupsReal14 cupsReal15 cupsReal16 cupsString1 cupsString2 cupsString3 cupsString4 cupsString5 '
    'cupsString6 cupsString7 cupsString8 cupsString9 cupsString10 cupsString11 cupsString12 cupsString13 cupsString14 '
    'cupsString15 cupsString16 cupsMarkerType cupsRenderingIntent cupsPageSizeName'
)

def read_ras3(rdata):
    if not rdata:
        raise ValueError('No data received')

    # Check for magic word (either big-endian or little-endian)
    magic = unpack('@4s', rdata[0:4])[0]
    if magic != b'RaS3' and magic != b'3SaR':
        raise ValueError("This is not in RaS3 format")
    rdata = rdata[4:]  # Strip magic word
    pages = []

    while rdata:  # Loop over all pages
        struct_data = unpack(
            '@64s 64s 64s 64s I I I I I II IIII I I I II I I I I I I I I II I I I I I I I I I I I I I '
            'I I I f ff ffff IIIIIIIIIIIIIIII ffffffffffffffff 64s 64s 64s 64s 64s 64s 64s 64s 64s 64s '
            '64s 64s 64s 64s 64s 64s 64s 64s 64s',
            rdata[0:1796]
        )
        data = [
            # Strip trailing null-bytes of strings
            b.decode().rstrip('\x00') if isinstance(b, bytes) else b
            for b in struct_data
        ]
        header = CupsRas3._make(data)

        # Read image data of this page into a bytearray
        imgdata = rdata[1796:1796 + (header.cupsWidth * header.cupsHeight * header.cupsBitsPerPixel // 8)]
        pages.append((header, imgdata))

        # Remove this page from the data stream, continue with the next page
        rdata = rdata[1796 + (header.cupsWidth * header.cupsHeight * header.cupsBitsPerPixel // 8):]

    return pages

pages = read_ras3(sys.stdin.buffer.read())

for i, datatuple in enumerate(pages):
    (header, imgdata) = datatuple

    auto_crop=True
    PRINT_START_WIDTH = 1280
    PRINT_START_HEIGHT = 1920

    PRINT_FINAL_WIDTH = 640
    PRINT_FINAL_HEIGHT = 1616

    try:
        image = Image.frombuffer(mode='RGB', data=imgdata, size=(header.cupsWidth, header.cupsHeight))

        width, height = image.size

        if auto_crop:
            scale_factor = max(PRINT_START_WIDTH / width, PRINT_START_HEIGHT / height)
        else:
            scale_factor = min(PRINT_START_WIDTH / width, PRINT_START_HEIGHT / height)

        scaled_width = int(width * scale_factor)
        scaled_height = int(height * scale_factor)

        if scaled_width != width or scaled_height != height:
            image = image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)

        offset = (
            (PRINT_START_WIDTH - scaled_width) // 2,
            (PRINT_START_HEIGHT - scaled_height) // 2
        )

        out_image = Image.new("RGB", (PRINT_START_WIDTH, PRINT_START_HEIGHT))
        out_image.paste(image, offset)


        out_image.save("/tmp/a.jpg", format="JPEG", quality=100)

    except OSError as ex:
        print("ERROR: System: " + str(ex), file=sys.stderr)
        exit(1)

    except:
        pass