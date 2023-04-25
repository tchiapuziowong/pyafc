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


def get_all_vrfs(auth_header, **kwargs):
	target_url = kwargs["url"] + "vrfs"
	# print("Target_url: " + target_url)
	response = kwargs["s"].get(target_url, headers=auth_header, verify=False)
	if response.status_code not in [200]:
		logging.warning("FAIL: get_all_vrfs failed with status code %d: %s" % (response.status_code, response.text))
		exit(-1)
	else:
		logging.info("SUCCESS: get_all_vrfs succeeded")
		output = response.json()
		return output['result']


def get_vrf(vrf_name, auth_header, **kwargs):
	uuid = get_vrfs_uuid(vrf_name, auth_header, **kwargs)
	target_url = kwargs["url"] + "vrfs/{}".format(uuid)
	# print("Target_url: " + target_url)
	response = kwargs["s"].get(target_url, headers=auth_header, verify=False)
	if response.status_code not in [200]:
		logging.warning("FAIL: get_vrf failed with status code %d: %s" % (response.status_code, response.text))
		exit(-1)
	else:
		logging.info("SUCCESS: get_vrf succeeded")
		output = response.json()
		return output['result']


def create_vrf(vrf_name, fabric_uuid, auth_header, switch_uuids=[], primary_route_target="65001:101",
				address_family="ipv4_unicast", evpn=False, route_mode="both", description="", route_distinguisher="",
				secondary_route_target=[], max_routes=0, vni=1, **kwargs):
	target_url = kwargs["url"] + "vrfs"
	# print("Target_url: " + target_url)

	data = {
		"fabric_uuid": fabric_uuid,
		"switch_uuids": switch_uuids,
		"name": vrf_name,
		"description": description,
		"route_target": {
			"primary_route_target": {
				"as_number": primary_route_target,
				"address_family": address_family,
				"evpn": evpn,
				"route_mode": route_mode
			},
			"secondary_route_targets": secondary_route_target
		},
		"route_distinguisher": route_distinguisher,
		"max_routes": max_routes,
		"vni": vni
	}

	# post_data = json.dumps(data, sort_keys=True, indent=4)

	response = kwargs["s"].post(target_url, json=data, headers=auth_header, verify=False)
	if response.status_code not in [200]:
		logging.warning("FAIL: create_vrf failed with status code %d: %s" % (response.status_code, response.text))
		exit(-1)
	else:
		logging.info("SUCCESS: create_vrf succeeded")
		output = response.json()
		return output


def delete_vrf(vrf_name, auth_header, **kwargs):
	uuid = get_vrfs_uuid(vrf_name, auth_header, **kwargs)

	target_url = kwargs["url"] + "vrfs/{}".format(uuid)
	# print("Target_url: " + target_url)
	response = kwargs["s"].delete(target_url, headers=auth_header, verify=False)
	if response.status_code not in [200]:
		logging.warning("FAIL: delete_vrf failed with status code %d: %s" % (response.status_code, response.text))
		exit(-1)
	else:
		logging.info("SUCCESS: delete_vrf succeeded")
		output = response.json()
		return output


def get_vrfs_uuid(vrf_name, auth_header, **kwargs):
	vrf_dict = get_all_vrfs(auth_header, **kwargs)
	uuid = ""
	for vrf in vrf_dict:
		if vrf["name"].casefold() == vrf_name.casefold():
			uuid = vrf["uuid"]
	return uuid

