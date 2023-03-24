from inspect import signature, getargspec
from dash.dependencies import Input
from dash.exceptions import PreventUpdate
from dash import callback_context

from callback_structs import *
from visualiser import Visualiser
from abstract_dash import AbstractDash

assets_ignore = '.*bootstrap.*'
class DashBoard(AbstractDash):
    def __init__(self, name):
        super().__init__(Visualiser(), name, assets_ignore=assets_ignore)
        self._build_app()
    
    def run(self):
        self.app.run_server(debug=True)
        
    def _build_app(self):
        # Add Options
        form_elements, identifiers = self._create_form_elements(self.visualiser, id_prefix=id_prefix)
        update_i.update(identifiers)

        gns = [{"label": c, "value": c} for c in []]
        inp = (self.create_dropdown(load_s["gns"].component_id, gns, multi=True,placeholder="Load Design") + 
               self.create_line_break(10) + self.create_button(load_i.component_id,"Submit"))
        acc_elements = [("Load Design", inp)]
        load_accordion = self.create_accordion("proj_accordion", acc_elements)
        
        form_div = self.create_div(graph_type_o["id"].component_id, form_elements)
        options = self.create_sidebar(not_modifier_identifiers["sidebar_id"], "Options", form_div, className="col sidebar")
        figure = self.visualiser.empty_graph(graph_id)
        graph = self.create_div(update_o["graph_id"].component_id, [figure], className="col")
        graph = self.create_div(load_o.component_id, graph)
        legend = self.create_div(update_o["legend_id"].component_id,[], className="col sidebar")
        elements = options+graph+legend
        container = self.create_div("row-main", elements, className="row flex-nowrap no-gutters")
        self.app.layout = self.create_div("main", load_accordion+container, className="container-fluid")[0]

        # Bind the callbacks
        def load_inner(click,gns):
            return self.load(click,gns)

        def update_graph_inner(*args):
            return self.update_graph(args)

        def export_img_inner(*args):
            return self.export_graph_img(*args)

        self.add_callback(load_inner, [load_i], [load_o],load_s.values())
        self.add_callback(update_graph_inner, update_i.values(), update_o.values())
        self.add_callback(export_img_inner,export_img_i, export_img_o)
        self.build()

    def load(self,click,gns):
        if not gns or not isinstance(self.visualiser, Visualiser):
            raise PreventUpdate()
        ctx = callback_context
        if ctx.triggered:
            self.visualiser.set_design_names(gns)
            figure = self.visualiser.build(graph_id=graph_id)
            d = self.create_div(update_o["graph_id"].component_id, figure, className="col")
            return d
        else:
            raise PreventUpdate()

    def update_graph(self, *args):
        if not isinstance(self.visualiser, Visualiser):
            raise PreventUpdate()
        args = args[0]
        for index, setter_str in enumerate(args):
            if setter_str is not None:
                try:
                    setter = getattr(self.visualiser, setter_str, None)
                    parameter = None
                except TypeError:
                    # Must be a input element rather than a checkbox.
                    # With annonymous implementation this is tough.
                    to_call = list(update_i.keys())[index]
                    parameter = setter_str
                    setter = getattr(self.visualiser, to_call, None)
                if setter is not None:
                    try:
                        if parameter is not None and len(getargspec(setter).args) > 1:
                            setter(parameter)
                        else:
                            setter()
                    except Exception as ex:
                        print(ex)
                        raise PreventUpdate()
        try:
            figure, legend = self.visualiser.build(graph_id=graph_id, legend=True)
            legend = self.create_legend(legend)
            return [figure], legend
        except Exception as ex:
            print(ex)
            raise PreventUpdate()

    def export_graph_img(self, get_jpg_clicks, get_png_clicks, get_svg_clicks):
        action = 'store'
        input_id = None
        ctx = callback_context
        if ctx.triggered:
            input_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if input_id != "tabs":
                action = "download"
        else:
            raise PreventUpdate()
        return [{'type': input_id, 'action': action}]


    def _create_form_elements(self, visualiser, style={}, id_prefix=""):
        default_options = [visualiser.set_full_graph_view,
                           visualiser.set_concentric_layout,
                           visualiser.add_node_no_labels,
                           visualiser.add_edge_no_labels,
                           visualiser.add_standard_node_color,
                           visualiser.add_standard_edge_color]

        options = self._generate_options(visualiser)
        removal_words = ["Add", "Set"]
        elements = []
        identifiers = {}
        for k, v in options.items():
            name = self._beautify_name(k)
            identifier = id_prefix + "_" + k
            element = []

            if isinstance(v, (int, float)):
                min_v = int(v/1.7)
                max_v = int(v*1.7)
                default_val = int((min_v + max_v) / 2)
                step = 1

                element += (self.create_heading_6("", name) +
                            self.create_slider(identifier, min_v, max_v, default_val=default_val, step=step))
                identifiers[k] = Input(identifier, "value")

            elif isinstance(v, dict):
                removal_words = removal_words + \
                    [word for word in name.split(" ")]
                inputs = []
                default_button = None
                for k1, v1 in v.items():
                    label = self._beautify_name(k1)
                    label = "".join(
                        "" if i in removal_words else i + " " for i in label.split())
                    inputs.append({"label": label, "value": k1})
                    if v1 in default_options:
                        default_button = k1

                element = (self.create_heading_6(k, name) +
                           self.create_radio_item(identifier, inputs, value=default_button))
                identifiers[k] = Input(identifier, "value")

            breaker = self.create_horizontal_row(False)
            elements = elements + \
                self.create_div(identifier + "_contamanual_toolbariner",
                                element, style=style)
            elements = elements + breaker


        exports = self.create_heading_4("export_img_heading", "Image Export")
        for e_input in export_img_i:
            exports += self.create_button(e_input.component_id,
                                          className="export_img_button")
            exports += self.create_line_break()
        export_div = self.create_div("export_data_container", exports, style=style)

        return (elements + export_div, identifiers)

    def _beautify_name(self, name):
        name_parts = name.split("_")
        name = "".join([p.capitalize() + " " for p in name_parts])
        return name

    def _generate_options(self, visualiser):
        blacklist_functions = ["empty_graph",
                               "build",
                               "mode",
                               "view",
                               "node_size",
                               "edge_color",
                               "node_color",
                               "copy_settings",
                               "get_design_names",
                               "edge_shape",
                               "edge_text",
                               "node_shape",
                               "node_text",
                               "set_design_names",
                               "get_load_predicates",
                               "get_loaded_design_names"]

        options = {"view": {},
                   "layout": {}}

        for func_str in dir(visualiser):
            if func_str[0] == "_":
                continue
            func = getattr(visualiser, func_str, None)

            if func is None or func_str in blacklist_functions or not callable(func):
                continue

            if len(signature(func).parameters) > 0:
                # When there is parameters a slider will be used.
                # Some Paramterised setters will return there default val if one isnt provided.
                default_val = func()
                if default_val is None:
                    default_val = 1
                options[func_str] = default_val
            else:
                # When no params radiobox.
                if func_str.split("_")[-1] == "preset":
                    option_name = "preset"

                elif func_str.split("_")[-1] == "view":
                    option_name = "view"

                elif func_str.split("_")[-1] == "mode":
                    option_name = "mode"

                elif func_str.split("_")[-1] == "layout":
                    option_name = "layout"

                elif func_str.split("_")[-1] == "connect":
                    option_name = "connect"

                elif "node" in func_str:
                    option_name = "node" + "_" + func_str.split("_")[-1]

                elif "edge" in func_str:
                    option_name = "edge" + "_" + func_str.split("_")[-1]
                elif func_str.split("_")[-1] == "level":
                    option_name = "detail"
                else:
                    option_name = "misc"

                if option_name not in options.keys():
                    options[option_name] = {func_str: func}
                else:
                    options[option_name][func_str] = func
        return options
