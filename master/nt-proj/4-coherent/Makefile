TARGET = 4-coherent
LATEX = xelatex

all: document

document:
	$(LATEX) -shell-escape $(TARGET)
	biber $(TARGET)
	makeglossaries $(TARGET)
	$(LATEX) -shell-escape $(TARGET)
	$(LATEX) -shell-escape $(TARGET)
	$(LATEX) -shell-escape $(TARGET)

tidy:
	rm -rf $(TARGET).acn $(TARGET).acr $(TARGET).alg $(TARGET).bbl \
		  $(TARGET).glg $(TARGET).glo $(TARGET).gls $(TARGET).ist \
		  $(TARGET).aux $(TARGET).blg $(TARGET).idx $(TARGET).ilg \
		  $(TARGET).ind $(TARGET).lof $(TARGET).lot $(TARGET).out \
		  $(TARGET).lol $(TARGET).run.xml $(TARGET).slg $(TARGET).syg \
		  $(TARGET).syi $(TARGET).nlo $(TARGET).bcf $(TARGET).log \
		  $(TARGET).toc _minted-$(TARGET)

clean: tidy
	rm -f $(TARGET).pdf
