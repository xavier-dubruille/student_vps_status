from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("vps_status_fetch"),
    autoescape=select_autoescape()
)

template = env.get_template("status.html")
print(template.render(the="variables", go="here"))
