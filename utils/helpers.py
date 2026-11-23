from typing import List

def convert_vertices_to_string(vertices: List[List[float]]) -> str:
    pairs = ",".join([f"{lon} {lat}" for lon, lat in vertices])
    return f"POLYGON(({pairs}))"
