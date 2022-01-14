from urllib import request
from flask import Flask, request, Response 
import sys
import json 
from numba import jit
import numpy as np
import io
import zlib


app = Flask(__name__)

serverName = sys.argv[1]

@app.route('/')
def hello():
    return serverName

@app.route('/compute')
def compute():
    Re = float(request.args.get('real'))
    Im = float(request.args.get('imag'))
    max_iter = int(request.args.get("iter"))
    iter_result = Mandelbrot(Re, Im, max_iter)
    is_mandelbrot = False
   
    if iter_result == max_iter:
        is_mandelbrot=True
    
    dico = {"served from": serverName, "Iteration": iter_result, "is_mandelbrot": is_mandelbrot }
    r = json.dumps(dico)
    return r

@app.route('/mandelbrot')
def mandelbrot():
    px = int(request.args.get('px'))
    py = int(request.args.get('py'))
    max_iter = int(request.args.get("iter"))
    result = np.zeros([px, py])
    for row_index, Re in enumerate(np.linspace(-2, 1, num = py)):
        for column_index, Im in enumerate(np.linspace(-1, 1, num = px)):
            
            result[row_index, column_index] = Mandelbrot(Re, Im, max_iter)
    
    resp, _, _ = compress_nparr(result)
    return Response(response=resp, status=200,
                    mimetype="application/octet_stream")



def compress_nparr(nparr):
    """
    Returns the given numpy array as compressed bytestring,
    the uncompressed and the compressed byte size.
    """
    bytestream = io.BytesIO()
    np.save(bytestream, nparr)
    uncompressed = bytestream.getvalue()
    compressed = zlib.compress(uncompressed)
    return compressed, len(uncompressed), len(compressed)

def uncompress_nparr(bytestring):
    """
    """
    return np.load(io.BytesIO(zlib.decompress(bytestring)))

@jit
def Mandelbrot(Re, Im, max_iter):
        c = complex(Re, Im)
        z = 0.0j

        for i in range(max_iter):
            z = z*z + c
            if (z.real*z.real + z.imag*z.imag) >= 4:
                return i 
        return(max_iter)
if __name__ == '__main__':
    app.run(port=sys.argv[2])