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
python svg_to_geojson.py altair-irvine.svg altair-irvine.json

```

## Features

- Converts SVG paths to GeoJSON LineString features
- Preserves SVG path attributes as feature properties
- Outputs a properly formatted GeoJSON FeatureCollection
