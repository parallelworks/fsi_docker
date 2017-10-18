# FSI parameter sweep

type file;
############################################
# ------ INPUT / OUTPUT DEFINITIONS -------#
############################################

# workflow inputs
# comment this line out when running under dakota
file params         <arg("paramFile","params.run")>; 

# other inputs
string outdir      = "results/"; # Directory where the outputs are saved
string casedir     = strcat(outdir,"case"); # Directory where the outputs for each case are saved

# add models
file[] mesh         <Ext;exec="utils/mapper.sh",root="models/mesh">;
file[] openfoam     <Ext;exec="utils/mapper.sh",root="models/openfoam">;
file[] calculix     <Ext;exec="utils/mapper.sh",root="models/calculix">;
file[] mapper       <Ext;exec="utils/mapper.sh",root="models/mapper">;
file[] mexdex       <Ext;exec="utils/mapper.sh",root="models/mexdex">;

# workflow outputs
file outhtml        <arg("html","results/output.html")>;
file outcsv         <arg("csv","results/output.csv")>; 
string path        = toString(@java("java.lang.System","getProperty","user.dir"));

##############################
# ---- APP DEFINITIONS ----- #
##############################
# Combines the parameters in params.run to produce all the cases
app (file out) prepInputs (file params, file s[])
{
  python "models/mexdex/prepinputs.py" @params @out; 
}

# generate parametric mesh
app (file[] meshOut, file o, file e) genMesh (string caseParams, string meshLocation, file[] mesh) {
  bash "models/mesh/genMesh.sh" caseParams meshLocation stdout=@o stderr=@e;
}

# run openfoam
app (file bodyFiles, file metricFile, file[] metricImages, file o, file e) runOpenFOAM (string caseParams, string meshLocation, file[] meshOut, string metricImagesLocation, file[] openfoam, file[] mexdex) {
  bash "models/openfoam/runOF.sh" caseParams meshLocation @bodyFiles @metricFile metricImagesLocation stdout=@o stderr=@e;
}

# map openfoam results to calculix mesh
app (file mapResults, file o, file e) mapMeshes (file bodyFiles, string meshLocation, file[] meshOut, file[] mapper) {
  bash "models/mapper/map.sh" @bodyFiles meshLocation @mapResults stdout=@o stderr=@e;
}

# run calculix
app (file metricFile, file[] metricImages, file o, file e) runCalculix (string caseParams, file mapResults, string meshLocation, file[] meshOut, string metricImagesLocation, file[] calculix, file[] mexdex) {
  bash "models/calculix/runCCX.sh" caseParams meshLocation @mapResults @metricFile metricImagesLocation stdout=@o stderr=@e;
}

# Produces the html file for visualization and organization of results
app (file outcsv, file outhtml, file so, file se) postProcess (file[] t, string rpath, file caselist, file[] mexdex) {
  bash "models/mexdex/postprocess.sh" filename(outcsv) filename(outhtml) rpath stdout=filename(so) stderr=filename(se);
}

######################
# ---- WORKFLOW ---- #
######################

file caselist <"cases.list">;

# comment this line out when running under dakota
caselist = prepInputs(params, mexdex);

# In built function to read each line in caselist into an array of strings
string[] cases = readData(caselist);

tracef("\n%i Cases in Simulation\n\n",length(cases));

# For each case run through the models
file[] metrics;
foreach c,caseIndex in cases{

  trace(caseIndex,c);
  
  # GENERATE MESH
  string meshLocation = strcat("results/case_",caseIndex,"/mesh");
  file[] meshOut      <FilesysMapper;location=meshLocation>;
  file mo 	          <strcat("results/logs/case_",caseIndex,"/mesh.out")>;
  file me 	          <strcat("results/logs/case_",caseIndex,"/mesh.err")>;
  (meshOut, mo, me) = genMesh(c, meshLocation, mesh);

  # RUN OPENFOAM
  file bodyFiles      <strcat("results/case_",caseIndex,"/openfoam/results.tgz")>;
  file metricFile     <strcat("results/case_",caseIndex,"/openfoam/metrics.csv")>;
  string metricImagesLocation = strcat("results/case_",caseIndex,"/openfoam/png");
  file[] metricImages <FilesysMapper;location=metricImagesLocation>;
  file oo 	          <strcat("results/logs/case_",caseIndex,"/openfoam.out")>;
  file oe 	          <strcat("results/logs/case_",caseIndex,"/openfoam.err")>;
  (bodyFiles, metricFile, metricImages, oo, oe) = runOpenFOAM(c, meshLocation, meshOut, metricImagesLocation, openfoam, mexdex);
  metrics[2*caseIndex-1]=metricFile; # Odd indices for openfoam

  # MAP THE MESHES
  file mapResults       <strcat("results/case_",caseIndex,"/mapper/results.tgz")>;
  file mapo 	          <strcat("results/logs/case_",caseIndex,"/mapper.out")>;
  file mape 	          <strcat("results/logs/case_",caseIndex,"/mapper.err")>;
  (mapResults, mapo, mape) = mapMeshes(bodyFiles, strcat(meshLocation,"/mesh.exo"), meshOut, mapper);

  # RUN CALCULIX
  file CCXmetricFile    <strcat("results/case_",caseIndex,"/calculix/metrics.csv")>;
  string CCXmetricImagesLocation = strcat("results/case_",caseIndex,"/calculix/png");
  file[] CCXmetricImages <FilesysMapper;location=CCXmetricImagesLocation>;
  file calo 	          <strcat("results/logs/case_",caseIndex,"/calculix.out")>;
  file cale 	          <strcat("results/logs/case_",caseIndex,"/calculix.err")>;
  (CCXmetricFile,CCXmetricImages,calo,cale) = runCalculix(c, mapResults, meshLocation, meshOut, CCXmetricImagesLocation, calculix, mexdex);
  metrics[2*caseIndex]=CCXmetricFile; # Even indices for calculix
}

# For all cases creates a csv list and html file for visualization and organization of results
file spout <"logs/post.out">;
file sperr <"logs/post.err">;
(outcsv,outhtml,spout,sperr) = postProcess(metrics,path,caselist,mexdex);