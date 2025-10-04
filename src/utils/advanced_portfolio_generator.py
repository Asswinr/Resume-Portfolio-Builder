"""
Advanced Portfolio Generator with Handlebars-like template support
"""
import re
from typing import Dict, Any, List
from pathlib import Path


import re
from typing import Dict, Any, List
from pathlib import Path
import html

def render_template(template_content: str, data: Dict[str, Any]) -> str:
    """
    Render a handlebars-like template with the provided data
    """
    content = template_content
    
    # Handle simple variable replacements
    for key, value in data.items():
        if isinstance(value, (str, int, float, bool)):
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, html.escape(str(value)))
    
    # Handle nested objects (e.g., personal_info.name)
    def replace_nested_placeholders(content: str, data: Dict[str, Any], prefix: str = "") -> str:
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                content = replace_nested_placeholders(content, value, full_key)
            elif isinstance(value, (str, int, float, bool)):
                placeholder = f"{{{{{full_key}}}}}"
                content = content.replace(placeholder, html.escape(str(value)))
        return content
    
    content = replace_nested_placeholders(content, data)
    
    # Handle conditional blocks {{#if condition}}...{{/if}}
    if_pattern = r'{{#if\s+([^}]+)}}([\s\S]*?){{/if}}'
    for match in re.finditer(if_pattern, content):
        condition_key = match.group(1).strip()
        block_content = match.group(2)
        
        # Check if condition is truthy
        condition_value = get_nested_value(data, condition_key)
        if condition_value:
            content = content.replace(match.group(0), block_content)
        else:
            content = content.replace(match.group(0), "")
    
    # Handle each loops {{#each array}}...{{/each}}
    each_pattern = r'{{#each\s+([^}]+)}}([\s\S]*?){{/each}}'
    for match in re.finditer(each_pattern, content):
        array_key = match.group(1).strip()
        block_content = match.group(2)
        
        array_data = get_nested_value(data, array_key)
        if isinstance(array_data, list):
            rendered_items = []
            for item in array_data:
                if isinstance(item, dict):
                    # Replace {{this.property}} with item values
                    item_content = block_content
                    for prop_key, prop_value in item.items():
                        item_content = item_content.replace(
                            f"{{{{this.{prop_key}}}}}", 
                            html.escape(str(prop_value))
                        )
                    item_content = item_content.replace("{{this}}", html.escape(str(item)))
                    rendered_items.append(item_content)
                else:
                    rendered_items.append(block_content.replace("{{this}}", html.escape(str(item))))
            
            content = content.replace(match.group(0), "\n".join(rendered_items))
        else:
            content = content.replace(match.group(0), "")
    
    return content


def get_nested_value(data: Dict[str, Any], key_path: str) -> Any:
    """
    Get nested value from dictionary using dot notation
    """
    keys = key_path.split('.')
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current


def generate_education_timeline(education_data: List[Dict[str, Any]]) -> str:
    """
    Generate HTML for education timeline
    """
    import html

    if not education_data:
        return ""
    
    timeline_items = []
    for edu in education_data:
        item = f"""
        <div class="timeline-item">
            <div class="timeline-content">
                <h3>{html.escape(edu.get('degree', ''))}</h3>
                <h4>{html.escape(edu.get('institution', ''))}</h4>
                <p class="timeline-date">{html.escape(edu.get('period', ''))}</p>
                <p>{html.escape(edu.get('description', ''))}</p>
            </div>
        </div>
        """
        timeline_items.append(item)
    
    return "\n".join(timeline_items)
def generate_experience_timeline(experience_data: List[Dict[str, Any]]) -> str:
    """
    Generate HTML for experience timeline
    """
    import html
    
    if not experience_data:
        return ""
    
    timeline_items = []
    for exp in experience_data:
        item = f"""
        <div class="timeline-item">
            <div class="timeline-content">
                <h3>{html.escape(exp.get('position', ''))}</h3>
                <h4>{html.escape(exp.get('company', ''))}</h4>
                <p class="timeline-date">{html.escape(exp.get('period', ''))}</p>
                <p>{html.escape(exp.get('description', ''))}</p>
                <ul class="responsibilities">
                    {''.join(f'<li>{html.escape(resp)}</li>' for resp in exp.get('responsibilities', []))}
                </ul>
            </div>
def generate_projects_timeline(projects_data: List[Dict[str, Any]]) -> str:
    """
    Generate HTML for projects grid
    """
    import html
    from urllib.parse import urlparse

    def is_safe_url(url: str) -> bool:
        """Check if URL uses a safe scheme"""
        if not url:
            return False
        try:
            parsed = urlparse(url)
            return parsed.scheme in ("http", "https")
        except Exception:
            return False

    if not projects_data:
        return ""
    
    project_items = []
    for project in projects_data:
        github_url = project.get("github_url", "")
        live_url   = project.get("live_url", "")

        item = f"""
        <div class="project-card">
def generate_portfolio_html(user_data: Dict[str, Any], css_content: str = '', js_content: str = '') -> str:
    """
    Generate complete portfolio HTML using the template and user data
    """
    # Load template
    template_path = Path(__file__).parent.parent / "pages" / "portfolio_template.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Generate dynamic content
    education_timeline = generate_education_timeline(user_data.get('education', []))
    experience_timeline = generate_experience_timeline(user_data.get('experience', []))
    projects_timeline = generate_projects_timeline(user_data.get('projects', []))

    # Prepare data for template rendering
    template_data = {
        **user_data,
        'education_timeline': education_timeline,
        'experience_timeline': experience_timeline,
        'projects_timeline': projects_timeline,
        'css_content': css_content,
        'js_content': js_content
    }

    # Render template
    return render_template(template_content, template_data)