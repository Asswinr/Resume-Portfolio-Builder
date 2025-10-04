"""
Advanced Portfolio Generator with Handlebars-like template support
"""
import re
from typing import Dict, Any, List
from pathlib import Path


def render_template(template_content: str, data: Dict[str, Any]) -> str:
    """
    Render a handlebars-like template with the provided data
    """
    content = template_content
    
    # Handle simple variable replacements
    for key, value in data.items():
        if isinstance(value, (str, int, float, bool)):
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))
    
    # Handle nested objects (e.g., personal_info.name)
    def replace_nested_placeholders(content: str, data: Dict[str, Any], prefix: str = "") -> str:
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                content = replace_nested_placeholders(content, value, full_key)
            elif isinstance(value, (str, int, float, bool)):
                placeholder = f"{{{{{full_key}}}}}"
                content = content.replace(placeholder, str(value))
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
                            str(prop_value)
                        )
                    item_content = item_content.replace("{{this}}", str(item))
                    rendered_items.append(item_content)
                else:
                    rendered_items.append(block_content.replace("{{this}}", str(item)))
            
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
    if not education_data:
        return ""
    
    timeline_items = []
    for edu in education_data:
        item = f"""
        <div class="timeline-item">
            <div class="timeline-content">
                <h3>{edu.get('degree', '')}</h3>
                <h4>{edu.get('institution', '')}</h4>
                <p class="timeline-date">{edu.get('period', '')}</p>
                <p>{edu.get('description', '')}</p>
            </div>
        </div>
        """
        timeline_items.append(item)
    
    return "\n".join(timeline_items)


def generate_experience_timeline(experience_data: List[Dict[str, Any]]) -> str:
    """
    Generate HTML for experience timeline
    """
    if not experience_data:
        return ""
    
    timeline_items = []
    for exp in experience_data:
        item = f"""
        <div class="timeline-item">
            <div class="timeline-content">
                <h3>{exp.get('position', '')}</h3>
                <h4>{exp.get('company', '')}</h4>
                <p class="timeline-date">{exp.get('period', '')}</p>
                <p>{exp.get('description', '')}</p>
                <ul class="responsibilities">
                    {''.join(f'<li>{resp}</li>' for resp in exp.get('responsibilities', []))}
                </ul>
            </div>
        </div>
        """
        timeline_items.append(item)
    
    return "\n".join(timeline_items)


def generate_projects_timeline(projects_data: List[Dict[str, Any]]) -> str:
    """
    Generate HTML for projects grid
    """
    if not projects_data:
        return ""
    
    project_items = []
    for project in projects_data:
        item = f"""
        <div class="project-card">
            <h3>{project.get('name', '')}</h3>
            <p class="project-description">{project.get('description', '')}</p>
            <div class="project-tech">
                {''.join(f'<span class="tech-tag">{tech}</span>' for tech in project.get('technologies', []))}
            </div>
            <div class="project-links">
                {f'<a href="{project.get("github_url", "")}" target="_blank" class="project-link">GitHub</a>' if project.get('github_url') else ''}
                {f'<a href="{project.get("live_url", "")}" target="_blank" class="project-link">Live Demo</a>' if project.get('live_url') else ''}
            </div>
        </div>
        """
        project_items.append(item)
    
    return "\n".join(project_items)


def generate_portfolio_html(user_data: Dict[str, Any], css_content: str = '', js_content: str = '') -> str:
    # Load template
    template_path = Path=__file__).parent.parent / "pages" / "portfolio_template.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Prepare template data
    template_data = {css_content: css_content, js_content: js_content}

    # Merge with user data
    template_data.update(user_data)

    # Render template
    return render_template(template_content, template_data)
    template_data = {}
    template = get_template('portfolio_template.html');
    # Embed CSS and JavaScript content directly into the template
    template_data['css_content'] = css_content
    template_data['js_content'] = js_content
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
        'projects_timeline': projects_timeline
    }
    
    # Render template
    return render_template(template_content, template_data)
    
    return final_html


def save_portfolio_html(html_content: str, output_path: str) -> None:
    """
    Save generated HTML to file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


# Example usage
if __name__ == "__main__":
    sample_data = {
        "personal_info": {
            "name": "John Doe",
            "role": "Full Stack Developer"
        },
        "about_me": {
            "biography": "Passionate developer with 5+ years of experience...",
            "skills": [
                {"name": "Python"},
                {"name": "JavaScript"},
                {"name": "React"},
                {"name": "Node.js"}
            ]
        },
        "education": [
            {
                "degree": "Bachelor of Science in Computer Science",
                "institution": "University of Technology",
                "period": "2015-2019",
                "description": "Graduated with honors"
            }
        ],
        "experience": [
            {
                "position": "Senior Developer",
                "company": "Tech Corp",
                "period": "2020-Present",
                "description": "Leading development teams",
                "responsibilities": ["Team leadership", "Code reviews", "Architecture design"]
            }
        ],
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Full-stack e-commerce solution",
                "technologies": ["React", "Node.js", "MongoDB"],
                "github_url": "https://github.com/johndoe/ecommerce",
                "live_url": "https://ecommerce.example.com"
            }
        ],
        "contact": {
            "email": "john.doe@example.com",
            "phone": "+1-555-0123",
            "linkedin": "https://linkedin.com/in/johndoe",
            "github": "https://github.com/johndoe",
            "twitter": "https://twitter.com/johndoe"
        }
    }
    
    html_output = generate_portfolio_html(sample_data)
    print("Portfolio generated successfully!")
    
    # Save to file
    save_portfolio_html(html_output, "sample_portfolio.html")