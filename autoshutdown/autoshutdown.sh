#!/bin/bash

# Check if any ssh session is active
if [ -z "$(who)" ]; then
  # If no ssh session is active, log a message and shut down the system
  logger "System is shutting down automatically by a scheduled script at ~/autoshutdown.sh"
  sudo shutdown -h now
else
  # If ssh session is active, do nothing
  exit 0
fi
