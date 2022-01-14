import questionary
from questionary import Style 
from termcolor import colored
import colorama
colorama.init()
import requests
import time
import matplotlib.pyplot as plt
import numpy as np
import io 
import zlib

def prompt():
    a = """
#####################
# MANDELBROT VIEWER #
#####################\n"""

    print(colored(a, 'cyan'))
    menu = questionary.select(
        "Choose a mode:", 
        choices=[
            "1) Verify if complex belongs to Mandelbrot set",
            "2) Compute the Mandelbrot set pixel by pixel",
            "3) Compute the Mandelbrot set at once"]
            ,style= custom_style_fancy).ask()

    if menu == "1) Verify if complex belongs to Mandelbrot set":
        is_mandelbrot()
    if menu == "2) Compute the Mandelbrot set pixel by pixel":
        compute_by_pixel()
    if menu == "3) Compute the Mandelbrot set at once":
        compute_at_once()




def is_mandelbrot():
    data = questionary.form(
        Re = questionary.text("Real part:", default='-0.36', style= custom_style_fancy),
        Im = questionary.text("Imaginary part:", default='0.38',style= custom_style_fancy),
        iter = questionary.text("Iterations:", default='100', style= custom_style_fancy)).ask()
    print("\n")
    r = requests.get(f'http://localhost:8000/compute?real={float(data["Re"])}&imag={float(data["Im"])}&iter={int(data["iter"])}')
    response = r.json() 
    if response['is_mandelbrot'] == True:
        print("The complex number C = {} + {}i belongs to the Mandelbrot set !".format(float(data["Re"]),float(data["Im"])))
    else:
        print("The complex number C = {} + {}i doesn't belongs to the Mandelbrot set !".format(float(data["Re"]),float(data["Im"])))

    print("Served from: {}".format(response["served from"]))

    time.sleep(5)
    prompt()

def compute_by_pixel():
    data = questionary.form(
        rows = questionary.text("Enter rows", default='50', style= custom_style_fancy),
        cols = questionary.text("Enter columns", default='50',style= custom_style_fancy),
        iter = questionary.text("Iterations:", default='100', style= custom_style_fancy)).ask()
    color_map = questionary.select(
        "Choose a color map:", 
        choices=[
            "hot",
            "spring",
            "afmhot",
            "viridis"]
            ,style= custom_style_fancy).ask()
    print("Rendering ...")
    #print(data)
    #print(cmap)

    session = requests.Session()
    start_time = time.time()

    result = np.zeros([int(data["rows"]), int(data["cols"])])
    for row_index, Re in enumerate(np.linspace(-2, 1, num = int(data["rows"]))):
        for column_index, Im in enumerate(np.linspace(-1, 1, num = int(data["cols"]))):
            r = session.get(f'http://localhost:8000/compute?real={Re}&imag={Im}&iter={50}').json()
            result[row_index, column_index] = r["Iteration"]
            #print(r["Iteration"])

    print("--- %s seconds ---" % (int(time.time() - start_time))) 

    plt.figure(dpi=250)
    plt.imshow(result.T, cmap = color_map, interpolation ='bilinear', extent = [-2, 1, -1, 1])
    plt.show()
    prompt()

def compute_at_once():
    data = questionary.form(
        rows = questionary.text("Enter rows", default='1000', style= custom_style_fancy),
        cols = questionary.text("Enter columns", default='1000',style= custom_style_fancy),
        iter = questionary.text("Iterations:", default='100', style= custom_style_fancy)).ask()

    color_map = questionary.select(
        "Choose a color map:", 
        choices=[
            "hot",
            "spring",
            "afmhot",
            "viridis",
            "jet",
            "hsv"]
            ,style= custom_style_fancy).ask()
    print("Rendering ...")

    start_time = time.time()
    r = requests.get(f'http://localhost:8000/mandelbrot?px={int(data["rows"])}&py={int(data["cols"])}&iter={int(data["iter"])}')

    result = uncompress_nparr(r.content)

    print("--- %s seconds ---" % (int(time.time() - start_time))) 
    plt.figure(dpi=250)
    plt.imshow(result.T, cmap = color_map, interpolation ='bilinear', extent = [-2, 1, -1, 1])
    plt.savefig("test.png", dpi=100)
    plt.show()
    
    prompt()

def uncompress_nparr(bytestring):
    """
    """
    return np.load(io.BytesIO(zlib.decompress(bytestring)))
custom_style_fancy = Style([
    ('qmark', 'fg:#673ab7 bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#f44336 bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),         # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])
if __name__ == '__main__':
    prompt()