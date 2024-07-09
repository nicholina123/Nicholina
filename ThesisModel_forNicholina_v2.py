# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import os 
import math 
import matplotlib.pyplot as plt

# Change work directory
os.chdir(r"C:\Users\nicho\Documents\Thesis\V2 Final")
# os.chdir(r"C:\Users\pinhosl3\Downloads") 

# Very Important! 
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)


BaseDir = os.getcwd()
Foldername = 1

while os.path.exists(BaseDir+"/"+str(Foldername))==True:
    Foldername = Foldername + 1
    
os.mkdir(BaseDir+"/"+str(Foldername))
os.chdir(BaseDir+"/"+str(Foldername))

import math

def CreateHexModel(variables):
     #hexagon dimentions 
     
    width = variables[0] #mm 
    length = variables[1] #mm
    height = variables[2] #mm
    theta = variables[3] #degrees
    ribs_t = variables[4] #mm
    plate_t = variables[5] #mm 
    n_x = variables[6] #hexagons 
    n_z = variables[7] #hexagons
    mesh_size = variables[8] #mm
       
    dist_1 = length * math.cos(theta*math.pi/180.0) * 2.0 + 2.0 * width 
    dist_2 = length * math.sin(theta*math.pi/180.0) 
    dist_3 = length * math.cos(theta*math.pi/180.0)

        # plate dimentions
    if theta <= 90.0:
        width_p = dist_1 * n_x - width #mm
        length_p = dist_2 * 2.0 * n_z #mm
    elif theta > 90.0:
        width_p = dist_1 * n_x - width - 2.0 * dist_3 #mm
        length_p = dist_2 * 2.0 * n_z #mm
    plate_t = 4.0 #mm 
    Area_p = width_p * length_p

        # Model_height = web_height + top_flange_thickness/2.0 + bot_flange_thickness/2.0 
    Mdb()

          # This code creates a section through a sketch
          
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(width, height))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Part-1'].BaseShell(sketch=
         mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']

    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(length, height))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-2', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Part-2'].BaseShell(sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__'] 
         
         # This creates the plate part 
         
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(width_p, length_p))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-3', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Part-3'].BaseShell(sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']

            # This creates the material
            
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Elastic(table=((210000.0, 0.3), ))
    mdb.models['Model-1'].materials['Material-1'].Plastic(table=((355.0, 0.0), ))

          # this creates the sections 
          
          # the thickness for the ribs 
          
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='Material-1', name='Section-1', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=ribs_t, thicknessField='', 
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
            
            # the thickness for the plate 
            
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material='Material-1', name='Section-2', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=plate_t, thicknessField='', 
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
            
            # this assign the sections for the ribs of the hexagon 
            
    mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        faces=mdb.models['Model-1'].parts['Part-1'].faces), sectionName='Section-1', 
        thicknessAssignment=FROM_SECTION)
            
    mdb.models['Model-1'].parts['Part-2'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        faces=mdb.models['Model-1'].parts['Part-2'].faces), sectionName='Section-1', 
        thicknessAssignment=FROM_SECTION)

            # this assign te section for the plate 

    mdb.models['Model-1'].parts['Part-3'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        faces=mdb.models['Model-1'].parts['Part-3'].faces), sectionName='Section-1', 
        thicknessAssignment=FROM_SECTION)
            
            
           # This starts the Assembly 
            
            # This creates the hexagons  
            
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-1', 
        part=mdb.models['Model-1'].parts['Part-1'])
            
    mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-2-1', 
        part=mdb.models['Model-1'].parts['Part-2'])
         
          # this rotate the 5th rib of the hexagon 
          
    mdb.models['Model-1'].rootAssembly.rotate(angle= 180.0 + theta, axisDirection=(0.0, 1.0, 
        0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Part-2-1', ))
            
    mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-2-2', 
        part=mdb.models['Model-1'].parts['Part-2'])
            
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-2-2', ), 
        vector=(-dist_3, 0.0, dist_2))
            
            # this rotate the 3rd rib of the hexagon 
            
    mdb.models['Model-1'].rootAssembly.rotate(angle=-theta, axisDirection=(0.0, 
        1.0, 0.0), axisPoint=(-dist_3, 0.0, dist_2), instanceList=('Part-2-2', 
        ))
         
    mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-2-3', 
        part=mdb.models['Model-1'].parts['Part-2'])
         
            # this starts the translations 
            
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-2-3', ), 
        vector=(width, 0.0, 0.0))
            
    mdb.models['Model-1'].rootAssembly.rotate(angle=-theta, axisDirection=(0.0, 
        1.0, 0.0), axisPoint=(width, 0.0, 0.0), instanceList=('Part-2-3', ))
            
    mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-2-4', 
        part=mdb.models['Model-1'].parts['Part-2'])
            
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-2-4', ), 
        vector=(dist_3 + width - length, 0.0, dist_2))
            
    mdb.models['Model-1'].rootAssembly.rotate(angle=theta, axisDirection=(0.0, 
        1.0, 0.0), axisPoint=(dist_3 + width, 0.0, dist_2), instanceList=('Part-2-4',))
            
            # this connect the hexagons in between 
            
    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(0.0, 0.0, 
        1.0), direction2=(1.0, 0.0, 0.0), instanceList=('Part-1-1', ), number1=n_z + 1, 
        number2=n_x, spacing1=dist_2 * 2.0, spacing2=dist_1)
            
            # this creates the hexagons on the X and z axis 
            
    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(0.0, 0.0, 
        1.0), direction2=(1.0, 0.0, 0.0), instanceList=('Part-2-4', 'Part-2-3', 
        'Part-2-2', 'Part-2-1'), number1=n_z, number2=n_x, spacing1=dist_2 * 2.0, spacing2=
        dist_1)
            
    mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-2', 
        part=mdb.models['Model-1'].parts['Part-1'])
            
          # this connect the hexagons in between       
            
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-1-2', ), 
        vector=(width + dist_3, 0.0, dist_2))
            
    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(0.0, 0.0, 
        1.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-1-2', ), number1=n_z, 
        number2=1, spacing1=dist_2 * 2.0, spacing2=height)    

          # this connect the hexagons in between 
          
    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0, 
        0.0), direction2=(0.0, 0.0, 1.0), instanceList=('Part-1-2', ), number1=n_x-1, 
        number2=n_z, spacing1=dist_1, spacing2=dist_2*2.0)

          # This create the plates 
          
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-3-1', 
        part=mdb.models['Model-1'].parts['Part-3'])
               

           # This moves the plate from the origine to the left
    
    
    if theta <= 90.0:
        mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-3-1-lin-1-2', 
            ), vector=(-dist_3, 0.0, 0.0))
        mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-3-1', ), 
            vector=(-dist_3, 0.0, 0.0))
     
            
         # this rotate the plate 90 degrees 
    mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 
        0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Part-3-1', ))
            
         # this specify the axisDirection 
         
    mdb.models['Model-1'].rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0, 
        0.0), direction2=(0.0, 1.0, 0.0), instanceList=('Part-3-1', ), number1=1, 
        number2=2, spacing1=2000.0, spacing2=height)
            

            
         # this makes some instance independent 
         
    mdb.models['Model-1'].rootAssembly.makeIndependent(instances=(
        mdb.models['Model-1'].rootAssembly.instances['Part-3-1'], 
        mdb.models['Model-1'].rootAssembly.instances['Part-3-1-lin-1-2']))
         
          # this creates the step 
          
    mdb.models['Model-1'].StaticStep(initialInc=0.05, maxInc=0.05, name='Step-1', 
        nlgeom=ON, previous='Initial')
             


            # this merge *connect* all the parts
                   
    mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
        instances=(mdb.models['Model-1'].rootAssembly.instances.values()), name='Part-4', originalInstances=SUPPRESS)           

               # This moves the model to the origine 

    mdb.models['Model-1'].rootAssembly.translate(instanceList=('Part-4-1', ), 
        vector=(dist_3, 0.0, 0.0))    
           
              # this creates the Load as a Pressure
        # mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1', 
            # distributionType=UNIFORM, field='', magnitude=15.0, name='Load-1', region=
            # Region(side2Faces=mdb.models['Model-1'].rootAssembly.instances['Part-4-1'].faces.getByBoundingBox(xMin=-1.0, 
            # yMin=height/2.0, zMin=-1.0, xMax=width_p+1.0, yMax=height+1.0, zMax=length_p+1.0)))

            # this creates the load as a top plate displacement
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-2', region=Region(
        faces=mdb.models['Model-1'].rootAssembly.instances['Part-4-1'].faces.getByBoundingBox(xMin=-1.0, 
        yMin=height/2.0, zMin=-1.0, xMax=width_p+1.0, yMax=height+1.0, zMax=length_p+1.0)), u1=UNSET, u2=-height*0.1, u3=
        UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
            
             # this creates the supports #boundary conditions
             
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-1', region=Region(faces=mdb.models['Model-1'].rootAssembly.instances['Part-4-1'].faces.getByBoundingBox(xMin=-1.0, 
        yMin=-1.0, zMin=-1.0, xMax=width_p+1.0, yMax=height/2.0, zMax=length_p+1.0)), 
        u1=0.0, u2=0.0, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)
            

             
            # this make the instance independent  
          
    mdb.models['Model-1'].rootAssembly.makeIndependent(instances=(
        mdb.models['Model-1'].rootAssembly.instances['Part-4-1'], ))
          
             
            # this creates the mesh 
             
    mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
        minSizeFactor=0.1, regions=(
        mdb.models['Model-1'].rootAssembly.instances['Part-4-1'], ), size=mesh_size)
            
            
    mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
        mdb.models['Model-1'].rootAssembly.instances['Part-4-1'], ))     
              

        # mdb.models['Model-1'].rootAssembly.Set(name='Set-1', vertices=
                # mdb.models['Model-1'].rootAssembly.instances['Part-4-1'].vertices.findAt((( 0.0, 
                # height, 0.0), )))
            
    mdb.models['Model-1'].rootAssembly.Set(name='Set-1', nodes=
        mdb.models['Model-1'].rootAssembly.instances['Part-4-1'].nodes.getByBoundingBox(xMin=-1.0, yMin=-1.0, zMin=-1.0, xMax=width_p+1.0, yMax=1.0, zMax=length_p+1.0))
            
            
    mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(rebar=
        EXCLUDE, region=mdb.models['Model-1'].rootAssembly.sets['Set-1'], 
        sectionPoints=DEFAULT, variables=('RF2', ))
        # mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', name=
            # 'H-Output-2', rebar=EXCLUDE, region=
            # mdb.models['Model-1'].rootAssembly.sets['Set-2'], sectionPoints=DEFAULT, 
            # variables=('RF2', ))

            
            # this creates the job 
            
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
        multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
        numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
        ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
        
    mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
        'S', 'E', 'U', 'RF', 'CF'))

          
           # This submits the job
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)


            # TO WAIT FOR JOB COMPLETION
    mdb.jobs['Job-1'].waitForCompletion()
    print("Hex Model finished running")


def PostProcessingModel(variables):

     # #hexagon dimentions 
     
    width = variables[0] #mm 
    lenght = variables[1] #mm
    height = variables[2] #mm
    theta = variables[3] #degrees
    ribs_t = variables[4] #mm
    plate_t = variables[5] #mm 
    n_x = variables[6] #hexagons 
    n_z = variables[7] #hexagons
    mesh_size = variables[8] #mm

    dist_1 = lenght * math.cos(theta*math.pi/180.0) * 2.0 + 2.0 * width 
    dist_2 = lenght * math.sin(theta*math.pi/180.0) 
    dist_3 = lenght * math.cos(theta*math.pi/180.0)

    # number of hexagons


        # plate dimentions

    width_p = dist_1 * n_x - width #mm
    length_p = dist_2 * 2.0 * n_z #mm
    Area_p = width_p * length_p

    CurrentDir = os.getcwd()
    odb = session.openOdb(CurrentDir +'/Job-1.odb')
    NrOfSteps = len(odb.steps['Step-1'].frames)

    displacements = []

        # odb.steps['Step-1'].frames[i].fieldOutputs['U'].values[2].data[1]

        # odb.steps['Step-1'].historyRegions['Node I_SECTION-1.%s'%i[0]].historyOutputs['%s'%i[1]].data

    for i in range(NrOfSteps):
        central_disp = odb.steps['Step-1'].frames[i].fieldOutputs['U'].values[2].data[1]*-1
        strain=central_disp/height
        displacements.append(strain)

    Forces = []

    for i in range(NrOfSteps):
        applied_force = 0.0
        for j in odb.steps['Step-1'].historyRegions.keys():
            applied_force = applied_force + odb.steps['Step-1'].historyRegions[j].historyOutputs['RF2'].data[i][1]
            # applied_force = odb.steps['Step-1'].frames[i].fieldOutputs['CF'].values[1].data[1]*-1
        Forces.append(applied_force/Area_p)

    fig, ax = plt.subplots()
    ax.plot(displacements, Forces, color='r', label='U2')
    plt.legend()
    ax.set(xlabel='Strains ', ylabel='Applied Stress [MPa]',
            title='Stress Strain Curve')
    ax.grid()

    fig.savefig("MAX_DISPLACMENT.png")
    plt.close(fig)
           
    opFile = BaseDir+"/"+str(Foldername)+"/"+str(variables)+'/'+'DatainExcel.csv'  
           
    try:
        opFileU = open(opFile,'w')
        opFileU.write("%10s,%10s,%10s\n"%('Force', 'U2', 'Stiffness') )
    except IOError:
        PrintToScreen('cannot open opFILE')
        exit(0)

    Stiffness=[]

    for i in range(NrOfSteps):
        displacement = displacements[i]
        force = Forces[i]
        if i!=0 and displacements[i-1]!= displacements[i]:
            Current_Stiffness = (Forces[i]-Forces[i-1])/(displacements[i]-displacements[i-1])
            Stiffness.append(Current_Stiffness)
        else:
            Current_Stiffness = 999999.0
            Stiffness.append(Current_Stiffness)
            opFileU.write("%10f,%10f,%10f\n" % (force, displacement, Current_Stiffness))
    opFileU.close()

Models = []
for i in range(5,175,10):
   Models.append([100.0, 100.0, 150.0, i, 3.0, 4.0, 2, 5, 800.0])
# Models.append([100.0, 100.0, 100.0, 5.0, 3.0, 4.0, 3, 7, 20.0])
# Models.append([100.0, 100.0, 100.0, 25.0, 3.0, 4.0, 3, 7, 20.0])
# Models.append([100.0, 100.0, 100.0, 35.0, 3.0, 4.0, 3, 7, 20.0])
# Models.append([100.0, 100.0, 100.0, 45.0, 3.0, 4.0, 3, 7, 20.0])


for variables in Models[0:]:
    os.mkdir(BaseDir+"/"+str(Foldername)+"/"+str(variables))
    os.chdir(BaseDir+"/"+str(Foldername)+"/"+str(variables))
    CreateHexModel(variables)
    PostProcessingModel(variables)
    
 