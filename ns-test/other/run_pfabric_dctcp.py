import threading
import os
import Queue

def worker():
	while True:
		try:
			j = q.get(block = 0)
		except Queue.Empty:
			return
		#Make directory to save results
		os.system('mkdir '+j[1])
		os.system(j[0])

q = Queue.Queue()

DEBUG_VALGRIND = False

sim_end = 10 # simulate for 30 seconds
link_rate = 10
mean_link_delay = 0.0000002
host_delay = 0.000020
queueSize = 140
# load_arr = [0.9,0.8,0.7,0.6,0.5]
load_arr = [0.5]
connections_per_pair = 1
meanFlowSize = 1138*1460
paretoShape = 1.05
flow_cdf = 'CDF_dctcp.tcl'

enableMultiPath = 1
perflowMP = 0

sourceAlg = 'DCTCP-Sack'
initWindow = 70
ackRatio = 1
slowstartrestart = 'true'
DCTCP_g = 0.0625
min_rto = 0.000250
prob_cap_ = 5

switchAlg = 'DropTail'
DCTCP_K = 65.0
drop_prio_ = 'true'
# prio_scheme_arr = [2,3]
prio_scheme_arr = [0]
deque_prio_ = 'true'
keep_order_ = 'true'
prio_num_ = 1
ECN_scheme_ = 2 #Per-port ECN marking
pias_thresh_0 = 46*1460
pias_thresh_1 = 1084*1460
pias_thresh_2 = 1717*1460
pias_thresh_3 = 1943*1460
pias_thresh_4 = 1989*1460
pias_thresh_5 = 1999*1460
pias_thresh_6 = 2001*1460

# topology_spt = 16
# topology_tors = 9
# topology_spines = 4
# topology_x = 1
# smaller topology
topology_spt = 4
topology_tors = 2
topology_spines = 1
topology_x = 1
#sets the number of machines needed on the destination (assumed to be on the same rack)
topology_dest_servers = 4 

ns_path = 'ns'
if DEBUG_VALGRIND:
	ns_path = 'valgrind -s --track-origins=yes --leak-check=full ns'

sim_script = 'spine_empirical.tcl'

for prio_scheme_ in prio_scheme_arr:
	for load in load_arr:
		scheme = 'unknown'

		if prio_scheme_ == 2:
			scheme = 'pfabric_remainingSize'
		elif prio_scheme_ == 3:
			scheme = 'pfabric_bytesSent'

		#Directory name: workload_scheme_load_[load]
		directory_name = 'websearch_%s_%d' % (scheme,int(load*100))
		directory_name = directory_name.lower()
		#Simulation command
		cmd = ns_path+' '+sim_script+' '\
			+str(sim_end)+' '\
			+str(link_rate)+' '\
			+str(mean_link_delay)+' '\
			+str(host_delay)+' '\
			+str(queueSize)+' '\
			+str(load)+' '\
			+str(connections_per_pair)+' '\
			+str(meanFlowSize)+' '\
			+str(paretoShape)+' '\
			+str(flow_cdf)+' '\
			+str(enableMultiPath)+' '\
			+str(perflowMP)+' '\
			+str(sourceAlg)+' '\
			+str(initWindow)+' '\
			+str(ackRatio)+' '\
			+str(slowstartrestart)+' '\
			+str(DCTCP_g)+' '\
			+str(min_rto)+' '\
			+str(prob_cap_)+' '\
			+str(switchAlg)+' '\
			+str(DCTCP_K)+' '\
			+str(drop_prio_)+' '\
			+str(prio_scheme_)+' '\
			+str(deque_prio_)+' '\
			+str(keep_order_)+' '\
			+str(prio_num_)+' '\
			+str(ECN_scheme_)+' '\
			+str(pias_thresh_0)+' '\
			+str(pias_thresh_1)+' '\
			+str(pias_thresh_2)+' '\
			+str(pias_thresh_3)+' '\
			+str(pias_thresh_4)+' '\
			+str(pias_thresh_5)+' '\
			+str(pias_thresh_6)+' '\
			+str(topology_spt)+' '\
			+str(topology_tors)+' '\
			+str(topology_spines)+' '\
			+str(topology_x)+' '\
			+str(topology_dest_servers)+' '\
			+str('./'+directory_name+'/flow.tr')+'  >'\
			+str('./'+directory_name+'/logFile.tr')

		q.put([cmd, directory_name])

#Create all worker threads
threads = []
number_worker_threads = 20

#Start threads to process jobs
for i in range(number_worker_threads):
	t = threading.Thread(target = worker)
	threads.append(t)
	t.start()

#Join all completed threads
for t in threads:
	t.join()