from PIL import Image, ImageDraw, ImageFont
# IMAGE_PATH = "image/iphone_img.png"
#img = Image.open(IMAGE_PATH)
class ObjectDetails:
    def __init__(self, object_name, coordinates):
        self.object_name = object_name
        self.coordinates = coordinates

def process_image(img):
    draw = ImageDraw.Draw(img) # Prepare to draw on the image

    # Define the number of grids
    num_grids_x = 10  # no. of vertical grids
    num_grids_y = 10  # no. of horizontal grids

    # Calculate grid size
    width, height = img.size
    grid_width = width // num_grids_x
    grid_height = height // num_grids_y

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)  # May need to change based on font availability on iphone
    except IOError:
        font = ImageFont.load_default()


    # Calculate height of the text based on the number of lines and font size
    font_height = font.size

    # Draw the grid lines and numbers
    for i in range(num_grids_x + 1):
        line_x = i * grid_width
        for j in range(num_grids_y + 1):
            line_y = j * grid_height
            # Draw vertical lines
            if i < num_grids_x:
                draw.line([(line_x, 0), (line_x, height)], fill="black", width=1)
            # Draw horizontal lines
            if j < num_grids_y:
                draw.line([(0, line_y), (width, line_y)], fill="black", width=1)

            # Don't draw labels on the outer boundary lines
            if i < num_grids_x and j < num_grids_y:
                label = f"({j+1}, {i+1})"  #  row and column labeling
                text_width = draw.textlength(label, font=font)

                # Calculate text position
                text_x = line_x + (grid_width - text_width) // 2
                text_y = line_y + (grid_height - font_height) // 2

                draw.text((text_x, text_y), label, font=font, fill="red") # Draw text in red

    #return img, grid_width, grid_height
    return img

def get_centroid_coordinates(objects, img):
    """
    Returns the pixel coordinates of the centroid for each specified object.
    """
    num_grids_x = 10 
    num_grids_y = 10 
    width, height = img.size
    grid_width = width / num_grids_x # I changed them to float division
    grid_height = height / num_grids_y
    
    centroids = []
    for object_detail in objects:
        center_points = []
        for coord in object_detail.coordinates:
            row, col = coord
            # Calculate the exact center x, y pixel coordinates based on grid index
            center_x = ((col - 1) * grid_width + (col * grid_width)) / 2
            center_y = ((row - 1) * grid_height + (row * grid_height)) / 2
            center_points.append((center_x, center_y))
        
        if center_points:
            centroid_x = sum(point[0] for point in center_points) / len(center_points)
            centroid_y = sum(point[1] for point in center_points) / len(center_points)
            centroids.append({'x': centroid_x, 'y': centroid_y, 'width': img.size[0], 'height': img.size[1]})
        else:
            centroids.append(None)  # No coordinates mean no centroid

    return centroids


def get_center_pixels(objects, img):
    """
    Returns the pixel information for the most central pixel in the specified grid areas of a 10x10 matrix mask
    for a list of objects.

    Parameters:
    - img (PIL.Image): The image to process.
    - objects (list of ObjectDetails): List of objects with their names and grid coordinates.

    Returns:
    - list of tuples: Each tuple contains the object's name and RGB values of the center pixel in its specified grid.
    """
    num_grids_x = 10
    num_grids_y = 10

    width, height = img.size
    grid_width = width // num_grids_x
    grid_height = height // num_grids_y

    results = []
    for obj in objects:
        for coord in obj.coordinates:
            x, y = coord
            # Adjust to zero-indexed by subtracting 1
            x -= 1
            y -= 1

            # Calculate the pixel coordinates of the grid's top-left corner
            start_x = x * grid_width
            start_y = y * grid_height

            # Calculate the pixel coordinates of the grid's center
            center_x = start_x + grid_width // 2
            center_y = start_y + grid_height // 2

            # Get pixel information at the center point
            pixel = img.getpixel((center_x, center_y))
            results.append((obj.object_name, pixel))

    return results

#grid_coords = [[1, 1], [1,2], [1,3] ] # example list of grid coordinates
#centers, centroid = get_grid_center_coordinates(grid_coords, grid_width, grid_height)
# print(centers)
# print("Centroid point:", centroid)
#draw.ellipse((centroid[0]-5, centroid[1]-5, centroid[0]+5, centroid[1]+5), fill='red', outline='red') # test accuracy using draw.ellipse

# Save or display the modified image
#img.show()  # This will display the image with the red point

def center_points(objects, img):
    """
    Returns the pixel coordinates of the centroid for each specified object.
    """
    num_grids_x = 10 
    num_grids_y = 10 
    width, height = img.size
    grid_width = width / num_grids_x # I changed them to float division
    grid_height = height / num_grids_y
    
    results = []
    for object_detail in objects:
        center_points = []
        for coord in object_detail.coordinates:
            row, col = coord
            # Calculate the exact center x, y pixel coordinates based on grid index
            center_x = ((col - 1) * grid_width + col * grid_width) / 2
            center_y = ((row - 1) * grid_height + row * grid_height) / 2
            center_points.append({"x": center_x, "y": center_y, "width": img.size[0], "height": img.size[1]})
        # Append the object's name and its center points to the results list
        results.append({'object_name': object_detail.object_name, 'centers': center_points})

    return results
