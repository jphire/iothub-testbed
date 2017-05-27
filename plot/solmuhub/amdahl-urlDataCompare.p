set encoding utf8

set term pdf font "Helvetica,8" size 5in,3in lw 2

set style data lines

set for [i=1:5] linetype i dt i

set style line 1 lc rgb "black" lw 2.0 ps 0.4 pi 1
set style line 2 lc rgb "black" lw 2.0 ps 0.4 pi 1
set style line 3 lc rgb "orange" lw 2.0 ps 0.4 pi 1
set style line 4 lc rgb "blue" lw 2.0 ps 1.0 pi 1
set style line 5 lc rgb "green" lw 2.0 ps 0.4 pi 1

set key autotitle columnhead

set xtics out nomirror
set ytics out nomirror

set ytics 0,2,20

set yrange [0:20]

set ylabel "Speedup factor"
set xlabel "Number of hubs"

set format y "%.0f"

set output '../../figures/amdahl-urlDataCompare.pdf'

#set title "Solmuhub and Amdahl's law, one-hop execution"
set title ""

plot '../../data/amdahl-types-full' u 2:xtic(1) ti 'Url-mapped' ls 4, \
'../../data/amdahl-types-full' u 3:xtic(1) ti 'Data-mapped' ls 3, \
'' u 8:xtic(1) ti '80% distributed' lt 2 lc rgb "#555555" lw 2, \
'' u 9:xtic(1) ti '90% distributed' lt 3 lc rgb "#555555" lw 2, \
'' u 10:xtic(1) ti '95%, SH theor. max' lt 4 lc rgb "#555555" lw 2, \

unset output
reset
