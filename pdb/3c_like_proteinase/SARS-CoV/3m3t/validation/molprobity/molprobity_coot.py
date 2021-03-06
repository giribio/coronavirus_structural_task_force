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
data['rama'] = [('A', '  46 ', 'ALA', 0.035763092526107515, (10.083000000000002, -11.585, 38.491)), ('A', '  48 ', 'ASP', 0.04579678861830303, (6.467999999999996, -14.440000000000003, 42.06900000000002)), ('A', ' 106 ', 'ILE', 0.004866228655986992, (-12.238000000000003, -16.139, 17.782000000000007)), ('A', ' 145 ', 'CYS', 0.001497405186634185, (2.8199999999999967, -7.487, 26.580000000000005)), ('A', ' 154 ', 'TYR', 0.03057681042013903, (-17.91700000000001, -1.131, 9.867000000000004)), ('A', ' 301 ', 'SER', 0.003585392323530038, (1.3800000000000008, -8.019, -5.485000000000002))]
data['omega'] = []
data['rota'] = [('A', '  12 ', 'LYS', 0.029120067114588064, (-8.934000000000001, 4.736, 17.021)), ('A', ' 127 ', 'GLN', 0.013773049722673375, (-2.3740000000000023, -8.989, 10.832000000000004)), ('A', ' 188 ', 'ARG', 0.029096875839293986, (3.1729999999999947, -18.419, 35.539)), ('A', ' 227 ', 'LEU', 0.1746068865551697, (4.808, -34.334, -1.9410000000000003)), ('A', ' 268 ', 'LEU', 0.1365237357390786, (13.674, -26.061000000000007, 0.8360000000000002))]
data['cbeta'] = []
data['probe'] = [(' A 131  ARG  HD2', ' A 200  ILE HD11', -0.963, (2.17, -20.856, 12.283)), (' A 108  PRO  HA ', ' A 130  MET  HB3', -0.845, (-6.399, -18.963, 15.123)), (' A   6  MET  HE2', ' A 298  ALA  HB1', -0.785, (-1.597, -6.665, 1.29)), (' A 186  VAL HG21', ' A 188  ARG  NH1', -0.762, (0.793, -23.099, 34.095)), (' A 131  ARG  NH1', ' A 200  ILE HG12', -0.757, (2.294, -23.682, 11.211)), (' A 286  ILE  O  ', ' A 286  ILE HD12', -0.744, (15.654, -16.69, 8.695)), (' A  86  LEU  HG ', ' A 179  GLY  HA2', -0.733, (-7.796, -12.353, 30.889)), (' A  10  SER  HB3', ' A 125  VAL HG21', -0.71, (-3.68, 0.48, 13.463)), (' A  88  ARG  HB3', ' A  88  ARG  NH1', -0.708, (-13.239, -4.59, 36.19)), (' A  45  THR HG22', ' A  48  ASP  OD2', -0.705, (6.769, -10.407, 42.864)), (' A  33  ASP  O  ', ' A  94  SER  HA ', -0.692, (-13.297, 5.982, 30.047)), (' A  40  ARG  O  ', ' A  43  ILE HG12', -0.671, (-0.632, -9.431, 38.308)), (' A 186  VAL HG21', ' A 188  ARG HH11', -0.666, (0.119, -22.475, 35.014)), (' A  31  TRP  CD2', ' A  95  ASN  HB2', -0.65, (-9.312, 5.501, 27.798)), (' A 276  MET  O  ', ' A 279  ARG  HG3', -0.647, (24.696, -21.092, 2.383)), (' A 165  MET  HE1', ' A 181  PHE  CZ ', -0.636, (-0.262, -16.643, 29.951)), (' A 293  PRO  O  ', ' A 297  VAL HG23', -0.626, (0.835, -15.076, -0.703)), (' A 210  ALA  HB2', ' A 296  VAL HG13', -0.62, (7.134, -12.831, -0.357)), (' A 232  LEU  O  ', ' A 236  LYS  HG2', -0.619, (11.656, -36.688, 7.115)), (' A  15  GLY  O  ', ' A  97  LYS  HE2', -0.603, (-7.617, 6.852, 23.697)), (' A 115  LEU HD13', ' A 125  VAL HG22', -0.599, (-2.564, -0.264, 15.917)), (' A 165  MET  HE1', ' A 181  PHE  HZ ', -0.595, (-0.264, -15.817, 29.99)), (' A 144  SER  O  ', ' A 145  CYS  CB ', -0.589, (4.457, -7.704, 27.091)), (' A 144  SER  O  ', ' A 145  CYS  HB2', -0.584, (4.558, -7.936, 27.081)), (' A 116  ALA  HB2', ' A 140  PHE  HD2', -0.583, (3.273, -5.897, 17.106)), (' A 227  LEU HD22', ' A 231  ASN HD21', -0.58, (3.349, -34.086, 1.463)), (' A  86  LEU  HG ', ' A 179  GLY  CA ', -0.575, (-8.852, -12.083, 30.651)), (' A  97  LYS  H  ', ' A  97  LYS  HD3', -0.567, (-10.427, 8.591, 23.615)), (' A  13  VAL HG11', ' A 150  PHE  CE2', -0.566, (-6.393, -2.187, 17.751)), (' A   8  PHE  HB3', ' A   9  PRO  HD2', -0.547, (-5.933, -3.249, 8.481)), (' A   3  PHE  HZ ', ' A 296  VAL  HA ', -0.547, (4.826, -10.861, 1.079)), (' A 276  MET  HE3', ' A 281  ILE HG13', -0.547, (19.257, -17.893, 2.771)), (' A   6  MET  HB3', ' A   8  PHE  HE1', -0.543, (-1.583, -6.388, 5.951)), (' A 131  ARG HH11', ' A 200  ILE HG12', -0.541, (2.411, -23.38, 12.169)), (' A 111  THR  HB ', ' A 127  GLN  OE1', -0.54, (-5.747, -11.819, 9.526)), (' A 256  GLN  OE1', ' A 302  GLY  HA3', -0.54, (2.769, -11.133, -8.417)), (' A 200  ILE  HA ', ' A 240  GLU  HG3', -0.533, (4.181, -24.886, 9.718)), (' A 260  ALA  HB3', ' A 263  ASP  OD2', -0.53, (8.319, -27.058, -10.585)), (' A 131  ARG  HD2', ' A 200  ILE  CD1', -0.529, (2.418, -21.285, 12.265)), (' A 133  ASN  O  ', ' A 134  HIS  HB2', -0.519, (-2.456, -22.948, 21.25)), (' A 210  ALA  HB2', ' A 296  VAL  CG1', -0.517, (6.473, -13.555, -0.438)), (' A 107  GLN  HG2', ' A 110  GLN  OE1', -0.514, (-12.218, -18.652, 14.869)), (' A  63  ASN  HB3', ' A  77  VAL  O  ', -0.508, (-7.667, 3.377, 42.582)), (' A 227  LEU  CD2', ' A 231  ASN HD21', -0.505, (3.374, -33.695, 1.035)), (' A 234  ALA  O  ', ' A 239  TYR  HB2', -0.504, (9.862, -30.704, 8.686)), (' A  31  TRP  CE2', ' A  95  ASN  HB2', -0.502, (-9.828, 5.983, 28.679)), (' A  10  SER  O  ', ' A  13  VAL HG23', -0.499, (-9.119, 0.268, 16.314)), (' A 211  ALA  HA ', ' A 282  LEU HD21', -0.497, (13.144, -11.968, -1.089)), (' A  12  LYS  HD3', ' A  12  LYS  N  ', -0.497, (-9.134, 5.083, 15.043)), (' A  48  ASP  O  ', ' A  52  PRO  HB3', -0.496, (3.82, -15.091, 40.39)), (' A 198  THR  HA ', ' A 238  ASN  OD1', -0.496, (7.637, -28.185, 14.643)), (' A 212  VAL  O  ', ' A 217  ARG  NH2', -0.495, (13.84, -13.622, -8.067)), (' A 223  PHE  CD2', ' A 223  PHE  N  ', -0.481, (17.844, -29.705, -8.956)), (' A 137  LYS  HD2', ' A 200  ILE HD11', -0.478, (3.505, -20.544, 12.891)), (' A  83  GLN  HG2', ' A 178  GLU  O  ', -0.475, (-12.203, -12.328, 32.248)), (' A   8  PHE  CE2', ' A 127  GLN  HG3', -0.469, (-4.35, -7.288, 7.394)), (' A  99  PRO  O  ', ' A 101  TYR  HD2', -0.469, (-16.281, 0.567, 21.976)), (' A 227  LEU HD21', ' A 242  LEU  O  ', -0.465, (2.024, -32.105, 1.064)), (' A 118  TYR  C  ', ' A 120  GLY  H  ', -0.464, (5.938, 1.153, 23.838)), (' A 233  VAL HG13', ' A 237  TYR  CE1', -0.464, (15.283, -33.248, 6.454)), (' A  27  LEU HD21', ' A  42  VAL  HB ', -0.463, (0.392, -6.547, 34.102)), (' A  95  ASN  OD1', ' A  97  LYS  HD3', -0.46, (-9.836, 8.326, 24.378)), (' A  88  ARG  HB3', ' A  88  ARG HH11', -0.459, (-12.9, -5.017, 37.116)), (' A 145  CYS  HA ', ' A 163  HIS  CD2', -0.458, (2.61, -9.011, 25.205)), (' A 107  GLN  HB2', ' A 108  PRO  CD ', -0.456, (-9.817, -21.573, 16.608)), (' A   8  PHE  CZ ', ' A 127  GLN  HG3', -0.454, (-3.853, -7.591, 7.759)), (' A  43  ILE HD11', ' A  54  TYR  HD2', -0.453, (-2.07, -11.329, 40.44)), (' A 276  MET  O  ', ' A 277  ASN  HB2', -0.452, (24.971, -21.917, 3.165)), (' A   3  PHE  CZ ', ' A 296  VAL  HA ', -0.45, (5.308, -10.933, 1.654)), (' A  83  GLN  O  ', ' A  84  ASN  HB2', -0.45, (-10.019, -13.29, 33.695)), (' A 131  ARG  HA ', ' A 131  ARG  HE ', -0.448, (-1.366, -21.395, 13.444)), (' A 203  ASN  OD1', ' A 292  THR  HA ', -0.442, (2.301, -17.99, 5.886)), (' A 142  ASN  HB2', ' A 317  HOH  O  ', -0.442, (9.916, -11.379, 19.601)), (' A 221  ASN HD21', ' A 267  ALA  HA ', -0.441, (16.679, -27.188, -3.646)), (' A 230  PHE  CD1', ' A 265  CYS  HB3', -0.44, (9.534, -30.168, -0.317)), (' A 200  ILE HG21', ' A 203  ASN  ND2', -0.439, (2.885, -20.721, 8.678)), (' A 205  LEU HD11', ' A 242  LEU HD22', -0.437, (5.161, -26.276, 1.107)), (' A 207  TRP  CZ3', ' A 287  LEU  HA ', -0.434, (14.465, -18.486, 5.983)), (' A 153  ASP  O  ', ' A 154  TYR  HB2', -0.43, (-18.925, -2.477, 11.325)), (' A 175  THR HG22', ' A 181  PHE  HA ', -0.424, (-5.588, -16.691, 27.812)), (' A  58  LEU  C  ', ' A  60  ARG  H  ', -0.423, (-3.266, -8.02, 47.483)), (' A  78  ILE HD11', ' A  90  LYS  HE3', -0.42, (-14.636, 4.244, 39.074)), (' A   6  MET  HB3', ' A   8  PHE  CE1', -0.42, (-1.614, -6.131, 5.962)), (' A 212  VAL  CG2', ' A 220  LEU HD11', -0.416, (13.443, -18.637, -6.665)), (' A 163  HIS  CE1', ' A 172  HIS  HD2', -0.415, (4.086, -12.286, 23.531)), (' A  40  ARG  NH1', ' A  82  MET  HE3', -0.412, (-7.172, -14.609, 39.194)), (' A 286  ILE  C  ', ' A 286  ILE HD12', -0.409, (15.855, -17.502, 9.244)), (' A  28  ASN  ND2', ' A 117  CYS  HB2', -0.408, (2.3, -2.355, 24.475)), (' A 133  ASN  ND2', ' A 196  THR  HA ', -0.407, (2.894, -24.532, 18.708)), (' A 106  ILE HG13', ' A 107  GLN  N  ', -0.406, (-10.08, -16.931, 17.383)), (' A 204  VAL  O  ', ' A 207  TRP  HB3', -0.406, (9.385, -18.447, 3.386)), (' A  88  ARG  CB ', ' A  88  ARG HH11', -0.405, (-12.638, -5.196, 36.676)), (' A 107  GLN  HB2', ' A 108  PRO  HD2', -0.403, (-10.313, -21.756, 16.67)), (' A  40  ARG  NH1', ' A  84  ASN  O  ', -0.403, (-6.747, -14.805, 37.512)), (' A  41  HIS  C  ', ' A  41  HIS  CD2', -0.403, (1.656, -9.664, 35.212)), (' A  90  LYS  HB3', ' A  90  LYS  HE3', -0.402, (-13.443, 2.835, 38.763)), (' A 251  GLY  N  ', ' A 252  PRO  CD ', -0.401, (-1.338, -19.966, -5.285)), (' A 231  ASN  OD1', ' A 242  LEU  N  ', -0.4, (3.468, -31.856, 3.945))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
