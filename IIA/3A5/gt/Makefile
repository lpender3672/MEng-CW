#Make file for Lab GT code
CODES=gtmain.f 
LINKS= -L$(LPATH) -L$(GPATH) -lgt -lhgraph -lX11
gt:	$(CODES) Makefile gtinc.f
	gfortran -g -o gt $(CODES) $(LINKS)

