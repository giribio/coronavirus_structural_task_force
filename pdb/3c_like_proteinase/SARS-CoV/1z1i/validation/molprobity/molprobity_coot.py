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
data['rama'] = [('A', '   2 ', 'GLY', 0.00171543, (58.378, -11.631, 22.491)), ('A', '  33 ', 'ASP', 0.0025323170699492327, (39.048, 4.276, -6.994)), ('A', '  59 ', 'ILE', 0.0060827593183486565, (26.122999999999994, 24.379999999999995, -0.942)), ('A', '  64 ', 'HIS', 0.016422223159891815, (37.51599999999999, 24.563, -7.836999999999999)), ('A', '  70 ', 'ALA', 0.014887158220079438, (47.695, 13.238, -4.093)), ('A', '  81 ', 'SER', 0.01762070943224803, (29.137, 15.574, -2.231)), ('A', ' 106 ', 'ILE', 0.002682801545290084, (34.095, -1.915, 14.045999999999998)), ('A', ' 132 ', 'PRO', 0.05013664928492683, (34.260999999999996, 1.355, 25.703)), ('A', ' 133 ', 'ASN', 0.03273862044122382, (32.868, 4.901, 25.686)), ('A', ' 142 ', 'ASN', 0.013769364078448205, (47.56199999999998, 19.627, 13.813999999999998)), ('A', ' 154 ', 'TYR', 0.0004620011480628745, (46.605, -9.873, 2.671)), ('A', ' 155 ', 'ASP', 0.010078644063480493, (44.27299999999999, -9.108, -0.468)), ('A', ' 161 ', 'TYR', 0.02976187556182538, (37.807, 4.698, 11.414)), ('A', ' 184 ', 'PRO', 0.00301368, (27.531, 10.052999999999999, 19.995)), ('A', ' 185 ', 'PHE', 0.03510578345663816, (29.699, 13.125, 19.397)), ('A', ' 187 ', 'ASP', 0.02595818963873789, (32.028, 17.413, 14.418)), ('A', ' 189 ', 'GLN', 0.038889302741192816, (34.221999999999994, 22.274, 18.475999999999996)), ('A', ' 191 ', 'ALA', 0.00200028415822952, (29.892, 21.149999999999995, 23.748)), ('A', ' 192 ', 'GLN', 0.0021473497941692133, (30.788999999999998, 17.381999999999998, 23.996)), ('A', ' 195 ', 'GLY', 0.01042003068445183, (31.583, 9.561, 29.599)), ('A', ' 216 ', 'ASP', 0.004643354331634605, (55.817, -15.102, 33.048)), ('A', ' 238 ', 'ASN', 0.0013335052541294397, (35.47099999999999, -0.43, 36.045))]
data['omega'] = []
data['rota'] = [('A', '   4 ', 'ARG', 0.27642939436087643, (54.396, -5.865, 21.901999999999997)), ('A', '   5 ', 'LYS', 0.0, (52.389, -3.128, 20.154)), ('A', '  22 ', 'CYS', 0.09693025173230356, (39.958, 24.426, 1.7199999999999998)), ('A', '  25 ', 'THR', 0.1944020251886031, (42.04399999999998, 24.146, 6.448)), ('A', '  38 ', 'CYS', 0.17528193128075886, (37.83899999999999, 13.057, 3.933)), ('A', '  48 ', 'ASP', 0.19998796529204907, (33.569, 24.846000000000007, 13.690999999999999)), ('A', '  75 ', 'LEU', 0.011613234945092416, (44.357, 15.843, -9.525)), ('A', ' 106 ', 'ILE', 0.25284769502851, (34.095, -1.915, 14.045999999999998)), ('A', ' 114 ', 'VAL', 0.2809786909449138, (46.07199999999999, 3.6499999999999995, 12.243)), ('A', ' 119 ', 'ASN', 0.2282403602343972, (49.238, 16.726, 4.181)), ('A', ' 125 ', 'VAL', 0.05934564650148238, (51.625, 3.764, 12.264)), ('A', ' 132 ', 'PRO', 0.1640967148586175, (34.260999999999996, 1.355, 25.703)), ('A', ' 141 ', 'LEU', 0.2373010544540632, (47.95699999999999, 16.443, 15.824)), ('A', ' 142 ', 'ASN', 0.18018521752295896, (47.56199999999998, 19.627, 13.813999999999998)), ('A', ' 187 ', 'ASP', 0.25428028668319147, (32.028, 17.413, 14.418)), ('A', ' 189 ', 'GLN', 0.12652416686512946, (34.221999999999994, 22.274, 18.475999999999996)), ('A', ' 208 ', 'LEU', 0.13376316635715216, (47.303, -12.781, 30.237)), ('A', ' 225 ', 'THR', 0.025823847848947944, (35.99699999999999, -18.988, 40.223)), ('A', ' 226 ', 'THR', 0.11799973922603112, (32.675, -18.633999999999993, 38.324)), ('A', ' 238 ', 'ASN', 0.025657236091428753, (35.47099999999999, -0.43, 36.045)), ('A', ' 274 ', 'ASN', 0.0765736643424936, (45.081, -7.78, 45.484)), ('A', ' 290 ', 'GLU', 0.022459866149998984, (44.45199999999999, -3.274999999999999, 24.329)), ('A', ' 292 ', 'THR', 0.008159601566148922, (42.135, -8.726, 21.401999999999997)), ('A', ' 293 ', 'PRO', 0.2898722024972066, (41.974, -12.503999999999996, 21.261)), ('A', ' 295 ', 'ASP', 0.1611454578914901, (45.51699999999999, -10.009999999999996, 18.106))]
data['cbeta'] = [('A', '  33 ', 'ASP', ' ', 0.67090721513485, (37.904, 3.4919999999999995, -6.978)), ('A', ' 154 ', 'TYR', ' ', 0.6828400948210194, (47.958999999999996, -10.582, 2.384))]
data['probe'] = [(' A  50  LEU  C  ', ' A  51  ASN  N  ', -1.457, (29.178, 26.274, 15.194)), (' A 216  ASP  C  ', ' A 217  ARG  N  ', -1.453, (54.913, -17.358, 33.86)), (' A 154  TYR  C  ', ' A 155  ASP  N  ', -1.415, (45.962, -9.178, 0.144)), (' A  64  HIS  CD2', ' A 655  HOH  O  ', -1.142, (35.601, 25.927, -10.224)), (' A 154  TYR  O  ', ' A 155  ASP  HB2', -1.108, (44.398, -11.036, 1.356)), (' A 154  TYR  O  ', ' A 155  ASP  CB ', -1.075, (44.719, -10.729, 0.212)), (' A 191  ALA  O  ', ' A 192  GLN  HG3', -0.991, (30.624, 19.318, 21.224)), (' A  77  VAL  HA ', ' A  91  VAL HG12', -0.923, (38.771, 15.566, -8.627)), (' A 253  LEU  H  ', ' A 253  LEU HD12', -0.922, (42.602, -19.358, 22.393)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.915, (38.403, -3.003, 22.831)), (' A  21  THR  HB ', ' A  67  LEU  HB3', -0.897, (43.723, 22.727, -1.564)), (' A 105  ARG  NH2', ' A 182  TYR  HA ', -0.895, (30.66, 4.913, 15.21)), (' A 235  MET  HE1', ' A 241  PRO  HB3', -0.831, (30.24, -6.687, 33.863)), (' A  49  MET  SD ', ' A 189  GLN  HG2', -0.816, (36.887, 25.066, 17.489)), (' A 190  THR  O  ', ' A 593  HOH  O  ', -0.815, (33.344, 21.457, 21.486)), (' A  70  ALA  HB2', ' A  75  LEU HD11', -0.807, (45.672, 12.839, -6.295)), (' A 190  THR  O  ', ' A 191  ALA  O  ', -0.794, (31.797, 19.815, 21.634)), (' A  40  ARG  HD3', ' A  85  CYS  HA ', -0.778, (29.988, 14.615, 7.748)), (' A 154  TYR  C  ', ' A 155  ASP  CA ', -0.773, (45.103, -9.812, 0.02)), (' A  64  HIS  CB ', ' A 655  HOH  O  ', -0.765, (35.933, 25.61, -9.75)), (' A  75  LEU  H  ', ' A  75  LEU HD12', -0.764, (45.85, 15.251, -7.509)), (' A 198  THR HG22', ' A 199  THR  H  ', -0.764, (36.138, -1.587, 31.138)), (' A 191  ALA  O  ', ' A 192  GLN  CG ', -0.763, (31.402, 18.124, 21.852)), (' A  86  LEU  HG ', ' A 179  GLY  HA2', -0.76, (31.884, 9.402, 7.13)), (' A  64  HIS  CG ', ' A 655  HOH  O  ', -0.758, (35.824, 25.465, -9.603)), (' A 268  LEU  HA ', ' A 271  LEU HD12', -0.757, (44.007, -11.284, 36.624)), (' A 152  ILE HG22', ' A 153  ASP  N  ', -0.756, (45.431, -8.591, 5.09)), (' A 106  ILE HD11', ' A 130  MET  HE2', -0.737, (36.39, 2.278, 16.989)), (' A 105  ARG HH22', ' A 182  TYR  HA ', -0.736, (30.205, 5.197, 15.35)), (' A 152  ILE HG22', ' A 153  ASP  H  ', -0.735, (44.72, -8.476, 4.741)), (' A 137  LYS  HE3', ' A 171  VAL HG12', -0.731, (42.412, 9.439, 24.735)), (' A 130  MET  HE1', ' A 136  ILE HD11', -0.729, (37.552, 4.77, 17.346)), (' A  64  HIS  HB3', ' A 655  HOH  O  ', -0.727, (36.169, 25.193, -10.237)), (' A 152  ILE HG22', ' A 154  TYR  H  ', -0.727, (45.528, -8.495, 4.612)), (' A 276  MET  HE2', ' A 279  ARG  O  ', -0.712, (53.607, -7.689, 38.016)), (' A 186  VAL  H  ', ' A 192  GLN  NE2', -0.71, (31.141, 15.84, 18.795)), (' A 161  TYR  HA ', ' A 175  THR  O  ', -0.709, (36.212, 5.666, 10.848)), (' A 115  LEU HD11', ' A 122  PRO  HB2', -0.707, (51.8, 6.564, 6.392)), (' A 154  TYR  C  ', ' A 155  ASP  CB ', -0.705, (45.245, -10.385, 0.759)), (' A  64  HIS  HD2', ' A 655  HOH  O  ', -0.704, (35.117, 25.773, -10.354)), (' A 140  PHE  HB3', ' A 144  SER  OG ', -0.702, (45.454, 13.414, 13.893)), (' A 288  GLU  HG2', ' A 291  PHE  HD2', -0.698, (47.776, -5.344, 25.521)), (' A 260  ALA  O  ', ' A 263  ASP  HB2', -0.698, (41.548, -21.387, 33.279)), (' A 154  TYR  O  ', ' A 155  ASP  CG ', -0.697, (45.017, -11.363, 0.526)), (' A 175  THR HG22', ' A 181  PHE  HA ', -0.697, (31.826, 8.743, 13.166)), (' A  70  ALA  CB ', ' A  75  LEU HD11', -0.684, (46.552, 12.903, -6.284)), (' A   5  LYS  H  ', ' A   5  LYS  HZ2', -0.683, (54.195, -3.113, 21.818)), (' A 202  LEU HD23', ' A 661  HOH  O  ', -0.676, (36.864, -9.73, 22.182)), (' A  40  ARG  CD ', ' A  85  CYS  HA ', -0.676, (29.645, 15.534, 7.751)), (' A 237  TYR  O  ', ' A 239  TYR  HD1', -0.674, (37.459, -2.63, 36.067)), (' A 100  LYS  HB3', ' A 155  ASP  O  ', -0.671, (41.774, -6.742, -1.684)), (' A  50  LEU  CB ', ' A  51  ASN  N  ', -0.671, (28.928, 27.968, 15.908)), (' A 207  TRP  CZ3', ' A 287  LEU  HA ', -0.669, (47.231, -6.159, 32.081)), (' A 105  ARG  O  ', ' A 106  ILE  O  ', -0.669, (31.831, -0.88, 14.285)), (' A  78  ILE HG12', ' A  90  LYS  O  ', -0.667, (35.479, 14.426, -9.919)), (' A  30  LEU HD23', ' A 177  LEU HD21', -0.667, (38.828, 5.462, 3.789)), (' A 258  GLY  C  ', ' A 259  ILE HD12', -0.666, (46.84, -23.97, 30.012)), (' A 274  ASN  N  ', ' A 274  ASN HD22', -0.664, (43.228, -9.083, 45.613)), (' A  45  THR  C  ', ' A  47  GLU  H  ', -0.663, (35.091, 28.358, 10.707)), (' A 152  ILE  CD1', ' A 157  VAL HG22', -0.663, (45.468, -3.662, 4.377)), (' A 100  LYS  HE3', ' A 156  CYS  SG ', -0.662, (38.684, -6.932, 0.473)), (' A 159  PHE  HB3', ' A 177  LEU HD13', -0.661, (37.835, 2.794, 5.618)), (' A 217  ARG  NH1', ' A 644  HOH  O  ', -0.657, (57.683, -20.367, 33.819)), (' A 260  ALA  HB3', ' A 263  ASP  OD2', -0.656, (40.868, -23.907, 34.523)), (' A 154  TYR  O  ', ' A 155  ASP  OD2', -0.654, (44.914, -11.124, 1.219)), (' A 163  HIS  HE1', ' A 172  HIS  HB3', -0.651, (41.06, 11.722, 17.265)), (' A 197  ASP  O  ', ' A 238  ASN  ND2', -0.65, (35.359, 2.387, 33.294)), (' A  19  GLN  HB3', ' A  69  GLN  HB3', -0.646, (47.547, 17.662, -1.719)), (' A 237  TYR  O  ', ' A 238  ASN  C  ', -0.642, (36.943, -2.045, 35.555)), (' A 249  ILE  O  ', ' A 252  PRO  HD2', -0.638, (39.354, -18.753, 21.626)), (' A 191  ALA  O  ', ' A 192  GLN  CB ', -0.635, (31.65, 18.209, 22.115)), (' A  63  ASN  N  ', ' A  63  ASN HD22', -0.628, (33.024, 21.461, -6.781)), (' A  31  TRP  CE2', ' A  95  ASN  HB2', -0.625, (43.613, 7.069, -6.627)), (' A 112  PHE  HE1', ' A 114  VAL HG23', -0.624, (43.309, 3.735, 13.998)), (' A 112  PHE  CE1', ' A 114  VAL HG23', -0.619, (43.009, 2.752, 13.864)), (' A 163  HIS  CE1', ' A 172  HIS  HB3', -0.619, (41.308, 11.066, 16.859)), (' A  50  LEU  CA ', ' A  51  ASN  N  ', -0.616, (29.401, 27.47, 16.382)), (' A 280  THR  HB ', ' A 284  SER  O  ', -0.614, (54.91, -5.946, 33.644)), (' A 213  ILE  CD1', ' A 256  GLN HE22', -0.613, (48.837, -19.544, 22.885)), (' A  45  THR  C  ', ' A  47  GLU  N  ', -0.612, (35.042, 27.948, 11.435)), (' A 199  THR HG23', ' A 289  ASP  OD2', -0.609, (40.965, -1.801, 29.76)), (' A 154  TYR  C  ', ' A 155  ASP  CG ', -0.608, (45.798, -10.733, 0.207)), (' A   5  LYS  HB2', ' A   5  LYS  HZ3', -0.605, (54.026, -1.783, 21.093)), (' A 213  ILE HD13', ' A 256  GLN HE22', -0.604, (49.713, -19.369, 22.865)), (' A 130  MET  CE ', ' A 136  ILE HD11', -0.604, (37.272, 4.009, 17.477)), (' A 135  THR  C  ', ' A 136  ILE HD12', -0.603, (37.693, 6.213, 20.546)), (' A 253  LEU  N  ', ' A 253  LEU HD12', -0.602, (43.054, -19.127, 22.658)), (' A 231  ASN  O  ', ' A 235  MET  HE2', -0.6, (31.38, -7.571, 37.263)), (' A   4  ARG  HG3', ' A   4  ARG HH11', -0.596, (56.761, -4.683, 19.477)), (' A  75  LEU  N  ', ' A  75  LEU HD12', -0.589, (45.909, 15.722, -7.816)), (' A   1  SER  O  ', ' A   2  GLY  O  ', -0.586, (57.054, -12.85, 20.894)), (' A  10  SER  O  ', ' A  14  GLU  HG3', -0.583, (50.772, 1.965, 3.393)), (' A 190  THR  C  ', ' A 191  ALA  O  ', -0.578, (31.331, 20.784, 21.714)), (' A  58  LEU  O  ', ' A  60  ARG  N  ', -0.576, (27.798, 25.343, -0.761)), (' A 107  GLN  H  ', ' A 110  GLN  NE2', -0.573, (34.121, -3.825, 15.82)), (' A  30  LEU HD23', ' A 177  LEU  CD2', -0.572, (38.044, 5.318, 3.569)), (' A  40  ARG  HG2', ' A  85  CYS  O  ', -0.57, (32.309, 15.013, 7.615)), (' A 208  LEU  HG ', ' A 219  PHE  CE1', -0.569, (48.001, -13.691, 32.84)), (' A  50  LEU  HB3', ' A  51  ASN  H  ', -0.567, (28.305, 27.971, 15.416)), (' A 151  ASN  O  ', ' A 152  ILE HD13', -0.564, (43.57, -4.579, 5.941)), (' A 152  ILE  CG2', ' A 153  ASP  H  ', -0.561, (45.014, -7.772, 4.842)), (' A   5  LYS  H  ', ' A   5  LYS  NZ ', -0.561, (54.032, -2.636, 22.22)), (' A 198  THR HG22', ' A 199  THR  N  ', -0.557, (36.052, -1.342, 31.148)), (' A  50  LEU  CB ', ' A  51  ASN  H  ', -0.556, (28.662, 27.582, 15.389)), (' A  40  ARG  HA ', ' A  87  LEU  HB2', -0.552, (33.549, 16.902, 3.834)), (' A 175  THR  HB ', ' A 180  LYS  O  ', -0.552, (31.619, 7.773, 11.098)), (' A 186  VAL HG23', ' A 188  ARG  HB2', -0.551, (29.798, 18.904, 17.355)), (' A 100  LYS  CG ', ' A 155  ASP  O  ', -0.55, (41.093, -7.587, -1.501)), (' A 251  GLY  O  ', ' A 254  SER  HB3', -0.547, (40.75, -22.134, 25.04)), (' A  76  ARG  HG3', ' A  76  ARG HH11', -0.545, (40.229, 20.338, -13.701)), (' A 288  GLU  HG2', ' A 291  PHE  CD2', -0.543, (48.263, -5.316, 24.903)), (' A  88  ARG  C  ', ' A  89  LEU HD23', -0.543, (33.6, 14.792, -2.2)), (' A 274  ASN  N  ', ' A 274  ASN  ND2', -0.542, (43.661, -9.317, 45.377)), (' A 112  PHE  HE1', ' A 114  VAL  CG2', -0.538, (43.077, 3.969, 13.784)), (' A 208  LEU HD23', ' A 264  MET  SD ', -0.536, (45.522, -14.901, 33.067)), (' A  58  LEU HD11', ' A  80  HIS  HD2', -0.535, (30.09, 20.438, -1.989)), (' A  63  ASN  N  ', ' A  63  ASN  ND2', -0.534, (32.961, 21.554, -7.03)), (' A  50  LEU  HB3', ' A  51  ASN  N  ', -0.531, (28.74, 27.879, 16.4)), (' A  58  LEU  O  ', ' A  61  LYS  N  ', -0.531, (29.497, 24.992, -0.935)), (' A 213  ILE HG12', ' A 257  THR HG22', -0.528, (49.389, -20.175, 25.46)), (' A 106  ILE  CD1', ' A 130  MET  HB2', -0.527, (37.169, 0.805, 17.623)), (' A  46  ALA  HB2', ' A 654  HOH  O  ', -0.527, (38.803, 31.183, 13.134)), (' A 215  GLY  O  ', ' A 216  ASP  C  ', -0.526, (54.591, -16.254, 32.345)), (' A  83  GLN  O  ', ' A  84  ASN  HB2', -0.525, (28.052, 10.357, 6.074)), (' A 106  ILE HD11', ' A 130  MET  HB2', -0.521, (36.916, 0.946, 17.173)), (' A 188  ARG  C  ', ' A 190  THR  H  ', -0.52, (32.088, 21.537, 18.495)), (' A 207  TRP  O  ', ' A 210  ALA  HB3', -0.52, (48.81, -12.086, 27.1)), (' A  45  THR  OG1', ' A  47  GLU  HG3', -0.517, (34.577, 29.37, 9.213)), (' A  27  LEU  O  ', ' A  27  LEU HD12', -0.512, (42.321, 16.885, 3.986)), (' A 154  TYR  O  ', ' A 155  ASP  CA ', -0.507, (44.267, -9.638, 0.601)), (' A  33  ASP  H  ', ' A  98  THR HG21', -0.506, (39.784, 2.314, -5.516)), (' A 217  ARG  HB2', ' A 220  LEU HD12', -0.504, (51.528, -19.96, 35.012)), (' A 218  TRP  CE2', ' A 279  ARG  HB3', -0.499, (53.999, -10.88, 38.63)), (' A 215  GLY  HA3', ' A 640  HOH  O  ', -0.498, (58.802, -16.164, 30.552)), (' A   5  LYS  HB2', ' A   5  LYS  NZ ', -0.495, (53.921, -1.958, 21.727)), (' A 152  ILE HD12', ' A 157  VAL HG22', -0.494, (45.027, -4.174, 4.149)), (' A 115  LEU HD11', ' A 122  PRO  CB ', -0.491, (51.334, 6.789, 6.402)), (' A 236  LYS  HB3', ' A 236  LYS  NZ ', -0.49, (35.874, -3.441, 44.295)), (' A 138  GLY  HA3', ' A 140  PHE  HE1', -0.49, (44.706, 8.424, 17.928)), (' A  21  THR HG22', ' A  22  CYS  N  ', -0.487, (42.43, 24.082, 1.18)), (' A 105  ARG  C  ', ' A 106  ILE  O  ', -0.486, (32.091, -1.077, 13.737)), (' A  77  VAL  O  ', ' A  77  VAL HG13', -0.486, (37.256, 19.615, -9.078)), (' A 119  ASN  N  ', ' A 119  ASN HD22', -0.486, (49.436, 17.27, 5.973)), (' A  35  THR HG22', ' A  36  VAL  N  ', -0.485, (36.346, 10.122, -3.249)), (' A 132  PRO  C  ', ' A 134  HIS  H  ', -0.485, (33.51, 3.327, 23.955)), (' A  40  ARG  NE ', ' A  85  CYS  HA ', -0.482, (29.138, 15.574, 8.491)), (' A 127  GLN  HG3', ' A 128  CYS  N  ', -0.482, (45.648, -0.48, 17.962)), (' A 152  ILE HG22', ' A 154  TYR  N  ', -0.477, (45.575, -9.001, 4.485)), (' A 100  LYS  CB ', ' A 155  ASP  O  ', -0.476, (41.608, -7.101, -1.891)), (' A  58  LEU  C  ', ' A  60  ARG  N  ', -0.475, (27.741, 25.442, -0.036)), (' A  88  ARG  O  ', ' A  89  LEU HD23', -0.473, (33.158, 14.638, -2.377)), (' A  63  ASN  H  ', ' A  63  ASN  ND2', -0.471, (32.705, 22.148, -7.249)), (' A 111  THR HG22', ' A 129  ALA  HB2', -0.468, (42.435, -1.959, 20.645)), (' A 150  PHE  CD2', ' A 150  PHE  N  ', -0.468, (43.219, 0.968, 9.36)), (' A  81  SER  OG ', ' A  82  MET  N  ', -0.467, (28.207, 14.288, -1.017)), (' A 200  ILE HG21', ' A 203  ASN  ND2', -0.467, (39.035, -5.342, 24.452)), (' A 207  TRP  CD2', ' A 288  GLU  HB3', -0.463, (47.999, -6.643, 28.533)), (' A 107  GLN  N  ', ' A 110  GLN  NE2', -0.461, (33.596, -3.559, 16.132)), (' A 240  GLU  CD ', ' A 241  PRO  HD2', -0.458, (31.062, -4.811, 29.752)), (' A 276  MET  CE ', ' A 281  ILE HG13', -0.453, (51.629, -8.079, 36.271)), (' A 186  VAL  C  ', ' A 188  ARG  H  ', -0.453, (31.088, 17.618, 16.214)), (' A 138  GLY  HA3', ' A 140  PHE  CE1', -0.451, (44.855, 8.312, 17.752)), (' A 191  ALA  O  ', ' A 192  GLN  HB2', -0.45, (31.996, 18.513, 22.382)), (' A 107  GLN  H  ', ' A 110  GLN HE21', -0.449, (33.854, -4.184, 16.464)), (' A 225  THR HG23', ' A 226  THR  N  ', -0.448, (34.219, -17.626, 39.476)), (' A 137  LYS  CE ', ' A 171  VAL HG12', -0.448, (42.737, 9.614, 25.481)), (' A   8  PHE  CD1', ' A 152  ILE  HB ', -0.448, (46.866, -6.504, 8.18)), (' A  30  LEU  CD2', ' A 177  LEU HD21', -0.447, (39.219, 5.187, 4.154)), (' A 209  TYR  CE1', ' A 264  MET  HG2', -0.446, (43.325, -16.601, 30.151)), (' A 106  ILE HD11', ' A 130  MET  CE ', -0.446, (36.207, 2.287, 16.74)), (' A 213  ILE  CD1', ' A 256  GLN  NE2', -0.446, (49.273, -20.01, 23.337)), (' A  35  THR  HA ', ' A  89  LEU  O  ', -0.443, (36.049, 10.447, -5.155)), (' A  62  SER  HB2', ' A  64  HIS  NE2', -0.44, (33.524, 27.001, -7.262)), (' A  26  THR  O  ', ' A  26  THR HG23', -0.44, (45.899, 20.907, 5.95)), (' A 253  LEU  CD1', ' A 253  LEU  H  ', -0.438, (42.495, -18.499, 23.315)), (' A 100  LYS  HG2', ' A 155  ASP  O  ', -0.435, (41.0, -7.86, -1.272)), (' A 105  ARG  HG3', ' A 176  ASP  OD2', -0.434, (30.73, 2.777, 11.407)), (' A  76  ARG  HG3', ' A  76  ARG  NH1', -0.433, (40.681, 20.086, -13.84)), (' A 107  GLN  N  ', ' A 110  GLN HE21', -0.433, (33.488, -4.124, 16.396)), (' A  50  LEU  C  ', ' A  51  ASN HD22', -0.432, (28.711, 25.632, 17.041)), (' A  45  THR  CG2', ' A 629  HOH  O  ', -0.431, (38.037, 29.875, 6.17)), (' A 203  ASN  OD1', ' A 292  THR  HA ', -0.43, (41.007, -7.834, 22.897)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.43, (42.685, 3.796, -6.152)), (' A 185  PHE  HA ', ' A 192  GLN HE21', -0.43, (30.478, 14.779, 19.962)), (' A 213  ILE HD13', ' A 256  GLN  NE2', -0.429, (49.722, -20.147, 22.928)), (' A 193  ALA  CB ', ' A 637  HOH  O  ', -0.429, (30.654, 14.368, 29.134)), (' A 202  LEU HD21', ' A 293  PRO  HG2', -0.428, (37.999, -11.876, 22.629)), (' A 140  PHE  CD1', ' A 140  PHE  N  ', -0.425, (46.018, 11.059, 17.236)), (' A  27  LEU  HB2', ' A 145  CYS  O  ', -0.425, (43.073, 15.653, 7.875)), (' A 183  GLY  O  ', ' A 184  PRO  O  ', -0.424, (28.785, 9.76, 18.13)), (' A 154  TYR  C  ', ' A 155  ASP  OD2', -0.423, (45.732, -11.365, 0.982)), (' A 280  THR  CG2', ' A 285  THR HG22', -0.42, (56.142, -3.839, 35.374)), (' A 221  ASN  ND2', ' A 267  ALA  HA ', -0.42, (44.632, -15.873, 40.432)), (' A  54  TYR  O  ', ' A  55  GLU  C  ', -0.419, (25.86, 22.88, 4.135)), (' A 103  PHE  CE2', ' A 177  LEU HD22', -0.419, (36.924, 3.534, 3.573)), (' A 207  TRP  HZ3', ' A 287  LEU  HA ', -0.418, (47.843, -6.735, 32.685)), (' A  62  SER  HB2', ' A  64  HIS  CE1', -0.418, (33.744, 27.014, -6.779)), (' A 208  LEU  O  ', ' A 212  VAL HG23', -0.417, (49.298, -15.626, 30.702)), (' A  40  ARG  HD3', ' A  85  CYS  CA ', -0.417, (29.928, 14.5, 7.509)), (' A 225  THR  CG2', ' A 226  THR  N  ', -0.416, (34.768, -17.458, 39.51)), (' A  68  VAL HG12', ' A  75  LEU HD13', -0.416, (44.136, 14.637, -5.56)), (' A 243  THR  O  ', ' A 247  VAL HG23', -0.415, (32.113, -15.632, 29.003)), (' A 259  ILE  N  ', ' A 259  ILE HD12', -0.413, (46.196, -23.331, 30.289)), (' A 141  LEU  H  ', ' A 144  SER  HB3', -0.413, (47.702, 14.564, 14.216)), (' A 167  LEU  C  ', ' A 169  THR  N  ', -0.412, (39.09, 17.014, 25.01)), (' A  19  GLN  HG2', ' A  20  VAL  N  ', -0.412, (45.538, 18.083, 1.147)), (' A  95  ASN  HA ', ' A  96  PRO  HD2', -0.412, (45.222, 6.355, -8.513)), (' A 227  LEU  O  ', ' A 231  ASN  ND2', -0.409, (30.24, -13.365, 35.562)), (' A 186  VAL  O  ', ' A 188  ARG  N  ', -0.409, (31.698, 18.04, 16.282)), (' A  31  TRP  CD2', ' A  95  ASN  HB2', -0.409, (43.471, 7.591, -5.848)), (' A 211  ALA  HA ', ' A 282  LEU  HG ', -0.407, (53.019, -12.342, 28.847)), (' A  21  THR  CG2', ' A  22  CYS  N  ', -0.406, (42.231, 23.685, 1.614)), (' A 195  GLY  HA2', ' A 631  HOH  O  ', -0.404, (30.237, 10.79, 30.193)), (' A   3  PHE  HE1', ' A 299  GLN  HB2', -0.404, (50.899, -11.846, 20.271)), (' A  58  LEU  C  ', ' A  60  ARG  H  ', -0.404, (27.843, 25.111, 0.439)), (' A  50  LEU  O  ', ' A 190  THR  CG2', -0.403, (30.076, 24.594, 17.885)), (' A  45  THR HG21', ' A 629  HOH  O  ', -0.401, (37.998, 30.019, 6.182)), (' A  97  LYS  O  ', ' A  98  THR  C  ', -0.4, (44.708, -0.343, -4.627))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
