import os

# Base config content
base_config = """topic_camera: "/dope/webcam/image_raw"
topic_camera_info: "/dope/webcam/camera_info"
topic_publishing: "dope"
input_is_rectified: True
downscale_height: 480

weights: {
%s
}

architectures: {
%s
}

dimensions: {
%s
}

class_ids: {
%s
}

draw_colors: {
%s
}



mesh_scales: {
%s
}

thresh_angle: 0.5
thresh_map: 0.0001
sigma: 3
thresh_points: 0.1
"""

# Define full object data
objects_data = {
    "obj_1": {
        "weight": "/weights/net_weights.pth",
        "architecture": "dope",
        "dimension": [15.899969482421875, 24.85395050048828, 7.419580078125],
        "class_id": 1,
        "color": [255, 0, 0],
        "scale": 0.001
    },
    "obj_2": {
        "weight": "/weights/net_weights.pth",
        "architecture": "dope",
        "dimension": [6.614794921875, 20.2759033203125, 6.6885009765625],
        "class_id": 2,
        "color": [0, 255, 0],
        "scale": 0.001
    },
    "obj_3": {
        "weight": "/weights/net_weights.pth",
        "architecture": "dope",
        "dimension": [9.778550720214844, 42.2700012207031255, 7.41875],
        "class_id": 3,
        "color": [0, 0, 255],
        "scale": 0.001
    },
    "obj_4": {
        "weight": "/weights/net_weights.pth",
        "architecture": "dope",
        "dimension": [6.580763, 11.633094, 7.075945],
        "class_id": 4,
        "color": [255, 255, 0],
        "scale": 0.001
    },
    "obj_5": {
        "weight": "/weights/net_weights.pth",
        "architecture": "dope",
        "dimension": [18.394457, 24.826819999999998, 2.7396],
        "class_id": 5,
        "color": [255, 0, 255],
        "scale": 0.001
    }
}

# Unique object IDs per scene
scene_objects = {
    "000001": [1],
    "000002": [1, 3],
    "000003": [3],
    "000004": [2, 4, 5],
    "000005": [2, 4, 5],
    "000006": [2, 4, 5],
    "000007": [2, 4],
    "000008": [2, 4, 5]
}

# Helper to format dict entries with comments for missing objects
def format_entries(scene_id, field):
    entries = []
    used_ids = scene_objects[scene_id]
    for obj, data in objects_data.items():
        obj_id = data["class_id"]
        line = f'"{obj}": {data[field]}'
        if obj_id not in used_ids:
            line = "# " + line
        entries.append(line)
    return ",\n    ".join(entries)

# Create config files
output_dir = "./"
for scene_id in scene_objects:
    weights = format_entries(scene_id, "weight")
    architectures = format_entries(scene_id, "architecture")
    dimensions = format_entries(scene_id, "dimension")
    class_ids = format_entries(scene_id, "class_id")
    draw_colors = format_entries(scene_id, "color")
    mesh_scales = format_entries(scene_id, "scale")

    config_text = base_config % (
        "    " + weights,
        "    " + architectures,
        "    " + dimensions,
        "    " + class_ids,
        "    " + draw_colors,
        "    " + mesh_scales
    )

    file_name = os.path.join(output_dir, f"config_pose_{scene_id}.yaml")
    with open(file_name, "w") as f:
        f.write(config_text)

    print(f"Wrote {file_name}")
