import boto3
import json
import os
from datetime import datetime, timezone, timedelta

ec2 = boto3.client("ec2")
iam = boto3.client("iam")
s3 = boto3.client("s3")

BUCKET = os.environ["INVENTORY_BUCKET"]
REGION = os.environ.get("AWS_REGION", "us-east-1")
SNAPSHOT_THRESHOLD_DAYS = 30


def lambda_handler(event, context):
    timestamp = datetime.now(timezone.utc).isoformat()

    # -------------------
    # INVENTORY (Phase 1)
    # -------------------
    instances = ec2.describe_instances()
    volumes = ec2.describe_volumes()
    snapshots = ec2.describe_snapshots(OwnerIds=["self"])
    users = iam.list_users()

    instance_count = sum(
        len(reservation["Instances"])
        for reservation in instances["Reservations"]
    )

    inventory_summary = {
        "timestamp": timestamp,
        "region": REGION,
        "ec2_instances": instance_count,
        "ebs_volumes": len(volumes["Volumes"]),
        "snapshots": len(snapshots["Snapshots"]),
        "iam_users": len(users["Users"]),
    }

    write_to_s3(
        f"inventory/{timestamp}.json",
        inventory_summary
    )

    # -------------------
    # PHASE 2 — HYGIENE
    # -------------------

    orphaned_volumes = [
        {
            "volume_id": v["VolumeId"],
            "size_gb": v["Size"],
            "volume_type": v["VolumeType"],
            "create_time": v["CreateTime"].isoformat(),
        }
        for v in volumes["Volumes"]
        if v["State"] == "available"
    ]

    orphaned_report = {
        "timestamp": timestamp,
        "region": REGION,
        "total_orphaned_volumes": len(orphaned_volumes),
        "volumes": orphaned_volumes,
    }

    write_to_s3(
        f"hygiene/orphaned-ebs/{timestamp}.json",
        orphaned_report
    )

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=SNAPSHOT_THRESHOLD_DAYS)

    old_snapshots = [
        {
            "snapshot_id": s["SnapshotId"],
            "volume_id": s.get("VolumeId"),
            "start_time": s["StartTime"].isoformat(),
        }
        for s in snapshots["Snapshots"]
        if s["StartTime"] < cutoff_date
    ]

    snapshot_report = {
        "timestamp": timestamp,
        "region": REGION,
        "threshold_days": SNAPSHOT_THRESHOLD_DAYS,
        "total_old_snapshots": len(old_snapshots),
        "snapshots": old_snapshots,
    }

    write_to_s3(
        f"hygiene/old-snapshots/{timestamp}.json",
        snapshot_report
    )

    return {
        "status": "success",
        "inventory": inventory_summary,
        "orphaned_volumes": len(orphaned_volumes),
        "old_snapshots": len(old_snapshots),
    }


def write_to_s3(key, data):
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(data, indent=2),
        ContentType="application/json",
    )

