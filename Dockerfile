# Use a small base image
FROM alpine:latest

# Copy the text file into the image
COPY message.txt /message.txt

# Default command to show file content
CMD ["cat", "/message.txt"]
