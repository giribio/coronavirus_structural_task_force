# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('A', '  92 ', 'ASP', 0.0, (33.91, 13.348, 11.565)), ('A', ' 154 ', 'TYR', 0.022000251179586393, (4.355, 18.904, 10.429)), ('A', ' 277 ', 'ASN', 0.005230704937629905, (-20.15, -12.455, 2.372)), ('A', ' 286 ', 'ILE', 0.004868754758170384, (-11.435, -8.214, 4.288))]
data['omega'] = []
data['rota'] = [('A', '  27 ', 'LEU', 0.19861337742477259, (24.257, -2.739, 6.601)), ('A', '  47 ', 'GLU', 0.21110569487289518, (30.501, -18.525, 12.971999999999998)), ('A', '  50 ', 'LEU', 0.03589755153004745, (24.513, -17.857, 17.648)), ('A', '  51 ', 'ASN', 0.004952465863445594, (25.895, -16.476, 20.934)), ('A', '  55 ', 'GLU', 0.11254433672285878, (30.516, -6.108, 24.567)), ('A', '  72 ', 'ASN', 0.0, (30.697, 7.756, -2.116)), ('A', '  92 ', 'ASP', 0.2782720572401332, (33.91, 13.348, 11.565)), ('A', ' 106 ', 'ILE', 0.015261404641375178, (5.768, 3.022, 19.653)), ('A', ' 123 ', 'SER', 0.25365596306314964, (14.788, 1.276, -2.405)), ('A', ' 125 ', 'VAL', 0.20297363546124925, (8.81, 3.234, 1.329)), ('A', ' 167 ', 'LEU', 0.03731686969507478, (11.408, -14.434, 11.918)), ('A', ' 214 ', 'ASN', 0.12545666772835518, (-15.986, 8.212, 2.428)), ('A', ' 216 ', 'ASP', 0.22352670894880933, (-19.869, 3.772, 2.59)), ('A', ' 222 ', 'ARG', 0.005215496913416037, (-32.189428571428564, -5.772857142857142, 11.983285714285715)), ('A', ' 224 ', 'THR', 0.012215936184994633, (-27.218, -2.978, 19.588)), ('A', ' 226 ', 'THR', 0.016319203132297844, (-22.674999999999997, -3.742, 25.153)), ('A', ' 227 ', 'LEU', 7.755794317504211e-05, (-18.801, -3.373, 25.271)), ('A', ' 235 ', 'MET', 0.06236594171951844, (-12.233, -12.504, 20.698)), ('A', ' 243 ', 'THR', 0.10610295386693665, (-10.994, -1.5719999999999996, 26.382)), ('A', ' 268 ', 'LEU', 0.0004437707052501585, (-18.325, -4.969, 13.372)), ('A', ' 277 ', 'ASN', 0.020376553815987433, (-20.15, -12.455, 2.372)), ('A', ' 286 ', 'ILE', 0.015194340562067104, (-11.435, -8.214, 4.288)), ('A', ' 298 ', 'ARG', 0.0910699405178921, (-0.8706000000000002, 10.171199999999999, 9.428400000000002))]
data['cbeta'] = [('A', '  41 ', 'HIS', ' ', 0.27174791631402645, (24.041, -8.22, 14.478999999999997)), ('A', '  48 ', 'ASP', ' ', 0.2596972968587642, (30.067, -16.229, 17.081)), ('A', '  55 ', 'GLU', ' ', 0.33986916088639857, (30.023, -5.689999999999999, 25.984)), ('A', '  92 ', 'ASP', ' ', 0.41527898748626146, (33.853, 12.95, 10.043)), ('A', ' 249 ', 'ILE', ' ', 0.2927757263904011, (-8.464, 5.909999999999998, 21.193)), ('A', ' 286 ', 'ILE', ' ', 0.335804001412371, (-9.951, -8.773, 4.059)), ('A', ' 290 ', 'GLU', ' ', 0.28251107550510846, (-2.301, -1.953, 8.75))]
data['probe'] = [(' A 145  CYS  SG ', ' A 401  AZP HBM2', -1.751, (20.826, -6.727, 7.181)), (' A 145  CYS  SG ', ' A 401  AZP  CBM', -1.346, (20.784, -7.665, 7.512)), (' A  19  GLN HE21', ' A  26  THR HG21', -0.928, (27.635, -2.055, 2.106)), (' A  72  ASN  H  ', ' A  72  ASN HD22', -0.895, (28.907, 9.787, -2.736)), (' A 231  ASN  O  ', ' A 235  MET  HG2', -0.889, (-14.261, -11.021, 22.028)), (' A 271  LEU  O  ', ' A 275  GLY  HA2', -0.881, (-18.958, -10.218, 8.142)), (' A  49  MET  HE2', ' A 401  AZP HBT2', -0.859, (25.764, -12.247, 9.827)), (' A 226  THR HG22', ' A 229  ASP  H  ', -0.817, (-21.71, -6.477, 25.48)), (' A 222 AARG  HG3', ' A 222 AARG HH11', -0.814, (-32.308, -5.126, 12.926)), (' A  72  ASN  H  ', ' A  72  ASN  ND2', -0.814, (28.966, 9.177, -3.186)), (' A 106  ILE HD13', ' A 160  CYS  CB ', -0.808, (7.117, 4.747, 16.091)), (' A 276  MET  HE3', ' A 281  ILE HD12', -0.804, (-16.537, -4.448, 4.501)), (' A  72  ASN  N  ', ' A  72  ASN HD22', -0.754, (28.921, 8.632, -2.669)), (' A   7  ALA  HB2', ' A 402  ACY  H3 ', -0.691, (4.35, 5.04, 1.773)), (' A 222 AARG  HG3', ' A 222 AARG  NH1', -0.664, (-32.144, -5.516, 13.158)), (' A 231  ASN  O  ', ' A 235  MET  CG ', -0.657, (-13.836, -11.654, 22.556)), (' A 106  ILE HD13', ' A 160  CYS  HB2', -0.653, (8.008, 4.362, 16.646)), (' A 284  SER  OG ', ' A 285  THR  O  ', -0.644, (-11.055, -5.438, 1.521)), (' A 167  LEU HD13', ' A 401  AZP  HAC', -0.64, (10.452, -14.376, 15.759)), (' A 106  ILE HD13', ' A 160  CYS  HB3', -0.612, (8.001, 5.38, 16.69)), (' A   7  ALA  CB ', ' A 402  ACY  H3 ', -0.605, (4.309, 5.474, 1.352)), (' A 145  CYS  SG ', ' A 401  AZP  CBK', -0.6, (20.326, -7.435, 7.522)), (' A 285  THR  O  ', ' A 286  ILE HG13', -0.6, (-10.416, -6.977, 2.256)), (' A 232  LEU  O  ', ' A 236  LYS  HD3', -0.577, (-15.74, -14.533, 21.388)), (' A 253  LEU  O  ', ' A 257  THR HG23', -0.576, (-16.695, 9.786, 12.51)), (' A 276  MET  O  ', ' A 277  ASN  C  ', -0.56, (-20.742, -10.844, 0.974)), (' A 123  SER  HB2', ' A 489  HOH  O  ', -0.536, (15.727, -0.701, -4.46)), (' A  19  GLN  HG3', ' A  26  THR  CG2', -0.526, (26.907, -0.605, 3.332)), (' A  22  CYS  SG ', ' A  61  LYS  NZ ', -0.524, (33.497, -3.944, 12.67)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.507, (14.368, 5.347, 0.803)), (' A 277  ASN  N  ', ' A 411  HOH  O  ', -0.493, (-18.716, -11.607, 3.904)), (' A  53  ASN  O  ', ' A  57  LEU  HG ', -0.488, (31.365, -10.127, 20.929)), (' A 271  LEU  O  ', ' A 275  GLY  CA ', -0.486, (-19.735, -10.596, 7.913)), (' A 233  VAL  O  ', ' A 236  LYS  HB2', -0.477, (-15.983, -14.12, 18.713)), (' A  19  GLN  HG3', ' A  26  THR HG23', -0.462, (27.094, -0.543, 3.888)), (' A  19  GLN  NE2', ' A  26  THR HG21', -0.452, (27.858, -1.072, 2.144)), (' A 253  LEU  HA ', ' A 256  GLN  HG2', -0.444, (-14.718, 11.535, 13.13)), (' A 167  LEU  N  ', ' A 167  LEU HD23', -0.438, (11.675, -12.472, 12.085)), (' A 401  AZP  CAI', ' A 401  AZP HD13', -0.435, (16.682, -16.16, 12.351)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.433, (9.209, 3.795, 9.08)), (' A  49  MET  HG2', ' A 401  AZP  HBI', -0.432, (24.681, -13.231, 13.29)), (' A 167  LEU HD13', ' A 401  AZP  CAC', -0.432, (10.941, -14.605, 15.951)), (' A 167  LEU  HG ', ' A 171  VAL HG23', -0.432, (8.421, -11.969, 12.646)), (' A 167  LEU HD21', ' A 173  ALA  HB2', -0.424, (11.147, -10.336, 15.187)), (' A 199  THR HG21', ' A 239  TYR  CZ ', -0.412, (-10.429, -8.038, 12.968)), (' A  27  LEU HD11', ' A  42  VAL  HB ', -0.406, (25.952, -3.06, 11.107)), (' A 220  LEU  HA ', ' A 220  LEU HD23', -0.406, (-22.858, 0.848, 10.41))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
