import sys, pyrosetta, pyrosetta.rosetta as r
PH = float(sys.argv[1]); PDB = sys.argv[2]
pyrosetta.init(f"-mute all -pH_mode -value_pH {PH} -ex1 -ex2 -use_input_sc")
sf = r.core.scoring.ScoreFunctionFactory.create_score_function("ref2015")
ST = r.core.scoring.ScoreType
print(f"pH_energy weight = {sf.get_weight(ST.e_pH)}")
pose = pyrosetta.pose_from_pdb(PDB)
task = r.core.pack.task.TaskFactory.create_packer_task(pose)
task.restrict_to_repacking(); task.or_include_current(True)
r.protocols.minimization_packing.PackRotamersMover(sf, task).apply(pose)
tot = sf(pose)
his = {i: pose.residue(i).name() for i in range(1, pose.total_residue()+1)
       if pose.residue(i).name3() == "HIS"}
e = pose.energies().total_energies()
print(f"pH={PH} pdb={PDB.split('/')[-1]} total={tot:.3f} "
      f"pH_energy={e[ST.e_pH]:.3f} fa_elec={e[ST.fa_elec]:.3f} "
      f"fa_sol={e[ST.fa_sol]:.3f} nprot={sum(1 for v in his.values() if v=='HIS_P')}")
print("  his states:", his)
