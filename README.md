# Economy Dashboard

An Economy Dashboard

## Project Structure

```text
economy-dashboard/
	app/
		__init__.py
		routes.py
		static/
			css/
				styles.css
		templates/
			base.html
			index.html
			bond_market.html
			stock_market.html
			real_estate_market.html
			global_market.html
	batch/
		common/
			data_sources.py
			openai_processor.py
		jobs/
			bond_job.py
			stock_job.py
			real_estate_job.py
			run_all.py
	run.py
	requirements.txt
```

## Python Environment

Create the Virtual Environment
```bash
python -m venv venv
```
Activate the Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux / MacOS
source venv/bin/activate
```

Install the Requirements
```bash
pip install -r requirements.txt
```

## Set Environment Variable for OpenAI API Key

```bash
# PowerShell
$env:OPENAI_API_KEY="your_openai_api_key"

# Windows
set OPENAI_API_KEY=your_openai_api_key

# Linux / MacOS
export OPENAI_API_KEY=your_openai_api_key
```

## Run The Web App

```bash
python run.py
```

Then open http://127.0.0.1:5000 in your browser.

## Run Batch Jobs

Run all batch jobs:

```bash
python -m batch.jobs.run_all
```

Run a single market job:

```bash
python -m batch.jobs.bond_job
python -m batch.jobs.stock_job
python -m batch.jobs.real_estate_job
```
