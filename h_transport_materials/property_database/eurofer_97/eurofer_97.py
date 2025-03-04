import h_transport_materials as htm
from h_transport_materials.property import Diffusivity, Solubility, Permeability
from pathlib import Path

import numpy as np

u = htm.ureg

aiello_permeability_data = np.genfromtxt(
    str(Path(__file__).parent) + "/aiello_2002/permeability.csv",
    delimiter=",",
)

aiello_permeability_data_H = aiello_permeability_data[2:, :2]

aiello_permeability_H = Permeability(
    data_T=1000 / aiello_permeability_data_H[:, 0] * u.K,
    data_y=aiello_permeability_data_H[:, 1]
    * u.mol
    * u.m**-1
    * u.Pa**-0.5
    * u.s**-1,
    source="aiello_hydrogen_2002",
    isotope="H",
    note="in the paper, only the 3 hottest points are fitted to measure lattice diffusion only",
)

aiello_permeability_data_D = aiello_permeability_data[2:, 2:]

aiello_permeability_D = Permeability(
    data_T=1000 / aiello_permeability_data_D[:, 0] * u.K,
    data_y=aiello_permeability_data_D[:, 1]
    * u.mol
    * u.m**-1
    * u.Pa**-0.5
    * u.s**-1,
    source="aiello_hydrogen_2002",
    isotope="D",
    note="in the paper, only the 3 hottest points are fitted to measure lattice diffusion only",
)

aiello_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/aiello_2002/diffusivity.csv",
    delimiter=",",
)

aiello_diffusivity_data_H = aiello_diffusivity_data[2:5, :2]

aiello_diffusivity_H = Diffusivity(
    data_T=1000 / aiello_diffusivity_data_H[:, 0] * u.K,
    data_y=aiello_diffusivity_data_H[:, 1] * u.m**2 * u.s**-1,
    source="aiello_hydrogen_2002",
    isotope="H",
    note="in the paper, only the 3 hottest points are fitted to measure lattice diffusion only",
)

aiello_diffusivity_data_D = aiello_diffusivity_data[2:5, 2:]

aiello_diffusivity_D = Diffusivity(
    data_T=1000 / aiello_diffusivity_data_D[:, 0] * u.K,
    data_y=aiello_diffusivity_data_D[:, 1] * u.m**2 * u.s**-1,
    source="aiello_hydrogen_2002",
    isotope="D",
    note="in the paper, only the 3 hottest points are fitted to measure lattice diffusion only",
)

chen_permeability_data = np.genfromtxt(
    str(Path(__file__).parent) + "/chen_2021/permeability.csv",
    delimiter=",",
)

chen_permeability = Permeability(
    data_T=1000 / chen_permeability_data[:, 0] * u.K,
    data_y=chen_permeability_data[:, 1] * u.mol * u.m**-1 * u.MPa**-0.5 * u.s**-1,
    source="chen_deuterium_2021",
    isotope="D",
    note="in the paper, only the 3 hottest points are fitted to measure lattice diffusion only",
)

chen_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/chen_2021/diffusivity.csv",
    delimiter=",",
)

chen_diffusivity = Diffusivity(
    data_T=1000 / chen_diffusivity_data[:, 0] * u.K,
    data_y=chen_diffusivity_data[:, 1] * u.m**2 * u.s**-1,
    source="chen_deuterium_2021",
    isotope="D",
    note="in the paper, only the 3 hottest points are fitted to measure lattice diffusion only",
)

chen_solubility = Solubility(
    S_0=4.0e2 * u.mol * u.m**-3 * u.MPa**-0.5,
    E_S=29.2 * u.kJ * u.mol**-1,
    range=(623 * u.K, 823 * u.K),
    source="chen_deuterium_2021",
    isotope="D",
    note="in the paper, only the 3 hottest points are fitted to measure lattice diffusion only",
)

esteban_permeability_data = np.genfromtxt(
    str(Path(__file__).parent) + "/esteban_2007/permeability.csv",
    delimiter=",",
)

esteban_permeability = Permeability(
    data_T=1000 / esteban_permeability_data[:, 0] * u.K,
    data_y=esteban_permeability_data[:, 1]
    * u.mol
    * u.m**-1
    * u.Pa**-0.5
    * u.s**-1,
    source="esteban_hydrogen_2007",
    isotope="H",
)

esteban_diffusivity = Diffusivity(
    D_0=4.57e-07 * u.m**2 * u.s**-1,
    E_D=22.3 * u.kJ * u.mol**-1,
    range=(376 * u.K, 724 * u.K),
    note="The authors also give an effective diffusivity, this is the lattice diffusivity measured at high temperature",
    source="esteban_hydrogen_2007",
    isotope="H",
)

esteban_solubility = Solubility(
    S_0=2.25e-02 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=15.1 * u.kJ * u.mol**-1,
    range=(376 * u.K, 724 * u.K),
    note="The authors also give an effective solubility, this is the lattice solubility measured at high temperature",
    source="esteban_hydrogen_2007",
    isotope="H",
)

montupet_leblond_permeability_data = np.genfromtxt(
    str(Path(__file__).parent) + "/montupet_leblond_2021/permeability.csv",
    delimiter=",",
)

montupet_leblond_permeability = Permeability(
    data_T=1000 / montupet_leblond_permeability_data[:, 0] * u.K,
    data_y=montupet_leblond_permeability_data[:, 1]
    * u.mol
    * u.m**-1
    * u.Pa**-0.5
    * u.s**-1,
    source="montupet_leblond_permeation_2021",
    isotope="H",
)

montupet_leblond_diffusivity = Diffusivity(
    D_0=2.52e-07 * u.m**2 * u.s**-1,
    E_D=0.16 * u.eV * u.particle**-1,
    range=(473 * u.K, 673 * u.K),
    note="The authors also give an effective diffusivity, this is the lattice diffusivity measured at high temperature",
    source="montupet_leblond_permeation_2021",
    isotope="H",
)

montupet_leblond_solubility = Solubility(
    S_0=1.76e-01 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=0.27 * u.eV * u.particle**-1,
    range=(473 * u.K, 673 * u.K),
    note="The authors also give an effective solubilty, this is the lattice solubility measured at high temperature",
    source="montupet_leblond_permeation_2021",
    isotope="H",
)

properties = [
    aiello_permeability_H,
    aiello_permeability_D,
    aiello_diffusivity_H,
    aiello_diffusivity_D,
    chen_permeability,
    chen_diffusivity,
    chen_solubility,
    esteban_permeability,
    esteban_diffusivity,
    esteban_solubility,
    montupet_leblond_permeability,
    montupet_leblond_diffusivity,
    montupet_leblond_solubility,
]

for prop in properties:
    prop.material = htm.EUROFER

htm.database += properties
