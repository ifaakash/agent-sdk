#!/bin/bash

pi5_ip="100.76.6.76"
ollama_port="11434"
base_endpoint="http://$pi5_ip:$ollama_port/api/chat"
echo "Calling curl endpoint for qwen: "

curl $base_endpoint \
   -d '{
   	"model": "qwen:0.5b",
    "messages": [{"role": "user", "content": "Hello!"}]
   }'
