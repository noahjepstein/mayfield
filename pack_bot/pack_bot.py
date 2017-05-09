import urllib, json, sys

usage_str = """Usage:

$ python [--without-ortools] pack_bot.py <suitcase_json_url> <parts_json_url>

Try this: 

$ python pack_bot.py http://pkit.wopr.c2x.io:8000/suitcases/rolly http://pkit.wopr.c2x.io:8000/robots/hey-you/parts
"""

def pack_bot_ortools(parts, volume_avail):

	from ortools.algorithms import pywrapknapsack_solver

#   name:    pack_bot_ortools
#   args:    parts        -- list of parts with "value", "id", "volume"
#            volume_avail -- integer value for total volume available
#   returns: dict containing list of final parts and total value
#   description: uses google's ortools knapsack problem solver to solve
#	 			 the bin packing problem using a dynamic programming soln.

	solver = pywrapknapsack_solver.KnapsackSolver(
      pywrapknapsack_solver.KnapsackSolver.
      KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER,
      'test')

	values  = [p['value'] for p in parts]
	volumes = [[p['volume']  for p in parts]]

	capacities = [volume_avail]
	solver.Init(values, volumes, capacities)
	computed_value = solver.Solve()

	packed_items = [parts[x] for x in range(0, len(volumes[0]))
	                if solver.BestSolutionContains(x)]

	volume_avail = sum(p['volume'] for p in packed_items)
	total_value  = sum(p['value']  for p in packed_items)

	final_parts = {}
	final_parts["part_ids"] = [p['id'] for p in packed_items]
	final_parts["value"]    = sum(p['value']  for p in packed_items)

	return final_parts



def dynamic_prog_pack_bot(parts, volume_avail):

#   name:    dynamic_prog_pack_bot
#   args:    parts        -- list of parts with "value", "id", "volume"
#            volume_avail -- integer value for total volume available
#   returns: dict containing list of final parts and total value
#   description: uses a dynamic programming solution to solve the bin packing 
# 				 problem. builds an array of partial solutions "bottom-up". 
#   complexity: O(n_parts * suitcase_size)

	# initialize partial solution arrays 
	partials = [[0 for x in range(volume_avail + 1)] for x in range(len(parts) + 1)]
	keep = [[False for x in range(volume_avail + 1)] for x in range(len(parts) + 1)]
	final_parts = {}
	final_parts['part_ids'] = []
	final_parts['value'] = 0

	# iterate bottom-up through parts and volumes
	for i in range(1, len(parts) + 1):
		for vol in range(volume_avail + 1): 
			if vol >= parts[i - 1]['volume']:
				# add part i to packing list
				# if value of part i + value of rest of the bin minus that volume > value of the bin with the volume
				if parts[i - 1]['value'] + partials[i - 1][vol - parts[i - 1]['volume']] > partials[i - 1][vol]:
					keep[i][vol] = True
					partials[i][vol] = parts[i - 1]['value'] + partials[i - 1][vol - parts[i - 1]['volume']] 
				else: 
					partials[i][vol] = partials[i - 1][vol]
			else: 
				partials[i][vol] = partials[i - 1][vol]

	# backtracks through the partial solutions grid 
	vol = volume_avail
	for i in range(len(parts), 0, -1):
		if keep[i][vol]: 
			final_parts['part_ids'].append(parts[i - 1]['id'])
			vol = vol - parts[i - 1]['volume']

	final_parts['value'] = partials[len(parts)][volume_avail]

	return final_parts



def jsons_same_test(first_json, second_json): 

	values_same = first_json['value'] == second_json['value']
	parts_same  = len(set(first_json['part_ids']) & set(second_json['part_ids'])) == len(set(first_json['part_ids']))
	print "Parts same? " + str(parts_same) + " Values same? " + str(values_same)



if __name__ == "__main__":

	without_ortools = False
	
	try: 
		if len(sys.argv) == 3: 
			suitcase_url = sys.argv[1]
			parts_url    = sys.argv[2]
		elif len(sys.argv) == 4: 
			if not sys.argv[1] == "--without-ortools": 
				raise TypeError
			suitcase_url = sys.argv[2]
			parts_url    = sys.argv[3]
			without_ortools = True
		
		suitcase_json = urllib.urlopen(suitcase_url)
		suitcase = json.loads(suitcase_json.read())

		parts_json = urllib.urlopen(parts_url)
		parts = json.loads(parts_json.read())

		dp_json = dynamic_prog_pack_bot(parts, suitcase['volume'])

		if not without_ortools: 
			ortools_json = pack_bot_ortools(parts, suitcase['volume'])
			# jsons_same_test(ortools_json, dp_json)

		print str(dp_json)

	except Exception, e: 
		print "An exception occurred with value " + str(e)
		print usage_str
		exit(1)
