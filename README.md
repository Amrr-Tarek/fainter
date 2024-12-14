# Fainter

Fainter is a Windows desktop application developed in Python using Tkinter, designed for applying a vareity of image filters.

Features:
- User-Friendly Interface
	- Modern design with light and dark themes (https://github.com/rdbende/Forest-ttk-theme)
	- Menu options for file management (Not complete)
- Image Filter Application:
	- Support several built-in filters, including:
		- Box Blur
		- Gaussian Blur
		- Unsharp Mask
		- Custom Kernel Filters
		- Rank Filters (Min, Median, Max)
		- Mode Filters
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
