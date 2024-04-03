
# DeepCASE-Dashboard

DeepCASE-Dashboard enhances deepCASE by providing a visualization interface. This tool is designed to build trust in deepCASE and is particularly useful in practical scenarios.

## Running DeepCASE-Dashboard with Docker-Compose

To facilitate easy setup and running of DeepCASE-Dashboard, Docker and `docker-compose` are recommended. Follow these instructions to get started:

1. **Docker Installation**: Ensure Docker and `docker-compose` are installed on your system. Visit the Docker official website for installation instructions specific to your operating system.

2. **Dockerfile & Docker-Compose File**: Ensure a `docker-compose.yml` and `Dockerfile` in the root directory of your project.

This configuration uses the `python:3.8-slim` Docker image, mounts the current directory to `.` inside the container, sets the working directory, and specifies the command to run the dashboard. It also maps port 8050 of the container to port 8050 on the host, allowing you to access the dashboard via `http://localhost:8050`.

3. **Running the Container**: Navigate to the directory, which is the root directory, containing the `docker-compose.yml` file and run:

```
docker-compose up
```

This command will build and start the DeepCASE-Dashboard container. Once the application is running, you can access the dashboard through your web browser.

4. **Stopping the Container**: To stop and remove the containers, use:

```
docker-compose down
```

## Usage

Follow the instructions displayed in the command line. The web interface will guide you through the rest. For more help, you can consult the user manual page. 

## Credits
Special thanks to Thijs van Ede for his assistance.

## License
I suggest we use one, git can add a fancy one.

