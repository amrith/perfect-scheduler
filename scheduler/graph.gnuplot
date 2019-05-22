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
set output 'simulate-1d-multisize-count.jpeg'
set xlabel 'iterations'
set ylabel 'objects placed'
set key right outside
set title "Number of objects placed (1d simulation)"
plot "simulate-1d-multisize.csv" u 1:2 w l title "fullest", \
     "simulate-1d-multisize.csv" u 1:4 w l title "emptiest", \
     "simulate-1d-multisize.csv" u 1:6 w l title "random"

set output 'simulate-1d-multisize-avg-util.jpeg'
set xlabel 'iterations'
set ylabel 'average box utilization (%)'
set key right outside
set title "Average box utilization (1d simulation)"
plot "simulate-1d-multisize.csv" u 1:3 w l title "fullest", \
     "simulate-1d-multisize.csv" u 1:5 w l title "emptiest", \
     "simulate-1d-multisize.csv" u 1:7 w l title "random"

set terminal jpeg small
set output 'simulate-2d-multisize-count.jpeg'
set xlabel 'iterations'
set ylabel 'objects placed'
set key right outside
set title "Number of objects placed (2d simulation)"
plot "simulate-2d-multisize.csv" u 1:2 w l title "fullest", \
     "simulate-2d-multisize.csv" u 1:4 w l title "emptiest", \
     "simulate-2d-multisize.csv" u 1:6 w l title "random"

set output 'simulate-2d-multisize-avg-util.jpeg'
set xlabel 'iterations'
set ylabel 'average box utilization (%)'
set key right outside
set title "Average box utilization (2d simulation)"
plot "simulate-2d-multisize.csv" u 1:3 w l title "fullest", \
     "simulate-2d-multisize.csv" u 1:5 w l title "emptiest", \
     "simulate-2d-multisize.csv" u 1:7 w l title "random"

set terminal jpeg small
set output 'simulate-3d-multisize-count.jpeg'
set xlabel 'iterations'
set ylabel 'objects placed'
set key right outside
set title "Number of objects placed (3d simulation)"
plot "simulate-3d-multisize.csv" u 1:2 w l title "fullest", \
     "simulate-3d-multisize.csv" u 1:4 w l title "emptiest", \
     "simulate-3d-multisize.csv" u 1:6 w l title "random"

set output 'simulate-3d-multisize-avg-util.jpeg'
set xlabel 'iterations'
set ylabel 'average box utilization (%)'
set key right outside
set title "Average box utilization (3d simulation)"
plot "simulate-3d-multisize.csv" u 1:3 w l title "fullest", \
     "simulate-3d-multisize.csv" u 1:5 w l title "emptiest", \
     "simulate-3d-multisize.csv" u 1:7 w l title "random"

##
set style line 100 lt 1 lc rgb "gray" lw 0.5
set style line 101 lt 0.5 lc rgb "gray" lw 0.1
set mytics 5
set grid mytics ytics ls 100, ls 101

set terminal jpeg small
set output 'simulate-1d-occupancy-summary.jpeg'
set xlabel 'algorithm'
set ylabel 'occupancy'
set key off
set title "Number of objects placed (1d simulation)"
set xrange [-1:6]
set yrange [*:*]
plot "simulate-1d-summary.csv" using (column(0)):4:2:3:4:xtic(1) \
     with candlestic notitle lw 2

set terminal jpeg small
set output 'simulate-1d-utilization-summary.jpeg'
set xlabel 'algorithm'
set ylabel 'utilization (%)'
set key off
set title "Box utilization (%) (1d simulation)"
set xrange [-1:6]
set yrange [0:110]
plot "simulate-1d-summary.csv" using (column(0)):8:6:7:8:xtic(1) \
     with candlestic notitle lw 2

set terminal jpeg small
set output 'simulate-2d-occupancy-summary.jpeg'
set xlabel 'algorithm'
set ylabel 'occupancy'
set key off
set title "Number of objects placed (2d simulation)"
set xrange [-1:6]
set yrange [*:*]
plot "simulate-2d-summary.csv" using (column(0)):4:2:3:4:xtic(1) \
     with candlestic notitle lw 2

set terminal jpeg small
set output 'simulate-2d-utilization-summary.jpeg'
set xlabel 'algorithm'
set ylabel 'utilization (%)'
set key off
set title "Box utilization (%) (2d simulation)"
set xrange [-1:6]
set yrange [0:110]
plot "simulate-2d-summary.csv" using (column(0)):8:6:7:8:xtic(1) \
     with candlestic notitle lw 2

set terminal jpeg small
set output 'simulate-3d-occupancy-summary.jpeg'
set xlabel 'algorithm'
set ylabel 'occupancy'
set key off
set title "Number of objects placed (3d simulation)"
set xrange [-1:6]
set yrange [*:*]
plot "simulate-3d-summary.csv" using (column(0)):4:2:3:4:xtic(1) \
     with candlestic notitle lw 2

set terminal jpeg small
set output 'simulate-3d-utilization-summary.jpeg'
set xlabel 'algorithm'
set ylabel 'utilization (%)'
set key off
set title "Box utilization (%) (3d simulation)"
set xrange [-1:6]
set yrange [0:110]
plot "simulate-3d-summary.csv" using (column(0)):8:6:7:8:xtic(1) \
     with candlestic notitle lw 2

