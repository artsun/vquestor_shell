from processors import getnode, getlinks
from classes import Vertex
from file_maker import to_file
from jsongen import make_json
import json
from globals import res#, set_presets


def dig_in(id_, depth_, mytoken, node_, nd_viz, ed_viz, style_viz):
    if depth_ == 0:
        return None
    print("depth: ", depth_)
    user = {id_: node_.links[id_]}

    node_next = Vertex(user, links = getlinks(id_, user, mytoken))

    node_next.links.pop(next(iter(node_.user)), None)
    node_.nodes.append(node_next)
    make_json(node_next, nd_viz, ed_viz, style_viz)
    for match_friend in node_next.links:
        dig_in(match_friend, depth_-1, mytoken, node_next, nd_viz, ed_viz, style_viz)


def start(base_id, mytoken, depth):
    global res
    res = 0
    print("START DIG")
    user = getnode(base_id, mytoken)
    links = getlinks(base_id, user, mytoken)
    node = Vertex(user, links)
    print("USER: ", user)
    print("LINKS: ", links)
    nd_viz, ed_viz, style_viz = make_json(node)
    for match_friend_id in node.links:
        dig_in(match_friend_id, depth, mytoken, node, nd_viz, ed_viz, style_viz)
    nodes_edges_js = {"nodes": nd_viz, "edges": ed_viz}
    user_data = list()
    user_data.append(nodes_edges_js)
    user_data.append(style_viz)
    to_file(json.dumps(user_data, ensure_ascii=False))
    res = 1

def parse_data(post_data):
    global res
    print("post_data", post_data)
    base_id = post_data[0].replace('base_id=', '')
    if base_id is (None or ''):
        base_id = None #need default
    mytoken = post_data[1].replace('mytoken=', '')
    if mytoken is (None or ''):
        mytoken = None #need default
    depth = post_data[2].replace('depth=', '')
    if depth is (None or ''):
        depth = 2
    #base_id, mytoken, depth = set_presets(base_id, mytoken, depth)
    start(base_id, mytoken, depth)
    res = 1
