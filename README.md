## Usage

### Running tests

After cloning the repo, cd to the project root

Run `npm install`

Cd to _run-tests_ folder

Run `node test.js` to run the tests

### Reproducing the test figures

cd to the _create-results_ folder, and run the following commands:
	
	```$ python create-results.py -d urlMapped -m url -n 1
	$ python create-results.py -d dataMapped -m data -n 1
	$ python create-results.py -d nested2 -m url -n 2
	$ python create-results.py -d nested3 -m url -n 3

	$ python create-cpu-results.py -d nested2 -n 2
	$ python create-cpu-results.py -d nested3 -n 3
	```

Now, all the results files should be under the _results_ folder

Next, produce the figures by going to the _plot_ folder and running the following command:

	`$ gnuplot *`

Now, all the figures should be under the _figures_ folder
