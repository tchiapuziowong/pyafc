#!/usr/bin/env python3

from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import requests
import os
import sys
import logging
import json
import pyafc.session as session
import pyafc.devices as devices
import pyafc.fabric as fabric
import pyafc.vrfs as vrfs
import pyafc.ntp as ntp
import pyafc.dns as dns

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)


def main():
	afc_ip = "10.0.0.0"
	username = "admin"
	password = "admin"
	switch_pass = "admin"
	auth_header = {}

	os.environ['no_proxy'] = afc_ip
	os.environ['NO_PROXY'] = afc_ip

	base_url = "https://{0}/api/v1/".format(afc_ip)

	leaf_switch_list = [
		"10.0.0.103",
		"10.0.0.104"
	]

	spine_switch_list = [
		"10.0.0.101",
		"10.0.0.102"
	]

	switch_list = leaf_switch_list + spine_switch_list
	fabric_name = "Fabric01"
	vrf_name = "test_VRF"
	ntp_name = "ntp-fabric"
	ntp_ip = "10.0.0.200"
	dns_afc_name = "dns-fabric"
	domain_name = "AFCLab.com"
	name_server_list = ["10.0.0.200"]

	try:
		login_session, auth_header = session.login(base_url, username, password)

		print(auth_header)
		session_dict = dict(s=login_session, url=base_url)

		print("Getting fabric UUID")
		fabric_uuid = fabric.get_fabrics_uuid(fabric_name, auth_header, **session_dict)

		print("Discovering Switches...")
		devices.discover_switches(switch_list, auth_header, switch_pass, password, **session_dict)

		print("Adding Leaf Switches to Fabric...")
		devices.add_switches_to_fabric(leaf_switch_list, auth_header, "leaf", fabric_uuid, **session_dict)

		print("Adding Spine Switches to Fabric...")
		devices.add_switches_to_fabric(spine_switch_list, auth_header, "spine", fabric_uuid, **session_dict)

		print("Adding NTP Server(s)...")
		ntp.create_ntp(ntp_name, [fabric_uuid], ntp_ip, auth_header, **session_dict)

		print("Adding DNS Server(s)...")
		dns.create_dns(dns_afc_name, [fabric_uuid], domain_name, name_server_list, auth_header, **session_dict)

		print("Creating VRF")
		vrfs.create_vrf(vrf_name, fabric_uuid, auth_header, primary_route_target="65001:101",
						address_family="ipv4_unicast", route_mode="both", max_routes=0, vni=5, **session_dict)

	except Exception as error:
		print('Ran into exception: {}. Logging out...'.format(error))
	session.logout(auth_header, **session_dict)


if __name__ == '__main__':
	main()