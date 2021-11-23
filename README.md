# Latex CV

This is how I did my CV in LaTeX.

This repository consists in three files:

- `cv_template.tex.jinja2`: The template itself. Written in jinja2 to generate LaTeX file with CV fields.
- `json_example.json`: A json file with all the fields (required and optional) to render the template into a valid `.tex` file.
- `render.py`: A simple python script to render the template to a `.tex` file.

# Quick start (with make)

To get an idea of what the CV would look like:

```bash
git clone github.com/SteampunkIslande/CV-Latex
cd CV-Latex
make
```

This will create `cv.tex` as well as `cv.pdf` in the CV-Latex directory.
Now, to fill it in with your personal information, just edit `cv_data.json`, then run:
```bash
make clean
make
```

# Behind the scenes

To get a CV from the template, you need python with jinja2 installed, as well as latex-recommended and fonts-extra packages for LaTeX.

There are two steps to get the pdf.

1) Get the `.tex` file
```bash
python render.py . cv_template.tex.jinja2 cv_data.json -o cv.tex
```

2) Convert the `.tex` file to pdf
```bash
pdflatex cv.tex
```

# Install dependencies

Since this repo relies on two technologies (LaTeX and Python), you may need to install some dependencies for this project to work.

## LaTeX dependencies

There are only two: texlive-latex-recommended and texlive-fonts-extra.

If you are on Debian, you can install required packages like so:

```bash
sudo apt install texlive-latex-recommended
sudo apt install texlive-fonts-extra
```

Otherwise, you can use your LaTeX package manager to install them.

## Python dependencies

There is only one: jinja2.

To install it, just run:

```bash
pip install jinja2
```

If you are using linux and are not inside a virtual environment, use
```bash
pip3 install jinja2
```
instead.
