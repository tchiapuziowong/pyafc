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
import pyafc.vsx as vsx
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
	ntp_name = "ntp-fabric01"
	ntp_ip = "10.0.10.200"
	dns_afc_name = "dns-fabric"
	domain_name = "AFCLab.com"
	name_server_list = ["10.0.10.200"]

	try:
		login_session, auth_header = session.login(base_url, username, password)

		# print(auth_header)
		session_dict = dict(s=login_session, url=base_url)

		print("Getting Switch UUIDs...")
		print(devices.get_switches_uuids(switch_list, auth_header, **session_dict))

		print("Deleting Switches...")
		devices.delete_switches_from_afc(switch_list, auth_header, **session_dict)

		print("Deleting NTP configuration for NTP server named {}".format(ntp_name))
		ntp.delete_ntp(ntp_name, auth_header, **session_dict)

		print("Deleting DNS configuration for DNS server named {}".format(dns_afc_name))
		dns.delete_dns(dns_afc_name, auth_header, **session_dict)

		print("Deleting Fabric named {}".format(fabric_name))
		fabric.delete_fabric(fabric_name, auth_header, **session_dict)

		print("Deleting VRF named {}".format(fabric_name))
		vrfs.delete_vrf(vrf_name, auth_header, **session_dict)


	except Exception as error:
		print('Ran into exception: {}. Logging out...'.format(error))
	session.logout(auth_header, **session_dict)


if __name__ == '__main__':
	main()