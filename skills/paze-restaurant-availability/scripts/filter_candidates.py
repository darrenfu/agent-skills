#!/usr/bin/env python3
"""Filter PazeMap candidates by radius or a buffered driving route.

This helper only creates candidates. A candidate is not confirmed until the
Clover guest-checkout page visibly exposes Paze.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterable


DEFAULT_DATA_URL = "https://pazemap.com/data/paze_map.json"
DEFAULT_CORRIDOR_MILES = 0.4
DEFAULT_RADIUS_MILES = 4.0
EARTH_RADIUS_MILES = 3958.7613
USER_AGENT = "Codex-Paze-Restaurant-Availability/1.0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate PazeMap candidates for live Clover checkout verification."
    )
    parser.add_argument("--mode", choices=("radius", "route"), required=True)
    parser.add_argument("--origin-lat", type=float, required=True)
    parser.add_argument("--origin-lng", type=float, required=True)
    parser.add_argument("--radius-miles", type=float, default=DEFAULT_RADIUS_MILES)
    parser.add_argument("--corridor-miles", type=float, default=DEFAULT_CORRIDOR_MILES)
    parser.add_argument("--home-lat", type=float)
    parser.add_argument("--home-lng", type=float)
    parser.add_argument(
        "--route-geojson",
        type=pathlib.Path,
        help="GeoJSON LineString/MultiLineString for the authoritative route.",
    )
    parser.add_argument("--paze-data-url", default=DEFAULT_DATA_URL)
    parser.add_argument(
        "--paze-data-file",
        type=pathlib.Path,
        help="Read a local PazeMap JSON snapshot instead of fetching the URL.",
    )
    parser.add_argument("--limit", type=int, default=0, help="0 means no limit.")
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument("--format", choices=("json", "tsv"), default="json")
    args = parser.parse_args()

    if args.radius_miles <= 0:
        parser.error("--radius-miles must be positive")
    if args.corridor_miles <= 0:
        parser.error("--corridor-miles must be positive")
    if args.limit < 0:
        parser.error("--limit cannot be negative")
    if args.mode == "route" and args.route_geojson is None:
        if args.home_lat is None or args.home_lng is None:
            parser.error(
                "route mode requires --route-geojson or both --home-lat and --home-lng"
            )
    return args


def fetch_json(url: str, timeout: float) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def load_paze_data(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.paze_data_file:
        with args.paze_data_file.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    else:
        data = fetch_json(args.paze_data_url, args.timeout_seconds)
    if not isinstance(data, list):
        raise ValueError("PazeMap data must be a JSON array")
    return [record for record in data if isinstance(record, dict)]


def radians(value: float) -> float:
    return value * math.pi / 180.0


def haversine_miles(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = (
        math.sin(dlat / 2.0) ** 2
        + math.cos(radians(lat1))
        * math.cos(radians(lat2))
        * math.sin(dlng / 2.0) ** 2
    )
    return 2.0 * EARTH_RADIUS_MILES * math.asin(min(1.0, math.sqrt(a)))


def coordinates_from_geojson(value: Any) -> list[list[tuple[float, float]]]:
    if isinstance(value, dict) and value.get("type") == "FeatureCollection":
        lines: list[list[tuple[float, float]]] = []
        for feature in value.get("features", []):
            lines.extend(coordinates_from_geojson(feature))
        return lines
    if isinstance(value, dict) and value.get("type") == "Feature":
        return coordinates_from_geojson(value.get("geometry"))
    if not isinstance(value, dict):
        raise ValueError("route GeoJSON must be an object")

    geometry_type = value.get("type")
    coordinates = value.get("coordinates")
    if geometry_type == "LineString":
        return [[(float(lat), float(lng)) for lng, lat in coordinates]]
    if geometry_type == "MultiLineString":
        return [
            [(float(lat), float(lng)) for lng, lat in line] for line in coordinates
        ]
    raise ValueError("route GeoJSON must contain a LineString or MultiLineString")


def load_route(
    args: argparse.Namespace,
) -> tuple[list[list[tuple[float, float]]], dict[str, Any]]:
    if args.route_geojson:
        with args.route_geojson.open("r", encoding="utf-8") as handle:
            geojson = json.load(handle)
        return coordinates_from_geojson(geojson), {
            "provider": "provided GeoJSON",
            "proxy": False,
        }

    coordinates = (
        f"{args.origin_lng},{args.origin_lat};{args.home_lng},{args.home_lat}"
    )
    query = urllib.parse.urlencode(
        {
            "overview": "full",
            "geometries": "geojson",
            "alternatives": "false",
            "steps": "false",
        }
    )
    url = f"https://router.project-osrm.org/route/v1/driving/{coordinates}?{query}"
    payload = fetch_json(url, args.timeout_seconds)
    routes = payload.get("routes", []) if isinstance(payload, dict) else []
    if not routes:
        raise ValueError(f"OSRM returned no route: {payload!r}")
    route = routes[0]
    return coordinates_from_geojson(route["geometry"]), {
        "provider": "OSRM route proxy",
        "proxy": True,
        "distance_miles": round(float(route["distance"]) / 1609.344, 3),
        "duration_minutes": round(float(route["duration"]) / 60.0, 1),
    }


def projected_xy(
    lat: float, lng: float, reference_lat: float
) -> tuple[float, float]:
    return (
        lng * 69.172 * math.cos(radians(reference_lat)),
        lat * 69.0,
    )


def point_segment_distance_miles(
    point: tuple[float, float],
    start: tuple[float, float],
    end: tuple[float, float],
) -> float:
    reference_lat = (point[0] + start[0] + end[0]) / 3.0
    px, py = projected_xy(point[0], point[1], reference_lat)
    ax, ay = projected_xy(start[0], start[1], reference_lat)
    bx, by = projected_xy(end[0], end[1], reference_lat)
    dx, dy = bx - ax, by - ay
    denominator = dx * dx + dy * dy
    if denominator == 0:
        return math.hypot(px - ax, py - ay)
    position = ((px - ax) * dx + (py - ay) * dy) / denominator
    position = max(0.0, min(1.0, position))
    nearest_x = ax + position * dx
    nearest_y = ay + position * dy
    return math.hypot(px - nearest_x, py - nearest_y)


def point_route_distance_miles(
    point: tuple[float, float], lines: Iterable[list[tuple[float, float]]]
) -> float:
    best = math.inf
    for line in lines:
        if len(line) == 1:
            best = min(best, haversine_miles(*point, *line[0]))
            continue
        for start, end in zip(line, line[1:]):
            best = min(best, point_segment_distance_miles(point, start, end))
    return best


def has_paze_map_proxy(record: dict[str, Any]) -> bool:
    methods = {
        str(method).upper() for method in (record.get("paymentMethods") or [])
    }
    return bool({"APPLE_PAY", "GOOGLE_PAY"} & methods)


def valid_coordinate(value: Any, lower: float, upper: float) -> bool:
    return isinstance(value, (int, float)) and lower <= float(value) <= upper


def candidate_base(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "merchant_id": record.get("merchantId") or record.get("id"),
        "name": str(record.get("name") or "").strip(),
        "address": str(record.get("address") or "").strip(),
        "city": str(record.get("city") or "").strip(),
        "state": str(record.get("state") or "").strip(),
        "zip": str(record.get("zip") or "").strip(),
        "lat": float(record["lat"]),
        "lng": float(record["lng"]),
        "clover_url": record.get("orderUrl") or record.get("website"),
        "payment_methods": record.get("paymentMethods") or [],
        "pazemap_filter_proxy": True,
    }


def generate_candidates(
    args: argparse.Namespace,
    records: list[dict[str, Any]],
    route_lines: list[list[tuple[float, float]]] | None,
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for record in records:
        if not has_paze_map_proxy(record):
            continue
        if not valid_coordinate(record.get("lat"), -90.0, 90.0):
            continue
        if not valid_coordinate(record.get("lng"), -180.0, 180.0):
            continue
        clover_url = record.get("orderUrl") or record.get("website") or ""
        if "clover.com/online-ordering/" not in str(clover_url):
            continue

        lat = float(record["lat"])
        lng = float(record["lng"])
        candidate = candidate_base(record)
        if args.mode == "radius":
            distance = haversine_miles(
                args.origin_lat, args.origin_lng, lat, lng
            )
            if distance > args.radius_miles:
                continue
            candidate["distance_from_origin_miles"] = round(distance, 3)
            candidate["_sort_distance"] = distance
        else:
            assert route_lines is not None
            distance = point_route_distance_miles((lat, lng), route_lines)
            if distance > args.corridor_miles:
                continue
            candidate["distance_from_route_miles"] = round(distance, 3)
            candidate["_sort_distance"] = distance
        candidates.append(candidate)

    candidates.sort(key=lambda item: (item["_sort_distance"], item["name"]))
    for candidate in candidates:
        candidate.pop("_sort_distance", None)
    if args.limit:
        return candidates[: args.limit]
    return candidates


def output_tsv(candidates: list[dict[str, Any]], mode: str) -> None:
    distance_key = (
        "distance_from_origin_miles"
        if mode == "radius"
        else "distance_from_route_miles"
    )
    print(
        "\t".join(
            [
                "name",
                "address",
                "city",
                "state",
                distance_key,
                "clover_url",
            ]
        )
    )
    for candidate in candidates:
        print(
            "\t".join(
                str(candidate.get(key, ""))
                for key in (
                    "name",
                    "address",
                    "city",
                    "state",
                    distance_key,
                    "clover_url",
                )
            )
        )


def main() -> int:
    args = parse_args()
    route_lines: list[list[tuple[float, float]]] | None = None
    route_metadata: dict[str, Any] | None = None
    if args.mode == "route":
        route_lines, route_metadata = load_route(args)

    records = load_paze_data(args)
    candidates = generate_candidates(args, records, route_lines)
    if args.format == "tsv":
        output_tsv(candidates, args.mode)
        return 0

    result: dict[str, Any] = {
        "mode": args.mode,
        "origin": {"lat": args.origin_lat, "lng": args.origin_lng},
        "pazemap_filter_proxy": "paymentMethods contains APPLE_PAY or GOOGLE_PAY",
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    if args.mode == "radius":
        result["radius_miles"] = args.radius_miles
    else:
        result["corridor_miles"] = args.corridor_miles
        result["route"] = route_metadata
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, urllib.error.URLError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
