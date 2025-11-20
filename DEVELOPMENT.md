# Development Environment

To set up a local development environment for the Meraki Home Assistant integration using Docker:

1.  **Ensure Docker is Running:** Make sure Docker Desktop (or your Docker daemon) is running on your system.
2.  **Navigate to Project Root:** Open your terminal and navigate to the root directory of this project.
3.  **Start Home Assistant:** Run the following command to start a Home Assistant instance with your custom component mounted:
    ```bash
    docker compose up
    ```
    The first time you run this, Docker will download the Home Assistant image, which may take some time.
4.  **Access Home Assistant:** Once the containers are running, you can access the Home Assistant UI in your web browser at `http://localhost:8123`.
    If this is your first time running Home Assistant, you will be prompted to create an owner account.
5.  **Configure Integration:** Follow the standard Configuration steps (as outlined in `README.md`) to add the Meraki integration using your API Key and Organization ID.
6.  **Stop Home Assistant:** To stop the Home Assistant instance, press `Ctrl+C` in the terminal where `docker compose up` is running, or use:
    ```bash
    docker compose down
    ```

## Remote Access Considerations

For true "remote" access (i.e., from outside your local network), you would need to configure port forwarding on your router to expose port `8123` of your machine to the internet. **Be aware that exposing Home Assistant to the internet without proper security measures (like HTTPS and strong authentication) can be a security risk.**

## Running Live End-to-End Tests

This project includes a live end-to-end test that runs against a running Home Assistant instance. This is useful for verifying the integration's UI and functionality in a real-world scenario.

### Prerequisites

1.  **Running Home Assistant Instance**: You must have a Home Assistant instance running at `http://localhost:8123`. You can start one using the `docker-compose.yml` file provided in this project:
    ```bash
    docker compose up
    ```
2.  **Configured Home Assistant User**: The Home Assistant instance must have at least one user account set up. The test will use this user to log in.
3.  **Environment Variables**: You must set the following environment variables with the credentials of your Home Assistant user:
    -   `HA_USERNAME`: The username for your Home Assistant user.
    -   `HA_PASSWORD`: The password for your Home Assistant user.

### Running the Test

Once you have met the prerequisites, you can run the live E2E test using `pytest`:

```bash
pytest tests/test_e2e_live.py
```