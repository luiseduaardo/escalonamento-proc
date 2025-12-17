PYTHON = python3
MAIN = main.py

EXP_DIR = test/saida_esperada
OUT_DIR = test/saida_obtida

DIFF_FLAGS = -w -s

.PHONY : clean alltests test1 test2 test_pdf

solver: $(MAIN)
	@echo "Script pronto."

test1: solver
	$(PYTHON) $(MAIN) "1_in.txt" "1_out.txt"
	@diff $(DIFF_FLAGS) "$(EXP_DIR)/1_out.txt" "$(OUT_DIR)/1_out.txt"
	@echo "TEST 1 OK"

test2: solver
	$(PYTHON) $(MAIN) "2_in.txt" "2_out.txt"
	@diff $(DIFF_FLAGS) "$(EXP_DIR)/2_out.txt" "$(OUT_DIR)/2_out.txt"
	@echo "TEST 2 OK"

testandson: solver
	$(PYTHON) $(MAIN) "EntradaProcessos.txt" "SaidaProcessos.txt"
	@diff $(DIFF_FLAGS) "$(EXP_DIR)/SaidaProcessos.txt" "$(OUT_DIR)/SaidaProcessos.txt"
	@echo "TEST ANDSON OK"

alltests: test1 test2 testandson

clean:
	rm -f $(OUT_DIR)/*.txt
	rm -rf __pycache__