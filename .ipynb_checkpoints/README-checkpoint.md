# Senior Data Analyst Hiring Challenge EDITED
👋 Welcome to Gigs' Senior Data Analyst take-home challenge!
> We will never use the code you provide for anything outside of the interview process! 

You will be working with real, yet anonymized data and will answer questions previously asked by stakeholders.

## Overview
This assignment assesses your business acumen, data analysis skills, and ability to derive actionable insights from telecom usage data. Data loading is handled for you using Jupyter Notebook with DuckDB.

**Time Expectation:** Timebox to 3-4 hours. You may outline additional analysis points you'd tackle with more time.

## About Gigs
Gigs is a platform that lets any business offer phone plans to their users - just like adding payments via Stripe. We provide APIs and tools to power mobile connectivity behind the scenes.

We operate in a B2B2C model: our customers offer these plans to their own end users. As a result, usage behaviour can vary significantly across customer types and verticals.

Gigs supports two main integration modes:
* Connect (White-Label Checkout): Our fully hosted onboarding and checkout experience. This is ideal for businesses that want to go live fast without needing to build telecom flows from scratch.
* API Integration: Gives customers full control to embed Gigs' telecom functionality directly into their own product or backend, allowing for highly customized experiences.

## Business Case
The Connectivity team wants to better understand usage patterns to optimize plan offerings and identify growth opportunities: 
- How much data does a subscription typically consume?
- How does usage look like at different plan data allowances?
- Do subscriptions typically consume consistent amounts of data throughout their lifetime? 

On top of that, the Head of Product approached you:
- Compare the retention pattern for the most recently launched project versus the two older ones.

List follow-up questions for stakeholders and state your assumptions. Note where you'd dive deeper with more time.

## Data Dictionary

### 1. usage_by_subscription_period.csv
| Column Name | Description |
|-------------|-------------|
| subscription_id | Unique identifier for each subscription |
| project_id__hashed | Project identifier |
| plan_id | Plan identifier |
| reporting_date | Reporting date to which maps to subscription_period_end and usage rolls up to  |
| subscription_period_start | Start date of the subscription period |
| subscription_period_end | End date of the subscription period |
| subscription_period_number | Sequential number of the subscription period |
| cumulative_data_usage_megabyte | Total data usage in megabytes for the period |
| cumulative_voice_usage_minutes | Total voice usage in minutes for the period |
| cumulative_sms_usage | Total SMS usage count for the period |
| number_of_addons_activated | Number of add-ons activated during the period |

### 2. plan_change_events.csv
| Column Name | Description |
|-------------|-------------|
| plan_id | Unique identifier for each plan |
| project_id__hashed | Project identifier |
| plan_created_at | Timestamp when the plan was first created |
| event_type | Type of plan event (created, updated, published, archived) |
| event_timestamp | Timestamp when the event occurred |
| plan_name | Display name of the plan |
| network_provider_id | Identifier for the network provider |
| price_currency | Currency code for plan pricing (e.g., USD) |
| plan_price_amount_local | Plan price in local currency |
| data_allowance_mb | Data allowance in megabytes (null if unlimited) |
| is_unlimited_data | Whether the plan has unlimited data allowance |
| voice_allowance_seconds | Voice allowance in seconds (null if unlimited) |
| is_unlimited_voice | Whether the plan has unlimited voice |
| sms_allowance | SMS allowance count (null if unlimited) |
| is_unlimited_sms | Whether the plan has unlimited SMS |
| validity_value | Plan validity duration value |
| validity_unit | Plan validity duration unit (day, month) |
| _valid_from | Start of validity period for event |
| _valid_to | End of validity period for this event |
| _is_current_state | Whether this is the current state of the plan |

### 3. projects.csv
| Column Name | Description |
|-------------|-------------|
| project_id__hashed | Unique identifier for each project |
| project_type | Type of project integration (API, Connect) |
| organization_name | Name of the organization using the project |
| device_type | Type of devices supported (Phones, Wearables) |



Feel free to also consult our API documentation: https://developers.gigs.com/

## Deliverable

Submit the following in a **forked repository**:
1. **Completed Jupyter notebook** with your analysis, SQL queries and code, and visualisation and findings
2. **Documentation of finding** A supporting written summary of your findings (typically sent in Slack to stakeholders). Not more than 1 page.

### Evaluation Criteria
We evaluate business understanding, technical skills, communication and problem solving equally.

We'll review your notebook, code quality, and analytical approach. AI tools are encouraged - highlight how you used them.


## Setup Instructions

### Prerequisites
- Python 3.9+ 
- `uv` for dependency management (installed below if not available)
- This was tested on MacOS, if you use a different OS you might have to consult Google if things don't immediately work.

### Quick Start
1. **Fork and clone repository:**

2. **Install uv:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
   # Or: pip install uv
   ```

3. **Create virtual environment and install dependencies:**
   ```bash
   # Create virtual environment
   uv venv
   
   # Activate virtual environment
   source .venv/bin/activate  
   # On Windows: .venv\Scripts\activate
   
   # Install dependencies (includes Jupyter, DuckDB, JupySQL, etc.)
   uv pip install -r requirements.txt
   ```

4. **Start analysis:**
   ```bash
   python setup.py  # Or: jupyter lab
   ```
   Open `analysis.ipynb` to begin

### **Good luck! We're excited to see your analysis and insights.**

For questions about the assignment (not technical setup), please reach out to your hiring contact.