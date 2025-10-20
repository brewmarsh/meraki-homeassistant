# Use a stable, minimal Debian/Ubuntu base
FROM ubuntu:22.04

# Define the official runner version (Check GitHub releases for latest)
ARG RUNNER_VERSION="2.329.0"
ARG RUNNER_ARCH="x64"

# Set non-interactive mode and install necessary dependencies for the .NET runtime
# The libicu-dev package resolves all prior Dotnet Core/Libicu errors
# Install ca-certificates to fix potential SSL verification failures (Exit Code 77)
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
    unzip \
    wget \
    # Clean up APT cache
    && rm -rf /var/lib/apt/lists/*

# Create the dedicated, non-root user for security
RUN useradd -m runner

# Copy the entrypoint script
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Download and extract the official GitHub Actions Runner
WORKDIR /home/runner/actions-runner
# Construct the full filename with version number as per GitHub's documentation
RUN FILENAME="actions-runner-linux-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz" && \
    RUNNER_URL="https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/${FILENAME}" && \
    echo "Downloading runner from: ${RUNNER_URL}" && \
    # Using curl with the correct, full URL/filename as shown by GitHub
    curl -o "$FILENAME" -L "$RUNNER_URL" && \
    tar xzf "$FILENAME" && \
    rm "$FILENAME"

# Set permissions and ownership
RUN chown -R runner:runner /home/runner/actions-runner

# Copy the entrypoint script and set permissions
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to the non-root user
USER runner

# Set the working directory to the runner path
WORKDIR /home/runner/actions-runner

# Use the entrypoint script to run the runner
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
