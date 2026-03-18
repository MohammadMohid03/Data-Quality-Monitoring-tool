import click
import os
from dq_core.utils import load_data
from dq_core.checks import run_all_checks
from dq_core.reporters import generate_json_report, generate_html_report

@click.command()
@click.option('--file', required=True, help="Path to the input CSV file")
@click.option('--output', default='report.html', help="Path to save the HTML report")
def main(file, output):
    """
    Data Quality Monitoring Tool - Automatically scans any CSV dataset and produces 
    a detailed data quality report in HTML and JSON, mimicking pre-production data engineering checks.
    """
    click.secho(f"Initializing Data Quality Scan for: {file}", fg='cyan')
    
    # 1. Load Data
    try:
        df = load_data(file)
        click.echo(f"Successfully loaded data: {df.shape[0]} rows, {df.shape[1]} columns.")
    except Exception as e:
        click.secho(f"Error loading file: {str(e)}", fg='red')
        return

    # 2. Run Checks
    click.echo("Running data quality checks (Nulls, Duplicates, Types, Outliers, Patterns)...")
    results = run_all_checks(df)
    
    # 3. Generate Reports
    json_output = output.rsplit('.', 1)[0] + '.json'
    
    # Locate template dir (relative to this script)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, 'templates')
    
    click.echo("Generating reports...")
    generate_json_report(results, json_output)
    try:
        generate_html_report(results, template_dir, 'report_template.html', output)
    except Exception as e:
        click.secho(f"Error generating HTML report: {str(e)}", fg='red')
        return

    click.secho("Data Quality scanning completed successfully!", fg='green')
    click.echo(f"  - HTML Report: {output}")
    click.echo(f"  - JSON Log: {json_output}")

if __name__ == '__main__':
    main()
