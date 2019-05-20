set terminal jpeg small
set output 'simple-1d-count.jpeg'
set xlabel 'iterations'
set ylabel 'objects placed'
set key right outside
set title "Number of objects placed"
plot "simple-1d.csv" u 1:2 w lp title "fullest", \
     "simple-1d.csv" u 1:6 w lp title "emptiest"

set output 'simple-1d-avg-util.jpeg'
set xlabel 'iterations'
set ylabel 'average box utilization (%)'
set key right outside
set title "Average box utilization"
plot "simple-1d.csv" u 1:5 w lp title "fullest", \
     "simple-1d.csv" u 1:9 w lp title "emptiest"
