import h_transport_materials as htm
from h_transport_materials.property import Diffusivity, Solubility, Permeability
from h_transport_materials import k_B, Rg, avogadro_nb
from pathlib import Path

import numpy as np

u = htm.ureg

molar_mass_li = 0.06941  # kg/mol
molar_mass_Pb = 0.2072  # kg/mol
rho_lipb = 10163.197  # kg/m3  at 300K


def molar_mass_lipb(nb_li: int, nb_pb: int):
    """Returns the molar mass (kg/mol) of a LiPb compound

    Args:
        nb_li (int): the number of Li atoms
        nb_pb (int): the number of Pb atoms

    Returns:
        float: the molar mass in kg/mol
    """

    return nb_pb * molar_mass_Pb + nb_li * molar_mass_li


def atom_density_lipb(nb_li: int, nb_pb: int):
    """Returns the atomic density (in m-3) of a LiPb compound

    Args:
        nb_li (int): the number of Li atoms
        nb_pb (int): the number of Pb atoms

    Returns:
        float: the atomic density in m-3
    """
    return (rho_lipb * avogadro_nb) / molar_mass_lipb(nb_li, nb_pb)


wu_solubility = Solubility(
    S_0=6.33e-07
    * atom_density_lipb(nb_li=17, nb_pb=83)
    * u.particle
    * u.m**-3
    * u.Pa**-0.5,
    E_S=0 * u.eV * u.particle**-1,
    range=(850 * u.K, 1040 * u.K),
    source="wu_solubility_1983",
    name="D Wu (1983)",
    isotope="D",
    units="m-3 Pa-1/2",
)


chan_solubility = Solubility(
    S_0=4.7e-07
    * atom_density_lipb(nb_li=17, nb_pb=1)
    * u.particle
    * u.m**-3
    * u.Pa**-0.5,
    E_S=9000 * u.J * u.mol**-1,
    range=(573 * u.K, 773 * u.K),
    source="chan_thermodynamic_1984",
    name="H Chan (1984)",
    isotope="H",
    units="m-3 Pa-1/2",
    note="extrapolated to Pb-17Li",
)


katsuta_solubility = Solubility(
    S_0=(1 / 2.9e3)
    * atom_density_lipb(nb_li=17, nb_pb=83)
    * u.particle
    * u.m**-3
    * u.atm**-0.5,
    E_S=0 * u.eV * u.particle**-1,
    range=(573 * u.K, 723 * u.K),
    source="katsuta_hydrogen_1985",
    name="H Katsuta (1985)",
    isotope="H",
    units="m-3 Pa-1/2",
)


fauvet_diffusivity = Diffusivity(
    D_0=1.5e-09 * u.m**2 * u.s**-1,
    E_D=0 * u.eV * u.particle**-1,
    range=(722 * u.K, 724 * u.K),  # TODO should be 723 link to issue #37
    source="fauvet_hydrogen_1988",
    name="H Fauvet (1988)",
    isotope="H",
    note="Fauvet gives the value for 723 K only",
)
fauvet_solubility = Solubility(
    S_0=2.7e-08
    * atom_density_lipb(nb_li=17, nb_pb=83)
    * u.particle
    * u.m**-3
    * u.Pa**-0.5,
    E_S=0 * u.eV * u.particle**-1,
    range=(722 * u.K, 724 * u.K),  # TODO should be 723 link to issue #37
    source="fauvet_hydrogen_1988",
    name="H Fauvet (1988)",
    isotope="H",
    units="m-3 Pa-1/2",
    note="Fauvet gives the value for 723 K only",
)


schumacher_solubility_data = np.genfromtxt(
    str(Path(__file__).parent) + "/schumacher_1990/solubility.csv",
    delimiter=",",
)

schumacher_solubility_data_y = schumacher_solubility_data[:, 1]  # ln(Ks/sqrt(bar))
schumacher_solubility_data_y *= (
    -1
)  # -ln(Ks/sqrt(bar)) = ln(sqrt(bar)/Ks) = ln(solubility * sqrt(bar))
schumacher_solubility_data_y = np.exp(
    schumacher_solubility_data_y
)  # solubility * sqrt(bar)

schumacher_solubility_data_y *= atom_density_lipb(nb_li=1, nb_pb=1)

schumacher_solubility = Solubility(
    data_T=1000 / schumacher_solubility_data[:, 0] * u.K,
    data_y=schumacher_solubility_data_y * u.particle * u.m**-3 * u.bar**-0.5,
    source="schumacher_hydrogen_1990",
    name="H Schumacher (1990)",
    isotope="H",
    units="m-3 Pa-1/2",
    note="in the review of E.Mas de les Valls there's a mistake in the conversion and"
    + "the activation energy of solubility should be positive"
    + "We decided to refit Schumacher's data",
)


reiter_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/reiter_1991/diffusivity.csv",
    delimiter=",",
)

reiter_difusivity_data_H = reiter_diffusivity_data[2:, 2:]

reiter_diffusivity_h = Diffusivity(
    data_T=1000 / reiter_difusivity_data_H[:, 0] * u.K,
    data_y=reiter_difusivity_data_H[:, 1] * u.m**2 * u.s**-1,
    range=(508 * u.K, 700 * u.K),
    source="reiter_solubility_1991",
    name="H Reiter (1991)",
    isotope="H",
)

reiter_difusivity_data_D = reiter_diffusivity_data[2:, :2]


reiter_diffusivity_d = Diffusivity(
    data_T=1000 / reiter_difusivity_data_D[:, 0] * u.K,
    data_y=reiter_difusivity_data_D[:, 1] * u.m**2 * u.s**-1,
    range=(508 * u.K, 700 * u.K),
    source="reiter_solubility_1991",
    name="D Reiter (1991)",
    isotope="D",
)


reiter_solubility_data = np.genfromtxt(
    str(Path(__file__).parent) + "/reiter_1991/solubility.csv",
    delimiter=",",
)

reiter_solubility_data_H = reiter_solubility_data[2:, :2]

reiter_solubility_data_H_y = reiter_solubility_data_H[:, 1]  # at.fr. Pa-1/2
reiter_solubility_data_H_y *= atom_density_lipb(nb_li=17, nb_pb=1)  # m-3 Pa-1/2

reiter_solubility_h = Solubility(
    data_T=1000 / reiter_solubility_data_H[:, 0] * u.K,
    data_y=reiter_solubility_data_H_y * u.particle * u.m**-3 * u.Pa**-0.5,
    range=(508 * u.K, 700 * u.K),
    source="reiter_solubility_1991",
    name="H Reiter (1991)",
    isotope="H",
    units="m-3 Pa-1/2",
)

reiter_solubility_data_D = reiter_solubility_data[2:, 2:]
reiter_solubility_data_D_T = reiter_solubility_data_D[:, 0]  # 1000/K
reiter_solubility_data_D_T = 1000 / reiter_solubility_data_D_T  # K

reiter_solubility_data_D_y = reiter_solubility_data_D[:, 1]  # at.fr. Pa-1/2
reiter_solubility_data_D_y *= atom_density_lipb(nb_li=17, nb_pb=1)  # m-3 Pa-1/2

reiter_solubility_d = Solubility(
    data_T=reiter_solubility_data_D_T[np.isfinite(reiter_solubility_data_D_T)] * u.K,
    data_y=reiter_solubility_data_D_y[np.isfinite(reiter_solubility_data_D_y)]
    * u.particle
    * u.m**-3
    * u.Pa**-0.5,
    range=(508 * u.K, 700 * u.K),
    source="reiter_solubility_1991",
    name="D Reiter (1991)",
    isotope="D",
    units="m-3 Pa-1/2",
)

reiter_solubility_t = Solubility(
    S_0=2.32e-08
    * atom_density_lipb(nb_li=17, nb_pb=1)
    * u.particle
    * u.m**-3
    * u.Pa**-0.5,
    E_S=1350 * u.J * u.mol**-1,
    range=(508 * u.K, 700 * u.K),
    source="reiter_solubility_1991",
    name="T Reiter (1991)",
    isotope="T",
    units="m-3 Pa-1/2",
)


data_aiello = np.genfromtxt(
    str(Path(__file__).parent) + "/aiello_2006/solubility_data.csv",
    delimiter=",",
)

aiello_solubility = Solubility(
    data_T=1000 / data_aiello[:, 0] * u.K,
    data_y=data_aiello[:, 1] * u.mol * u.m**-3 * u.Pa**-0.5,
    range=(600 * u.K, 900 * u.K),
    source="aiello_determination_2006",
    name="H Aiello (2006)",
    isotope="H",
    units="m-3 Pa-1/2",
)


shibuya_diffusivity = Diffusivity(
    data_T=np.array([300, 400, 500]) * u.degC,
    data_y=np.array([6.6e-6, 7.8e-6, 9.5e-6]) * u.cm**2 * u.s**-1,
    source="shibuya_isothermal_1987",
    name="T Shibuya (1987)",
    isotope="T",
)

terai_diffusivity = Diffusivity(
    D_0=2.50e-07 * u.m**2 * u.s**-1,
    E_D=27000 * u.J * u.mol**-1,
    range=(573 * u.K, 973 * u.K),
    source="terai_diffusion_1992",
    name="T Terai (1987)",
    isotope="T",
)

alberro_solubility = Solubility(
    S_0=8.64e-3 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=9000 * u.J * u.mol**-1,
    range=(523 * u.K, 922 * u.K),
    source="alberro_experimental_2015",
    name="H Alberro (2015)",
    isotope="H",
    units="m-3 Pa-1/2",
)


# TODO fit Edao data ourselves
edao_permeability_h = Permeability(
    pre_exp=1.20e-9 * u.mol * u.s**-1 * u.m**-1 * u.Pa**-0.5,
    act_energy=20.0 * u.kJ * u.mol**-1,
    isotope="H",
    range=(573 * u.K, 873 * u.K),
    source="edao_experiments_2011",
    note="Li17Pb83",
)

edao_permeability_d = Permeability(
    pre_exp=1.30e-9 * u.mol * u.s**-1 * u.m**-1 * u.Pa**-0.5,
    act_energy=16.7 * u.kJ * u.mol**-1,
    isotope="D",
    range=(573 * u.K, 873 * u.K),
    source="edao_experiments_2011",
    note="Li17Pb83",
)


edao_diffusivity_h = Diffusivity(
    D_0=8.18e-8 * u.m**2 * u.s**-1,
    E_D=15.8 * u.kJ * u.mol**-1,
    isotope="H",
    range=(573 * u.K, 873 * u.K),
    source="edao_experiments_2011",
    note="Li17Pb83",
)

edao_diffusivity_d = Diffusivity(
    D_0=5.73e-8 * u.m**2 * u.s**-1,
    E_D=13.6 * u.kJ * u.mol**-1,
    isotope="D",
    range=(573 * u.K, 873 * u.K),
    source="edao_experiments_2011",
    note="Li17Pb83",
)


edao_solubility_h = Solubility(
    units="m-3 Pa-1/2",
    S_0=2.73e-7
    * atom_density_lipb(nb_li=17, nb_pb=83)
    * u.particle
    * u.m**-3
    * u.Pa**-0.5,
    E_S=4.18 * u.kJ * u.mol**-1,
    isotope="H",
    range=(573 * u.K, 873 * u.K),
    source="edao_experiments_2011",
    note="Li17Pb83",
)

edao_solubility_d = Solubility(
    units="m-3 Pa-1/2",
    S_0=4.21e-7
    * atom_density_lipb(nb_li=17, nb_pb=83)
    * u.particle
    * u.m**-3
    * u.Pa**-0.5,
    E_S=3.10 * u.kJ * u.mol**-1,
    isotope="D",
    range=(573 * u.K, 873 * u.K),
    source="edao_experiments_2011",
    note="Li17Pb83",
)

properties = [
    fauvet_diffusivity,
    reiter_diffusivity_h,
    reiter_diffusivity_d,
    shibuya_diffusivity,
    terai_diffusivity,
    wu_solubility,
    chan_solubility,
    katsuta_solubility,
    fauvet_solubility,
    schumacher_solubility,
    reiter_solubility_h,
    reiter_solubility_d,
    reiter_solubility_t,
    aiello_solubility,
    alberro_solubility,
    edao_permeability_h,
    edao_permeability_d,
    edao_diffusivity_h,
    edao_diffusivity_d,
    edao_solubility_h,
    edao_solubility_d,
]

for prop in properties:
    prop.material = "lipb"

htm.database += properties
