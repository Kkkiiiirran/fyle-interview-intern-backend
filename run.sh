#!/bin/bash

# to stop on first error
set -e

# Run server using waitress
python -c "
from core.server import app
from waitress import serve
serve(app, host='0.0.0.0', port=8000)
"
