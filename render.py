# Via http://pydanny.com/jinja2-quick-load-function.html
from jinja2 import FileSystemLoader, Environment


def render_from_template(
    directory: str, template_name: str, data: dict, environment_options: dict
) -> str:
    """Returns a string, rendered from template template_name in directory directory.
    Uses data as context

    Args:
        directory (str): Directory where the template is
        template_name (str): Name of the template
        data (dict): A dict containing the context to use to render the template
        environment_options (dict): A dict containing options to construct the jinja2 Environment

    Returns:
        str: A rendered string, from template, with data as the context.
    """
    loader = FileSystemLoader(directory)
    env = Environment(
        loader=loader,
        **environment_options,
        comment_start_string="-#",
        comment_end_string="#-"
    )
    template = env.get_template(template_name)
    return template.render(**data)


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="The directory where to find the template")
    parser.add_argument("template_name", help="A file you want to render from")
    parser.add_argument("json", help="A json file containing the appropriate context")

    parser.add_argument("--block-start-string", type=str, default="((*")
    parser.add_argument("--block-end-string", type=str, default="*))")

    parser.add_argument("--variable-start-string", type=str, default="((")
    parser.add_argument("--variable-end-string", type=str, default="))")

    parser.add_argument("-o", "--output", type=str, help="Output file name")

    args = parser.parse_args()

    import json

    with open(args.json, "r") as f:
        context = json.load(f)

        if os.path.exists(args.output):
            if (
                input(f"File {args.output} already exists. Overwrite ? (YES/no)")
                == "no"
            ):
                exit(0)

        with open(args.output, "w") as outf:

            result = render_from_template(
                args.directory,
                args.template_name,
                context,
                dict(
                    block_start_string=args.block_start_string,
                    block_end_string=args.block_end_string,
                    variable_start_string=args.variable_start_string,
                    variable_end_string=args.variable_end_string,
                ),
            )
            outf.write(result)
