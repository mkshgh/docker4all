# Simple Hello World Docker Example
# This demonstrates the most basic Dockerfile

FROM alpine:latest

# Add a simple script
RUN echo '#!/bin/sh' > /hello.sh && \
    echo 'echo "Hello from Docker!"' >> /hello.sh && \
    echo 'echo "Container ID: $(hostname)"' >> /hello.sh && \
    echo 'echo "Current time: $(date)"' >> /hello.sh && \
    chmod +x /hello.sh

# Run the script when container starts
CMD ["/hello.sh"]
