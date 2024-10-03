# Histogram Playground

This is a client/server prototype for an image scaling tool that allows users to set the high and low points of an
image and generate a RGB stack.

The frontend displays 3 images, taken in astronomical filters that map roughly to red/green/blue. There are high and low sliders
to adjust the 16-bit value of the lowest (black) and highest (white) points, and scales and displays an 8 bit image accordingly.

## Setup
1. Install dependencies into virtual environment:

```
pip install -r requirements.txt
```

2. Run a http server to host the static files

```
python -m http.server 8000
```

3. In a separate terminal, run the flask backend

```
flask run
```

4. Navigate to http://localhost:8000/frontend.html

5. Have fun! Clicking "generate RGB image" will write a JPEG (`rgb_image.jpg`) to the current working directory. Adjustments will also be done on the fly as sliders are moved, but sometimes the backend has trouble keeping up with the rate of changes.
