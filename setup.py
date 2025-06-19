#!/usr/bin/env python3
"""
Environment Verification Script for Gigs Data Analyst Challenge
This script validates that your environment is properly set up for the analysis.
"""

import os
import sys
import subprocess
import duckdb
import re
import json
from typing import Dict, List, Tuple, Optional


# Configuration - centralized hardcoded values
CONFIG = {
    "data_files": [
        "data/usage_by_subscription_period.csv",
        "data/plan_change_events.csv", 
        "data/projects.csv",
    ],
    "notebook_path": "analysis.ipynb",
    "required_duckdb_version": (1, 2),  # (major, minor)
    "required_packages": {
        "duckdb": "DuckDB Python client",
        "sql": "JupySQL magic commands", 
        "pandas": "Pandas for data manipulation",
        "jupyter": "Jupyter notebook",
        "duckdb_engine": "DuckDB SQLAlchemy engine",
    }
}


def check_uv_installed():
    """Check if uv is installed and available"""
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ uv is installed: {result.stdout.strip()}")
            return True
        else:
            print("⚠️  uv is not working properly (optional)")
            return True  # Don't fail on this
    except FileNotFoundError:
        print("⚠️  uv is not installed (optional)")
        print("💡 Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return True  # Don't fail on this


def check_virtual_env():
    """Check if we're in a virtual environment"""
    in_venv = (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
        or os.environ.get("VIRTUAL_ENV") is not None
    )

    if in_venv:
        venv_path = os.environ.get("VIRTUAL_ENV", "detected")
        print(f"✅ Running in virtual environment: {os.path.basename(venv_path)}")
        return True
    else:
        print("⚠️  Not in a virtual environment (recommended)")
        print("💡 Create with: uv venv && source .venv/bin/activate")
        return True  # Don't fail on this


def check_jupyter_packages():
    """Check if required Jupyter packages are installed"""
    print("📦 Checking required packages...")
    missing_packages = []

    for package, description in CONFIG["required_packages"].items():
        try:
            if package == "duckdb_engine":
                import duckdb_engine
            else:
                __import__(package)
            print(f"✅ {package}: {description}")
        except ImportError:
            print(f"❌ Missing {package}: {description}")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n❌ Missing packages: {missing_packages}")
        print("💡 Install with: uv pip install -r requirements.txt")
        return False

    return True


def check_duckdb_version():
    """Check if DuckDB version supports required features"""
    try:
        import duckdb

        version = duckdb.__version__
        print(f"✅ DuckDB version: {version}")

        # Extract version number using regex - handle various formats
        version_match = re.search(r"v?(\d+)\.(\d+)(?:\.(\d+))?", version)

        if not version_match:
            print("❌ Could not parse DuckDB version")
            return False

        major, minor = int(version_match.group(1)), int(version_match.group(2))
        required_major, required_minor = CONFIG["required_duckdb_version"]

        if major > required_major or (major == required_major and minor >= required_minor):
            print("✅ DuckDB version supports required features")
            return True
        else:
            print(f"❌ DuckDB version too old (need {required_major}.{required_minor}+)")
            print("💡 Please upgrade with: uv pip install duckdb --upgrade")
            return False
    except Exception as e:
        print(f"❌ Error checking DuckDB version: {e}")
        return False


def verify_data_files():
    """Verify all required data files exist"""
    print("📁 Verifying data files...")
    missing_files = []
    
    for file_path in CONFIG["data_files"]:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"❌ Missing: {file_path}")
        else:
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"✅ Found {file_path} ({size_mb:.1f} MB)")

    if missing_files:
        print(f"\n❌ Missing data files: {missing_files}")
        print("💡 Make sure you're in the data-analyst directory")
        return False

    return True


def test_duckdb_integration() -> Tuple[bool, Dict[str, int]]:
    """Test that DuckDB works with the data files and return actual counts"""
    print("🧪 Testing DuckDB integration...")
    
    counts = {}

    try:
        # Test basic DuckDB functionality
        conn = duckdb.connect(":memory:")
        result = conn.execute("SELECT 'Hello from DuckDB!' as message").fetchone()[0]
        print(f"✅ DuckDB basic test: {result}")

        # Test data loading and get actual counts
        file_queries = [
            ("usage", "data/usage_by_subscription_period.csv"),
            ("plans", "data/plan_change_events.csv"), 
            ("projects", "data/projects.csv")
        ]
        
        for name, file_path in file_queries:
            try:
                count = conn.execute(f"SELECT COUNT(*) FROM '{file_path}'").fetchone()[0]
                counts[name] = count
                print(f"✅ {file_path}: {count:,} records")
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
                conn.close()
                return False, {}

        conn.close()
        return True, counts

    except Exception as e:
        print(f"❌ DuckDB integration test failed: {e}")
        return False, {}


def verify_starter_notebook():
    """Verify that the starter notebook exists and is valid"""
    print("📓 Verifying starter notebook...")

    notebook_path = CONFIG["notebook_path"]

    if not os.path.exists(notebook_path):
        print(f"❌ Starter notebook not found: {notebook_path}")
        print("💡 Make sure you're in the data-analyst directory")
        return False

    try:
        with open(notebook_path, "r") as f:
            notebook = json.load(f)

        if "cells" not in notebook:
            print("❌ Invalid notebook format")
            return False

        cell_count = len(notebook["cells"])
        sql_cells = [
            cell
            for cell in notebook["cells"]
            if cell.get("cell_type") == "code"
            and any("%%sql" in str(line) for line in cell.get("source", []))
        ]

        print(f"✅ Found {notebook_path}")
        print(f"✅ Notebook has {cell_count} cells ({len(sql_cells)} SQL cells)")
        return True

    except Exception as e:
        print(f"❌ Error reading notebook: {e}")
        return False


def check_jupyter_availability():
    """Check that Jupyter commands are available"""
    print("🔬 Checking Jupyter availability...")

    # Test jupyter lab
    try:
        result = subprocess.run(
            ["jupyter", "lab", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"✅ Jupyter Lab: {result.stdout.strip()}")
        else:
            print("❌ Jupyter Lab not working")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Jupyter Lab command not found")
        return False

    return True


def start_jupyter():
    """Start Jupyter Lab with the analysis starter notebook"""
    try:
        print(f"\n🚀 Starting Jupyter Lab with {CONFIG['notebook_path']}...")
        print("This will open your browser automatically.")
        print("If it doesn't open, navigate to the URL shown below.")
        print("\nPress Ctrl+C to stop Jupyter when you're done.\n")

        # Start Jupyter Lab with the starter notebook
        subprocess.run(["jupyter", "lab", CONFIG["notebook_path"]], check=True)

    except KeyboardInterrupt:
        print("\n👋 Jupyter Lab stopped.")
    except FileNotFoundError:
        print("❌ Jupyter Lab command not found")
        print("Trying regular Jupyter notebook...")
        try:
            subprocess.run(["jupyter", "notebook"], check=True)
        except Exception as e:
            print(f"❌ Could not start Jupyter: {e}")
            return False
    except Exception as e:
        print(f"❌ Error starting Jupyter: {e}")
        return False

    return True


def print_data_summary(counts: Dict[str, int]):
    """Print dynamic data summary based on actual counts"""
    print("\n📊 Data Summary:")
    
    if counts:
        # Dynamic summary based on actual data
        usage_count = counts.get("usage", 0)
        plans_count = counts.get("plans", 0) 
        projects_count = counts.get("projects", 0)
        
        print(f"   - Usage records: {usage_count:,}")
        print(f"   - Plan change events: {plans_count:,}")
        print(f"   - Project records: {projects_count:,}")
        
        # Try to get unique customers from usage data if possible
        try:
            conn = duckdb.connect(":memory:")
            unique_customers = conn.execute(
                "SELECT COUNT(DISTINCT customer_id) FROM 'data/usage_by_subscription_period.csv'"
            ).fetchone()[0]
            print(f"   - Unique customers: {unique_customers}")
            conn.close()
        except:
            pass  # If we can't get this info, that's ok
    else:
        # Fallback if counts couldn't be determined
        print("   - Data files verified but counts unavailable")


def main():
    """Main validation function"""
    print("🔍 Gigs Data Analyst Challenge - Environment Verification")
    print("=" * 60)

    # Optional checks (don't fail on these)
    check_uv_installed()
    check_virtual_env()

    print()

    # Required checks
    checks_passed = True
    data_counts = {}

    if not check_jupyter_packages():
        checks_passed = False

    if not check_duckdb_version():
        checks_passed = False

    if not verify_data_files():
        checks_passed = False

    # Get actual data counts
    duckdb_success, data_counts = test_duckdb_integration()
    if not duckdb_success:
        checks_passed = False

    if not verify_starter_notebook():
        checks_passed = False

    if not check_jupyter_availability():
        checks_passed = False

    print("\n" + "=" * 60)

    if checks_passed:
        print("✅ All validation checks passed! Environment is ready.")
        
        # Use dynamic data summary
        print_data_summary(data_counts)

        print("\n🚀 Ready to start your analysis!")
        print(f"   1. Open {CONFIG['notebook_path']} in Jupyter Lab")
        print("   2. Follow the setup cells to load data into DuckDB")
        print("   3. Start your analysis!")

        choice = input("\nStart Jupyter Lab now? (y/N): ").strip().lower()

        if choice == "y":
            start_jupyter()
        else:
            print("\n📝 To start analysis manually:")
            print("   jupyter lab")
            print(f"\n💡 Open {CONFIG['notebook_path']} to get started")
    else:
        print("❌ Some validation checks failed.")
        print("\n💡 Common fixes:")
        print("   - Install missing packages: uv pip install -r requirements.txt")
        print("   - Activate virtual environment: source .venv/bin/activate")
        print("   - Ensure you're in the data-analyst directory")

    print("=" * 60)


if __name__ == "__main__":
    main()
