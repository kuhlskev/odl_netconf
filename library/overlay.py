"""
put-node.

adds a node to ODL

parameter:
* ODL IP address
* node IP address
* node name
* netconf port (optional - default is 830)
* netconf user (optional - default is 'cisco')
* netconf pass (optional - default is 'cisco')

uses HTTP PUT with JSON payload
"""

import sys
import os
import requests

devices = [
            {'address':'172.26.170.83',
             'name':'kevios2',
             'port':830,
             'username':'admin',
             'password':'c1sco123'
            },
            {'address':'172.26.170.84',
             'name':'kevios3',
             'port':830,
             'username':'admin',
             'password':'c1sco123'
            }
          ]
ODL_SERVER = '10.203.27.104'
headers = {'Content-Type': 'application/json'}
odl_user = os.environ.get('ODL_USER', 'admin')
odl_pass = os.environ.get('ODL_PASS', 'admin')

request_body = '''{
  "vlan": {
    "vlan-list": [
      {
        "id": "3240",
        "name": "10_103_240_0-DATA"
      },
      {
        "id": "2241",
        "name": "10_102_241_0-IOT2"
      },
      {
        "id": "1240",
        "name": "10_101_240_0-DATA"
      },
      {
        "id": "2240",
        "name": "10_102_240_0-IOT1"
      },
      {
        "id": "3241",
        "name": "10_103_241_0-VOICE"
      },
      {
        "id": "1241",
        "name": "10_101_241_0-VOICE"
      }
    ]
  }
}'''
url = 'http://10.203.27.104:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/kevios2/yang-ext:mount/ned:native/vlan'
print 'Adding Vlan'
print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))

request_body = '''{    "vrf": {
      "definition": [
        {
          "name": "VRF-DEVELOPMENT",
          "address-family": {
            "ipv4": {
              "route-target": {
                "export": [
                  {
                    "asn-ip": "103:103"
                  }
                ],
                "import": [
                  {
                    "asn-ip": "103:103"
                  }
                ]
              }
            }
          },
          "rd": "103:103"
        },
        {
          "name": "VRF-EMPLOYEE",
          "address-family": {
            "ipv4": {
              "route-target": {
                "export": [
                  {
                    "asn-ip": "101:101"
                  }
                ],
                "import": [
                  {
                    "asn-ip": "101:101"
                  }
                ]
              }
            }
          },
          "rd": "101:101"
        },
        {
          "name": "Mgmt-vrf",
          "address-family": {
            "ipv4": {},
            "ipv6": {}
          }
        },
        {
          "name": "VRF-IOT",
          "address-family": {
            "ipv4": {
              "route-target": {
                "export": [
                  {
                    "asn-ip": "102:102"
                  }
                ],
                "import": [
                  {
                    "asn-ip": "102:102"
                  }
                ]
              }
            }
          },
          "rd": "102:102"
        }
      ]
    }
}'''

url = 'http://10.203.27.104:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/kevios2/yang-ext:mount/ned:native/vrf'
print "Adding VRF's"
print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))

request_body = '''{      
"isis-container": {
  "isis": [
    {
      "area-tag": "UNDERLAY",
      "log-adjacency-changes": {},
      "net": [
        {
          "tag": "49.0001.0100.0001.4001.00"
        }
      ],
      "authentication": {
        "mode": {
          "md5": {}
        },
        "key-chain": {
          "name": "UNDERLAY-AUTH"
        }
      },
      "metric-style": {
        "wide": {}
      }
    }
  ]
  }
}'''  

# Put Node to ODL
url = 'http://10.203.27.104:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/kevios2/yang-ext:mount/ned:native/router/isis-container'
print 'Adding ISIS'
print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))

request_body = '''
{
  "lisp": {
    "ipv4": {
      "use-petr": [
        {
          "locator-address": "10.0.0.2",
          "priority": 1,
          "weight": 1
        },
        {
          "locator-address": "10.0.0.1",
          "priority": 1,
          "weight": 1
        }
      ],
      "etr": {
        "map-server": [
          {
            "ip-addr": "10.4.49.100",
            "key": {
              "key-7": "011057175804575D72"
            }
          },
          {
            "ip-addr": "10.4.49.101",
            "key": {
              "key-7": "104D580A061843595F"
            }
          }
        ]
      },
      "map-cache-limit": {
        "max-map-cache-entries": 5000
      },
      "sgt": [
        null
      ],
      "itr-enable": {
        "itr": [
          null
        ]
      },
      "itr": {
        "map-resolver": [
          {
            "ip-addr": "10.4.49.101"
          },
          {
            "ip-addr": "10.4.49.100"
          }
        ]
      },
      "etr-enable": {
        "etr": [
          null
        ]
      }
    },
    "eid-table": {
      "instance-list": [
        {
          "instance-id": 102,
          "vrf": "VRF-IOT",
          "ipv4": {
            "map-cache-limit": {
              "max-map-cache-entries": 20000
            }
          },
          "dynamic-eid": [
            {
              "name": "IOT.EID.10_102_240_0",
              "database-mapping": [
                {
                  "eid-prefix": "10.102.240.0/24",
                  "locator-set": "campus_fabric"
                }
              ]
            },
            {
              "name": "IOT.EID.10_102_241_0",
              "database-mapping": [
                {
                  "eid-prefix": "10.102.241.0/24",
                  "locator-set": "campus_fabric"
                }
              ]
            }
          ]
        },
        {
          "instance-id": 103,
          "vrf": "VRF-DEVELOPMENT",
          "ipv4": {
            "map-cache-limit": {
              "max-map-cache-entries": 20000
            }
          },
          "dynamic-eid": [
            {
              "name": "DEVELOPMENT.EID.10_103_240_0",
              "database-mapping": [
                {
                  "eid-prefix": "10.103.240.0/24",
                  "locator-set": "campus_fabric"
                }
              ]
            },
            {
              "name": "DEVELOPMENT.EID.10_103_241_0",
              "database-mapping": [
                {
                  "eid-prefix": "10.103.241.0/24",
                  "locator-set": "campus_fabric"
                }
              ]
            }
          ]
        },
        {
          "instance-id": 101,
          "vrf": "VRF-EMPLOYEE",
          "ipv4": {
            "map-cache-limit": {
              "max-map-cache-entries": 20000
            }
          },
          "dynamic-eid": [
            {
              "name": "EMPLOYEE.EID.10_101_241_0",
              "database-mapping": [
                {
                  "eid-prefix": "10.101.241.0/24",
                  "locator-set": "campus_fabric"
                }
              ]
            },
            {
              "name": "EMPLOYEE.EID.10_101_240_0",
              "database-mapping": [
                {
                  "eid-prefix": "10.101.240.0/24",
                  "locator-set": "campus_fabric"
                }
              ]
            }
          ]
        },
        {
          "instance-id": 0,
          "default": [
            null
          ]
        }
      ]
    },
    "locator-set": [
      {
        "name": "campus_fabric",
        "IPv4-interface": [
          {
            "name": "Loopback0",
            "priority": 0,
            "weight": 0
          }
        ]
      }
    ],
    "loc-reach-algorithm": {
      "rloc-probing": [
        null
      ]
    },
    "locator-table": {
      "default": [
        null
      ]
    },
    "encapsulation": {
      "vxlan": [
        null
      ]
    }
  }
}'''

url = 'http://10.203.27.104:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/kevios2/yang-ext:mount/ned:native/router/lisp'
print 'Adding LISP'
print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))

request_body = '''{
      "Vlan": [
        {
          "name": 2240,
          "ip": {
            "local-proxy-arp": [
              null
            ],
            "route-cache": {
              "same-interface": true
            },
            "dhcp": {
              "relay": {
                "source-interface": "Loopback0"
              }
            },
            "helper-address": [
              {
                "address": "10.4.49.11",
                "global": [
                  null
                ]
              }
            ],
            "redirects": false,
            "address": {
              "primary": {
                "mask": "255.255.255.0",
                "address": "10.102.240.1"
              }
            }
          },
          "vrf": {
            "forwarding": "VRF-IOT"
          },
          "lisp": {
            "mobility": {
              "dynamic-eid": {
                "dynamic-eid-name": "IOT.EID.10_102_240_0"
              }
            }
          }
        }
    ]
}'''

url = 'http://10.203.27.104:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/kevios2/yang-ext:mount/ned:native/interface/Vlan/2240'
print 'Adding SVI2240'
print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))

request_body = '''{
      "Vlan": [
        {
          "name": 2241,
          "ip": {
            "local-proxy-arp": [
              null
            ],
            "route-cache": {
              "same-interface": true
            },
            "dhcp": {
              "relay": {
                "source-interface": "Loopback0"
              }
            },
            "helper-address": [
              {
                "address": "10.4.49.11",
                "global": [
                  null
                ]
              }
            ],
            "redirects": false,
            "address": {
              "primary": {
                "mask": "255.255.255.0",
                "address": "10.102.241.1"
              }
            }
          },
          "vrf": {
            "forwarding": "VRF-IOT"
          },
          "lisp": {
            "mobility": {
              "dynamic-eid": {
                "dynamic-eid-name": "IOT.EID.10_102_241_0"
              }
            }
          }
        }
      ]
   }
}'''
url = 'http://10.203.27.104:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/kevios2/yang-ext:mount/ned:native/interface/Vlan/2241'
print 'Adding SVI2241'
print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))

request_body = '''{
      "Vlan": [
        {
          "name": 3241,
          "ip": {
            "local-proxy-arp": [
              null
            ],
            "route-cache": {
              "same-interface": true
            },
            "dhcp": {
              "relay": {
                "source-interface": "Loopback0"
              }
            },
            "helper-address": [
              {
                "address": "10.4.49.11",
                "global": [
                  null
                ]
              }
            ],
            "redirects": false,
            "address": {
              "primary": {
                "mask": "255.255.255.0",
                "address": "10.103.241.1"
              }
            }
          },
          "vrf": {
            "forwarding": "VRF-DEVELOPMENT"
          },
          "lisp": {
            "mobility": {
              "dynamic-eid": {
                "dynamic-eid-name": "DEVELOPMENT.EID.10_103_241_0"
              }
            }
          }
        }
      ]
   }
}'''
url = 'http://10.203.27.104:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/kevios2/yang-ext:mount/ned:native/interface/Vlan/3241'
print 'Adding SVI3241'
print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))

request_body = '''{
      "Vlan": [
        {
          "name": 3240,
          "ip": {
            "local-proxy-arp": [
              null
            ],
            "route-cache": {
              "same-interface": true
            },
            "dhcp": {
              "relay": {
                "source-interface": "Loopback0"
              }
            },
            "helper-address": [
              {
                "address": "10.4.49.11",
                "global": [
                  null
                ]
              }
            ],
            "redirects": false,
            "address": {
              "primary": {
                "mask": "255.255.255.0",
                "address": "10.103.240.1"
              }
            }
          },
          "vrf": {
            "forwarding": "VRF-DEVELOPMENT"
          },
          "lisp": {
            "mobility": {
              "dynamic-eid": {
                "dynamic-eid-name": "DEVELOPMENT.EID.10_103_240_0"
              }
            }
          }
        }
      ]
   }
}'''
url = 'http://10.203.27.104:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/kevios2/yang-ext:mount/ned:native/interface/Vlan/3240'
print 'Adding SVI3240'
print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))

request_body = '''{
      "Vlan": [
        {
          "name": 1240,
          "ip": {
            "local-proxy-arp": [
              null
            ],
            "route-cache": {
              "same-interface": true
            },
            "dhcp": {
              "relay": {
                "source-interface": "Loopback0"
              }
            },
            "helper-address": [
              {
                "address": "10.4.49.11",
                "global": [
                  null
                ]
              }
            ],
            "redirects": false,
            "address": {
              "primary": {
                "mask": "255.255.255.0",
                "address": "10.101.240.1"
              }
            }
          },
          "vrf": {
            "forwarding": "VRF-EMPLOYEE"
          },
          "lisp": {
            "mobility": {
              "dynamic-eid": {
                "dynamic-eid-name": "EMPLOYEE.EID.10_101_240_0"
              }
            }
          }
        }
      ]
  }'''
url = 'http://10.203.27.104:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/kevios2/yang-ext:mount/ned:native/interface/Vlan/1240'
print 'Adding SVI1240'
print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))