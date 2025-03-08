# FROM python:3.10.6
# RUN mkdir /bot && chmod 777 /bot
# WORKDIR /bot
# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt -qq update && \
#     apt -qq install -y git wget pv jq python3-dev ffmpeg mediainfo neofetch && \
#     apt-get install wget -y -f && \
#     apt-get install fontconfig -y -f

# COPY . .
# RUN pip3 install -r requirements.txt
# CMD ["bash", "run.sh"]

FROM python:3.10.6

# Set working directory
WORKDIR /bot

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages (including ffmpeg)
RUN apt update -qq && \
    apt install -y --no-install-recommends \
        git wget pv jq python3-dev ffmpeg mediainfo neofetch fontconfig && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Verify ffmpeg installation
RUN which ffmpeg && ffmpeg -version

# Copy bot files
COPY . .

# Ensure run.sh is executable
RUN chmod +x run.sh

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["bash", "run.sh"]
