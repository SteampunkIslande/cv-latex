# Latex CV

This is how I did my resume (Curriculum Vitae) in LaTeX.

This repository consists of three main files:

- `cv_template.tex.jinja2`: The template itself. Written in jinja2 to generate LaTeX file with resume fields.
- `cv_data.json`: A json file with all the fields (required and optional) to render the template into a valid `.tex` file.
- `render.py`: A simple python script to render the template to a `.tex` file.

## Install

You need singularity installed on your computer.

Fist, create the image:

```bash
singularity build --fakeroot cvlatex.sif python-latex.def
```

Then run:

```bash
singularity run -B $PWD cvlatex.sif
```

Inside `$PWD`, you only need `cv_data.json` to be present.
