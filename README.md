# AI Streaming 

Project related to stream processing with DeepStream.

## Installation


Please install docker container following the instructions at [Docker Containers](https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_docker_containers.html).

```bash
docker run -it --rm --gpus all nvcr.io/nvidia/deepstream:7.0-gc-triton-devel
docker exec -it <container_id_or_name> /bin/bash
```

Exec into the container and install the required packages for the project.
```bash
pip install -r requirements.txt
```

## Usage
Start FastAPI
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload 
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MQ ICT Solutions](https://mqsolutions.vn/)