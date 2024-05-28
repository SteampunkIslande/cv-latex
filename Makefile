all: cv.pdf

cv.pdf: cv.tex
	pdflatex cv.tex

cv.tex: cv_data.json
	python /cv-latex/render.py /cv-latex/data cv_template.tex.jinja2 cv_data.json -o cv.tex

clean:
	rm -f cv.tex cv.pdf cv.aux cv.log cv.out