"""
The base python sgems plugin.
"""
import os
import sgems


class ExportPropertyToEclipse:
    def __init__(self):
        pass

    def initialize(self, params):
        print params
        self.grid_name = params['GridName']['grid']
        self.prop_name = params['GridName']['property']
        self.header = params['header']['value']
        self.filename = params['filename']['value']
        self.location = params['location']['value']
        return True

    def execute(self):
        # d = np.array(sgems.get_property(self.grid_name,self.prop_name))
        # np.clip(d, -12, self.cap_value, out=d)
        # sgems.set_property(self.grid_name, self.out_name, d.tolist())
        print "executing..."

        inactive_flag = 0.0

        # Get grid dimensions
        ni, nj, nk = sgems.get_dims(self.grid_name)
        # Get user specified property:
        prop = sgems.get_property(self.grid_name, self.prop_name)

        property_values = []
        for k in range(nk - 1, -1, -1):
            for j in range(0, nj):
                for i in range(0, ni):
                    # node_id = sgems.get_nodeid(self.grid_name, i, j, k)
                    node_id = sgems.get_nodeid_from_ijk(self.grid_name, i, j, k)
                    if node_id != -1:
                        # grid block is active get property
                        property_values.append(prop[node_id])
                    else:
                        # grid block is inactive set inactive flag:
                        property_values.append(inactive_flag)


        full_file_name = os.path.join(self.location, self.filename)
        per_line = 10
        with open(full_file_name, 'w') as f:
            f.write("{}\n".format(self.header))
            cnt = 0
            for v in property_values:
                f.write("{}".format(v))
                cnt += 1
                if cnt % per_line == 0:
                    f.write("\n")
                else:
                    f.write(" ")
            f.write("/")
        print "{} values saved to file: {}".format(cnt, full_file_name)
        print "{} ...".format(property_values[0:min(10,len(property_values))])
        return True

    def finalize(self):
        return True

    def name(self):
        return "export_property_to_eclipse"


###############################################################
def get_plugins():
    return ["ExportPropertyToEclipse"]
