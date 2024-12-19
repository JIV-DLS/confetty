#!/bin/bash

# List of platforms to build for
platforms=(
    "linux/amd64"
    "linux/arm64"
    "linux/arm"
    "windows/amd64"
    "windows/arm64"
    "darwin/amd64"
    "darwin/arm64"
)

# Output directory
output_dir="./build"
mkdir -p "$output_dir"

# Build for each platform
for platform in "${platforms[@]}"; do
    IFS="/" read -r -a platform_split <<< "$platform"
    GOOS=${platform_split[0]}
    GOARCH=${platform_split[1]}
    output_name="$output_dir/popnglow-$GOOS-$GOARCH"
    if [ "$GOOS" = "windows" ]; then
        output_name+='.exe'
    fi

    echo "Building for $GOOS/$GOARCH..."
    env GOOS=$GOOS GOARCH=$GOARCH CGO_ENABLED=0 go build -o "$output_name" main.go
    if [ $? -ne 0 ]; then
        echo "An error occurred while building for $GOOS/$GOARCH! Aborting..."
        exit 1
    fi
done

echo "Builds completed. Binaries are in the $output_dir directory."