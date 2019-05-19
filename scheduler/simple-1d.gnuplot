set terminal pdf
set output 'runs.pdf'
plot "runs.csv" u 1:2 w lp
replot "runs.csv" u 1:6 w lp
