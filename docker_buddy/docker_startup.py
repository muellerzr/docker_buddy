# AUTOGENERATED! DO NOT EDIT! File to edit: 01_docker.ipynb (unless otherwise specified).

__all__ = ['inspect_container']

# Cell
from rich import print as rprint
from rich.table import Table
from .cli_colors import _run, console
from fastcore.script import call_parse, Param

# Cell
def _parse_arguments(args:str):
    "Seperates out additional arguments for an image, and grabs their default values"
    sets = []
    is_pair = False
    curr_pair = []
    for word in args:
        if word.startswith('-'):
            if is_pair:
                curr_pair[0] += f', {word}'
            else:
                is_pair = True
                curr_pair.append(word)
            continue
        elif is_pair:
            curr_pair.append(word)
            is_pair = False
            sets.append(curr_pair)
            curr_pair = []
    return sets

# Cell
def _format_inspection(inspection:str):
    "Formats prettily an inspection from rekcod for an image"
    _color_a, _color_b, _color_c = "#0C7BDC", "#40B0A6", "#0C7BDC"
    image_name, _, command = inspection.split('\n')
    start_cmd = command.split('-')[0]
    s = f'[bold {_color_a}]Image[/bold {_color_a}]: {image_name}\n\n[bold {_color_a}]Command for Running Container[/bold {_color_a}]: {start_cmd}\n\n'
    s += f'[bold {_color_a}]Possible Arguments:[/bold {_color_a}]'
    table = Table(show_header=True, header_style=f'bold {_color_a}', show_lines=True)
    table.add_column('Argument(s)', justify="center")
    table.add_column('Value', justify='Center')
    sets = _parse_arguments(command.split(' '))
    for arg, val in sets:
        if ',' in arg:
            def _add_color(o): return f'[{_color_b}]{o}[/{_color_b}]'
            arg = ','.join([_add_color(o) for o in arg.split(',')])
        else:
            arg = f'[{_color_b}]{arg}[/{_color_b}]'
        val = f'{val}'
        table.add_row(arg, val)
    return s,table

# Cell
@call_parse
def inspect_container(container_name:Param("The name of a downloaded DockerHub container", str)):
    "Reports all possible configuration values for a container"
    cmd = ['rekcod', container_name]
    res = _run(cmd)
    image_and_cmd, arguments = _format_inspection(res)
    console.print(image_and_cmd)
    console.print(arguments)