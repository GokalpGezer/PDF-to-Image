from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Set Matplotlib Backend to 'Agg' to avoid GUI issues
import matplotlib

matplotlib.use('Agg')  # Non-interactive backend for rendering without GUI


# 2. Convert PDF to Image
def convert_pdf_to_image(pdf_path, poppler_path):
    """
    Convert the first page of the given PDF to an image.
    """
    start_time = time.time()  # Start timing the PDF to image conversion
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    end_time = time.time()  # End timing

    image_conversion_time = end_time - start_time
    return images[0], image_conversion_time  # Return the first page and the time taken


# 3. Convert Image to Grid
def image_to_grid(image, rows, cols):
    """
    Convert the given image to a grid where each cell is marked as 1
    if it contains dark pixels and 0 if it is mostly empty (light pixels).
    """
    start_time = time.time()  # Start timing the image to grid conversion

    # Convert the image to grayscale
    image = image.convert("L")
    img_array = np.array(image)
    height, width = img_array.shape

    # Calculate the height and width of each grid cell
    cell_height = height // rows
    cell_width = width // cols

    # Initialize a grid with zeros
    grid = np.zeros((rows, cols), dtype=int)

    for r in range(rows):
        for c in range(cols):
            # Extract the portion of the image corresponding to the current cell
            cell = img_array[r * cell_height:(r + 1) * cell_height, c * cell_width:(c + 1) * cell_width]

            # If any pixel in the cell is darker than a threshold (200), mark the grid as 1
            if np.any(cell < 200):  # Pixels < 200 are considered non-white (dark)
                grid[r, c] = 1

    end_time = time.time()  # End timing
    grid_conversion_time = end_time - start_time

    return grid, grid_conversion_time  # Return the grid and the time taken


# 4. Main Program with Execution Time Display
def main(pdf_path, poppler_path, rows, cols):
    # Convert PDF to Image
    image, image_conversion_time = convert_pdf_to_image(pdf_path, poppler_path)

    # Convert Image to Grid
    grid, grid_conversion_time = image_to_grid(image, rows, cols)

    # Print the results
    print("Execution Times:")
    print(f"PDF to Image Conversion: {image_conversion_time:.2f} seconds")
    print(f"Image to Grid Conversion: {grid_conversion_time:.2f} seconds")
    total_time = image_conversion_time + grid_conversion_time
    print(f"Total Execution Time: {total_time:.2f} seconds")

    # Optional: Print the grid
    print("Generated Grid (partial view):")
    for row in grid[:10]:  # Print the first 10 rows as an example
        print(row)

    # Save the grid as an image file
    plt.imshow(grid, cmap="gray", interpolation='nearest')
    plt.title(f"{rows}x{cols} Grid Representation")
    plt.savefig("grid_output.png")


# Example usage
pdf_file_path = r"C:\Users\Gokalp\Desktop\sekil3.pdf"  # Path to your PDF file
poppler_path = r"C:\Users\Gokalp\Desktop\poppler-24.08.0\Library\bin"  # Path to Poppler's bin folder
main(pdf_file_path, poppler_path, 108, 192)  # Adjust rows and columns if necessary
