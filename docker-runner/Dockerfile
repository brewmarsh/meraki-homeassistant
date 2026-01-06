# Use a stable, minimal Ubuntu base
<<<<<<< HEAD
<<<<<<< HEAD
FROM ubuntu:22.04
=======
FROM ubuntu:24.04
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
FROM ubuntu:24.04
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129

# Define the official runner version (Check GitHub releases for latest)
ARG RUNNER_VERSION="2.329.0"
ARG RUNNER_ARCH="x64"

# Install all necessary dependencies, including sudo for the final execution step
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
    rsync \
    # Clean up APT cache
    && apt-get clean && rm -rf /var/lib/apt/lists/*

<<<<<<< HEAD
<<<<<<< HEAD
# CRITICAL: Create the dedicated 'runner' user, as the GitHub Actions Runner software 
=======
# CRITICAL: Create the dedicated 'runner' user, as the GitHub Actions Runner software
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
# CRITICAL: Create the dedicated 'runner' user, as the GitHub Actions Runner software
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
# must NOT run as root for security reasons.
RUN useradd -m runner

# Grant the 'runner' user passwordless sudo access for deployment
RUN echo "runner ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/runner && \
    chmod 0440 /etc/sudoers.d/runner

# Set the working directory for the runner download and execution
WORKDIR /home/runner/actions-runner

# Download and extract the official GitHub Actions Runner
RUN FILENAME="actions-runner-linux-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz" && \
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

<<<<<<< HEAD
<<<<<<< HEAD
# FINAL PERMISSION FIX: The container runs as 'root' (default user) to allow 
# write access to the Host OS volume. The entrypoint script uses 'sudo' to switch 
=======
# FINAL PERMISSION FIX: The container runs as 'root' (default user) to allow
# write access to the Host OS volume. The entrypoint script uses 'sudo' to switch
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
# FINAL PERMISSION FIX: The container runs as 'root' (default user) to allow
# write access to the Host OS volume. The entrypoint script uses 'sudo' to switch
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
# to the non-root 'runner' user for the final runner commands.
# Do NOT set USER here.

# Set the entrypoint to run the registration and loop
ENTRYPOINT ["/usr/local/bin/runner-entrypoint.sh"]
