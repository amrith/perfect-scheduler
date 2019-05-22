set terminal jpeg small
set output 'simulate-1d-count.jpeg'
set xlabel 'iterations'
set ylabel 'objects placed'
set key right outside
set title "Number of objects placed (1d simulation)"
plot "simulate-1d.csv" u 1:2 w l title "fullest", \
     "simulate-1d.csv" u 1:4 w l title "emptiest", \
     "simulate-1d.csv" u 1:6 w l title "random"

set output 'simulate-1d-avg-util.jpeg'
set xlabel 'iterations'
set ylabel 'average box utilization (%)'
set key right outside
set title "Average box utilization (1d simulation)"
plot "simulate-1d.csv" u 1:3 w l title "fullest", \
     "simulate-1d.csv" u 1:5 w l title "emptiest", \
     "simulate-1d.csv" u 1:7 w l title "random"

set terminal jpeg small
set output 'simulate-2d-count.jpeg'
set xlabel 'iterations'
set ylabel 'objects placed'
set key right outside
set title "Number of objects placed (2d simulation)"
plot "simulate-2d.csv" u 1:2 w l title "fullest", \
     "simulate-2d.csv" u 1:4 w l title "emptiest", \
     "simulate-2d.csv" u 1:6 w l title "random"

set output 'simulate-2d-avg-util.jpeg'
set xlabel 'iterations'
set ylabel 'average box utilization (%)'
set key right outside
set title "Average box utilization (2d simulation)"
plot "simulate-2d.csv" u 1:3 w l title "fullest", \
     "simulate-2d.csv" u 1:5 w l title "emptiest", \
     "simulate-2d.csv" u 1:7 w l title "random"

set terminal jpeg small
set output 'simulate-3d-count.jpeg'
set xlabel 'iterations'
set ylabel 'objects placed'
set key right outside
set title "Number of objects placed (3d simulation)"
plot "simulate-3d.csv" u 1:2 w l title "fullest", \
     "simulate-3d.csv" u 1:4 w l title "emptiest", \
     "simulate-3d.csv" u 1:6 w l title "random"

set output 'simulate-3d-avg-util.jpeg'
set xlabel 'iterations'
set ylabel 'average box utilization (%)'
set key right outside
set title "Average box utilization (3d simumation)"
plot "simulate-3d.csv" u 1:3 w l title "fullest", \
     "simulate-3d.csv" u 1:5 w l title "emptiest", \
     "simulate-3d.csv" u 1:7 w l title "random"

set terminal jpeg small
set output 'simulate-2-2d-count.jpeg'
set xlabel 'iterations'
set ylabel 'objects placed'
set key right outside
set title "Number of objects placed (2d simulation)"
plot "simulate-2-2d.csv" u 1:2 w l title "fullest", \
     "simulate-2-2d.csv" u 1:4 w l title "emptiest", \
     "simulate-2-2d.csv" u 1:6 w l title "random"

set output 'simulate-2-2d-avg-util.jpeg'
set xlabel 'iterations'
set ylabel 'average box utilization (%)'
set key right outside
set title "Average box utilization (2d simulation)"
plot "simulate-2-2d.csv" u 1:3 w l title "fullest", \
     "simulate-2-2d.csv" u 1:5 w l title "emptiest", \
     "simulate-2-2d.csv" u 1:7 w l title "random"

set terminal jpeg small
set output 'simulate-2-3d-count.jpeg'
set xlabel 'iterations'
set ylabel 'objects placed'
set key right outside
set title "Number of objects placed (3d simulation)"
plot "simulate-2-3d.csv" u 1:2 w l title "fullest", \
     "simulate-2-3d.csv" u 1:4 w l title "emptiest", \
     "simulate-2-3d.csv" u 1:6 w l title "random"

set output 'simulate-2-3d-avg-util.jpeg'
set xlabel 'iterations'
set ylabel 'average box utilization (%)'
set key right outside
set title "Average box utilization (3d simulation)"
plot "simulate-2-3d.csv" u 1:3 w l title "fullest", \
     "simulate-2-3d.csv" u 1:5 w l title "emptiest", \
     "simulate-2-3d.csv" u 1:7 w l title "random"
