# OCI Instance Monitoring Script

This Python script collects **CPU and Memory utilization metrics** for multiple Oracle Cloud Infrastructure (OCI) compute instances and outputs the data in a structured JSON format.

It uses the **OCI Python SDK** to fetch:
- Instance metadata
- Oracle Cloud Agent status
- CPU utilization
- Memory utilization

---

## 🚀 Features

- 🔍 Reads multiple instance OCIDs from a file  
- 📈 Fetches latest CPU & Memory usage (last 5 minutes)  
- 🤖 Checks Oracle Cloud Agent monitoring status  
- 🧾 Outputs clean JSON for further processing or dashboards  
- ⚡ Efficient and scalable for multiple instances  

---

## 🧰 Prerequisites

Make sure you have:

- Python 3.7+
- OCI Python SDK installed  
  ```bash
  pip install oci
````

* OCI config file (`~/.oci/config`) properly set up
* Required IAM permissions:

  * `inspect instances`
  * `read metrics`

---

## 📂 File Structure

```
.
├── script.py
├── all_instances.txt
└── README.md
```

---

## 📝 Input File

### `all_instances.txt`

Contains a list of **instance OCIDs**, one per line:

```
ocid1.instance.oc1...
ocid1.instance.oc1...
```

---

## ⚙️ Configuration

Update your OCI config profile inside the script:

```python
config = oci.config.from_file("~/.oci/config", "SPB")
```

Replace `"SPB"` with your profile name if needed.

---

## ▶️ Usage

Run the script:

```bash
python script.py
```

---

## 📤 Output

The script prints JSON output like this:

```json
[
  {
    "DisplayName": "my-instance",
    "MachineStatus": "RUNNING",
    "UsageOCPU": "12.45%",
    "UsageMemory": "65.23%",
    "OracleAgent": "RUNNING",
    "AvailabilityDomain": "XYZ-AD-1",
    "CompartmentID": "ocid1.compartment...",
    "TimeUTC": "2026-04-01 10:00:00 UTC",
    "InstanceOCID": "ocid1.instance..."
  }
]
```

---

## 🧠 How It Works

1. Reads instance OCIDs from file
2. Fetches instance details using Compute API
3. Checks if **Compute Instance Monitoring plugin** is enabled
4. Queries metrics from OCI Monitoring:

   * `CpuUtilization`
   * `MemoryUtilization`
5. Aggregates latest datapoint (mean over 5 minutes)
6. Outputs structured JSON

---

## ⚠️ Notes

* Memory metrics require **Oracle Cloud Agent** to be enabled
* If no metrics are available, values default to `0.0%`
* Ensure instances are actively sending metrics

---

## 🔮 Future Improvements

* Export to CSV / Excel
* Push data to Grafana / Prometheus
* Add alerts for high CPU/Memory usage
* Parallel processing for faster execution

---

## 🤝 Contributing

Feel free to fork this repo and submit pull requests for improvements.

---

## 📄 License

This project is licensed under the MIT License.

```
```
