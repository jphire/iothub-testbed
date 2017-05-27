set encoding utf8

set term pdf font "Helvetica,8" size 6in,5in

set style data histogram
set style histogram rowstacked gap 0.8 title textcolor lt -1 offset character 0, -0.5, 0

set boxwidth 0.7 relative
set style fill solid 0.5

set tmargin 3
set key outside bottom horizontal Left reverse noenhanced autotitle columnhead nobox height 4

set xtics out nomirror
set ytics out nomirror

set ytics 0,10,100

set yrange [0:100]

set ylabel "Relative time spent"

set format y "%.0f%%"

set output '../../figures/profiles-nested3.pdf'

#set title "Solmuhub profile using URL mapper and depth 3"
set title ""

set palette rgbformulae 7,5,15
unset colorbox

plot newhistogram "8-Nodes" lt 1, '../../results/nested3/8-nodes-3-depth-profile-stacked' u (100.*$2/$9):xtic(1) lt palette frac 2/9. ti column(2), for [i=3:9] '' using (100.*(column(i)-column(i-1))/$9) lt palette frac i/9. ti column(i), \
	 newhistogram "16-Nodes" lt 1, '../../results/nested3/16-nodes-3-depth-profile-stacked' u (100.*$2/$9):xtic(1) lt palette frac 2/9. notitle, for [i=3:9] '' using (100.*(column(i)-column(i-1))/$9) lt palette frac i/9. notitle, \
	 newhistogram "32-Nodes" lt 1, '../../results/nested3/32-nodes-3-depth-profile-stacked' u (100.*$2/$9):xtic(1) lt palette frac 2/9. notitle, for [i=3:9] '' using (100.*(column(i)-column(i-1))/$9) lt palette frac i/9. notitle, \
     newhistogram "Local" lt 6, '../../results/nested3/0-nodes-3-depth-profile-stacked' u (100.*$2/$5):xtic(1) lt palette frac 2/5. ti column(2), for [i=3:5] '' using (100.*column(i)/$5) lt palette frac i/5. title column(i), \

unset output
reset
