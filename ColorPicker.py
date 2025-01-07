import colorsys

def number_to_rgb(dimple_diameter):
    # Ensure the number is within the valid range
    if not (0.050 <= dimple_diameter <= 0.200):
        raise ValueError("Number must be between 0.050 and 0.200")

    # Normalize the number to a range of 0 to 1
    normalized_value = (dimple_diameter - 0.050) / (0.200 - 0.050)

    # Map the normalized value to the Hue (0 to 1)
    hue = normalized_value

    # Convert HSL to RGB
    # Full saturation (1.0) and lightness (0.5) for vibrant colors
    r, g, b = colorsys.hls_to_rgb(hue, 0.5, 1.0)

    # Scale RGB values to 0-255
    rgb = (int(r * 255), int(g * 255), int(b * 255))

    return rgb

# Example usage
#dimple_diameter = 0.05  # Replace with your number between 0.050 and 0.200
rgb_color = number_to_rgb(dimple_diameter)
print(f"RGB color for {dimple_diameter}: {rgb_color}")

def adjust_brightness(rgb_color, dimple_depth):
    # Ensure the brightness factor is within the valid range
    if not (0.005 <= dimple_depth <= 0.015):
        raise ValueError("Brightness factor must be between 0.005 and 0.015")

    # Invert brightness factor so 0.015 is dark and 0.005 is bright
    inverted_brightness = 1 - ((dimple_depth - 0.005) / (0.015 - 0.005))

    # Scale down the RGB values by the inverted brightness
    adjusted_rgb = tuple(int(channel * inverted_brightness) for channel in rgb_color)

    return adjusted_rgb

adjusted_rgb_color = adjust_brightness(rgb_color, brightness)
print(f"Original RGB: {rgb_color}")
print(f"Adjusted RGB for brightness {brightness}: {adjusted_rgb_color}")


################################################################################################################
################################################################################################################

def calculate_rgb(self, dimple_diameter, dimple_depth):
        selected_objects = FreeCADGui.Selection.getSelection()
        if not selected_objects:
            raise ValueError("No object selected. Please select an object in FreeCAD.")

        # Assign the first selected object to get_selected_body_label
        get_selected_body_label = selected_objects[0]
        # Ensure inputs are within the valid ranges
        if not (0.050 <= dimple_diameter <= 0.200):
            raise ValueError("DimpleDiameter must be between 0.050 and 0.200")
        if not (0.005 <= dimple_depth <= 0.015):
            raise ValueError("DimpleDepth must be between 0.005 and 0.015")

        # Map DimpleDiameter to a base color (0.050 to 0.200 maps to 0 to 255)
        normalized_diameter = (dimple_diameter - 0.050) / (0.200 - 0.050)
        base_color = int(normalized_diameter * 255)

        # Create an initial RGB color based on DimpleDiameter (e.g., shades of red)
        r, g, b = base_color, 0, 255 - base_color

        # Adjust brightness based on DimpleDepth (0.005 to 0.015 maps to 0.5 to 1.0)
        normalized_depth = (dimple_depth - 0.005) / (0.015 - 0.005)
        brightness_factor = 0.5 + (normalized_depth * 0.5)

        # Apply brightness adjustment
        r = int(r * brightness_factor)
        g = int(g * brightness_factor)
        b = int(b * brightness_factor)

        # Normalize RGB values to 0-1 for FreeCAD
        r_normalized = r / 255
        g_normalized = g / 255
        b_normalized = b / 255

        # Set color to the selected FreeCAD object
        if 'get_selected_body_label' in globals():
            get_selected_body_label.ViewObject.ShapeColor = (r_normalized, g_normalized, b_normalized)
            print(get_selected_body_label.ViewObject.ShapeColor)
        else:
            raise NameError("get_selected_body_label is not defined")



################################################################################################################
################################################################################################################



import colorsys

def number_to_rgb_and_brightness(main_number, brightness_factor):
    """
    Convert a main number to an RGB color and adjust its brightness.

    Parameters:
        main_number (float): A number between 0.050 and 0.200 to generate the RGB color.
        brightness_factor (float): A number between 0.005 and 0.015 to adjust brightness.

    Returns:
        tuple: The adjusted RGB color as a tuple (R, G, B).
    """
    # Ensure the main number is within the valid range
    if not (0.050 <= main_number <= 0.200):
        raise ValueError("Main number must be between 0.050 and 0.200")

    # Ensure the brightness factor is within the valid range
    if not (0.005 <= brightness_factor <= 0.015):
        raise ValueError("Brightness factor must be between 0.005 and 0.015")

    # Normalize the main number to a range of 0 to 1
    normalized_value = (main_number - 0.050) / (0.200 - 0.050)

    # Map the normalized value to the Hue (0 to 1)
    hue = normalized_value

    # Convert HSL to RGB
    r, g, b = colorsys.hls_to_rgb(hue, 0.5, 1.0)
    rgb_color = (int(r * 255), int(g * 255), int(b * 255))

    # Invert brightness factor so 0.015 is dark and 0.005 is bright
    inverted_brightness = 1 - ((brightness_factor - 0.005) / (0.015 - 0.005))

    # Scale down the RGB values by the inverted brightness
    adjusted_rgb = tuple(int(channel * inverted_brightness) for channel in rgb_color)

    return adjusted_rgb

# Example usage
main_number = 0.125  # Replace with your number between 0.050 and 0.200
brightness_factor = 0.010  # Replace with your number between 0.005 and 0.015
adjusted_rgb_color = number_to_rgb_and_brightness(main_number, brightness_factor)
print(f"Adjusted RGB color for main number {main_number} and brightness factor {brightness_factor}: {adjusted_rgb_color}")
