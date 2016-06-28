import os
import sys
import json
import numpy as np
import scipy as sp
import scipy.stats
import shutil

'''
This script is used to get the averages and confidence intervals of latency and CPU and memory usages.
Results are saved in a timestamped folder. 

Example usage: 

$ python avg.py 512 5

Where 512 represents image size and 5 is the total number of nodes, including controller node.

'''

latest = 0
sizes = []
nodes = []
types = ['cpu', 'mem', 'latency', 'payload', 'profile']
tags_zero = ['feed_fetched', 'after_data_fetch', 'execution_end', 'before_sending_response']
tags_multi = ['feed_fetched', 'after_data_fetch', 'after_data_map', 'piece_response_latency', 'dist_response_latency', 'after_reducer', 'before_sending_response']
tags = ['feed_fetched', 'after_data_fetch', 'execution_end', 'after_data_map', 'piece_response_latency', 'dist_response_latency', 'after_reducer', 'before_sending_response']
tags_map = {
	'feed_fetched':'Fetching-feed', 
	'after_data_fetch':'Fetching-data', 
	'execution_end':'Executing-code',
	'after_data_map':'Mapping-data',
	'piece_response_latency':'Getting-a-shared-piece', 
	'dist_response_latency':'Getting-all-pieces', 
	'after_reducer':'Reducing-data', 
	'before_sending_response':'After-all-processing'
}

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h

def run(filename, nodes, size):
	dataMap = {}
	profile = {}
	means = {}
	cpuData = []
	memData = []
	latencyData = []
	content_length = []
	with open(filename) as file:
		for line in file:
			data = json.loads(line)['profiler']['data']
			latency = json.loads(line)['profiler']['latency']
			for key, val in data.items():
				usage = val[0]['usage']
				cpuData.append(usage['cpu'])
				memData.append(usage['mem'])
				latencyData.append(latency)
				# payload data
				if ('contentLength' in val[0]):
					content_length.append(val[0]['contentLength'])

				# profiling data
				if not key in profile:
					profile[key] = []
				for value in val:
					profile[key].append(value['time'])

	for tag, val in profile.items():
		means[tag] = mean_confidence_interval(val)

	mem = mean_confidence_interval(memData)
	cpu = mean_confidence_interval(cpuData)
	latency = mean_confidence_interval(latencyData)

	if len(content_length) > 0: 
		payload = mean_confidence_interval(map(int, content_length))
	else:
		payload = []

	return {'nodes':nodes, 'size':size, 'cpu':cpu, 'mem':mem, 'latency':latency, 'payload':payload, 'profile':means}

def prettify(tag):
	return tags_map[tag]


# Get latest raw results' directory path
for dirname, dirnames, filenames in os.walk('../logs/profiler'):
	for subdirname in dirnames:	
		tmp = int(subdirname)
		latest = max(latest, tmp)
		latest_path = os.path.join(dirname, str(latest))

# Get node count and sizes from the raw results folder
for dirname, dirnames, filenames in os.walk(latest_path):
	for name in filenames:
		n = name.split('-')[0]
		s = name.split('-')[2]
		if s not in sizes:
			sizes.append(s)
		if n not in nodes:
			nodes.append(n)


# Create new timestamped folder in results and remove old ones
results_path = '../results/' + str(latest)
if not os.path.exists(results_path):
    os.makedirs(results_path)
else:
	shutil.rmtree(results_path)
	os.makedirs(results_path)

os.unlink('../results/latest')
os.symlink(results_path, '../results/latest')


# Write new results to timestamped folder
profile_data = {}
latency_data = {}
cpu_data = {}
data = {'cpu':{}, 'mem':{}, 'latency':{}, 'payload':{}, 'profile':{}}
for node in range(0, len(nodes)):
	is_first = True
	for size in sizes:
		filename = "-".join([str(node), 'node', size]) 
		ret = run(os.path.join(latest_path, filename), str(node), str(size))

		# Write the averages
		for name in types:
			if len(ret[name]) == 0:
				continue

			if node not in data[name]:
				data[name][node] = {}
			data[name][node][size] = ret[name]
			
			if name == 'profile':
				outfile = os.path.join(results_path, str(node) + "-" + str(size) + '-profile')
				# Write all profiling data
				with open(outfile, 'a') as out:
					profile = ret[name]
					# To keep correct order in tags, use list
					for tag in tags:
						if tag in profile.keys():
							# print "\t".join([tag, str(means[tag][0]), str(means[tag][1]), str(means[tag][2]), "0.6", "\n"])
							out.write("\t".join([tag, str(profile[tag][0]), str(profile[tag][1]), str(profile[tag][2]), "\n"]))
			else:
				outfile = os.path.join(results_path, name + ".out")

				with open(outfile, 'a') as out:
					# print outfile, "\t".join([ret['nodes'], str(ret[name][0]), str(ret[name][1]), str(ret[name][2])])
					if is_first:
						out.write("\t".join([ret['nodes'], str(ret[name][0]), str(ret[name][1]), str(ret[name][2]), "0.6", "\t"]))
					else:
						out.write("\t".join([str(ret[name][0]), str(ret[name][1]), str(ret[name][2]), "0.6", "\t"]))
		is_first = False
	for name in types:
		outf = os.path.join(results_path, name + ".out")
		with open(outf, 'a') as out:
			out.write("\n")

# Aggregate data to plottable files
tags_data = {}
for node in range(0, len(nodes)):
	profile_file = os.path.join(results_path, str(node) + '-' + 'profile')
	with open(profile_file, 'a') as prof:
		prof.write("Size\t")
		if node == 0:
			prof.write("\t".join(map(prettify, tags_zero)))
		else:
			prof.write("\t".join(map(prettify, tags_multi)))
		prof.write("\n")

		for size in sizes:
			prof.write(size + "\t")
			for i, tag in enumerate(tags_multi):
				if tag in data['profile'][node][size]:
					tmp = data['profile'][node][size][tag]
					prof.write("\t".join([str(tmp[0]), "\t"]))

			# Write newline after each finished tag line
			prof.write("\n")
