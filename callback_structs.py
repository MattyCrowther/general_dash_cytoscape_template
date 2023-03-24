from collections import OrderedDict

from dash.dependencies import Input, Output, State

id_prefix = "cyto"
graph_id = "full_graph"
default_options = []
preset_i = OrderedDict()
preset_o = OrderedDict()
update_i = OrderedDict()

not_modifier_identifiers = {"sidebar_id": "sidebar-left",
                            "utility_id": "utility"}

update_i_i = Input(graph_id, "style")
update_i_o = Output("load_i", "options")
load_i = Input("load_submit", "n_clicks")
load_s = {"gns": State(update_i_o.component_id, "value")}
load_o = Output("graph_content", "children")

update_o = {"graph_id": Output("content", "children"),
            "legend_id": Output("sidebar-right", "children")}

graph_type_o = {"id": Output("options", "style"),
                "div": Output("div", "children")}

export_img_i = [Input("png", "n_clicks"),
                Input("jpg", "n_clicks"),
                Input("svg", "n_clicks")]
export_img_o = [Output(graph_id, "generateImage")]









