#!/bin/bash

uvicorn config.server:app --host 0.0.0.0 --port 9001