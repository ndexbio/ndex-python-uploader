__author__ = 'dexter'

import tsv.delim2cx as d2c
import json
import ndex.client as nc
import requests
import os

# body

# this utility currently uses an early prototype cx as an intermediate form for a network
# parsed from a tsv file in which each row corresponds to an edge

# later it will be converted to use the real cx API

import argparse, sys

parser = argparse.ArgumentParser(description='create NDEx network from TSV, one edge per line')

parser.add_argument('username', action='store')
parser.add_argument('password', action='store')
parser.add_argument('server', action='store')
parser.add_argument('tsv', action='store')
parser.add_argument('plan', action='store')
parser.add_argument('name', action='store')
parser.add_argument('desc', action='store')

arg = parser.parse_args()

try:
    # set up the ndex connection
    # error thrown if cannot authenticate
    my_ndex = nc.Ndex("http://" + arg.server, arg.username, arg.password)

    current_directory = os.path.dirname(os.path.abspath(__file__))

    plan_filename = os.path.join(current_directory, "import_plans", arg.plan)

    print "loading plan from: " + plan_filename

    # error thrown if no plan is found
    with open(plan_filename) as json_file:
        import_plan = json.load(json_file)

    # set up the tsv -> cx converter
    tsv_converter = d2c.TSV2CXConverter(import_plan)

    tsv_filename = os.path.join(current_directory, "import", arg.tsv)

    print "loading tsv from: " + tsv_filename

    cx = tsv_converter.convert_tsv_to_cx_using_networkn(tsv_filename)

    #cx = tsv_converter.convert_tsv_to_cx(tsv_filename)

    print json.dumps(cx)

    #for element in cx:
    #    print json.dumps(element)

    #cx_stream = tsv_converter.convert_cx_to_stream(cx)


    #====================================
    # Create Networkn obj and populate
    # it with the tsv data.
    #====================================

    response_json = my_ndex.save_cx_stream_as_new_network(cx_stream)


    '''Gsmall = nx.Graph()

    Gsmall.add_weighted_edges_from(main_data_tuples)

    export_edges = Gsmall.edges()
    export_nodes = Gsmall.nodes()

    #ndex_gsmall = NdexGraph(networkx_G=Gsmall)
    ndex_gsmall = NdexGraph()
    ndex_nodes_dict = {}

    for export_node in export_nodes:
        ndex_nodes_dict[export_node] = ndex_gsmall.add_new_node(export_node)

    for export_edge in export_edges:
        ndex_gsmall.add_edge_between(ndex_nodes_dict[export_edge[0]],ndex_nodes_dict[export_edge[1]])
        #print export_edge[0] + ' ' + export_edge[1]
        #print str(ndex_nodes_dict[export_edge[0]]) + ' ' + str(ndex_nodes_dict[export_edge[1]])

    ndex_gsmall.write_to('../../cx/' + elasticId + '_manual.cx')

'''


    # # OLD Prototype CODE
    # # (prototype) cx from tsv
    # # this is NOT the standard CX under development as of september 2015
    # cx_network = tsv_converter.convert_tsv_to_cx(tsv_filename)
    #
    # # add a name and description
    #
    # response_json = my_ndex.save_new_network(ndex_network)
    #
    # # set up the cx -> ndex converter
    # c2n_converter = c2n.Cx2NdexConverter(cx_network)
    #
    # # ndex json object converted from prototype cx
    # ndex_network = c2n_converter.convertToNdex()
    #
    # # add a name and description
    # ndex_network['name'] = arg.name
    # ndex_network['description'] = arg.desc
    #
    # #print json.dumps(ndex_network, sort_keys=True, indent=4, separators=(',', ': '))
    #
    # # save the network
    # response_json = my_ndex.save_new_network(ndex_network)

except requests.exceptions.RequestException, e:
    print "error in request to NDEx server: " + str(e)
    raise e











