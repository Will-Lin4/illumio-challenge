from main import *
import random

def random_range(lower_bound, upper_bound):
	lower = random.randint(lower_bound, upper_bound)
	upper = random.randint(lower, upper_bound)

	return str(lower), str(upper)

# Can import random rules to an external file. Used for stress tests
def random_rules(n, file_path):
	with open(file_path, 'a', encoding='utf-8') as file:
		for i in range(n):
			if random.randint(0,1):
				direction = "inbound"
			else:
				direction = "outbound"

			if random.randint(0,1):
				protocol = "tcp"
			else:
				protocol = "udp"

			if random.randint(0,1):
				port = str(random.randint(1, 65535))
			else:
				port_range = random_range(1, 65535)
				port = port_range[0] + "-" + port_range[1]

			if random.randint(0,1):
				ip_address = str(random.randint(0, 255)) \
				+ "." + str(random.randint(0, 255)) \
				+ "." + str(random.randint(0, 255)) \
				+ "." + str(random.randint(0, 255))
			else:
				ip_range_0 = random_range(0, 255)
				ip_range_1 = random_range(0, 255)
				ip_range_2 = random_range(0, 255)
				ip_range_3 = random_range(0, 255)

				ip_address = ip_range_0[0] \
				+ "." + ip_range_1[0] \
				+ "." + ip_range_2[0] \
				+ "." + ip_range_3[0] \
				+ "-" \
				+ ip_range_0[0] \
				+ "." + ip_range_1[1] \
				+ "." + ip_range_2[1] \
				+ "." + ip_range_3[1] \

			file.write(direction + "," + protocol + "," + port + "," + ip_address + "\n")

fw = Firewall("./rules.csv")
print(fw.accept_packet("inbound", "tcp", 80, "192.168.1.2"))
print(fw.accept_packet("inbound", "udp", 53, "192.168.2.1"))
print(fw.accept_packet("outbound", "tcp", 10234, "192.168.10.11"))
print(fw.accept_packet("inbound", "tcp", 81, "192.168.1.2"))

print(fw.accept_packet("outbound", "tcp", 80, "192.168.1.5"))
print(fw.accept_packet("inbound", "tcp", 80, "192.168.1.5"))

print(fw.accept_packet("outbound", "tcp", 99, "192.168.1.3"))
print(fw.accept_packet("outbound", "tcp", 1000, "192.168.1.3"))
print(fw.accept_packet("outbound", "tcp", 1001, "192.168.1.3"))
print(fw.accept_packet("outbound", "tcp", 999, "192.168.1.3"))
