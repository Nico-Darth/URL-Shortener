
# URL Shortener App

A lightweight desktop application for shortening URLs using the TinyURL API. Built with Python and PyQt5, this app is intuitive, fast, and user-friendly.

## Features

- **URL Shortening**: Quickly shorten any valid URL using the [TinyURL API](https://tinyurl.com/app/terms).
- **Theme Customization**: Toggle between **Light Mode** and **Dark Mode** for a better user experience.
- **Clipboard Support**: Copy the shortened URL directly to your clipboard with one click.
- **Acknowledgment**: Credits for the app and its API integration.

## Installation

Clone the repository:
```bash
git clone https://github.com/Nico-Darth/URL-Shortener.git
```

Navigate to the project directory:
```bash
cd URL-Shortener
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python url-service-controller.py
```

## Requirements

- **Python**: 3.6 or higher
- **Dependencies**: Listed in `requirements.txt`:
  - `PyQt5`
  - `requests`
  - `validators`
  - `pyperclip`

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## Usage

Open the application by running:
```bash
python app.py
```

Enter a URL in the input field and click **Shorten URL**.

Copy the shortened URL using the **Copy URL** button.

Adjust themes or check credits in the **Settings** menu.

## Settings

In the **Settings** window, you can:
- Switch between **Light Mode** and **Dark Mode**.
- View the acknowledgment links:
  - **Powered by TinyURL**: [Terms of Use](https://tinyurl.com/app/terms)
  - **Developed by Niels Coert**: [GitHub Profile](https://github.com/Nico-Darth)

## Credits

- **API Integration**: [TinyURL](https://tinyurl.com)
- **Developed by**: [Niels Coert](https://github.com/Nico-Darth)
- **Framework**: [PyQt5](https://riverbankcomputing.com/software/pyqt/intro)
