import json
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def deduce_status(percentage: float, critical_threshold=5.0, warning_threshold=0.0):
    """
    Returns 'critical', 'warning', or 'ok' based on the given percentage and thresholds.
    """
    if percentage > critical_threshold:
        return 'critical'
    elif percentage > warning_threshold:
        return 'warning'
    return 'ok'

def generate_json_report(results: dict, output_path: str):
    """
    Exports the data quality findings to a JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
        print(f"JSON Report successfully exported to {output_path}")

def generate_html_report(results: dict, template_dir: str, template_name: str, output_path: str):
    """
    Generates a human-readable HTML report using Jinja2 with color-coded warnings.
    """
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    
    # Pre-process the results to assign status colors based on thresholds
    
    # Process Nulls
    for col, data in results['nulls'].items():
        data['status'] = deduce_status(data['percentage'])
        
    # Process Duplicates
    results['duplicates']['status'] = deduce_status(results['duplicates']['percentage'], critical_threshold=2.0)
    
    # Process Outliers
    for col, data in results['outliers'].items():
        data['status'] = deduce_status(data['outlier_percentage'], critical_threshold=5.0)
        
    # Process Patterns
    for col, data in results['patterns'].items():
        data['status'] = deduce_status(data['invalid_percentage'], critical_threshold=2.0)
        
    # Rendering
    html_out = template.render(
        report_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        results=results
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_out)
        print(f"HTML Report successfully generated at {output_path}")

