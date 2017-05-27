import os
import sys
import getopt
import utils
import shutil

'''
This script is used to get the averages and confidence intervals of latency and CPU and memory usages.
Results are saved in a results folder.

Example usage: 

$ python create-results.py -d urlMapped

'''

latest = 0
sizes = []
nodes = []
nodes2 = []
depths = []
nesting_level = 1
results_path = ''
logs_path = ''
nodeCountMultiplier = 1
mapping = 'url'
types = ['cpu', 'mem', 'latency', 'payload', 'profile']
tags_zero = ['feed_fetched', 'after_data_fetch', 'execution_end', 'before_sending_response']
tags_multi = ['feed_fetched', 'after_data_fetch', 'after_data_map', 'piece_response_latency', 'dist_response_latency', 'after_reducer', 'before_sending_response', 'after_response']
tags = ['feed_fetched', 'after_data_fetch', 'execution_end', 'after_data_map', 'piece_response_latency', 'dist_response_latency', 'after_reducer', 'before_sending_response', 'after_response']

try:
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "d:m:n:")
except getopt.GetoptError:
    print 'create-results.py -d <source_path> -m <mapping_type> -n <depth>'
    sys.exit(2)

for opt, arg in opts:
    if opt == '-d':
        logs_path = '../logs/solmuhub/' + str(arg)
        results_path = '../results/' + str(arg)
    elif opt == '-m':
        mapping = str(arg)
    elif opt == '-n':
        nesting_level = str(arg)

if results_path == '':
    latest, logs_path = utils.getLatestTimestamp()
    results_path = '../results/' + str(latest)

print 'Source files > ' + logs_path
print 'Result files > ' + results_path

sizes, nodes, depths = utils.configureTest(logs_path)

# Create new folder in results and remove old ones
if not os.path.exists(results_path):
    os.makedirs(results_path)
else:
    shutil.rmtree(results_path)
    os.makedirs(results_path)

# Remove latest folder
if os.path.exists('../results/latest'):
    os.unlink('../results/latest')

# Create new symlink to point to the latest results
os.symlink(results_path, '../results/latest')

# Write new results to the results folder
profile_data = {}
latency_data = {}
cpu_data = {}
data = {'cpu':{}, 'mem':{}, 'latency':{}, 'payload':{}, 'profile':{}}

for depth in depths:
    for node in nodes:
        node = int(node)
        is_first = True
        for size in sizes:

            filename = "-".join([str(node), 'node', mapping, size, 'depth', depth])
            ret = utils.run(os.path.join(logs_path, filename), str(node), str(size))
            print '----------------------------------------------'
            print 'Size: ' + str(size)
            print 'Depth: ' + str(depth)
            print 'Node: ' + str(node)
            print 'CPU: ' + str(ret['cpu'])
            print '++++++++++++++++++++++++++++++++++++++++++++++'
            # Write the averages
            for name in types:
                if len(ret[name]) == 0:
                    continue

                if node not in data[name]:
                    data[name][node] = {}
                data[name][node][size] = ret[name]

                if name == 'profile':
                    outfile = os.path.join(results_path, str(node) + "-" + str(size) + '-' + str(depth) + '-profile')
                    
                    with open(outfile, 'a') as out:
                        profile = ret[name]
                        # To keep correct order in tags, use list
                        for tag in tags:
                            if tag in profile.keys():
                                # print "\t".join([tag, str(means[tag][0]), str(means[tag][1]), str(means[tag][2]), "0.6", "\n"])
                                out.write("\t".join([tag, str(profile[tag][0]), str(profile[tag][1]), str(profile[tag][2]), "\n"]))
                else:
                    # Write all other than profile data
                    outfile = os.path.join(results_path, name + ".out")

                    with open(outfile, 'a') as out:
                        # print outfile, "\t".join([ret['nodes'], str(ret[name][0]), str(ret[name][1]), str(ret[name][2])])
                        if is_first:
                            nodeCount = utils.getTotalNodeCount(nesting_level, ret['nodes'])
                            out.write("\t".join([nodeCount, str(ret[name][0]), str(ret[name][1]), str(ret[name][2]), "0.6", "\t"]))
                        else:
                            out.write("\t".join([str(ret[name][0]), str(ret[name][1]), str(ret[name][2]), "0.6", "\t"]))

            is_first = False
        for name in types:
            outf = os.path.join(results_path, name + ".out")
            with open(outf, 'a') as out:
                out.write("\n")
                # Add empty row for correct comparing with nested-2 results
                if (nesting_level == '3' and node == 0 and name in ['mem', 'latency']):
                    out.write("4\tNaN\tNaN\tNaN\tNaN\tNaN\tNaN\tNaN\tNaN\tNaN\tNaN\tNaN\tNaN\n")

# Aggregate data for the profile plots
tags_data = {}
for depth in depths:
    for node in nodes:
        node = int(node)
        
        # Change total node amount to profile output files to be correct
        total_node_count = utils.getTotalNodeCount(nesting_level, node)

        profile_file = os.path.join(results_path, total_node_count + '-nodes-' + str(depth) + '-depth-profile-stacked')
        with open(profile_file, 'a') as prof:
            prof.write("Size\t")
            if node == 0:
                prof.write("\t".join(map(utils.prettify, tags_zero)))
            else:
                prof.write("\t".join(map(utils.prettify, tags_multi)))
            prof.write("\n")

            for size in sizes:
                prof.write(size + "\t")
                for i, tag in enumerate(tags_multi):
                    if tag in data['profile'][node][size]:
                        tmp = data['profile'][node][size][tag]
                        prof.write("\t".join([str(tmp[0]), "\t"]))

                # Write newline after each finished tag line
                prof.write("\n")

