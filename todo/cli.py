import click
from .rule import TodoRule
from .manager import Manager
from .parser import parse_editor


EDITOR_HELP = """
// You must follow this format:
//
// TITLE
// # GROUP
// ? DUE DATE
//         (EMPTY LINE)
// COMMENT
// ...
//
// Lines which begin with double slashes ("//") is ignored. If you don't want to
// set the GROUP or the DUE DATE field, delete the whole line.
"""


@click.group()
@click.pass_context
def main(ctx: click.Context):
    ctx.ensure_object(Manager)


@main.command(help="List up TODOs.")
@click.option("--date", "-d", help="Pick up TODOs for the date.")
@click.option(
    "status", "--completed", "-c", flag_value=True, help="Show completed TODOs."
)
@click.option(
    "-c",
    "--completed",
    "status",
    flag_value="completed",
    help="Show completed TODOs.",
)
@click.option(
    "-u",
    "--uncompleted",
    "status",
    flag_value="uncompleted",
    default=True,
    help="Show uncompleted TODOs. (default)",
)
@click.option(
    "-p",
    "--not-planed",
    "status",
    flag_value="not-planed",
    help="Show TODOs marked as not-planed.",
)
@click.pass_context
def list(ctx: click.Context, date: str | None, status: str):
    manager: Manager = ctx.obj
    items = manager.instances(date, status)
    for i in items:
        click.echo(i.fmt_line())


@main.command(help="Show detailed information about a TODO.")
@click.argument("id", type=int)
@click.pass_context
def info(ctx: click.Context, id: int):
    manager: Manager = ctx.obj
    try:
        info = manager.info(id)
    except KeyError as e:
        click.echo(e, err=True)
        return 1
    else:
        click.echo(info.fmt_full())


@main.command(help="Create a new TODO.")
@click.option(
    "-i", "--interactive", is_flag=True, help="Create on this shell interactively."
)
@click.pass_context
def new(ctx: click.Context, interactive: bool):
    if interactive:
        title: str = click.prompt("title")
        group: str = click.prompt("group", default="")
        due_date: str = click.prompt("due date", default="")
        comment = ""
    else:
        txt = click.edit("\n\n" + EDITOR_HELP)
        if txt == None:
            return 0

        try:
            title, group, due_date, comment = parse_editor(txt)
        except SyntaxError as e:
            click.echo(e, err=True)
            return 1

    manager: Manager = ctx.obj
    try:
        id = manager.append(TodoRule(title, group, due_date, comment))
    except ValueError as e:
        click.echo(e, err=True)
        return 1
    else:
        click.echo(f"Created #{id} {title}")
    manager.save()


@main.command(help="Edit messages, or moves a TODO to another group.")
@click.argument("id", type=int)
@click.option(
    "-i", "--interactive", is_flag=True, help="Create on this shell interactively."
)
@click.pass_context
def edit(ctx: click.Context, id, interactive: bool):
    manager: Manager = ctx.obj
    try:
        item = manager.info(id)
    except KeyError as e:
        click.echo(e, err=True)
        return 1

    if interactive:
        title: str = click.prompt("title", default=item.title)
        group: str = click.prompt("group", default=item.group)
        due_date: str = click.prompt("due date", default=item.date)
        comment = item.comment
    else:
        txt = click.edit(item.fmt_editor() + "\n" + EDITOR_HELP)
        if txt == None:
            return 0

        try:
            title, group, due_date, comment = parse_editor(txt)
        except SyntaxError as e:
            click.echo(e, err=True)
            return 1

    try:
        manager.update(id, TodoRule(title, group, due_date, comment))
    except ValueError as e:
        click.echo(e, err=True)
        return 1
    else:
        manager.save()


@main.command(help="Mark a TODO as completed.")
@click.argument("id", type=int)
@click.option(
    "-c",
    "--completed",
    "status",
    flag_value="completed",
    default=True,
    help="Mark the TODO as completed. (default)",
)
@click.option(
    "-u",
    "--uncompleted",
    "status",
    flag_value="uncompleted",
    help="Mark the TODO as uncompleted instead.",
)
@click.option(
    "-p",
    "--not-planed",
    "status",
    flag_value="not-planed",
    help="Mark the TODO as not-planed instead. Useful if you want to skip one of the scheduled TODO series.",
)
@click.pass_context
def mark(ctx: click.Context, id: int, status: str):
    manager: Manager = ctx.obj
    try:
        manager.mark(id, status)
    except KeyError as e:
        click.echo(e, err=True)
        return 1
    else:
        manager.save()


@main.command(help="Remove a TODO. If it is scheduled, all related TODOs are removed.")
@click.argument("id", type=int)
@click.pass_context
def remove(ctx: click.Context, id: int):
    manager: Manager = ctx.obj
    try:
        title = manager.info(id).title
    except KeyError as e:
        click.echo(e, err=True)
        return 1

    if click.confirm(f"Do you want to remove #{id} {title}"):
        manager.remove(id)
        manager.save()
