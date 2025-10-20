# Use a stable, minimal Ubuntu base
FROM ubuntu:22.04

# Define the official runner version (Check GitHub releases for latest)
ARG RUNNER_VERSION="2.329.0"
ARG RUNNER_ARCH="x64"

# Set non-interactive mode and install all necessary dependencies
# libicu-dev is crucial for the .NET runtime. ca-certificates fixes SSL errors.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    iputils-ping \
    libicu-dev \
    libkrb5-3 \
    libssl-dev \
    procps \
    sudo \
    tar \
    unzip \
    wget \
    # Clean up APT cache
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create the dedicated, non-root user (although we run as root for permissions)
RUN useradd -m runner

# Set the working directory for the runner download and execution
WORKDIR /home/runner/actions-runner

# Download and extract the official GitHub Actions Runner
RUN FILENAME="actions-runner-linux-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz" && \
    RUNNER_URL="https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/${FILENAME}" && \
    echo "Downloading runner from: ${RUNNER_URL}" && \
    # Download the correct artifact and extract it into the WORKDIR
    curl -o "$FILENAME" -L "$RUNNER_URL" && \
    tar xzf "$FILENAME" && \
    rm "$FILENAME"

# Set ownership of the runner directory to the runner user
RUN chown -R runner:runner /home/runner/actions-runner

# Create the mount point directory, ensuring it exists before volume mounting
RUN mkdir -p /ha_config

# Copy the entrypoint script and ensure it is executable
# We rename the script to avoid caching issues seen earlier
COPY entrypoint.sh /usr/local/bin/runner-entrypoint.sh
RUN chmod +x /usr/local/bin/runner-entrypoint.sh

# FINAL PERMISSIONS FIX: Do NOT set the USER to 'runner'.
# Running as 'root' (the default) is necessary for the 'cp -rf' command 
# in the workflow to avoid 'Permission denied' errors on the mounted Host OS volume.
# # USER runner <--- COMMENTED OUT FOR PERMISSION FIX

# Set the entrypoint to run the registration and loop
ENTRYPOINT ["/usr/local/bin/runner-entrypoint.sh"]
