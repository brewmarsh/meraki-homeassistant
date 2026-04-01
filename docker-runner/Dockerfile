# Use a stable, minimal Ubuntu base
FROM ubuntu:24.04

# Define the official runner version (Check GitHub releases for latest)
ARG RUNNER_VERSION="2.329.0"

# Install all necessary dependencies, including sudo for the final execution step
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg \
    git \
    iputils-ping \
    libicu-dev \
    libkrb5-3 \
    libssl-dev \
    procps \
    coreutils \
    sudo \
    tar \
    unzip \
    wget \
    rsync \
    jq \
    build-essential \
    # Clean up APT cache
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Action: Install Node.js 20 LTS from NodeSource
# This is required for frontend build steps (npm install, vite build, etc.)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Action 1 & 2: Install Docker CLI using modern "Noble" compliant logic
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu noble stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce-cli libltdl7 iptables && \
    # Ensure binary visibility across all shell types
    ln -sf $(which docker) /usr/local/bin/docker && \
    # Action 3: Verification Gate - Fail build if Docker is missing
    docker --version || (echo "Docker CLI failed to install" && exit 1) && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# CRITICAL: Create the dedicated 'runner' user, as the GitHub Actions Runner software
# must NOT run as root for security reasons.
RUN useradd -m runner && groupadd docker && usermod -aG docker runner

# Grant the 'runner' user passwordless sudo access for deployment
RUN echo "runner ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/runner && \
    chmod 0440 /etc/sudoers.d/runner

# Set the working directory for the runner download and execution
WORKDIR /home/runner/actions-runner

# DYNAMIC ARCHITECTURE DETECTION
# Automatically downloads the correct binary whether the container is running on x64 or ARM64
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        RUNNER_ARCH="x64"; \
    elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then \
        RUNNER_ARCH="arm64"; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    FILENAME="actions-runner-linux-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz" && \
    RUNNER_URL="https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/${FILENAME}" && \
    echo "Downloading runner from: ${RUNNER_URL}" && \
    curl -o "$FILENAME" -L "$RUNNER_URL" && \
    tar xzf "$FILENAME" && \
    rm "$FILENAME"

# Set ownership of the runner directory to the non-root user
RUN chown -R runner:runner /home/runner/actions-runner

# Create the /ha_config mount point and copy the entrypoint script
RUN mkdir -p /ha_config
COPY entrypoint.sh /usr/local/bin/runner-entrypoint.sh
RUN chmod +x /usr/local/bin/runner-entrypoint.sh

# FINAL PERMISSION FIX: The container runs as 'root' (default user) to allow
# write access to the Host OS volume. The entrypoint script uses 'sudo' to switch
# to the non-root 'runner' user for the final runner commands.
# Do NOT set USER here.

# Set the entrypoint to run the registration and loop
ENTRYPOINT ["/usr/local/bin/runner-entrypoint.sh"]
