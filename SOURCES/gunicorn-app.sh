#!/bin/bash
set -e
. var/lib/geonode/bin/activate
cd /var/lib/geonode/mapstory-geonode
exec python /var/lib/geonode/bin/gunicorn --pythonpath=. --workers=2 --bind=localhost:8000  --log-level=error mapstory.wsgi