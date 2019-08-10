
import os
import math
import copy
import re
import io

from google.cloud import vision
from google.cloud.vision import types
from wand.image import Image
from wand.color import Color
from wand.display import display


items = {
    types.FaceAnnotation.Landmark.LEFT_EYE: {"section": "left_eye", "name": "left_eye", "order": -1},
    types.FaceAnnotation.Landmark.LEFT_OF_LEFT_EYEBROW: {"section": "left_eye", "name": "left_of_left_eyebrow", "order": 0},
    types.FaceAnnotation.Landmark.RIGHT_OF_LEFT_EYEBROW: {"section": "left_eye", "name": "right_of_left_eyebrow", "order": 2},
    types.FaceAnnotation.Landmark.LEFT_EYE_TOP_BOUNDARY: {"section": "left_eye", "name": "left_eye_top_boundary", "order": -1},
    types.FaceAnnotation.Landmark.LEFT_EYE_RIGHT_CORNER: {"section": "left_eye", "name": "left_eye_right_corner", "order": 3},
    types.FaceAnnotation.Landmark.LEFT_EYE_BOTTOM_BOUNDARY: {"section": "left_eye", "name": "left_eye_bottom_boundary", "order": 4},
    types.FaceAnnotation.Landmark.LEFT_EYE_LEFT_CORNER: {"section": "left_eye", "name": "left_eye_left_corner", "order": 5},
    types.FaceAnnotation.Landmark.LEFT_EYEBROW_UPPER_MIDPOINT: {"section": "left_eye", "name": "left_eyebrow_upper_midpoint", "order": 1},
    types.FaceAnnotation.Landmark.LEFT_EYE_PUPIL: {"section": "left_eye", "name": "left_eye_pupil", "order": -1},

    types.FaceAnnotation.Landmark.RIGHT_EYE: {"section": "right_eye", "name": "right_eye", "order": -1},
    types.FaceAnnotation.Landmark.LEFT_OF_RIGHT_EYEBROW: {"section": "right_eye", "name": "left_of_right_eyebrow", "order": 0},
    types.FaceAnnotation.Landmark.RIGHT_OF_RIGHT_EYEBROW: {"section": "right_eye", "name": "right_of_right_eyebrow", "order": 2},
    types.FaceAnnotation.Landmark.RIGHT_EYE_TOP_BOUNDARY: {"section": "right_eye", "name": "right_eye_top_boundary", "order": -1},
    types.FaceAnnotation.Landmark.RIGHT_EYE_RIGHT_CORNER: {"section": "right_eye", "name": "right_eye_right_corner", "order": 3},
    types.FaceAnnotation.Landmark.RIGHT_EYE_BOTTOM_BOUNDARY: {"section": "right_eye", "name": "right_eye_bottom_boundary", "order": 4},
    types.FaceAnnotation.Landmark.RIGHT_EYE_LEFT_CORNER: {"section": "right_eye", "name": "right_eye_left_corner", "order": 5},
    types.FaceAnnotation.Landmark.RIGHT_EYEBROW_UPPER_MIDPOINT: {"section": "right_eye", "name": "right_eyebrow_upper_midpoint", "order": 1},
    types.FaceAnnotation.Landmark.RIGHT_EYE_PUPIL: {"section": "right_eye", "name": "right_eye_pupil", "order": -1},

    types.FaceAnnotation.Landmark.NOSE_TIP: {"section": "nose", "name": "nose_tip", "order": 0},
    types.FaceAnnotation.Landmark.NOSE_BOTTOM_RIGHT: {"section": "nose", "name": "nose_bottom_right", "order": 1},
    types.FaceAnnotation.Landmark.NOSE_BOTTOM_LEFT: {"section": "nose", "name": "nose_bottom_left", "order": 3},
    types.FaceAnnotation.Landmark.NOSE_BOTTOM_CENTER: {"section": "nose", "name": "nose_bottom_center", "order": 2},

    types.FaceAnnotation.Landmark.MOUTH_LEFT: {"section": "mouth", "name": "mouth_left", "order": 0},
    types.FaceAnnotation.Landmark.MOUTH_RIGHT: {"section": "mouth", "name": "mouth_right", "order": 2},
    types.FaceAnnotation.Landmark.MOUTH_CENTER: {"section": "mouth", "name": "mouth_center", "order": -1},
    types.FaceAnnotation.Landmark.UPPER_LIP: {"section": "mouth", "name": "upper_lip", "order": 1},
    types.FaceAnnotation.Landmark.LOWER_LIP: {
        "section": "mouth", "name": "lower_lip", "order": 3}
}

SECTIONS = set([items[k]["section"] for k in items])

CLIENT = vision.ImageAnnotatorClient()


def prepare(filename, resolution, images_dir):
    out_filename = os.path.join(images_dir, "main.png")
    with io.open(filename, 'rb') as image_file:
        with Image(file=image_file) as foreground:
            foreground.transform(
                resize="{:d}x{:d}".format(resolution, resolution))
            with Image(width=resolution, height=resolution, background=Color('black')) as background:
                left = int((resolution - foreground.width) / 2)
                top = int((resolution - foreground.height) / 2)
                background.composite(foreground, left=left, top=top)
                background.format = 'png'
                background.save(filename=out_filename)
    return out_filename


def get_faces(filename):
    """
    Extract the faces using Google Vision API

    For dev purposes we can use the cached option to avoid hitting the API.

    """
    print "Getting faces in", filename
    with io.open(filename, 'rb') as image_file:
        content = image_file.read()

    print "Using Google face API"
    # Get the client and extract faces
    image = vision.types.Image(content=content)
    response = CLIENT.face_detection(image=image)
    gfaces = response.face_annotations

    if not gfaces:
        raise ValueError("No faces in this image:", filename)

    print "Found {} faces in {}".format(len(gfaces), filename)

    result = []
    for i, gface in enumerate(gfaces):
        print "Getting features for face {}".format(i)
        result.append(
            {"features": get_features(gface)}
        )
    return result


def get_features(gface):
    # features = []
    features = {}
    for m in gface.landmarks:
        item = items.get(m.type)
        if not item:
            continue
        section = item["section"]
        if section not in features:
            features[section] = []
        features[section].append({
            "order": item["order"],
            "name": item["name"],
            "x": int(round(m.position.x)),
            "y": int(round(m.position.y))
        })
        features[section].sort(key=lambda x: x["order"])
    return features


def make_crops(filename, faces, margin):
    result = {"faces": copy.deepcopy(faces)}

    images_dir = os.path.dirname(filename)

    with io.open(filename, 'rb') as image_file:
        with Image(file=image_file) as img:
            width = img.width
            height = img.height
            print "Original image size {}x{}".format(width, height)
            result["resolution"] = {
                "x": width, "y": height
            }
            result["filename"] = os.path.basename(filename)

            print "Loop over faces"
            for i, face in enumerate(result["faces"]):

                this_margin = margin

                bounds = get_bounds(face)

                bounds = pad_bounds(bounds, (width, height), margin)

                minx, miny, maxx, maxy = bounds

                print "Crop is top-left:{},{} - bottom-right:{},{}".format(minx, maxx, miny, maxy)
                with img[minx:maxx, miny:maxy] as cropped:
                    # root, ext = os.path.splitext(filename)
                    face["filename"] = "face_{}.png".format(i)
                    print "Cropped filename is:", face["filename"]
                    cropped.format = 'png'
                    cropped.save(filename=os.path.join(
                        images_dir, face["filename"]))
                    face["crop"] = {
                        "minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy
                    }
                    display(cropped)
    return result


def get_bounds(face):
    feature_set = face["features"]
    minx = miny = 999999
    maxx = maxy = 0

    for feature in [f for f in feature_set]:
        #  if f in SECTIONS
        # e.g. left_eye
        for landmark in feature_set[feature]:
            x = landmark["x"]
            y = landmark["y"]
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x
            if y < miny:
                miny = y
            if y > maxy:
                maxy = y

    return (
        int(math.floor(minx)),
        int(math.floor(miny)),
        int(math.floor(maxx)),
        int(math.floor(maxy)))


def pad_bounds(bounds, resolution, margin):

    minx, miny, maxx, maxy = bounds
    w, h = resolution
    # make it square
    # square_size = maxx-minx
    # if square_size < maxy-miny:
    #     square_size = maxy-miny
    #     minx, maxx = expand((minx, maxx), square_size,  w)
    # else:
    #     miny, maxy = expand((miny, maxy), square_size,  h)

    # shrink margin so it fits
    margin = min(margin, minx)
    margin = min(margin, miny)
    margin = min(margin, w-maxx)
    margin = min(margin, h-maxy)

    minx -= margin
    miny -= margin
    maxx += margin
    maxy += margin

    print "Padded crop:", minx, miny, maxx, maxy

    return (minx, miny, maxx, maxy)


# def expand(extents, square_size, orig_length):
#     # generate new extents
#     minval, maxval = extents
#     curr_length = maxval - minval
#     if curr_length >= square_size:
#         return (minval, maxval)

#     newmin = minval - ((square_size-curr_length) / 2)
#     if newmin < 0:
#         return (0, square_size)

#     return (
#         newmin, newmin+square_size
#     )
