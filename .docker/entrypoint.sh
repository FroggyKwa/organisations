#!/bin/bash

set -e

echo "Starting tests..."

pytest -vv || { echo "Tests failed!"; exit 1; }

echo "All tests passed! Whooray! Starting API..."

exec "$@"