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
data['rama'] = [('A', '  51 ', 'ASN', 0.05366343529770439, (28.805000000000007, -1.3480000000000003, 14.481999999999998))]
data['omega'] = []
data['rota'] = [('A', '   5 ', 'LYS', 0.1362176901570257, (-9.425, 4.556, 22.631999999999994)), ('A', '  27 ', 'LEU', 0.27181605663114433, (13.378, -10.058, 25.098999999999993)), ('A', '  39 ', 'PRO', 0.028433995298120088, (14.315999999999997, -8.876999999999997, 16.952)), ('A', '  47 ', 'GLU', 0.1418061544841016, (29.514000000000003, -2.529, 21.947)), ('A', '  50 ', 'LEU', 0.23172709563937635, (27.865999999999996, 0.7959999999999998, 17.453)), ('A', '  59 ', 'ILE', 0.22630470090322946, (27.176999999999996, -17.415, 11.796)), ('A', '  67 ', 'LEU', 0.07676380071909399, (16.907000000000004, -20.473, 24.810999999999993)), ('A', '  73 ', 'VAL', 0.2923901841297378, (8.425000000000004, -24.997, 29.416)), ('A', '  74 ', 'GLN', 0.003400350373279306, (11.681000000000001, -24.731, 27.416999999999998)), ('A', '  93 ', 'THR', 0.11673001005751123, (6.703999999999997, -27.882, 18.924)), ('A', ' 188 ', 'ARG', 0.0, (22.226, 0.057, 15.085999999999997)), ('A', ' 190 ', 'THR', 0.0223772404724455, (23.526999999999997, 5.833, 15.361)), ('A', ' 286 ', 'ILE', 0.1410504180977089, (-7.722999999999998, 19.129, 21.311999999999998))]
data['cbeta'] = [('A', ' 128 ', 'CYS', ' ', 0.25044237212024184, (-0.0749999999999984, 2.477, 18.64399999999999))]
data['probe'] = [(' A  27  LEU HD21', ' A  42  VAL  HB ', -1.116, (16.3, -10.286, 20.234)), (' A 107  GLN  H  ', ' A 110  GLN HE21', -0.926, (-1.957, 0.541, 7.007)), (' A   4  ARG  H  ', ' A 299  GLN HE22', -0.899, (-14.764, 5.468, 22.467)), (' A  27  LEU HD21', ' A  42  VAL  CB ', -0.854, (17.297, -10.364, 21.048)), (' A  53  ASN HD22', ' A  56  ASP  H  ', -0.806, (27.969, -10.708, 9.669)), (' A 216  ASP  OD1', ' A 352  HOH  O  ', -0.769, (-23.075, 19.89, 20.3)), (' A 186  VAL  H  ', ' A 192  GLN HE22', -0.722, (17.513, 3.734, 12.171)), (' A 107  GLN  H  ', ' A 110  GLN  NE2', -0.718, (-1.676, 0.236, 6.747)), (' A 107  GLN  N  ', ' A 110  GLN HE21', -0.668, (-0.982, 0.8, 6.768)), (' A  53  ASN  ND2', ' A  56  ASP  H  ', -0.647, (27.467, -10.179, 9.327)), (' A  51  ASN  HB3', ' A 501  HOH  O  ', -0.617, (31.532, -2.839, 14.737)), (' A  20  VAL HG22', ' A  68  VAL HG22', -0.615, (13.407, -17.732, 21.743)), (' A 307  S89  HAQ', ' A 513  HOH  O  ', -0.602, (17.411, 6.301, 21.613)), (' A  86  LEU  HG ', ' A 179  GLY  HA2', -0.576, (11.384, -8.308, 10.795)), (' A 100  LYS  HD3', ' A 156  CYS  HB2', -0.53, (-8.638, -15.656, 9.928)), (' A   4  ARG  H  ', ' A 299  GLN  NE2', -0.527, (-15.121, 4.843, 22.265)), (' A  27  LEU HD21', ' A  42  VAL  CG2', -0.518, (17.078, -10.856, 21.781)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.51, (1.147, -21.939, 17.241)), (' A  21  THR  HB ', ' A  67  LEU  HG ', -0.501, (18.176, -17.866, 26.487)), (' A  23  GLY  HA3', ' A 507  HOH  O  ', -0.489, (24.584, -13.153, 25.129)), (' A 196  THR HG23', ' A 414  HOH  O  ', -0.467, (12.109, 16.798, 10.457)), (' A  40  ARG  HD3', ' A  85  CYS  HA ', -0.466, (17.302, -8.04, 10.932)), (' A  19  GLN HE21', ' A 119  ASN  HB3', -0.463, (11.661, -13.262, 30.845)), (' A 276  MET  HE3', ' A 281  ILE HG13', -0.462, (-14.051, 20.162, 20.123)), (' A  86  LEU  HG ', ' A 179  GLY  CA ', -0.457, (11.588, -8.494, 10.659)), (' A 176  ASP  HB2', ' A 356  HOH  O  ', -0.453, (4.675, -7.143, 8.751)), (' A 279  ARG  O  ', ' A 432  HOH  O  ', -0.446, (-12.266, 23.159, 23.923)), (' A 251  GLY  O  ', ' A 254  SER  HB3', -0.444, (-20.6, 10.026, 3.518)), (' A  45  THR  O  ', ' A  48  ASP  HB2', -0.439, (26.377, -5.406, 20.948)), (' A  19  GLN  NE2', ' A 119  ASN  HB3', -0.438, (11.282, -13.188, 31.091)), (' A 142  ASN HD22', ' A 307  S89  HA ', -0.416, (15.355, -2.622, 26.025)), (' A  83  GLN  OE1', ' A  88  ARG  HD2', -0.413, (10.871, -14.178, 8.015)), (' A   1  SER  OG ', ' A   2  GLY  N  ', -0.408, (-21.725, 7.582, 24.32)), (' A  31  TRP  HA ', ' A  35  THR  O  ', -0.407, (6.88, -18.909, 16.897)), (' A 227  LEU  C  ', ' A 227  LEU HD23', -0.403, (-8.252, 20.085, -1.641)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.4, (17.552, -11.426, 14.743))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
