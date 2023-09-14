#!/usr/bin/env python3

from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import requests
import os
import sys
import logging
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)


# def get_vsx(auth_header, **kwargs):
# 	target_url = kwargs["url"] + "fabrics'vsx"
# 	# print("Target_url: " + target_url)
# 	response = kwargs["s"].get(target_url, headers=auth_header, verify=False)
# 	if response.status_code not in [200]:
# 		logging.warning("FAIL: get_vsx failed with status code %d: %s" % (response.status_code, response.text))
# 		exit(-1)
# 	else:
# 		logging.info("SUCCESS: get_vsx succeeded")
# 		output = response.json()
# 		return output['result']


def create_underlay(vrf_uuid,
					auth_header,
					underlay_type="OSPF",
					name="MyUnderlay",
					description=None,
					ipv4_address="192.168.10.0",
					ipv4_prefix_length=24,
					transit_vlan=3,
					**kwargs):
	target_url = kwargs["url"] + f"vrfs/{vrf_uuid}/underlay"
	print("Target_url: " + target_url)

	data = {
		"name":name,
		"description": description,
		"enabled": True,
		"underlay_type": underlay_type,
		"bfd": True,
		"transit_vlan": transit_vlan,
		"ipv4_address": {
			"address": ipv4_address,
			"prefix_length": ipv4_prefix_length
		},
		"bgp": {
			"asn_type": "DUAL",
			"dual_asn": {
				"spine_asn": "65000.0",
				"leaf_asn": "65001.0"
			},
			"multi_asn": {
				"starting_sl_asn": "65000.0",
				"starting_bdr_asn": "65100.0"
			},
			"keepalive_timer": 60,
			"holddown_timer": 180,
			"activate_ip_routes": True,
			"allowas_in": True,
			"auth_password": "string",
			"force_timers_update": False
		},
		"ospf": {
			"hello_interval": 10,
			"dead_interval": 40,
			"area_id": 0,
			"max_metric": {
				"router_lsa": True,
				"include_stub": True,
				"on_startup": 300
			},
			"passive_interface_default": True,
			"trap_enable": True,
			"authentication_type": "null",
			"md5_key_id": 1,
			"authentication_key_type": "string",
			"authentication_key": "string"
		}
	}

	response = kwargs["s"].post(target_url, json=data, headers=auth_header, verify=False)
	if response.status_code not in [200]:
		logging.warning("FAIL: create_underlay failed with status code %d: %s" % (response.status_code, response.text))
		exit(-1)
	else:
		logging.info("SUCCESS: create_underlay succeeded")
		output = response.json()
		return output['result']
#
#
# def delete_all_vsx_pairs(auth_header, **kwargs):
# 	target_url = kwargs["url"] + "fabrics/vsx"
# 	# print("Target_url: " + target_url)
# 	response = kwargs["s"].delete(target_url, headers=auth_header, verify=False)
# 	if response.status_code not in [200]:
# 		logging.warning("FAIL: delete_all_vsx_pairs failed with status code %d: %s" % (response.status_code, response.text))
# 		exit(-1)
# 	else:
# 		logging.info("SUCCESS: delete_all_vsx_pairs succeeded")
# 		output = response.json()
# 		return output
#
# def get_all(fabric_uuid, auth_header, **kwargs):
# 	target_url = kwargs["url"] + f"fabrics/{fabric_uuid}/vsx"
# 	# print("Target_url: " + target_url)
# 	response = kwargs["s"].get(target_url, headers=auth_header, verify=False)
# 	if response.status_code not in [200]:
# 		logging.warning("FAIL: get_all_fabrics failed with status code %d: %s" % (response.status_code, response.text))
# 		exit(-1)
# 	else:
# 		logging.info("SUCCESS: get_all VSX succeeded")
# 		output = response.json()
# 		return output['result']
#
# def get_uuid(fabric_uuid, vsx_name,auth_header, **kwargs):
# 	vsx_list = get_all(fabric_uuid, auth_header, **kwargs)
# 	uuid = ""
# 	for vsx in vsx_list:
# 		if vsx["name"].casefold() == vsx_name.casefold():
# 			uuid = vsx["uuid"]
# 	return uuid