
# [ {
#     "nodes": [{"data":{"id": x, "label": ""}}, ...], "edges": [{"data": {"id": x, "source": y, "target": z}}, ...]
#   },
#  [{"selector": "node#x", "style": {"label": "data(label)", "background-image": ""}},]
# ]


def make_json(node, nd=None, ed=None, style=None):
    user_id = next(iter(node.user))
    if nd is None and ed is None and style is None:
        nd = list()
        ed = list()
        style = list()
        style.append(
                        {"selector": "node#" + str(user_id),
                         "style": {"label": "data(label)", "background-image": node.user[user_id]['photo_50']}}
                    )
        nd.append(nodepaint(user_id, node.user[user_id]['first_name'] + " " + node.user[user_id]['last_name']))
    for key in node.links:
        nd.append(nodepaint(key, node.links[key]['first_name'] + " " + node.links[key]['last_name']))
        ed.append(edgepaint(user_id, key))
        style.append(stylepaint(key, node))
    return nd, ed, style


def nodepaint(user_id, label_):
    return {"data": {"id": user_id, "label": label_}}


def edgepaint(user_id1, user_id2):
    return {"data": {"id": (user_id1 + user_id2), "source": user_id1, "target": user_id2}}


def stylepaint(user_id, node_):
    return {"selector": "node#" + str(user_id), "style": {"label": "data(label)",
                                                          "background-image": node_.links[user_id]['photo_50']}}
