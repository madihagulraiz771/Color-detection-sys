import cv2
import pandas as pd
import argparse
import os

# Creating argument parser to take the image path from the command line
ap = argparse.ArgumentParser(description="Find the name and RGB values of any color in an image.")
ap.add_argument('-i', '--image', required=True, help="Path to the image file. Example: python script.py -i image.jpg")
args = vars(ap.parse_args())
image_path = args['image']

# Check if the image file exists
if not os.path.exists(image_path):
    print("Error: Image file not found. Please provide a valid path.")
    exit()

# Check if the colors.csv file exists
csv_file = 'colors.csv'
if not os.path.exists(csv_file):
    print(f"Error: '{csv_file}' file not found. Ensure the file exists in the same directory.")
    exit()

# Reading the image with OpenCV
image = cv2.imread(image_path)

# Declaring global variables
mouse_clicked = False
selected_color = {"r": 0, "g": 0, "b": 0, "color_name": "", "x": 0, "y": 0}

# Reading the CSV file with pandas and assigning column names
column_names = ["color", "color_name", "hex", "R", "G", "B"]
color_data = pd.read_csv(csv_file, names=column_names, header=None)

# Function to calculate the most matching color
def get_color_name(R, G, B):
    distances = abs(color_data["R"] - R) + abs(color_data["G"] - G) + abs(color_data["B"] - B)
    closest_index = distances.idxmin()
    return color_data.loc[closest_index, "color_name"]

# Function to handle mouse double-click events
def handle_mouse_event(event, x, y, flags, param):
    global mouse_clicked, selected_color
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouse_clicked = True
        blue, green, red = image[y, x]
        selected_color = {
            "r": int(red),
            "g": int(green),
            "b": int(blue),
            "color_name": get_color_name(int(red), int(green), int(blue)),
            "x": x,
            "y": y,
        }

# Create a resizable window and set mouse callback
cv2.namedWindow('Image Window', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Image Window', handle_mouse_event)

while True:
    # Create a copy of the image for display
    display_image = image.copy()

    if mouse_clicked:
        # Draw a rectangle filled with the selected color
        cv2.rectangle(display_image, (20, 20), (750, 60), 
                      (selected_color["b"], selected_color["g"], selected_color["r"]), -1)

        # Create a text string with the color name and RGB values
        color_text = f'{selected_color["color_name"]} R={selected_color["r"]} G={selected_color["g"]} B={selected_color["b"]}'

        # Choose the font style for the text
        font = cv2.FONT_HERSHEY_COMPLEX  # You can change this to any of OpenCV's built-in fonts

        # For very light colors, use a black text color for better visibility
        text_color = (255, 255, 255) if selected_color["r"] + selected_color["g"] + selected_color["b"] < 600 else (0, 0, 0)

        # Display the text on the image using the selected font style
        cv2.putText(display_image, color_text, (50, 50), font, 0.8, text_color, 2, cv2.LINE_AA)

    # Display the image
    cv2.imshow("Image Window", display_image)

    # Break the loop when the user presses the 'Esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

# Destroy all OpenCV windows
cv2.destroyAllWindows()
