# SVG to GeoJSON Converter

This Python script converts SVG files to GeoJSON format. It extracts path data from SVG files and converts them into GeoJSON features.

## Requirements

- Python 3.x
- svgpathtools
- geojson

Install the required packages using:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python svg_to_geojson.py <input_svg_file> <output_geojson_file>
```

Example:
```bash
python svg_to_geojson.py input.svg output.geojson
```

## Features

- Converts SVG paths to GeoJSON LineString features
- Preserves SVG path attributes as feature properties
- Outputs a properly formatted GeoJSON FeatureCollection

## Linux Deployment

### System Requirements

- Linux operating system
- Internet connection (for downloading Docker)
- At least 512MB RAM
- 1GB available disk space

### Quick Deployment

1. Clone the project:
```bash
git clone <your-repository-url>
cd forgeojson
```

2. Run the deployment script:
```bash
chmod +x deploy.sh
./deploy.sh
```

3. Access the service:
Open a browser and access http://localhost:8881

### Manual Deployment Steps

If you do not want to use the deployment script, you can manually execute the following steps:

1. Install Docker and Docker Compose (if not already installed)

2. Create the necessary directories:
```bash
mkdir -p uploads
chmod 777 uploads
```

3. Build and start the service:
```bash
docker-compose up --build -d
```

### Usage

1. Access http://localhost:8881
2. Click the "Choose File" button to select an SVG file
3. Click the "Upload and Convert" button
4. Wait for the conversion to complete and download the JSON file

### File Explanation

- `app.py`: Web application main program
- `Dockerfile`: Docker image build file
- `docker-compose.yml`: Docker Compose configuration file
- `deploy.sh`: Automatic deployment script
- `requirements.txt`: Python dependency file

### Common Issues

1. If you encounter permission issues:
```bash
sudo chown -R $USER:$USER uploads/
```

2. If you need to view logs:
```bash
docker-compose logs
```

3. If you need to restart the service:
```bash
docker-compose restart
```

### Security Notes

- The service runs using a non-root user
- Upload directory permissions are properly configured
- Container health checks are configured
- Log rotation is configured

### Maintenance

- Check container status: `docker-compose ps`
- Stop the service: `docker-compose down`
- Update the service: `docker-compose up --build -d`
