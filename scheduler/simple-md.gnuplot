set terminal jpeg small
set output 'simple-md-count.jpeg'
set xlabel 'iterations'
set ylabel 'objects placed'
set key right outside
set title "Number of objects placed"
plot "simple-md.csv" u 1:2 w lp title "fullest", \
     "simple-md.csv" u 1:6 w lp title "emptiest", \
     "simple-md.csv" u 1:10 w lp title "random"

set output 'simple-md-avg-util.jpeg'
set xlabel 'iterations'
set ylabel 'average box utilization (%)'
set key right outside
set title "Average box utilization"
plot "simple-md.csv" u 1:5 w lp title "fullest", \
     "simple-md.csv" u 1:9 w lp title "emptiest", \
     "simple-md.csv" u 1:13 w lp title "random"
