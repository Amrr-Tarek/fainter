# Fainter
#### Video Demo:  https://youtu.be/85A2io1GUWo
#### Description:
Fainter is a Windows desktop application developed in Python using Tkinter, designed for applying a variety of image filters.

Features:
- User-Friendly Interface
	- Modern design with light and dark themes (https://github.com/rdbende/Forest-ttk-theme)
	- Menu options for file management (Not complete)
- Image Filter Application:
	- Support several built-in filters, including:
		- **Box Blur:** Smooths the image by averaging the pixel values in a square. Removes noise and creates a soft, blurred effect.
			- **Adjustable Parameters:**
				- Blur radius (You can separate values and tweek the blur in the x direction and y direction).
		- **Gaussian Blur:** Applies a weighted average to the pixel values in a neighborhood, with weights determined by a Gaussian distribution. This creates a more natural, smoother blur compared to the box blur.
			- **Adjustable Parameters:**
				- Blur radius (Separating values is supported here as well).
		- **Unsharp Mask:** Enhances the details in an image by subtracting a blurred version of the image from the original, resulting in a sharpening effect.
			- **Adjustable Parameters:**
				- Radius
				- Percent (Intensity)
				- Threshold
		- **Custom Kernel Filters:** This feature allows users o design their own convolution kernels, enabling a wide range of effects, such as the presets embedded in the app as follows:
			- **Presets:**
				- Blur
				- Contour
				- Detail
				- Enhance Edges
				- Enhance Edges (More)
				- Emboss
				- Find Edges
				- Sharpen
				- Smooth
				- Smooth (More)
			- **Adjustable Parameters:**
				- Kernel Size (3x3) or (5x5)
				- Scale (with a switch to disable it)
				- Offset
		- **Rank Filters (Min, Median, Max):** Sorts the pixel values in a neighborhood and replace the center pixel with a specific value based on its rank in the sorted list.
			- **Presets:**
				- **Min Filter:** Replaces the pixel with the *smallest value* in the neighborhood **(Rank = 0)**. Useful for removing *salt noise*.
				- **Median Filter:** Replaces the pixel with the *median value* in the neighborhood **(Rank = size * size / 2)**. Useful for removing *impulse noise*.
				- **Max Filter:** Replaces the pixel with the *largest value* in the neighborhood **(Rank = size * size - 1)**. Useful for removing *pepper noise*.
			- **Adjustable Parameters:**
				- Size
				- Rank
		- **Mode Filters:** Replaces the pixel with the most frequently occurring value in its neighborhood. Useful for removing *small specks of noise* while maintaining sharp boundaries.
			- **Adjustable Parameters:**
				- Radius
	- Filters parameters are adjustable to fine-tune the image effects.
- Dynamic Preview:
	- Real-time preview in the app canvas.
	- Easily revert to the original image.
- Wide Format Support
	- Compatible with most popular image formats: (PNG, BMP, JPEG, JPG, and ICO)
	- Note: Alpha channels are not currently supported.
- Save and Export Options
- exe format release

Dependencies:
- Pillow (PIL): For image processing and filters.
- TKinter: For GUI developement.
