#!/bin/bash

sass -t expanded                  \
  -C --sourcemap=none             \
  --update .:../jizera/static/css
