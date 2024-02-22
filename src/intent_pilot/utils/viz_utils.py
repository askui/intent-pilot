from PIL import ImageDraw


def draw_thick_circle(draw, center, radius, thickness, color):
    """
    Draws a thick circle on an image with given parameters.

    :param draw: The ImageDraw object to draw on.
    :param center: Tuple (x, y) coordinates for the center of the circle.
    :param radius: The radius of the circle.
    :param thickness: The thickness of the circle line.
    :param color: The color of the circle line.
    """
    for i in range(thickness):
        draw.ellipse(
            (
                center[0] - radius + i,
                center[1] - radius + i,
                center[0] + radius - i,
                center[1] + radius - i,
            ),
            outline=color,
        )


def draw_red_circle(image, bbox, thickness=5):
    """
    Draws a big red circle in the middle of the specified bounding box on the image.

    :param image: The PIL image to draw on
    :param bbox: The bounding box as a list [xmin, ymin, xmax, ymax]
    :return: Image with a red circle drawn on it
    """
    draw = ImageDraw.Draw(image)
    # Calculate the center of the bounding box
    center_x = (bbox[0] + bbox[2]) // 2
    center_y = (bbox[1] + bbox[3]) // 2
    radius = min(
        (bbox[2] - bbox[0]) // 2, (bbox[3] - bbox[1]) // 2
    )  # Half the smaller dimension of the bbox
    # Define the bounding box of the circle
    # Draw the thick circle
    draw_thick_circle(draw, (center_x, center_y), radius, thickness, "red")
    return image
