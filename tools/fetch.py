from mp_api.client import MPRester
from pymatgen.io.vasp.outputs import Chgcar
import os

API_KEY = "<YOUR_API_KEY>"
criteria = "Si-O"

with MPRester(API_KEY) as mpr:
	#api call to get all materials containing the criteria
	docs = mpr.materials.summary.search(chemsys=criteria, fields=["material_id"])
	#make a data directory
	os.makedirs("data", exist_ok=True)

	count = 0
	for material in docs:
		count += 1
		try:
			#get the charge density info for each material
			chg_density = mpr.get_charge_density_from_material_id(material.material_id)
			#if the data is available, save the CHGCAR and POSCAR files into a directory
			if chg_density:
				try:
					directory = f"data/{material.material_id}"
					os.makedirs(directory, exist_ok=True)
					chg_density.write_file(f"{directory}/{material.material_id}_CHGCAR.txt")
					chg_density.structure.to(fmt="poscar", filename= f"{directory}/{material.material_id}_POSCAR.txt")
					print(f"Saved Charge Density files for {material.material_id}")
				except Exception as e:
					print(f"An error occurred while writing the files for {directory}: {e}")
		#if not, move along
		except Exception as e:
			print(f"Charge density data is NOT available for {material.material_id}")
		print(f"{count}/{len(docs)} materials have been handled")
