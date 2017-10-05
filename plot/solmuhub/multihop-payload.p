set encoding utf8

set term pdf font "Helvetica,8" size 5in,3in

set style histogram errorbars gap 1 title textcolor lt -1 lw 2.0
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
set xrange [0:3]
set yrange [0:16]

set xlabel "Number of hubs"

set ylabel "Response size (MB)"

set format y "%.0fs"

set ytics format "%2.1f"

set output '../../figures/payload-multi-hop.pdf'

#set title "Response payloads for multi-hop execution"
set title ""

n = 1000000
plot '../../results/nested2/payload-no-4-hubs.out' u ($10/n):($11/n):($12/n):xtic(1) ti 'Two-hop' ls 1, \
	'../../results/nested3/payload.out' u ($10/n):($11/n):($12/n):xtic(1) ti 'Three-hop' ls 3
unset output
reset
