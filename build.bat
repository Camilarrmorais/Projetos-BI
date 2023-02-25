
cls

if "%ENV%" == "dev" (
    echo "Building DEV image."

    docker build --tag image-dev:0.0.1 --file Dockerfile.dev .

    echo "DEV image building completed successfully."
    )
else
    echo "Your ENV environment variable must be equal to 'dev' or 'prod'."
    echo "ENV=%ENV%"