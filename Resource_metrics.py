import oci
from datetime import datetime, timezone, timedelta
import json

# ---- CONFIG ----
config = oci.config.from_file("~/.oci/config", "SPB")
compute_client = oci.core.ComputeClient(config)
monitoring_client = oci.monitoring.MonitoringClient(config)

# ---- STEP 0: Read instance OCIDs from file ----
with open("all_instances.txt", "r") as f:
    instance_ocids = [line.strip() for line in f if line.strip()]

# ---- STEP 1: Helper to get latest metric value (Mean over last 5 min) ----
def get_metric_value(namespace, query, compartment_id, start_seconds=300, end_seconds=0):
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(seconds=start_seconds)
    end_time = now - timedelta(seconds=end_seconds)

    response = monitoring_client.summarize_metrics_data(
        compartment_id=compartment_id,
        summarize_metrics_data_details=oci.monitoring.models.SummarizeMetricsDataDetails(
            namespace=namespace,
            query=query,
            start_time=start_time,
            end_time=end_time,
            resolution="1m"
        )
    )

    if response.data and response.data[0].aggregated_datapoints:
        latest = response.data[0].aggregated_datapoints[-1]
        return float(latest.value)

    return 0.0

# ---- STEP 2: Loop over all instances ----
all_instances_data = []

for instance_ocid in instance_ocids:
    try:
        # Get instance details
        instance = compute_client.get_instance(instance_ocid).data
        compartment_id = instance.compartment_id

        # Check Oracle Agent status
        agent_plugins = {p.name: p.desired_state for p in instance.agent_config.plugins_config}
        oracle_agent_status = "RUNNING" if agent_plugins.get("Compute Instance Monitoring") == "ENABLED" else "DISABLED"

        # ---- FIX: Use resourceId filter instead of availabilityDomain ----
        cpu_query = f'CpuUtilization[1m]{{resourceId="{instance_ocid}"}}.mean()'
        memory_query = f'MemoryUtilization[1m]{{resourceId="{instance_ocid}"}}.mean()'

        # Fetch metrics
        cpu_value = get_metric_value("oci_computeagent", cpu_query, compartment_id, start_seconds=300)
        memory_value = get_metric_value("oci_computeagent", memory_query, compartment_id, start_seconds=300)

        # Prepare output for this instance
        instance_data = {
            "DisplayName": instance.display_name,
            "MachineStatus": instance.lifecycle_state,
            "UsageOCPU": f"{cpu_value:.2f}%",
            "UsageMemory": f"{memory_value:.2f}%",
            "OracleAgent": oracle_agent_status,
            "AvailabilityDomain": instance.availability_domain,
            "CompartmentID": compartment_id,
            "TimeUTC": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "InstanceOCID": instance.id
        }

        all_instances_data.append(instance_data)

    except Exception as e:
        print(f"Error fetching data for {instance_ocid}: {e}")

# ---- Final JSON output ----
print(json.dumps(all_instances_data, indent=2))
