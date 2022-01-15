#!/bin/bash
echo "Stopping server"
pkill -f 'java -jar product-qa-groovy-1.0.1.jar'
echo "Server stopped"