set encoding utf8

set term pdf font "Helvetica,8" size 5in,3in

set style histogram gap 1 title textcolor lt -1
set style data histograms

set style fill solid 0.5
set bars front

set style line 1 lc rgb "#888888" lw 2.0 ps 1.0 pi 1
set style line 2 lc rgb "#555555" lw 2.0 ps 1.0 pi 1
set style line 3 lc rgb "#111111" lw 2.0 ps 1.0 pi 1

set xtics out nomirror
set ytics out nomirror

set offset 1.0,0,0,0

set xtics 0,1,4
set xrange [0:4]
set ytics 0,20,100
set yrange [0:100]

set xlabel "Number of hubs"

set ylabel "CPU usage"

set format y "%.0f%%"

#set logscale y 10

set output '../../figures/processed-cpu-leveledCompare-u.pdf'

#set title "Total CPU usage for multi-hop execution"
set title ""

plot '../../results/nested2/processed-cpu-no-4-hubs.out' u 4:xtic(1) ti 'Two-hop' ls 1, \
	'../../results/nested3/processed-cpu-no-4-hubs.out' u 4:xtic(1) ti 'Three-hop' ls 2

unset output
reset
