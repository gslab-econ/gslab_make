set obs 10
gen var = _n

export delimited "test/output/output.csv", replace

display "Test script complete"
