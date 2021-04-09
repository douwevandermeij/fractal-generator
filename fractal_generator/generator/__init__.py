import os
from shutil import rmtree

from dill.source import getsource
from jinja2 import Environment, PackageLoader, contextfilter, Markup

from fractal.core.utils.string import snake_to_camel, camel_to_snake

env = Environment(
    loader=PackageLoader('fractal_generator', 'generator/templates'),
)

from fractal_generator.modeler import Application


@contextfilter
def camel(context, value):
    result = snake_to_camel(value)
    if context.eval_ctx.autoescape:
        result = Markup(result)
    return result


env.filters['camel'] = camel


@contextfilter
def snake(context, value):
    result = camel_to_snake(value)
    if context.eval_ctx.autoescape:
        result = Markup(result)
    return result


env.filters['snake'] = snake


def write_file(template, filename, **context):
    with open(filename, 'w') as fp:
        fp.write(template.render(**context) + '\n')


def render(path, subdir, *, filename, **context):
    if subdir:
        path = os.path.join(path, subdir)
    os.makedirs(path, exist_ok=True)
    if subdir:
        template = env.get_template(os.path.join(subdir, f'{filename}.jinja2'))
    else:
        template = env.get_template(f'{filename}.jinja2')
    write_file(template, os.path.join(path, filename), **context)


def render_subdir(path, subdir, *, render_filename, template_filename, **context):
    if subdir:
        path = os.path.join(path, subdir, template_filename.split('.')[0])
    os.makedirs(path, exist_ok=True)
    if subdir:
        template = env.get_template(os.path.join(subdir, f'{template_filename}.jinja2'))
    else:
        template = env.get_template(f'{template_filename}.jinja2')
    write_file(template, os.path.join(path, render_filename), **context)


def generate(application: Application):
    path = os.path.join(os.getcwd(), application.name.lower())
    if os.path.exists(path):
        rmtree(path)

    render(path, '', filename='main.py', application=application)
    render(path, '', filename='context.py', application=application)
    render(path, '', filename='settings.py', application=application)

    render(path, 'domain', filename='entities.py', application=application)
    render(path, 'domain', filename='repositories.py', application=application)
    render(path, 'domain', filename='exceptions.py', application=application)
    render(path, 'domain', filename='contracts.py', application=application)
    render(path, 'domain', filename='events.py', application=application)
    render(path, 'domain', filename='services.py', application=application,
           services=application.internal_services + application.ingress_services + application.egress_services)
    for entity in application.entities:
        for command in entity.commands:
            render_subdir(path, 'domain', render_filename=camel_to_snake(command.name + entity.name) + '.py',
                          template_filename='commands.py', application=application, entity=entity, command=command,
                          process_actions_source=getsource(command.process_actions) if command.process_actions else None)

    render(path, 'adapters', filename='repositories.py', application=application)
    render_subdir(path, 'adapters', render_filename='ingress.py',
                  template_filename='services.py', application=application, services=application.ingress_services)
    render_subdir(path, 'adapters', render_filename='egress.py',
                  template_filename='services.py', application=application, services=application.egress_services)

    if application.contrib:
        if application.contrib["name"] == "fastapi":
            render(path, 'contrib/fastapi', filename='main.py', application=application)
