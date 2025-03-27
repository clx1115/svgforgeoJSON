import sys
import os
from svgpathtools import svg2paths
from geojson import Feature, FeatureCollection, Polygon, LineString
import json

def transform_coordinates(x, y, control_point=None, scale=None):
    """
    使用简化的变换方法转换坐标
    
    Args:
        x, y: SVG坐标
        control_point: 控制点，格式为 (x,y,lon,lat)，表示SVG上的一个点及其对应的经纬度
        scale: 缩放比例，格式为 (scale_x, scale_y)，表示x和y方向上的缩放比例
    """
    if control_point is None:
        # 默认控制点，将SVG坐标映射到合理的经纬度范围
        control_point = (185.39, 289.54, -117.716728, 33.683458)  # 左上角点
        scale = (0.0000163, -0.0000127)  # 默认缩放比例
    
    # 提取控制点和缩放比例
    x1, y1, lon1, lat1 = control_point
    scale_x, scale_y = scale
    
    # 转换坐标
    lon = lon1 + (x - x1) * scale_x
    lat = lat1 + (y - y1) * scale_y
    
    return lon, lat

def extract_path_points(path):
    """提取路径的所有点"""
    points = []
    for segment in path:
        # 添加起点
        start_x, start_y = segment.start.real, segment.start.imag
        points.append((start_x, start_y))
        
        # 添加终点
        end_x, end_y = segment.end.real, segment.end.imag
        points.append((end_x, end_y))
    return points

def svg_to_geojson(svg_file, output_file, control_point=None, scale=None):
    """
    将SVG转换为GeoJSON
    
    Args:
        svg_file (str): SVG文件路径
        output_file (str): 输出JSON文件路径
        control_point: 控制点，用于坐标转换
        scale: 缩放比例，用于坐标转换
    """
    try:
        # 解析SVG文件
        paths, attributes = svg2paths(svg_file)
        
        features = []
        
        # 处理每个路径
        for path, attr in zip(paths, attributes):
            # 提取路径点
            svg_points = extract_path_points(path)
            
            # 转换为地理坐标
            geo_points = []
            for x, y in svg_points:
                lon, lat = transform_coordinates(x, y, control_point, scale)
                geo_points.append([lon, lat])
            
            # 移除重复的连续点
            filtered_points = [geo_points[i] for i in range(len(geo_points)) 
                             if i == 0 or geo_points[i] != geo_points[i-1]]
            
            # 如果路径闭合，创建多边形；否则创建线段
            if filtered_points and filtered_points[0] == filtered_points[-1]:
                geometry = Polygon([filtered_points])
            else:
                geometry = LineString(filtered_points)
            
            # 创建Feature
            properties = dict(attr)
            properties['svg_type'] = 'path'
            feature = Feature(geometry=geometry, properties=properties)
            features.append(feature)
        
        # 创建FeatureCollection
        feature_collection = FeatureCollection(features)
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(feature_collection, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully converted {svg_file} to {output_file}")
        
    except Exception as e:
        print(f"Error converting SVG to GeoJSON: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python svg_to_geojson.py <input_svg_file> <output_json_file>")
        sys.exit(1)
    
    svg_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # 确保输出文件使用.json后缀
    if not output_file.endswith('.json'):
        output_file = os.path.splitext(output_file)[0] + '.json'
    
    # 使用默认控制点和缩放比例进行转换
    svg_to_geojson(svg_file, output_file)
