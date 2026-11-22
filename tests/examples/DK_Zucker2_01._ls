SAINT V8.38A
C:\bn\SAINT\saint.exe q7vkh_.slm /BATCH /CONFIG:q7vkh_.ini /NOPROMPT /PLAIN /PRI&
ORITY:4 /SOCKET:2000

!====================================================
!04/16/2019 16:17:15 
INTEGRATE &
 "D:\frames\guest\DK_Zucker2\mo_DK_Zucker2_[1-14]_0001.sfrm,mo_fastscan_01_0001" &
 "D:\frames\guest\DK_Zucker2\work\DK_Zucker2_[1-14].raw,DK_Zucker2_01A" &
 /2THETA=-9999.0000 /ACTTHRESH=0.2000 /ALPHA12 /AMNAME=$NEW /BATCH=1 &
 /BGCSCALE=0 /BGQSCALE=1 /BGSIG=1.000 /CHI=-9999.0000 /CRYSTAL=1 &
 /CYCLIM=25 /DAAP=0.0000 /DAPHI=0.00000 /DFRAME /ESDSCALE=1.00000 &
 /EXPOSURE=0.000 /GLOBAL /GMARQ=2.000000e-003 /GMIN=0 /GREFLIM=9999 &
 /GRLVERR=0.0250 /GSVD=1.000000e-006 /IAXIS=-9999 /IOVSIGMA=-3.00000 &
 /K1=3 /K2=3 /L1=T /L2=0 /LATTICE=0 /LMARQ=2.000000e-003 /LMIN=0 &
 /LORENTZ=0.02000 /LORMODEL=0.07500 /LRES=9999.00000 /LSFIT /LSFREQ=50 &
 /LSVD=5.000000e-005 /LTHR=8.000 /LWT=0.000 /MACHINE_ERROR=0.0000 &
 /MAXSATIND=1 /MCESDS /MCREFLIM=4096 /MCVERB=1 /MEDMSK=-1 &
 /MISSING=0.6000 /MMIC=20.00000 /NEXP=-9999 &
 /NFRAMES="304,304,304,304,304,304,304,304,304,304,304,304,304,66,180" &
 /NODECAY /NSIM=20 /OMEGA=-9999.0000 &
 /ORIENTATION=D:\frames\guest\DK_Zucker2\work\q7vkh_.p4p &
 /ORTUPDSCALE=1.000 /OVRTIME=-9999.00000 /PHI=-9999.0000 /PLANEBG &
 /POINTGROUP="2/m" /PROFXHALF=4 /PROFYHALF=4 /PROFZHALF=4 /QUEUEHALF=9 &
 /RESOLUTION=0.43000 /ROLL=0.000 /SEED=0 /SHRMSK=-1 /SMAP=1 &
 /SMIC=20.00000 /SNAP=999 /SPATIAL=$NULL /SSBIAS=1.0000 /STRONG=10.000 &
 /TIMEOUT=0.000 /TITLE="Integration of DK_zucker" /TOPFILT &
 /TPROF=0.0500 /TTM=0.000 /TWINBOXRATIO=1.30000 /TWINMINCOMVOL=0.04000 &
 /TWINSEPARATION=1.00000 /VERBOSITY=2 /VOLANGSTROMS=1.00000 &
 /VOLTARGET=1.00000 /WIDTH=-9999.0000 /WTMETH=2 /XSIZE=0.4720 &
 /YSIZE=0.4720 /ZSIZE=1.4866 /ZW=1.000


Saving spots >    10.00 sigma(I) in D:\frames\guest\DK_Zucker2\work\DK_Zucker2_01._ma

Multiple runs have been specified:
  (current run indicated with "*")
 FRAME                  MATRIX                 OUTPUT                 #FRAMES
*mo_DK_Zucker2_01_0001  q7vkh_.p4p             DK_Zucker2_01.raw          304
 mo_DK_Zucker2_02_0001  q7vkh_.p4p             DK_Zucker2_02.raw          304
 mo_DK_Zucker2_03_0001  q7vkh_.p4p             DK_Zucker2_03.raw          304
 mo_DK_Zucker2_04_0001  q7vkh_.p4p             DK_Zucker2_04.raw          304
 mo_DK_Zucker2_05_0001  q7vkh_.p4p             DK_Zucker2_05.raw          304
 mo_DK_Zucker2_06_0001  q7vkh_.p4p             DK_Zucker2_06.raw          304
 mo_DK_Zucker2_07_0001  q7vkh_.p4p             DK_Zucker2_07.raw          304
 mo_DK_Zucker2_08_0001  q7vkh_.p4p             DK_Zucker2_08.raw          304
 mo_DK_Zucker2_09_0001  q7vkh_.p4p             DK_Zucker2_09.raw          304
 mo_DK_Zucker2_10_0001  q7vkh_.p4p             DK_Zucker2_10.raw          304
 mo_DK_Zucker2_11_0001  q7vkh_.p4p             DK_Zucker2_11.raw          304
 mo_DK_Zucker2_12_0001  q7vkh_.p4p             DK_Zucker2_12.raw          304
 mo_DK_Zucker2_13_0001  q7vkh_.p4p             DK_Zucker2_13.raw          304
 mo_DK_Zucker2_14_0001  q7vkh_.p4p             DK_Zucker2_14.raw           66
 mo_fastscan_01_0001    q7vkh_.p4p             DK_Zucker2_01A.raw         180
Current batch number is 1

Integration of DK_zucker

Logical CPUs detected:             8
Number of threads to be used:      8
Additional read-ahead threads:     0

Input linear pixel scale:         1.00000
Input frame rows, columns:      1024  768
Frame queue half-size:             9
Number of frames in queue:        19
Profile X,Y,Z half-widths:         4  4  4
Number of X,Y,Z profile points:    9  9  9
Fraction-of-maximum method will be used to determine summation volume

SMART CCD DETECTOR PARAMETERS ------------
Detector type = 1 was obtained from CONFIGURE menu
Multiwire reference correction will be disabled
Detector is a single tile            (from CONFIGURE menu)
Read noise (e-):                1.04 (from frame mo_DK_Zucker2_01_0001.sfrm)
Electrons per A/D unit:        36.60 (from frame mo_DK_Zucker2_01_0001.sfrm)
Electrons per x-ray photon:   259.92 (from frame mo_DK_Zucker2_01_0001.sfrm)
Base offset per exposure:         64 (from frame mo_DK_Zucker2_01_0001.sfrm)
Per-exposure full scale:      163809 (from frame mo_DK_Zucker2_01_0001.sfrm)
Nominal pixels per CM:        36.955 (from CONFIGURE menu)
CM from face to imaging plane: 1.004 (from CONFIGURE menu)
Fiducial spot spacing(CM):     0.425 (from CONFIGURE menu)
Faceplate transmittance:      0.9686 (from CONFIGURE menu)
Phosphor absorption:          0.9000 (from CONFIGURE menu)
Air absorption (per CM):      0.0012 (from CONFIGURE menu)
Active pixel threshold:        0.200 (from Advanced menu)

Frames were acquired with BIS V6.2.10/2018-10-02
   Booster system: rescan threshold is 60,000 ADU

Starting swing angle will be obtained from frame header
Starting omega will be obtained from frame header
Starting phi will be obtained from frame header
Starting chi will be obtained from frame header
Number of exposures summed will be obtained from frame header
Scan axis will be obtained from frame header
Scan width will be obtained from frame header
Exposure time will be obtained from frame header

Initial background ================== 04/16/2019 16:17:15

Initial background range (deg) =      10.00, interleave = 2
Number of BG pixels >= 64K:               0
 
Initial BG frame written to mo_DK_Zucker2_ib_01_0001.sfrm
 
Nominal time per frame (s):          30
Intensity normalization in deg/min:  1
Output intensities are multiplied by this value
   to place on scale of 1 min/deg

Reading orientation and spatial calibration ========== 04/16/2019 16:17:15
INFO:  No spatial correction will be used
Orientation for 1 component read from D:\frames\guest\DK_Zucker2\work\q7vkh_.p4p
Detector distance of 2.396 cm was obtained from header of D:\frames\guest\DK_Zucker2\mo_DK_Zucker2_01_0001.sfrm

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file
... Input P4P data for sample 1 of 1:
... This sample is a single crystal with 3 indices (HKL)

... Component 1.1(1) (component 1 in sample 1, 1 of 1 in file)
Orientation ("UB") matrix:
  -0.0107284  -0.0355863   0.0858602
  -0.1293326  -0.0206750  -0.0337897
   0.0283684  -0.1077162  -0.0218802

Unit Cell: A           B           C       Alpha        Beta       Gamma
      7.7250      8.6722     10.8216      90.000     102.974      90.000

Detector corrections:      X-Cen   Y-Cen    Dist   Pitch    Roll     Yaw
                          -0.203  -0.144   0.010  -0.240  -0.060  -0.250

Goniometer zeros (deg):       0.0000      0.0000      0.0000      0.0000
Crystal translations (pixels):            0.0000      0.0000      0.0000
... End component 1.1(1)
... End sample 1 of 1

Mean, a1, a2 wavelength (Angstroms):     0.71073     0.70930     0.71359
Alpha1:alpha2 ratio:                     2.00000
Nominal detector distance (cm):            2.396
X,Y beam center @swing=0 (pixels):        386.44      506.71

Input sample map:    1

Input components will be treated as follows:

 Component   Lattice      PointGroup    Wanted    Indices  Subsystems
    1.1(1)       0=P   2/m(B-unique)         Y      3=HKL           1

Active pixel mask ================== 04/16/2019 16:17:15

Median filter size:   input, used    -1,  4
Mask shrinkage (pix): input, used    -1,  6
No diamond-anvil cell occlusions will be computed
Active area will be limited according to x-ray aperture file:
   mo_DK_Zucker2_xa_01_0001.sfrm
Active pixel mask written to mo_DK_Zucker2_am_01_0001.sfrm
Fraction of mask marked active:  0.8888

Scan axis is OMEGA
Spatially corrected beam center:       386.44  506.71
Direction cosines of rotation axis:    -0.001   0.000   1.000
Starting frame angles (degrees):      294.275 128.461 200.000  54.736
Vertical tilt of beam (degrees):      -0.0600
Exposures per frame:                        1
Output sigma(I)'s will be scaled by:                   1.0000
Fraction of I to be combined with sigma(I)'s:          0.0000
Maximum number of frames to be processed:                 304
Mark-up frames will not be written
Narrow-frame algorithm will be used.
Per-frame BG offsets will be used.
Best-fit plane BG will be used.
Direct beam monitor will not be used.
Alpha1,2 splitting will be added to box sizes
Box volumes will be multiplied by exp(0.00000 * [sin(theta)/lambda]^2
Target volume factor is 1.000 at 1.000 angstroms
Max allowed missing profile intensity:                  0.600
Lorentz cutoff for exclusion from output:              0.0200
Lorentz cutoff for exclusion from model profiles:      0.0750
LS will use individual reflection weights

Initial orientation and spot-shape refinement ============== 04/16/2019 16:17:16
Input X,Y,Z spot size (deg):    0.472   0.472   1.487
Scale for orientation update length:            1.00000
#Frames running average for orientation update:      18
Frames between full refinements of orientation:      50
Frames in BG running avg (correlation length):       16
Nominal frame width in degrees:                   0.500
Accurate-timing indicator is set in the frame headers:
   Velocity normalization will be computed for each frame
Pixel spacing (deg):              0.176
Profile X,Y,Z spacing (deg):      0.074   0.052   0.150
Profile convolver halfwidth:       1.61    1.61    1.51
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
    0_0001    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   14 0.47 0.47 1.49 1.000
    1_0002    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   16 0.47 0.47 1.49 1.000
    2_0003    8  0.15 -0.03  0.16  0.25  0.08  0.27 8173.0  47   13  0.41   20 0.47 0.47 1.49 1.000
    3_0004   32  0.25  0.08  0.12  0.37  0.27  0.26 3064.6  24   13  0.49   23 0.47 0.47 1.49 1.000
    4_0005   30  0.23  0.10  0.05  0.27  0.23  0.21 3062.2  23    3  0.58   25 0.47 0.47 1.49 1.000
    5_0006   29  0.28  0.12  0.03  0.39  0.32  0.17 2277.3  19    7  0.58   27 0.47 0.47 1.49 1.000
    6_0007   27  0.16  0.06  0.10  0.33  0.21  0.24 3457.6  23    4  0.61   25 0.47 0.47 1.49 1.000
    7_0008   24  0.17  0.07  0.07  0.31  0.23  0.25 4096.9  24    8  0.59   25 0.47 0.47 1.49 1.000
    8_0009   25  0.24  0.12  0.01  0.26  0.28  0.19 5223.5  26    0  0.72   27 0.47 0.47 1.49 1.000
    9_0010   30  0.24  0.06 -0.04  0.29  0.25  0.20 4106.0  25   10  0.66   26 0.47 0.47 1.49 1.000
   10_0011   29  0.23  0.05 -0.01  0.35  0.27  0.26 6067.9  35    7  0.62   25 0.47 0.47 1.49 1.000
   11_0012   30  0.15  0.04  0.04  0.23  0.10  0.16 4197.0  24    7  0.65   26 0.47 0.47 1.49 1.000
   12_0013   29  0.19  0.11  0.02  0.24  0.23  0.20 4327.0  29    0  0.71   28 0.47 0.47 1.49 1.000
   13_0014   25  0.15  0.11  0.05  0.32  0.40  0.22 6815.2  33    8  0.64   26 0.47 0.47 1.49 1.000
   14_0015   28  0.20  0.03 -0.01  0.23  0.12  0.14 2699.1  23    4  0.62   25 0.47 0.47 1.49 1.000
   15_0016   33  0.19  0.03  0.06  0.25  0.16  0.15 4547.4  27    0  0.65   25 0.47 0.47 1.49 1.000
   16_0017   29  0.11 -0.00  0.03  0.25  0.15  0.17 4820.6  29    0  0.65   25 0.47 0.47 1.49 1.000
   17_0018   33  0.13 -0.05  0.04  0.27  0.32  0.17 2968.0  21   12  0.62   25 0.47 0.47 1.49 1.000
   18_0019   27  0.12  0.04  0.04  0.32  0.21  0.17 2339.6  19    7  0.68   25 0.47 0.47 1.49 1.000
   19_0020   25  0.06  0.01  0.05  0.19  0.11  0.16 2216.9  17   16  0.57   23 0.47 0.47 1.49 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   20_0021   16  0.12 -0.01  0.05  0.15  0.06  0.12 5340.7  25    0  0.67   27 0.47 0.47 1.49 1.000
   21_0022   28  0.11  0.05 -0.02  0.23  0.19  0.17 3520.7  23    4  0.65   25 0.47 0.47 1.49 1.000

I/Sigma = 37.15   Thresh = 0.020   Blend = F   #Contributing = 171   InitialProfileWt = 0.069
Region 1
Sum = 9002.42;   Maximum = 102.906;   FM = 0.839
!Region 1: Section 1->3
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    1  4  7  6  4  3  2  1  0  
  0  0  0  0  0  0  0  0  0    1  2  4  4  2  1  0  0  0    4 11 15 14 10  6  4  2  1  
  0  0  0  0  0  0  0  0  0    1  4  6  5  3  1  1  0  0    9 21 29 25 17 11  7  4  1  
  0  0  0  0  0  0  0  0  0    2  5  7  6  3  1  1  0  0   11 27 37 31 20 12  7  3  1  
  0  0  0  0  0  0  0  0  0    1  5  7  6  3  1  0  0  0    8 22 29 24 14  8  5  2  1  
  0  0  0  0  0  0  0  0  0    1  4  6  6  3  1  1  0  0    8 21 28 25 16  9  5  2  1  
  0  0  0  0  0  0  0  0  0    1  3  5  5  3  1  0  0  0    8 20 28 24 15  8  5  2  1  
  0  0  0  0  0  0  0  0  0    1  2  4  3  1  1  0  0  0    5 13 17 15  8  4  2  1  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    2  5  6  5  3  1  1  0  0  
!Region 1: Section 4->6
  4 13 17 19 19 18 13  5  2    7 18 23 30 36 33 22  8  3    4  9 15 24 28 23 13  5  2  
  9 25 31 31 32 30 22  9  3   13 31 39 50 61 59 37 16  5    8 18 32 49 61 49 26 11  3  
 16 35 43 41 39 36 25 11  3   14 28 36 46 60 60 38 17  4    7 18 32 48 61 51 26 11  3  
 21 44 55 52 48 43 28 13  3   18 37 47 59 74 74 47 20  4    9 21 36 56 67 57 31 12  3  
 18 45 54 52 51 46 32 13  4   21 48 62 80100 92 59 23  6   11 26 49 78 97 75 39 15  4  
 17 45 55 55 52 47 33 13  4   20 46 59 75 91 86 54 21  5   11 25 43 66 84 67 34 13  3  
 15 35 43 40 34 30 20  8  2   14 30 36 45 54 54 34 14  3    7 15 26 39 50 43 23  9  2  
 10 20 24 21 18 15 10  5  1    9 18 21 26 33 33 21  9  2    5 10 17 27 34 28 15  6  2  
  4  7  8  7  7  7  5  2  1    4  8  9 11 16 16 11  5  1    2  5  8 12 15 13  8  3  1  
!Region 1: Section 7->9
  2  4  9 15 15 11  6  3  1    1  1  2  3  3  2  1  1  0    0  0  0  0  0  0  0  0  0  
  3  8 16 24 27 19 10  4  2    1  2  3  4  3  2  2  1  0    0  0  0  0  0  0  0  0  0  
  3  9 18 26 28 19  9  4  1    1  3  4  4  4  2  1  1  0    0  0  0  0  0  0  0  0  0  
  3 11 21 32 32 22 11  4  1    2  4  5  7  6  3  2  1  0    0  1  0  0  0  0  0  0  0  
  5 13 26 42 45 30 15  6  2    2  4  6  7  7  4  3  1  1    0  1  0  0  0  0  0  0  0  
  4 11 22 35 39 27 13  5  2    1  3  5  6  5  3  2  1  1    0  0  0  0  0  0  0  0  0  
  3  8 14 21 23 16  7  3  1    1  3  4  4  3  2  1  1  0    0  0  0  0  0  0  0  0  0  
  2  5 10 14 14 10  5  2  1    1  2  3  3  2  1  1  0  0    0  0  0  0  0  0  0  0  0  
  1  2  4  5  5  4  2  1  0    0  1  1  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 0.00   Thresh = 0.020   Blend = F   #Contributing = 0   InitialProfileWt = 1.000
Region 2
Sum = 1.02272;   Maximum = 0.0166878;   FM = 0.734
!Region 2: Section 1->3
  0  0  0  0  0  0 -1 -1  0    0  1  1  1  1  0 -1 -1  0    1  3  3  2  1  1  0  0  0  
  0  1  1  1  0 -1 -1 -1  0    2  4  6  4  1  0 -1 -1  0    4 10 10  6  3  1  1  0  0  
  1  2  3  1  0 -1 -1 -1  0    4  9 12  7  2  0 -1 -1  0   10 20 19 11  5  2  2  1  0  
  1  2  4  2  0 -1  0  0  0    5 14 18 11  2  0  0  0  0   17 32 30 16  6  3  2  1  0  
  1  2  4  2 -1 -1  0  0  0    7 18 22 13  3  0  0  0  0   22 45 41 20  7  3  3  2  0  
  0  2  3  2  0 -1  0  0 -1    7 19 23 13  3  0  0  0 -1   24 48 45 21  7  4  3  1  0  
  0  2  3  1  0 -1  0  0 -1    6 17 20 11  3  1  0  0 -1   19 40 41 21  7  3  2  0 -1  
  0  2  2  1  0  0  0  0  0    4 13 17 10  2  0  0  0  0   10 28 35 19  5  2  1  0  0  
  0  1  1  1  0  0  0  0  0    1  6  9  5  1  0 -1  0  0    3 12 18 10  3  0  0  0  0  
!Region 2: Section 4->6
  1  3  3  3  4  5  4  1  0    1  2  3  5  9 13 10  4  1    0  3  9 11  9  8  6  3  1  
  4  9  9  8 10 13 11  4  1    2  5  7 11 23 37 28 10  2    1  7 19 25 21 22 16  6  1  
  9 16 15 12 16 23 18  6  2    3  6  8 16 38 59 44 14  4    2  8 24 34 31 33 24  9  2  
 14 24 20 16 24 34 25  9  2    4  7 10 24 58 84 57 17  4    2  8 28 43 43 44 29 10  2  
 17 31 26 20 30 42 31 10  2    4  9 14 34 76 99 65 19  4    2  8 27 47 54 51 30 10  2  
 18 32 27 22 33 45 33 10  2    4  9 15 39 82100 65 19  3    2  8 22 42 55 48 26  8  2  
 13 25 23 20 28 40 30  8  1    3  6 14 37 72 85 55 15  2    2  6 17 34 44 38 20  6  1  
  6 15 18 16 19 27 21  6  0    2  4 12 29 50 56 37 10  1    1  5 12 24 30 24 12  3  1  
  1  5  8  7  8 10  8  3  0    0  1  6 13 20 21 15  5  1    0  2  5  9 12  9  5  2  0  
!Region 2: Section 7->9
  0  3  8 10  5  2  1  1  0    0  0  0  0  0  1  0  0  0    0  0  0  0  0  0  0  0  0  
  1  6 18 21 10  4  2  1  1    0  1  1  0  0  1  1 -1  0    0  0  0 -1 -1  0  0  0  0  
  1  7 22 28 13  5  3  2  1    0  1  1  0  0  1  1  0  0    0  0  0 -1  0  0  1  0  0  
  1  7 26 33 16  7  4  2  1    1  1  1  1  1  2  2  1  0    0  0  0  0  0  1  0  1  0  
  1  6 23 32 18  9  5  3  1    1  1  0  1  2  2  1  1  0    0  0  0  0  0  0  1  0  0  
  1  6 16 25 18  8  4  2  1    0  0  1  2  3  2  1  0  0    0  0  0  0  1  1  0  0  0  
  1  5 12 17 13  7  3  1  0    0  0  1  2  2  1  0  0  0    0 -1  0  0  0  0  0  0  0  
  1  4  8 10  8  4  2  0  0    0  0  0  2  2  1  1  0  0    0 -1  0  0  0  0  0  0  0  
  0  1  3  3  3  1  1  0  0   -1 -1  0  1  1  1  0  0  0    0 -1  0  0  0  0  0  0  0  

I/Sigma = 17.85   Thresh = 0.020   Blend = F   #Contributing = 4   InitialProfileWt = 0.586
Region 3
Sum = 2233.7;   Maximum = 47.559;   FM = 0.694
!Region 3: Section 1->3
  0  0  0  1  0  0 -1 -1  0    0  0  1  2  1  0 -1 -1  0    1  3  3  2  1  0  1  0  0  
 -1  0  2  3  1  0 -1 -1  0    0  3  8  7  2  0 -1 -1  0    4 10 10  7  2  1  2  1  0  
  0  2  5  4  1  0 -1 -1  0    1  8 16 12  3  0 -1 -2 -1    8 18 18 11  3  3  3  1  0  
  1  3  6  4  1  0  0 -1  0    2 11 20 15  3  0  0 -1 -1   15 28 24 14  4  3  4  2  0  
  0  4  7  5  0 -1  0  0  0    3 13 22 16  4  0  0  0 -1   20 36 28 14  5  4  4  2  0  
  0  3  7  4  0 -1 -1  0 -1    3 12 20 13  4  1  1  0  0   21 36 26 12  5  4  4  2  0  
  0  3  5  3  1  0  0  0 -1    3 11 13  8  3  2  1  0 -1   16 29 20  8  3  3  3  1  0  
  0  2  3  2  1  0  0  0  0    1  6  7  4  1  0 -1 -1  0    5 15 11  4  2  2  1  0  0  
  0  0  1  1  1  0  0  0  0    0  1  2  2  0  0 -1  0  0    0  3  4  2  0  0  1  0  0  
!Region 3: Section 4->6
  2  3  2  2  2  3  3  1  0    0  0  1  2  7 15 12  5  0    0  0  0  1  5  9  7  3  0  
  5  9  8  5  6 11 10  4  1    0  1  3  7 22 43 36 12  1    0  0  1  4 13 26 20  7  1  
  9 16 13  9 11 18 16  6  1    1  1  3 14 41 70 55 17  2    0  0  1  8 24 41 31  9  1  
 15 25 18 13 17 24 20  7  1    1  2  6 25 65 92 63 19  3    0  0  3 15 38 54 36 10  2  
 20 32 22 16 22 26 19  7  1    2  3  9 37 86100 59 18  3    0  0  5 22 50 58 34 10  2  
 22 33 22 17 24 24 15  5  0    2  4 12 47 93 92 47 13  2    0  2  8 29 55 53 26  7  1  
 16 26 18 16 21 19 10  3  0    1  4 15 49 85 72 32  8  1    1  3 10 30 49 41 18  5  1  
  5 12 11 12 15 12  6  2  0    1  3 13 41 60 43 17  5  1    1  3  9 24 35 25 10  3  1  
  0  2  5  6  6  5  2  1  0    0  1  7 19 24 16  6  2  0    0  1  4 11 14  9  3  1  0  
!Region 3: Section 7->9
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  1  1  1  0 -1  0    0  1  1  0 -1  0  0  0  0    0  1  1  0 -1 -1  0  0  0  
  0  0  0  0  1  1  0 -1  0    1  1  0  0  0  0  1  0  0    1  1  0  0 -1  0  1  0  0  
 -1 -1  0  0  1  1  1  0  0    0  0  0  0  0  1  1  0  0    0  0  0  0  0  0  0  1  0  
 -1  0  1  1  1  2  1  0  0    0  0  0 -1  0  1  1  0  0    0  0  0  0  0  0  1  0  0  
  0  1  2  3  3  2  1  0  0    0 -1 -1 -1  1  1  1  0  0   -1 -1 -1  0  0  1  0  0  0  
  1  2  3  4  3  2  1  0  0    0 -1 -1  0  1  1  0  0  0    0 -1 -1  0  0  0  0  0  0  
  1  2  3  3  3  1  0  0  0    0  0 -1  0  1  0  0  1  1    0 -1 -1  0  0  0  0  1  1  
  0  1  1  2  1  0  0  0  0    0  0  0  0  1  0  0  1  1    0 -1 -1  0  0  0  0  1  1  

I/Sigma = 27.72   Thresh = 0.020   Blend = F   #Contributing = 15   InitialProfileWt = 0.301
Region 4
Sum = 5058.34;   Maximum = 82.3599;   FM = 0.805
!Region 4: Section 1->3
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    1  3  4  3  4  4  2  1  0  
  0  0  0  0  0  0  0  0  0    1  2  4  3  1  1  0  0  0    2  7 10  9  9 10  6  2  0  
  0  0  0  0  0  0  0  0  0    2  6  8  6  2  1  0  0  0    4 14 21 17 13 14  8  3  0  
  0  1  1  1  0  0  0  0  0    3  9 14 10  3  1  0  0  0    6 22 34 26 15 14  8  2  0  
  0  1  1  1  0  0  1  0  0    3 12 17 12  4  1  0  0  0    9 30 42 30 15 11  6  1  0  
  0  1  2  1  0  0  1  0  0    3 11 17 11  4  1  0  0  0   11 35 45 30 12  8  4  1  0  
  0  1  1  1  0  0  0  0  0    3  9 13  9  3  1  0  0  0   12 33 40 24  9  4  2  1  0  
  0  1  1  1  0  0  0  0  0    2  6  8  5  1  0  0  0  0   11 29 30 17  5  2  1  0  0  
  0  0  0  0  0  0  0  0  0    1  3  3  2  0  0  0  0  0    5 13 13  7  2  1  0  0  0  
!Region 4: Section 4->6
  1  2  3  5 10 12  8  3  1    0  1  2  5 10 13 10  4  0    0  1  2  3  4  5  4  2  0  
  2  6  9 14 28 37 24  7  1    0  2  5 14 35 45 29  9  1    0  1  3  8 15 17 11  5  1  
  3 11 17 23 41 53 35 11  2    1  3  8 24 56 72 45 14  3    0  2  6 15 30 32 19  7  2  
  6 19 30 34 48 57 36 11  2    2  6 15 38 80 90 51 16  3    1  2  9 26 49 48 25  8  2  
 10 30 41 40 48 54 32  9  1    4 10 20 49 95100 53 15  2    1  4 13 38 67 60 28  8  1  
 15 40 50 41 40 41 23  7  1    5 14 26 53 93 89 43 11  2    1  3 16 45 73 62 26  6  1  
 18 45 49 35 30 27 14  4  1    7 17 25 45 75 68 30  7  1    1  3 14 40 63 49 19  4  0  
 18 43 42 26 18 15  7  2  1    7 17 22 32 49 41 16  4  1    1  3 12 31 45 33 11  3  0  
  8 19 18 11  7  5  2  1  1    3  8 10 14 20 16  5  1  0    0  1  5 13 20 13  4  1  0  
!Region 4: Section 7->9
  0  0  1  0  0  0  0  0  0    0  0  0  0 -1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  1  1  1  1  1  1  1    0  1  1  0 -1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  2  3  3  3  2  2  1    0  1  1  0  0 -1  0  0  0    0  0  0  0  0  0  0 -1  0  
  0  1  3  5  7  6  3  2  1    0  0  0  0  0  0  0  0  0    1  1  0  0  0  0  0  0  0  
  0  2  4  9 12 10  4  2  1    0  1  1  0  0  0  0  0  0    0  1  0  0  0  0  0  0  0  
  0  1  5 11 15 12  5  2  0    0  1  1  1  1  1  1  1  0    0  0  0  0  0  0  0  0  0  
  0  2  4 10 13  9  4  1  0    0  1  1  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  4  9 11  7  2  1  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4  5  3  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 113.94   Thresh = 0.020   Blend = F   #Contributing = 45   InitialProfileWt = 0.090
Region 5
Sum = 78903.2;   Maximum = 1525.49;   FM = 0.822
!Region 5: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  2  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    1  2  4  5  4  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  2  2  1  1  0  0  0    1  5 10 11  8  5  2  1  0  
  0  0  0  0  0  0  0  0  0    1  2  3  3  2  1  0  0  0    3 10 20 22 15  7  2  1  0  
  0  0  0  0  0  0  0  0  0    1  3  4  4  2  1  0  0  0    5 15 28 29 19  8  2  1  0  
  0  0  0  0  0  0  0  0  0    1  4  5  4  2  1  0  0  0    5 18 31 31 19  7  2  1  0  
  0  0  0  0  0  0  0  0  0    1  4  5  4  2  1  0  0  0    6 18 29 27 15  5  1  0  0  
  0  0  0  0  0  0  0  0  0    1  3  4  3  1  1  0  0  0    4 12 19 17  8  3  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  2  1  1  0  0  0  0    2  4  7  6  3  1  0  0  0  
!Region 5: Section 4->6
  0  1  3  7  7  4  2  1  0    0  1  4 10 11  8  4  1  0    0  0  2  4  6  5  2  1  0  
  1  4 11 20 22 15  8  3  0    1  4 15 33 41 31 16  5  1    0  1  6 15 20 16  9  3  1  
  2 11 30 45 46 33 14  4  1    1  9 36 70 82 60 27  8  1    0  3 13 30 39 29 14  4  1  
  5 23 55 76 67 40 15  4  1    3 18 55 95100 67 28  7  1    1  5 19 37 44 31 15  4  1  
  9 35 73 89 71 37 13  3  1    5 25 65 97 98 62 25  7  1    1  7 21 37 43 31 15  4  1  
 10 38 73 84 62 29 10  3  0    6 27 58 77 68 41 16  4  1    2  7 18 28 30 21  9  3  0  
 10 35 62 65 42 17  5  1  0    6 23 42 50 40 21  8  2  0    2  6 12 16 16 10  5  2  0  
  8 23 37 36 21  8  2  1  0    5 16 25 26 18 10  4  1  0    1  4  7  8  7  5  3  1  0  
  2  7 12 10  6  3  1  0  0    2  5  8  7  5  3  1  0  0    0  2  2  3  2  1  1  0  0  
!Region 5: Section 7->9
  0  0  0  1  1  1  1  1  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  3  4  4  3  1  1    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  3  6  8  7  4  2  1    0  0  1  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  1  4  7  9  7  4  1  0    0  1  1  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  2  3  6  8  7  5  2  0    0  1  1  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  1  2  4  7  8  7  4  1  0    0  1  1  2  2  1  1  0  0    0  0  0  0  0  0  0  0  0  
  1  2  3  4  4  3  2  1  0    0  1  1  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  2  2  2  2  1  1  0    0  0  1  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  1  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 143.56   Thresh = 0.020   Blend = F   #Contributing = 46   InitialProfileWt = 0.079
Region 6
Sum = 110721;   Maximum = 1551.27;   FM = 0.803
!Region 6: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  1  3  3  2  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0    1  4  7  8  6  3  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    3  8 12 13 10  5  2  0  0  
  0  0  0  0  0  0  0  0  0    1  2  2  2  1  1  0  0  0    4 13 22 23 14  6  2  0  0  
  0  0  0  0  0  0  0  0  0    1  1  2  2  1  1  0  0  0    5 14 22 20 13  6  2  1  0  
  0  0  0  0  0  0  0  0  0    1  2  2  2  1  1  0  0  0    4 12 18 17 12  5  2  0  0  
  0  0  0  0  0  0  0  0  0    1  2  2  2  1  0  0  0  0    4 12 19 18 11  5  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    3  7 10  8  5  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    1  2  2  2  1  1  0  0  0  
!Region 6: Section 4->6
  1  3  6  7  7  5  2  1  0    2  5  8 11 11  9  7  4  1    1  3  6 10 11  9  7  4  1  
  3 11 21 26 24 15  7  1  0   11 26 43 53 48 30 15  6  1   11 23 37 46 41 24 12  5  1  
  7 22 36 43 37 21  8  1  0   16 44 75 96 88 54 23  6  1   13 37 68 92 88 56 25  7  1  
  9 27 45 50 40 25 11  4  0   11 34 59 83 84 66 32 12  2    7 24 54 90 98 74 35 12  2  
  9 27 46 52 42 25 10  3  0   14 38 68 89 83 56 26  9  1   12 32 61 81 74 47 22  8  1  
  9 25 41 46 36 18  7  1  0   15 43 77100 89 51 21  4  1   11 34 66 93 87 52 21  5  1  
  8 21 33 34 25 13  5  1  0    8 23 39 53 51 39 19  6  1    5 17 36 61 65 48 23  7  1  
  4 13 19 20 17 11  5  2  0    4 12 21 26 26 22 11  5  1    3  9 16 21 20 17  9  4  1  
  1  4  7  7  6  5  2  1  0    2  8 15 14 12  8  4  1  0    2  5  9  9  7  4  2  1  0  
!Region 6: Section 7->9
  1  1  3  4  5  5  3  2  0    0  1  1  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  2  7 13 18 18 11  5  2  1    1  2  3  3  3  2  1  1  0    0  0  0  0  0  0  0  0  0  
  3 11 22 32 32 23 10  3  1    1  3  5  6  5  4  2  1  0    0  1  1  1  0  0  0  0  0  
  2  9 22 37 40 30 13  4  1    1  3  5  6  5  4  2  1  0    0  1  1  1  0  0  0  0  0  
  3 12 24 33 30 18  8  3  1    1  4  5  6  5  3  2  1  0    0  1  1  1  0  0  0  0  0  
  3 11 21 29 28 18  7  2  0    1  3  5  6  5  3  1  1  0    0  1  1  1  0  0  0  0  0  
  2  7 16 26 27 19  7  2  0    1  2  4  5  4  3  1  1  0    0  0  1  1  0  0  0  0  0  
  1  5  9 12 12  8  4  2  0    1  2  3  4  3  2  1  0  0    0  0  0  0  0  0  0  0  0  
  1  2  3  4  3  2  1  1  0    0  1  1  2  1  1  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 92.34   Thresh = 0.020   Blend = F   #Contributing = 54   InitialProfileWt = 0.090
Region 7
Sum = 51142.9;   Maximum = 948.945;   FM = 0.811
!Region 7: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    1  2  2  2  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    2  5  7  5  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  0  0  0  0  0  0    2  7  9  7  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  0  0  0  0  0    3  7  9  7  4  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  0  0  0  0  0    2  5  7  6  4  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    1  3  4  4  3  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  2  3  3  2  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 7: Section 4->6
  4 10 13 12  6  2  1  0  0    5 14 22 22 13  6  2  0  0    2  7 13 17 14  7  3  1  0  
  8 22 33 28 15  6  2  0  0   10 30 49 50 36 19  7  1  0    5 16 29 38 36 25 11  2  0  
  9 27 40 35 22 10  3  1  0   11 36 62 71 58 35 13  3  0    5 20 42 61 63 45 20  5  1  
  8 25 38 37 26 14  5  1  0   10 32 63 85 81 51 19  4  1    5 18 45 80 94 68 28  7  1  
  5 16 29 34 28 15  6  1  0    5 21 52 84 86 55 22  5  1    3 14 42 83100 74 32  8  1  
  2  8 17 24 22 12  5  1  0    3 12 35 64 69 43 16  4  1    2  8 31 67 83 58 23  6  1  
  1  4 10 15 14  8  3  1  0    1  6 19 37 41 27 11  3  1    1  4 16 36 48 37 16  5  1  
  0  1  4  6  7  5  2  1  0    0  2  7 15 19 14  6  2  0    0  2  6 16 21 17  8  3  1  
  0  0  1  2  2  2  1  0  0    0  1  2  4  5  4  2  1  0    0  0  1  4  6  6  3  1  0  
!Region 7: Section 7->9
  1  2  5  7  7  4  2  0  0    0  1  1  2  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  2  5 10 15 16 13  6  2  0    1  2  3  4  3  2  1  0  0    0  0  1  1  1  0  0  0  0  
  2  7 16 25 28 22 11  3  1    1  3  4  5  5  3  2  1  0    0  1  1  1  1  0  0  0  0  
  2  7 17 33 43 34 15  4  1    1  3  5  6  6  4  2  1  0    0  1  1  1  1  0  0  0  0  
  2  6 17 35 46 38 17  5  1    1  3  4  6  6  5  2  1  0    0  1  1  1  1  0  0  0  0  
  1  4 13 30 40 31 14  4  1    1  2  4  5  5  4  2  1  0    0  1  1  1  0  0  0  0  0  
  1  2  7 16 24 21 10  3  1    1  1  2  3  3  3  2  1  0    0  0  1  0  0  0  0  0  0  
  0  1  3  7 10  9  5  2  1    0  1  1  1  2  1  1  1  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  3  4  2  1  0    0  0  0  0  0  1  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 54.84   Thresh = 0.020   Blend = F   #Contributing = 18   InitialProfileWt = 0.176
Region 8
Sum = 12728.2;   Maximum = 237.334;   FM = 0.767
!Region 8: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    4  9  9  4  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  0  0  0  0  0  0    8 22 22  9  2  0  1  1  0  
  0  0  0  0  0  0  0  0  0    1  1  1  0  0  0  0  0  0   10 28 28 12  2  0  1  0  0  
  0  0  0  0  0  0  0  0  0    1  2  2  1  0  0  0  0  0   11 27 26 11  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  2  1  1  1  0  0  0    8 21 21 10  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  0  0  0    6 14 14  7  3  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  0  0  0    3  7  7  4  2  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  0  0  0  0  0  0  0    1  4  4  2  1  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    1  1  1  0  0  0  0  0  0  
!Region 8: Section 4->6
  8 22 20  9  4  2  1  1  0    6 17 18 16 16 10  3  1  0    2  5 10 20 28 19  6  1  0  
 16 46 47 23 11  6  2  1  0   12 32 37 36 40 27  8  2  0    4 11 22 46 63 43 13  2  0  
 19 53 55 30 19 12  4  1  0   11 30 38 51 70 49 13  2  0    3 10 25 63 93 63 18  3  0  
 18 47 48 31 27 18  5  1  0    8 22 34 62 92 65 18  3  0    2  8 25 68100 68 19  3  0  
 13 35 37 30 31 21  6  1  0    5 14 26 62100 71 20  3  0    1  5 19 55 86 61 19  4  1  
  8 21 24 25 30 20  5  1  0    2  7 19 58 94 64 17  2  0    1  3 13 42 67 47 14  3  1  
  4  9 12 18 23 15  4  1  0    1  4 13 43 69 47 13  2  0    0  2  9 27 41 30 11  3  1  
  2  4  6  9 12  9  3  1  0    1  2  6 22 37 27  8  1  0    0  1  4 13 22 17  7  2  0  
  1  2  2  2  4  3  1  1  0    0  0  2  7 11  8  3  1  0    0  0  1  4  7  5  2  1  0  
!Region 8: Section 7->9
  0  1  4  9 13  9  3  0  0    0  1  1  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  1  3  9 21 30 21  6  1  0    1  2  2  2  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  1  4 11 28 40 27  8  2  0    1  2  2  2  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  1  3 11 27 38 26  8  2  1    1  2  2  1  1  1  1  1  0    1  1  0  0  0  0  0  0  0  
  1  2  7 18 27 19  7  2  1    1  2  2  1  0  0  0  0  0    0  1  0  0  0  0  0  0  0  
  1  2  4 10 16 11  5  2  1    1  1  1  0  0  0  0  1  0    0  0  0  0  0  0  0  0  0  
  0  1  3  5  7  6  3  2  1    0  1  1  0  0  0  0  1  0    0  0  0  0  0  0  0  0  0  
  0  1  1  2  3  3  2  1  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  1  1  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 28.46   Thresh = 0.020   Blend = F   #Contributing = 1   InitialProfileWt = 0.875
Region 9
Sum = 908.772;   Maximum = 13.5775;   FM = 0.552
!Region 9: Section 1->3
  0  1  0 -1 -1  0  0 -1  0    1  1  1  0  0  0 -1 -1  0    0  1  1  1  1  0  0  0  0  
  2  2  0 -2 -1 -1 -1 -1 -1    4  5  2 -1 -1 -1 -2 -2  0    4  7  6  2  1  0 -1  0  0  
  3  2  0 -2 -2 -1 -1  0  0    8 11  6  0 -1 -2 -2 -1  0   11 20 14  5  3 -1 -2  0  1  
  2  1  0 -1 -2 -1  0  1  1   10 17 14  4  0 -1 -1  1  1   19 36 31 13  6  0 -2  0  1  
  1  0 -1 -2 -2 -1  0  1  1   13 25 23  9  1 -1  0  2  1   26 57 55 24  6  0  0  1  0  
  0  0 -1 -1 -1 -1  0  0  0   13 29 29 12  2 -1  0  0 -1   28 65 68 30  8  1  0 -1 -1  
  1  1  0  0 -1 -1  0  0  0   10 26 31 16  4  0  0  0 -1   22 56 68 36 10  2  0 -2 -1  
  1  2  2  1  0 -1  0  1  0    8 23 32 18  4 -1  0  0  0   15 47 68 39  9  0 -1 -1  0  
  1  1  2  1  0  0  0  0  0    4 12 19 10  2 -1 -1  0  0    7 24 38 21  5  0 -1  0  0  
!Region 9: Section 4->6
  0  1  1  2  3  3  2  0  0    0  0  1  2  4  5  3  1  0    0  6 18 20  9  2  1  2  1  
  2  4  4  5  9 11  7  2  1    1  3  4  6 13 17 11  3  1    1 12 40 45 18  6  5  4  2  
  6 10  8  7 15 23 16  5  3    4  7  6  9 21 35 25  7  5    3 16 52 63 28 12  9  6  3  
  8 14 13 10 24 40 29  9  4    4  7  6  9 34 61 44 13  6    3 17 60 75 37 20 14  7  3  
  9 20 21 15 31 57 44 12  3    3  7  8 12 44 85 66 17  4    2 14 51 68 40 26 18  8  2  
 10 22 24 18 35 67 56 16  3    3  6  7 14 50100 84 24  4    2 11 34 50 39 29 20  7  2  
  8 18 23 18 33 66 57 15  1    2  3  5 12 46 99 86 23  2    2  8 24 34 29 27 19  6  1  
  5 14 22 17 23 48 43 11  1    1  2  5  9 31 72 65 17  2    1  6 13 18 17 18 13  3  0  
  2  7 13  8 10 18 17  6  1    0  1  3  3 13 27 26  9  1    0  2  4  5  6  7  5  2  0  
!Region 9: Section 7->9
  0  6 18 21  8  1  1  2  1    0  0  0  0  0  1  0  0  0    0  0  0  0  0  1  0  0  0  
  1 12 41 45 16  4  3  4  2    0  0  0 -1  0  3  1 -1 -1    0  0 -1 -1  0  1  0 -1  0  
  2 16 53 64 26  7  5  5  2    0  0  1  0  1  3  2  0  0    0  0 -1 -1  0  1  1  0  0  
  2 17 61 76 33 10  7  6  2    1  1  0  1  1  2  2  2  1    0  0 -1 -1  0  1  1  1  1  
  2 13 51 69 34 12  7  5  2    1  1  0  3  3  2  1  1  1    1  0 -1  0  1  1  1  1  0  
  2 11 34 51 32 12  5  3  1    0  0  2  5  5  1  0  1  0    0  0  0  2  2  0  0  0  0  
  1  8 24 34 23 10  4  1  0    0  0  2  5  4  1  0 -1 -1    0  0  1  2  1  0  0  0  0  
  1  5 13 18 13  6  2  0  0   -1 -1  1  3  3  2  1 -2 -2   -1  0  0  1  1  1  0 -1 -1  
  0  1  4  5  5  3  1  0  0   -1 -1  1  2  2  2  0 -1 -1   -1 -1  0  1  1  1  0  0  0  

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (354 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.500
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):         -0.0600
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  0.7107300,  0.0000089

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       354         0       354    2.1231    0.4313    19.271   110.967

Orientation ('UB') matrix:
  -0.0109673  -0.0356963   0.0857365
  -0.1293333  -0.0206423  -0.0340830
   0.0284189  -0.1077181  -0.0218805

         A         B         C     Alpha      Beta     Gamma           Vol
    7.7257    8.6700   10.8259    90.000   103.055    90.000        706.39
    0.0005    0.0006    0.0013     0.000     0.007     0.000          0.13
Corrected for goodness of fit:
    0.0007    0.0009    0.0018     0.000     0.010     0.000          0.17

Crystal system constraint:            3  (Monoclinic B-uniq)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):          -98.601     106.647      12.899
Goniometer zeros (deg):          0.0000*     0.0074      0.0000*     0.0120    (*=never refined)
Crystal translations (pixels):               0.0000      0.0000      0.0000

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.1738  -0.1784   0.0117  -0.1858  -0.0296  -0.1178

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        5.49808e+003  1.87460e+003    1.34       3         4       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 354             354             346
 Average input ESD (pix, pix, deg):          0.11668         0.11406         0.04345
 Goodness of fit:                            1.37193         1.64351         0.85360

Average missing volume:         0.131

Repeat orientation and spot-shape refinement ============= 04/16/2019 16:17:16

Current XYZ spot size:            0.472   0.472   1.487
Accurate-timing indicator is set in the frame headers:
   Velocity normalization will be computed for each frame
Pixel spacing (deg):              0.176
Profile X,Y,Z spacing (deg):      0.074   0.052   0.150
Profile convolver halfwidth:       1.61    1.61    1.51
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
    0_0001    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   15 0.47 0.47 1.49 1.000
    1_0002    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   15 0.47 0.47 1.49 1.000
    2_0003    7 -0.04 -0.03  0.04  0.25  0.04  0.25 8107.9  46   14  0.50   21 0.47 0.47 1.49 1.000
    3_0004   25 -0.01  0.04  0.02  0.20  0.14  0.13 2155.6  18   16  0.39   24 0.47 0.47 1.49 1.000
    4_0005   29  0.02  0.03 -0.00  0.13  0.11  0.10 2188.4  19    3  0.56   26 0.47 0.47 1.49 1.000
    5_0006   25  0.06  0.02 -0.05  0.13  0.08  0.10 2154.0  19    4  0.58   26 0.47 0.47 1.49 1.000
    6_0007   28 -0.03  0.03  0.02  0.18  0.20  0.18 1179.0  14   11  0.58   24 0.47 0.47 1.49 1.000
    7_0008   21 -0.03  0.02 -0.01  0.16  0.17  0.14 1191.7  12   14  0.59   24 0.47 0.47 1.49 1.000
    8_0009   20  0.04 -0.05  0.00  0.12  0.16  0.10 4406.7  25    0  0.74   29 0.47 0.47 1.49 1.000
    9_0010   27  0.04 -0.00 -0.03  0.18  0.10  0.13 3029.6  21   11  0.63   25 0.47 0.47 1.49 1.000
   10_0011   26  0.05  0.01 -0.04  0.21  0.12  0.17 1925.7  19    8  0.59   25 0.47 0.47 1.49 1.000
   11_0012   31 -0.01  0.02 -0.00  0.19  0.13  0.13 2276.6  19    6  0.66   26 0.47 0.47 1.49 1.000
   12_0013   23  0.01 -0.03  0.00  0.08  0.15  0.08 3610.9  25    0  0.67   25 0.47 0.47 1.49 1.000
   13_0014   22 -0.05  0.02 -0.01  0.31  0.42  0.15 2231.8  17   14  0.64   27 0.47 0.47 1.49 1.000
   14_0015   28  0.05 -0.03 -0.04  0.13  0.07  0.11 2811.1  22    4  0.64   25 0.47 0.47 1.49 1.000
   15_0016   30  0.01 -0.03  0.00  0.20  0.16  0.10 2419.6  18    0  0.66   25 0.47 0.47 1.49 1.000
Average BG >1K.  Output file and statistics will reflect <BG>/1000.
   16_0017   32 -0.04 -0.06  0.01  0.23  0.20  0.13 3763.8  23    3  0.68   25 0.47 0.47 1.49 1.000
   17_0018   34 -0.02 -0.01  0.01  0.16  0.25  0.17 3008.5  21    9  0.64   25 0.47 0.47 1.49 1.000
   18_0019   26 -0.05 -0.01  0.02  0.25  0.16  0.12 1945.3  17    8  0.69   25 0.47 0.47 1.49 1.000
   19_0020   24 -0.03  0.00  0.01  0.20  0.14  0.15 1524.7  15   17  0.59   23 0.47 0.47 1.49 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   20_0021   18  0.01 -0.05 -0.01  0.15  0.13  0.14 3345.9  16    0  0.68   26 0.47 0.47 1.49 1.000
   21_0022   25 -0.01 -0.01  0.02  0.12  0.08  0.12 2794.0  21    4  0.68   25 0.47 0.47 1.49 1.000

I/Sigma = 37.65   Thresh = 0.020   Blend = F   #Contributing = 164   InitialProfileWt = 0.069
Region 1
Sum = 8977.33;   Maximum = 101.164;   FM = 0.849
!Region 1: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0    1  3  6  7  5  4  3  1  0  
  0  0  0  0  0  0  0  0  0    0  1  3  4  3  1  1  0  0    2  8 15 16 13  9  6  3  1  
  0  0  0  0  0  0  0  0  0    1  3  5  6  5  2  1  1  0    5 16 29 31 24 16 10  5  1  
  0  0  0  0  0  0  0  0  0    1  3  7  8  5  2  1  0  0    6 19 36 39 28 18 10  5  1  
  0  0  0  0  0  0  0  0  0    1  3  6  7  5  2  1  0  0    4 15 29 31 21 13  7  4  1  
  0  0  0  0  0  0  0  0  0    1  3  6  7  5  2  1  0  0    5 16 29 31 24 15 10  5  1  
  0  0  0  0  0  0  0  0  0    1  3  5  7  5  2  1  0  0    5 15 29 32 24 16 10  4  1  
  0  0  0  0  0  0  0  0  0    0  2  3  4  3  1  0  0  0    3 10 18 20 14  8  5  2  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    1  3  6  6  4  2  2  1  0  
!Region 1: Section 4->6
  4  9 14 16 17 18 16  8  1    4 10 16 22 28 31 25 12  2    1  4  9 17 26 26 17  8  1  
  7 18 31 33 34 34 31 15  3    7 20 31 40 53 58 47 22  4    3  9 19 34 53 55 35 15  3  
  8 26 43 45 43 42 35 17  4    7 22 34 44 56 66 54 25  6    4 11 23 39 55 59 39 16  4  
  9 33 53 57 51 50 40 20  5    8 29 43 55 69 81 67 31  8    4 14 27 46 63 64 44 18  4  
 11 33 52 54 52 52 43 23  5   11 36 54 67 87100 78 38  8    5 17 34 59 90 90 57 24  4  
 13 34 58 61 61 58 50 25  4   12 35 57 70 91 99 78 37  7    5 17 32 54 82 84 53 22  4  
  9 27 46 50 48 44 38 18  3    7 23 37 46 57 63 53 23  5    3 11 20 34 47 49 33 13  3  
  4 16 26 27 24 22 19 10  2    4 14 20 23 29 35 30 14  3    2  7 12 21 30 31 21  8  2  
  2  6  9  9  9 10  9  5  1    2  6 10 12 16 20 19  9  2    1  3  6 10 14 15 12  6  1  
!Region 1: Section 7->9
  1  2  6 10 15 13  8  4  1    0  1  1  2  2  2  1  1  0    0  0  0  0  0  0  0  0  0  
  1  4 10 18 28 25 15  7  1    0  1  2  3  3  3  2  1  0    0  0  0  0  0  0  0  0  0  
  1  4 10 18 24 22 13  6  1    0  2  3  3  3  2  1  1  0    0  0  0  0  0  0  0  0  0  
  1  5 12 21 28 24 14  6  1    0  2  4  4  4  3  2  1  0    0  0  1  0  0  0  0  0  0  
  2  6 16 29 44 38 22  9  2    1  2  4  5  6  5  3  1  0    0  0  1  0  0  0  0  0  0  
  2  7 15 27 40 36 20  9  2    1  2  3  4  5  4  2  1  0    0  0  0  0  0  0  0  0  0  
  1  4 10 16 22 20 11  5  1    0  2  3  3  3  2  1  1  0    0  0  0  0  0  0  0  0  0  
  1  3  6 11 15 13  8  3  1    0  1  2  2  2  2  1  0  0    0  0  0  0  0  0  0  0  0  
  0  1  3  4  6  5  3  2  0    0  1  1  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 0.00   Thresh = 0.020   Blend = F   #Contributing = 0   InitialProfileWt = 1.000
Region 2
Sum = 1.02298;   Maximum = 0.0181812;   FM = 0.79
!Region 2: Section 1->3
  0  0  1  1  0  0  0  0  0    0  0  3  3  1  0  0  0  0    0  2  5  5  2  1  1  0  0  
  0  0  2  2  0  0  0  0  0    0  1  8  9  3  1  0  0  0    0  3 12 12  5  2  1  0  0  
  0  0  3  3  0  0  0  0  0    0  3 14 14  5  1  0  0  0    0  7 21 19  8  4  2  1  0  
  0  0  3  3  0 -1  0  0  0    0  4 18 18  6  1  0  0  0    0  8 28 26 11  5  2  0  0  
  0  0  2  2  0 -1  0  0  0    0  5 21 20  7  1  0  0  0    0 11 36 32 13  4  1  0  0  
  0  0  1  0  0  0  0  0  0    0  6 21 18  7  1  0  0  0    0 11 38 33 13  5  2  0  0  
  0  0  1  0  0  0  0  0  0    0  4 17 18  7  1  0  0  0    0  8 31 32 14  5  2  1  0  
  0  0  1  0  0  0  0  0  0    0  3 15 17  7  1  0  0  0    0  6 27 30 14  3  1  0  0  
  0  0  1  0  0  0  0  0  0    0  1  8  9  4  1  0  0  0    0  1 13 16  7  2  0  0  0  
!Region 2: Section 4->6
  0  2  5  5  4  5  4  1  0    0  1  2  6 14 20 11  2  0    0  0  2 10 18 17  7  1  0  
  1  4 11 12 11 13 10  2  0    1  2  6 15 33 48 30  6  0    0  1  8 27 40 39 21  4  0  
  1  6 16 17 16 23 21  6  0    1  3  8 23 50 76 53 12  0    0  2 15 44 60 59 34  7  0  
  1  8 20 20 20 32 29  7  0    1  4 12 31 66 96 69 16  1    0  3 19 55 76 70 39  9  0  
  1  9 22 21 22 37 37 10  0    1  5 14 37 74100 74 19  1    0  3 18 56 80 70 36  9  0  
  1  8 21 21 23 39 39 10  0    1  5 14 38 70 90 66 16  1    0  3 15 46 70 58 27  6  0  
  1  5 15 17 20 34 36 10  0    1  3 11 31 53 67 54 14  0    0  2 12 35 50 38 17  4  0  
  0  3 11 14 14 22 25  7  0    0  1  7 22 34 40 35 10  0    0  1  7 22 30 21  8  2  0  
  0  1  5  7  6  9  7  1  0    0  1  3 10 14 16 11  2  0    0  1  3  8 11  8  3  1  0  
!Region 2: Section 7->9
  0  0  1  6  7  3  1  0  0    0  0  0  0  0  0  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  5 17 15  6  2  1  0    0  0 -1 -1 -1  1  2  1  0    0  0  0 -1 -1  0  0  0  0  
  0  1 10 26 22  8  3  1  0    0  0 -1 -1 -1  0  1  1  0    0  0  0 -1 -1  0  0  0  0  
  0  2 12 32 27 10  3  1  0    0  0 -1 -1  0  1  1  0  0    0  0 -1 -1  0  0  0  0  0  
  0  1 10 28 28 13  4  1  0    0  0 -1  0  2  2  1  0  0    0  0  0  0  1  1  0  0  0  
  0  1  8 21 23 12  4  1  0    0  0  0  2  3  2  0  0  0    0  0  0  0  1  1  0  0  0  
  0  1  6 15 15  8  2  0  0    0  0  0  2  3  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  1  3  8  9  4  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  1  2  3  1  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 15.96   Thresh = 0.020   Blend = F   #Contributing = 3   InitialProfileWt = 0.670
Region 3
Sum = 1593.6;   Maximum = 42.9079;   FM = 0.726
!Region 3: Section 1->3
  0  0  1  2  0  0  0  0  0    0  1  4  5  1  0  0  0  0    0  2  7  6  2  0  0  0  0  
  0  0  3  4  1  0  0  0  0    0  2 11 13  5  1  1  0  0    0  3 14 14  5  2  1  0  0  
  0  1  4  5  2  0  0  0  0    0  2 15 17  6  1  1  0  0    0  5 18 18  7  3  2  1  0  
  0  1  4  5  1  0  0  0  0    0  3 15 17  6  1  1  0  0    0  5 19 18  7  3  2  0  0  
  0  1  3  4  1  0  0  0  0    0  2 12 13  4  1  0  0  0    0  5 17 14  5  3  2  0  0  
  0  1  2  2  1  0  0  0  0    0  2  7  6  2  0  0  0  0    0  4 12  9  3  2  1  0  0  
  0  0  1  1  1  0  0  0  0    0  1  3  2  0  0  0  0  0    0  2  6  5  2  1  1  0  0  
  0  0  0 -1  0  0  0  0  0    0  0  1  0  0  1  0  0  0    0  1  3  2  1  1  0  0  0  
  0  0  0 -1  0  0  0  0  0    0  0  0 -1 -1  1  0  0  0    0  0  1  1  0  0  0  0  0  
!Region 3: Section 4->6
  0  2  6  4  3  2  1  0  0    0  0  1  5 15 22 11  1  0    0  0  0  3 12 19  9  1  0  
  0  3 11 10  6  7  4  1  0    0  0  3 11 35 54 31  5  0    0  0  1  8 28 44 26  4  0  
  0  5 15 14 10 12  9  2  0    0  1  4 20 56 86 53  9  0    0  0  2 16 45 69 42  7  0  
  0  5 16 15 12 14 10  2  0    0  1  7 29 74100 62 13  0    0  0  4 24 61 79 48 10  0  
  0  5 15 14 12 14  9  2  0    0  1  8 37 81 94 52 11  0    0  0  6 31 67 74 39  8  0  
  0  4 12 11 10 11  6  1  0    0  1  9 39 75 73 35  6  0    0  1  7 32 61 57 26  5  0  
  0  2  6  8  8  7  3  1  0    0  1  8 33 57 46 20  4  0    0  1  7 28 47 36 15  3  0  
  0  1  4  5  6  4  1  0  0    0  0  5 24 36 25  9  1  0    0  0  4 20 30 19  6  1  0  
  0  0  1  3  2  1  0  0  0    0  0  2 11 15  9  3  0  0    0  0  2  9 12  7  2  0  0  
!Region 3: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  1  1  0  0    0  0 -1  0  0  0  0  0  0    0  0 -1  0  0 -1  0  0  0  
  0  0  0  0  0  1  1  0  0    0  0 -1  0 -1  0  0  0  0    0  0 -1  0 -1  0  0  0  0  
  0  0  1  2  1  1  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0 -1  0  0  0  0  0  
  0  0  0  2  3  1  1  0  0    0  0  0  0  1  1  1  0  0    0  0  0  0  0  1  0  0  0  
  0  0  1  3  3  1  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  1  3  3  1  0  0  0    0  0  0  1  2  1  0  0  0    0  0 -1  0  1  1  0  0  0  
  0  0  1  2  2  0 -1  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0 -1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 23.47   Thresh = 0.020   Blend = F   #Contributing = 11   InitialProfileWt = 0.393
Region 4
Sum = 3270.42;   Maximum = 52.1331;   FM = 0.833
!Region 4: Section 1->3
  0  0  0  0  0  0  0  0  0    0  2  5  4  1  1  0  0  0    0  3  8  7  3  2  1  0  0  
  0  0  0  1  1  0  0  0  0    0  3  9 10  5  1  0  0  0    0  7 18 18  9  5  3  1  0  
  0  0  0  1  1  0  0  0  0    0  5 13 13  7  2  1  0  0    0 11 29 27 14  9  5  1  0  
  0  0  1  1  0  0  0  0  0    0  6 16 14  6  2  0  0  0    1 15 37 32 15  8  5  1  0  
  0  0  0  0  0  0  1  0  0    0  6 15 14  5  2  1  0  0    1 16 39 33 14  7  3  1  0  
  0  0  1  1  0  0  1  0  0    0  5 13 11  4  1  1  0  0    1 14 33 26 10  5  3  1  0  
  0  0  1  1  0  0  0  0  0    0  4  8  8  3  1  1  0  0    0  9 22 18  7  3  2  1  0  
  0  0  0  0  0  0  0  0  0    0  1  3  4  2  1  0  0  0    0  4 10  9  4  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  1  3  2  1  1  0  0  0  
!Region 4: Section 4->6
  0  3  6  6  8  8  4  1  0    0  2  3  7 13 14  7  1  0    0  0  2  6  9  9  5  1  0  
  0  6 14 18 27 33 19  4  0    0  3  7 19 44 56 31  7  0    0  1  5 16 31 34 19  5  0  
  1 11 25 29 38 53 37  9  0    1  5 14 31 69 92 57 14  1    0  1  9 28 56 61 32  8  1  
  1 17 39 37 39 49 37 12  0    1  9 22 42 81 99 62 17  1    0  2 13 43 79 79 40 10  1  
  2 23 49 41 34 38 27  8  0    2 14 30 49 84 92 53 14  1    0  3 17 56100 90 41 10  1  
  2 26 52 38 25 25 17  5  0    2 18 36 48 73 73 38  9  1    0  4 19 59100 86 36  7  0  
  2 24 45 30 17 14  9  3  0    3 18 33 39 53 48 22  5  0    0  4 17 50 82 63 23  4  0  
  2 15 29 20 10  6  3  1  0    2 11 21 24 30 24 10  2  0    0  2  9 30 53 40 13  2  0  
  0  3  8  6  3  2  2  1  0    0  2  5  7  8  7  3  1  0    0  0  2  8 15 12  4  1  0  
!Region 4: Section 7->9
  0  0  1  2  2  2  1  0  0    0  0  1  1  0  0  0  0  0    0  0  0  1  0  0  0  0  0  
  0  1  3  6  8  6  3  1  0    0  0  1  1  0  0  0  0  0    0  0  0  1  0  0  0  0  0  
  0  1  4 11 15 14  7  2  0    0  0  1  1  0  0  0  0  0    0  0  0  1  0  0  0  0  0  
  0  1  6 17 24 21 10  2  0    0  0  1  1  1  1  1  0  0    0  0  0  1  0  0  0  0  0  
  0  1  8 24 36 28 12  3  0    0  0  1  1  1  1  1  0  0    0  0  0  1  0  0 -1  0  0  
  0  1  9 27 40 30 12  2  0    0  1  1  2  1  1  0  0  0    0  0  1  0  0  0 -1  0  0  
  0  1  8 25 36 24  8  1  0    0  1  1  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  5 16 27 18  5  0  0    0  1  1  0  0  0  0 -1  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4  8  6  2  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 70.31   Thresh = 0.020   Blend = F   #Contributing = 39   InitialProfileWt = 0.103
Region 5
Sum = 26868.1;   Maximum = 458.887;   FM = 0.874
!Region 5: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  1  2  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    1  2  5  6  5  4  2  1  0  
  0  0  0  0  0  0  0  0  0    0  1  2  2  1  0  0  0  0    1  5  9 10  8  5  2  1  0  
  0  0  0  0  0  0  0  0  0    0  2  3  3  1  1  0  0  0    1  7 15 16 11  7  3  1  0  
  0  0  0  0  0  0  0  0  0    1  3  5  5  2  1  0  0  0    2 12 23 23 13  6  2  1  0  
  0  0  0  0  0  0  0  0  0    0  2  4  4  2  1  0  0  0    1 11 21 20 11  4  2  1  0  
  0  0  0  0  0  0  0  0  0    0  2  3  3  1  1  0  0  0    1  9 18 17  9  3  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  2  2  1  0  0  0  0    1  5 11 10  5  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  0  0  0  0  0  0    0  1  3  3  2  1  0  0  0  
!Region 5: Section 4->6
  0  1  2  4  8  9  7  2  0    0  1  2  4 11 16 13  4  1    0  0  1  3  7 10  9  4  1  
  0  2  8 16 28 29 17  6  1    0  2  8 22 45 53 36 14  2    0  1  4 11 24 31 24 10  2  
  1  6 17 32 45 43 24  8  1    1  5 18 44 76 85 55 19  3    0  2  7 22 46 58 41 15  3  
  1 10 28 45 57 50 27  8  1    1  9 28 59 95 95 57 18  2    1  3 13 34 65 71 46 15  2  
  3 19 45 61 60 45 22  7  1    2 17 44 75100 92 52 17  2    1  6 17 38 68 73 46 15  2  
  2 22 49 55 45 30 15  5  1    3 24 52 69 76 65 36 11  1    1  8 20 36 56 56 34 10  1  
  2 19 45 50 36 19  8  3  0    3 22 47 58 53 38 19  6  1    2  9 18 27 34 31 18  6  1  
  2 17 34 33 20  9  4  1  0    3 20 38 40 30 19  9  3  0    1  7 13 17 18 15  8  3  0  
  1  6 11 10  8  4  2  0  0    1  9 15 14 11  7  3  1  0    1  4  7  7  7  5  2  0  0  
!Region 5: Section 7->9
  0  0  0  1  2  3  3  2  1    0  0  0  0  0  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  3  7  9  8  4  1    0  0  0  1  1  1  1  1  0    0  0  0  0  0  0  0  0  0  
  0  1  2  7 14 19 15  7  1    0  0  1  1  2  3  2  1  0    0  0  0  0  0  0  0  0  0  
  0  1  4 12 23 27 19  7  1    0  1  1  3  4  4  3  1  0    0  0  0  0  0  0  0  0  0  
  0  1  5 13 23 26 18  7  1    0  1  2  3  4  4  3  1  0    0  0  0  0  0  0  0  0  0  
  0  2  6 12 20 23 15  5  1    0  1  2  3  4  4  3  1  0    0  0  0  0  0  0  0  0  0  
  0  2  6  9 13 12  8  3  0    0  1  2  3  3  2  1  0  0    0  0  0  0  0  0  0  0  0  
  0  2  3  5  6  6  4  1  0    0  1  1  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  1  2  2  3  2  1  0  0    0  0  1  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 93.16   Thresh = 0.020   Blend = F   #Contributing = 25   InitialProfileWt = 0.154
Region 6
Sum = 57520.4;   Maximum = 894.236;   FM = 0.878
!Region 6: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  1  3  4  4  3  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    1  3  7 10 11  8  4  1  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  0  0  0    1  4 11 18 21 16  7  3  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0    2  7 17 26 26 18  7  2  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0    2  9 19 25 22 15  6  2  0  
  0  0  0  0  0  0  0  0  0    0  1  2  2  1  1  0  0  0    2  6 15 22 22 17  8  3  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    2  7 15 22 22 15  7  2  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    1  4  9 12 10  7  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  1  3  3  4  3  1  1  0  
!Region 6: Section 4->6
  1  4  8 11 12 13 10  4  0    0  3  6 10 14 17 13  6  0    0  1  2  6 11 13  9  3  0  
  2 11 27 42 45 38 21  9  0    1 10 27 46 52 47 29 13  1    0  3  9 18 26 26 16  6  1  
  2 12 37 61 71 57 29 10  1    1 13 35 59 70 62 34 13  2    1  5 13 27 36 38 23  7  1  
  4 18 44 66 69 55 29 11  1    2 14 35 53 61 56 34 13  2    1  6 17 38 54 53 30  7  1  
  5 23 56 88 91 70 33 12  1    2 18 51 88100 83 43 17  1    1  7 20 38 48 44 25  9  1  
  3 18 47 74 84 69 36 12  1    2 17 48 77 89 76 41 14  2    1  6 16 28 35 32 18  4  0  
  3 13 36 54 55 42 22  8  1    1 12 31 45 45 36 20  7  1    1  5 13 25 31 26 11 -2 -1  
  2  9 22 34 37 29 13  5  0    1  7 17 30 36 31 16  5  1    1  2  6 14 17 16  8  1  0  
  1  4  9 13 16 13  7  2  0    1  4 10 14 17 15  8  3  0    0  1  3  4  5  6  4  1  0  
!Region 6: Section 7->9
  0  1  2  3  6  8  6  2  0    0  0  1  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  2  5 10 15 16  9  3  0    0  1  2  2  3  2  1  0  0    0  0  0  0  0  0  0  0  0  
  0  4  8 16 20 22 12  1  0    0  2  3  4  4  3  2  0  0    0  0  1  1  0  0  0  0  0  
  0  3 10 23 34 34 19  3  0    0  1  3  5  5  4  2  0  0    0  0  1  1  1  0  0  0  0  
  1  4 10 22 31 31 18  6  1    0  1  3  4  5  5  3  1  0    0  0  1  1  1  0  0  0  0  
  1  4  8 13 16 15  8  1  0    0  1  3  4  4  3  2  0  0    0  0  1  1  0  0  0  0  0  
  0  0  2 10 15 14  3 -6 -2    0  1  1  2  2  2  0 -1  0    0  0  0  1  0  0  0  0  0  
  0  0  0  6 10 11  5 -1  0    0  0  1  1  2  2  1  0  0    0  0  0  0  0  0  0  0  0  
  0  1  1  2  3  4  3  1  0    0  0  1  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 90.04   Thresh = 0.020   Blend = F   #Contributing = 50   InitialProfileWt = 0.103
Region 7
Sum = 41086.6;   Maximum = 726.716;   FM = 0.919
!Region 7: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  2  4  4  3  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  5 13 14  9  4  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    0  7 17 20 14  7  2  1  0  
  0  0  0  0  0  0  0  0  0    0  1  2  2  1  1  0  0  0    0  8 21 23 16  9  4  1  0  
  0  0  0  0  0  0  0  0  0    0  1  2  2  1  1  0  0  0    0  6 17 22 18 10  3  1  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0    0  4 11 15 14  9  3  1  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  2  6 10  9  5  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  1  2  4  5  4  2  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  1  0  0  
!Region 7: Section 4->6
  0  5 12 12  8  4  1  0  0    1  5 12 14 10  4  1  0  0    0  1  4  8  7  4  1  0  0  
  1 12 32 38 27 13  4  1  0    1 10 27 37 33 21  9  2  0    1  4 11 18 23 20 10  3  0  
  1 16 43 56 46 27 11  3  0    1 14 39 59 59 45 23  7  1    1  6 19 34 42 39 24  9  2  
  1 18 51 67 59 39 17  4  0    2 14 43 74 88 73 36 10  1    1  5 19 43 68 67 38 13  2  
  1 13 41 65 67 48 21  6  0    1 11 38 76100 88 47 13  1    0  5 20 47 74 79 50 16  3  
  1  8 27 48 58 44 20  5  0    0  6 27 63 94 83 42 12  1    0  3 15 43 75 76 43 15  2  
  0  4 16 33 41 31 14  4  0    0  3 15 40 64 59 31  9  1    0  1  8 24 48 54 33 11  2  
  0  1  6 14 21 18  8  2  0    0  1  6 19 32 31 18  6  1    0  1  4 13 24 27 18  7  1  
  0  0  2  4  6  5  3  1  0    0  0  2  5 10 11  6  2  0    0  0  1  3  9 11  7  2  0  
!Region 7: Section 7->9
  0  1  2  2  3  2  1  0  0    0  0  1  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  2  4  7  8  7  4  1  0    0  1  2  2  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  2  6 11 14 14  9  3  1    0  1  2  3  3  2  1  0  0    0  0  0  1  1  0  0  0  0  
  0  2  7 15 22 22 13  5  1    0  1  3  4  4  2  1  0  0    0  0  1  1  1  0  0  0  0  
  0  2  7 15 24 27 18  6  1    0  1  3  4  4  3  1  0  0    0  0  1  1  1  0  0  0  0  
  0  2  6 14 24 26 15  6  1    0  1  3  3  3  2  1  0  0    0  0  1  1  1  0  0  0  0  
  0  1  4  9 16 19 12  4  1    0  1  2  3  2  2  1  0  0    0  0  1  1  0  0  0  0  0  
  0  1  2  5  8  9  6  3  1    0  0  1  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  1  3  4  2  1  0    0  0  0  1  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 51.60   Thresh = 0.020   Blend = F   #Contributing = 20   InitialProfileWt = 0.135
Region 8
Sum = 10831.8;   Maximum = 236.968;   FM = 0.828
!Region 8: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  1  4  3  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  0  0  0  0  0    0  8 19 13  3  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  2  1  0  0  0  0  0    1 14 32 22  6  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  2  3  2  0  0  0  0  0    1 15 36 25  7  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  2  4  3  1  0  0  0  0    1 14 30 21  7  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  3  2  1  1  0  0  0    1  9 21 16  6  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  2  2  1  1  1  0  0    1  6 13 11  5  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  0  0  0  0  0    0  3  6  5  3  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  1  2  2  1  0  0  0  0  
!Region 8: Section 4->6
  0  3  7  5  2  1  1  0  0    0  2  5  5  6  6  3  1  0    0  0  1  3  8  8  3  1  0  
  1 15 34 23 11  7  3  1  0    1 10 21 22 28 27 12  2  0    0  2  6 16 35 35 16  3  0  
  1 23 51 38 23 17  8  2  0    1 12 27 34 55 56 26  6  0    0  2  9 29 64 66 30  6  0  
  1 22 49 41 33 30 14  3  0    1  9 22 39 79 87 40  8  1    0  2  8 33 79 83 37  7  1  
  1 16 38 35 38 38 18  4  0    0  5 15 37 89100 47 10  1    0  1  6 28 71 77 36  8  1  
  1 10 24 28 39 40 19  4  0    0  3  9 32 82 95 47 10  1    0  1  4 19 50 58 29  7  1  
  1  6 14 20 33 34 16  3  0    0  1  5 26 68 75 36  8  0    0  0  2 13 33 37 19  5  0  
  0  2  5  9 17 18  9  2  0    0  0  2 12 34 39 20  5  0    0  0  1  6 14 17 10  3  0  
  0  1  2  3  4  4  2  0  0    0  0  0  2  6  9  5  1  0    0  0  0  1  3  5  3  1  0  
!Region 8: Section 7->9
  0  0  0  1  3  3  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  2  6 12 12  5  1  0    0  0  1  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  3 11 23 23 10  2  0    0  0  1  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  3 12 25 25 11  2  0    0  1  1  1  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  3  9 20 20  9  2  0    0  1  1  1  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4 11 12  6  2  0    0  0  1  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  5  5  3  1  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  2  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 25.36   Thresh = 0.020   Blend = F   #Contributing = 1   InitialProfileWt = 0.875
Region 9
Sum = 703.32;   Maximum = 10.7064;   FM = 0.603
!Region 9: Section 1->3
  0  0  0 -1 -1 -1  0  0  0    0  0  0  0 -1  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0 -2 -3 -2 -1  0  0    0  0  1  0 -1 -1 -1  0  0    0  0  2  4  2  1  0  0  0  
  0  0  0 -2 -3 -2 -1  0  0    0  3 10  5  0  0 -2 -1  0    0  5 16 11  5  2 -1 -1  0  
  0  0  0 -1 -3 -2  0  0  0    0  4 19 16  5  1 -1 -1  0    0  8 33 29 13  5 -1 -1  0  
  0  0 -2 -2 -2 -1  0  0  0    0  9 34 29  9  1  0  0  0    0 16 61 54 20  3 -1  0  0  
  0  0 -1 -2 -1 -1 -1  0  0    0 12 43 38 14  2 -1  0  0    0 19 75 68 25  5  1  0  0  
  0  0  1  0  0 -1 -1  0  0    0  9 40 42 18  3  0  0  0    0 15 68 72 30  7  2  0  0  
  0  1  2  2  1  0  0  0  0    0  9 41 46 20  3  0  0  0    0 13 65 74 32  5  1  0  0  
  0  1  2  2  1  0  0  0  0    0  2 21 26 11  2  0  0  0    0  3 32 42 17  4  0  0  0  
!Region 9: Section 4->6
  0  0  0  1  3  5  5  2  0    0  0  0  3  6  6  5  2  0    0  0  2 17 21  6  0  0  0  
  0  0  2  6  9 17 14  2  0    0  0  3 11 15 20 16  3  0    0  0 14 52 45 12  1  0  0  
  0  2  7  9 14 30 32  8  0    0  1  7 16 22 36 38 10  0    0  3 31 82 68 22  5  2  0  
  0  4 12 13 20 50 51 11  0    0  3 10 18 28 60 61 13  0    0  4 38 98 81 31  9  2  0  
  0  6 20 20 26 65 76 19  0    0  4 11 19 33 79 90 22  0    0  4 31 84 76 35 14  3  0  
  0  7 22 24 30 74 85 21  0    0  3  9 16 35 88100 25  0    0  4 21 55 60 35 14  3  0  
  0  5 18 22 28 70 85 22  0    0  2  6 12 29 83100 25  0    0  3 16 37 39 25 11  3  0  
  0  3 16 23 22 48 63 18  0    0  0  4 10 19 56 74 21  0    0  2  8 18 21 14  7  2  0  
  0  0  8 13 10 19 16  1  0    0  0  2  5  8 22 19  2  0    0  1  3  5  6  5  2  0  0  
!Region 9: Section 7->9
  0  0  1 13 16  5  0  0  0    0  0 -1 -2 -2  1  2  0  0    0  0  0 -1 -1  0  1  0  0  
  0  0 11 41 35  9  1  0  0    0  0 -1 -4 -3  2  4  1  0    0  0  0 -1 -1  1  1  0  0  
  0  2 25 66 54 16  3  1  0    0  0 -1 -3 -2  1  3  1  0    0  0  0 -1 -1  0  1  0  0  
  0  3 30 78 65 22  4  1  0    0  0 -2 -3 -1  1  2  0  0    0  0 -1 -1 -1  0  1  0  0  
  0  2 24 67 61 24  5  1  0    0 -1 -3 -1  2  2  1  0  0    0  0 -1  0  1  1  0  0  0  
  0  2 17 45 49 23  5  1  0    0 -1 -1  2  5  2 -1 -1  0    0  0  0  1  2  1  0  0  0  
  0  2 12 30 31 16  3  0  0    0  0  0  2  3  1  0 -1  0    0  0  0  1  1  0  0  0  0  
  0  1  7 15 16  8  1  0  0    0  0  0  1  2  2  1  0  0    0  0  0  0  1  1  0  0  0  
  0  1  2  4  5  3  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  0  1  0  0  0  

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (313 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.500
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):         -0.0600
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  0.7107300,  0.0000089

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       313         0       313    2.0044    0.4312    20.424   110.999

Orientation ('UB') matrix:
  -0.0109623  -0.0357032   0.0857397
  -0.1293617  -0.0206374  -0.0340903
   0.0284118  -0.1077395  -0.0218828

         A         B         C     Alpha      Beta     Gamma           Vol
    7.7245    8.6684   10.8256    90.000   103.063    90.000        706.11
    0.0006    0.0008    0.0015     0.000     0.008     0.000          0.14
Corrected for goodness of fit:
    0.0007    0.0009    0.0017     0.000     0.010     0.000          0.17

Crystal system constraint:            3  (Monoclinic B-uniq)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):          -98.596     106.648      12.894
Goniometer zeros (deg):          0.0000*     0.0132      0.0000*     0.0155    (*=never refined)
Crystal translations (pixels):               0.0000      0.0000      0.0000

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.1643  -0.1941   0.0106  -0.1910  -0.0361  -0.1367

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        1.38323e+003  1.26285e+003    1.17       4         4       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 313             313             306
 Average input ESD (pix, pix, deg):          0.11165         0.11149         0.04371
 Goodness of fit:                            1.29116         1.29519         0.84014


Old XYZ spot size:              0.472   0.472   1.487
New XYZ spot size:              1.858   2.732   2.040
Average missing volume:         0.163
% with too much missing I:      6.875
Fractional overlap in H,K,L:    0.000   0.000   0.000

End of pass 2.  Repeating shape determination...

Repeat orientation and spot-shape refinement ============= 04/16/2019 16:17:16

Current XYZ spot size:            1.858   2.732   2.040
Accurate-timing indicator is set in the frame headers:
   Velocity normalization will be computed for each frame
Pixel spacing (deg):              0.176
Profile X,Y,Z spacing (deg):      0.240   0.247   0.187
Profile convolver halfwidth:       1.00    1.00    1.21
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
    0_0001    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   17 0.00 0.00 0.00 1.000
    1_0002    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   17 0.00 0.00 0.00 1.000
    2_0003    1  0.05  0.02 -0.03  0.05  0.02  0.03  39727 131    0  0.68   23 4.29 3.93 4.41 1.000
    3_0004   27 -0.01  0.04  0.04  0.17  0.16  0.15 3934.6  27   11  0.43   27 2.42 3.01 2.56 1.000
    4_0005   32  0.02  0.01  0.02  0.15  0.18  0.13 3919.7  26    6  0.74   29 2.21 3.00 2.34 1.000
    5_0006   28  0.01  0.05 -0.00  0.20  0.20  0.09 5335.4  30    0  0.74   28 2.23 3.02 2.34 1.000
    6_0007   25 -0.00 -0.03  0.03  0.18  0.20  0.16 1504.8  15   12  0.74   28 2.17 2.90 2.28 1.000
    7_0008   21  0.00  0.05  0.00  0.14  0.11  0.14 4038.2  23    5  0.73   28 2.16 2.88 2.26 1.000
    8_0009   23  0.08  0.04 -0.02  0.21  0.17  0.09 5829.2  29    4  0.82   33 2.19 3.02 2.30 1.000
    9_0010   27 -0.01  0.02 -0.01  0.15  0.13  0.14 3851.6  24   15  0.74   28 2.22 3.02 2.33 1.000
   10_0011   25  0.07  0.01 -0.05  0.14  0.13  0.10 4012.4  27    4  0.76   30 2.23 3.05 2.32 1.000
   11_0012   29  0.00  0.03  0.03  0.15  0.13  0.10 7091.9  33    3  0.79   30 2.22 3.05 2.32 1.000
   12_0013   23  0.04  0.01  0.03  0.10  0.13  0.07 5167.4  32    0  0.77   30 2.23 3.06 2.35 1.000
   13_0014   24  0.07 -0.00  0.00  0.17  0.17  0.12 5040.2  27    4  0.77   31 2.25 3.16 2.36 1.000
   14_0015   28  0.03  0.01  0.00  0.12  0.11  0.11 5189.8  30    4  0.76   28 2.26 3.18 2.35 1.000
   15_0016   30 -0.01  0.02  0.02  0.23  0.22  0.12 3917.7  25    0  0.74   29 2.25 3.17 2.36 1.000
   16_0017   31 -0.00 -0.02  0.00  0.19  0.19  0.13 6820.8  36    0  0.78   29 2.25 3.15 2.37 1.000
   17_0018   31  0.02  0.10  0.00  0.23  0.25  0.13 3852.5  24   10  0.74   29 2.26 3.14 2.37 1.000
   18_0019   25 -0.03  0.10  0.06  0.16  0.28  0.15 2130.1  17    8  0.79   29 2.24 3.12 2.34 1.000
   19_0020   25 -0.01 -0.02 -0.00  0.11  0.07  0.11 2897.7  21   16  0.72   26 2.24 3.11 2.34 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   20_0021   19 -0.01 -0.06  0.02  0.09  0.17  0.08 5347.1  23    5  0.77   30 2.24 3.12 2.34 1.000
   21_0022   28 -0.01  0.01  0.01  0.18  0.21  0.14 5158.8  29    4  0.79   29 2.25 3.13 2.35 1.000

I/Sigma = 30.41   Thresh = 0.020   Blend = F   #Contributing = 171   InitialProfileWt = 0.079
Region 1
Sum = 13405.2;   Maximum = 856.12;   FM = 0.867
!Region 1: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  0  0  0    0  1  2  9 10  3  1  0  0  
  0  0  0  0  0  0  0  0  0    1  2  2  3  3  1  1  0  0    0  2  5 21 23  6  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  0  0  0    0  1  2  8 10  3  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  3  2  1  0  0    0  0  1  3  4  4  1  0  0    0  0  1  2  4  3  1  0  0  
  0  1  6 22 28 20  4  0  0    0  1  7 24 44 40  7  0  0    0  1  3 13 36 23  3  1  0  
  0  1 12 53 62 41  7  1  0    0  1 15 57100 85 13  1  0    0  1  6 28 81 50  6  1  0  
  0  1  5 22 26 17  3  0  0    0  1  7 23 39 34  6  1  0    0  1  3 12 31 19  3  1  0  
  0  0  1  3  3  2  1  0  0    0  1  2  4  5  4  1  0  0    0  0  2  3  4  2  1  0  0  
  0  0  1  1  0  0  0  0  0    0  0  1  1  1  1  0  0  0    0  0  1  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  2  5 11  6  2  1  0    0  1  1  2  1  1  1  1  0    0  0  0  1  0  0  0  0  0  
  0  1  3 10 23 12  3  1  0    0  0  2  3  2  1  1  1  1    0  0  0  1  0  0  0  0  0  
  0  1  2  6 10  5  2  1  0    0  0  1  2  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  3  3  1  0  0  0    0  0  1  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  1  1  0  0  0  0    0  0  0  1  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 0.00   Thresh = 0.020   Blend = F   #Contributing = 0   InitialProfileWt = 1.000
Region 2
Sum = 1.08101;   Maximum = 0.0744499;   FM = 0.745
!Region 2: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0 -1  0  0 -1 -1  0  
  0  0 -1  0  0 -1  0  0  0    0  0  0  1  0 -1  0 -1  0    0  0  0 -1  1  0  0  0  0  
  0  0 -1  0 -1 -1  0 -1  0    0  0 -1  0  0 -1  0  0  0    0  1  1  1  0 -1  0  1  0  
  0  0  0  2  0 -1  0  1  0    0  0  1  6  4  0  0  0  0    0  1  3 14  7  0  1  1  0  
  0  1  2  3  0 -1  0  0  0    0  2  4 12  6  0  0  0  0    0  3 14 51 25  2  0  1  0  
  0  1  1  1  1  0 -1 -1  0    0  2  2  3  2  0 -1 -1  0    0  1  6 23 16  0  0  0  0  
  0  0  0  0  1  0  1  0  0    0  1  0  1  1  0  0  0  0    0  0  1  1  2  1  0 -1  0  
  0  0  0  0  2  0  2  0  0    0  0  0  1  2  0  2  0  0    0  1  1  1  0  1  0  1  0  
  0  0  0  0  0  0  0  0  0    0  0 -1  1  0  0  1  0  0    0  0  0  0  0  1  0  0  0  
!Region 2: Section 4->6
  0  0  0 -1  1 -1  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  1  0  0  
  0 -1  0 -1  1  0  1  1  0    0  0  0  0  0  0  1  1  0    0 -1  0  1  1  0  1  1  0  
  0 -1  1  2  2  1  1  1  0    0  0  1  2  3  3  0  0  0    0  1  1  3  5  2  0  1  0  
  0  1 11 19 11  9  3  1  0    0  1  7  8 31 41  5  1  0    0  1  0 11 39 25  5  3  0  
  0  3 33 50 27 36  7  1  0    0  3 15 21 85100 12  1  1    0  1  1 24 89 42  6  1  0  
  0  2 15 18 14 19  4  1  0    1  4  5  9 32 37  6  1  1    0  2  1 10 26  9  3  0  0  
  0  2  3  2  3  3  1  0  0    0  3  2  3  5  3  1  1  0    0  1  1  4  4  1  1  0  0  
  0  1  1  1  1  1  0  0  0    0  1  2  2  2  1  0  0  0    0  1  1  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 2: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0 -1  0 -1 -1  0  0  0    0  0  0  0  0  0  0  0  0  
  0 -1  0  0  1  0  0  0  0    0  0  0  1  0 -1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  2  2  2  0  0  1  0    0  0  1  1  1  0 -1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  5 11  3  1  1  0    0 -1  1  0  1  1 -1  0  0    0 -1  0  0  0  0  0  0  0  
  0  1  1  9 22  6  2  1  0    0  0  2  1  2  1  0  2  0    0  0  0  0  0  0  0  1  0  
  0  0  1  5  8  2  1  0  0    0  1  1  2  2  2 -1 -1  0    0  1  0  0  0  0  0  1  0  
  0  0  1  2  2  0  0  0  0    0  0  2  2  1 -1 -1  0  0    0  1  0  0  0  0  0  0  0  
  0 -1  0  0  0  0  0  1  0    0 -1 -1 -1  0  0  1 -1  0    0  0  0  0  0  0  0 -1  0  
  0  0  0  0  0  0  1  1  0    0  0 -1  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 15.74   Thresh = 0.020   Blend = F   #Contributing = 3   InitialProfileWt = 0.670
Region 3
Sum = 3247.64;   Maximum = 288.596;   FM = 0.66
!Region 3: Section 1->3
  0  1  0  0  0  0  0  0  0    0  0  1  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0 -1  0  1  0  0  0  0    0  0  0  1  1 -1 -1 -1  0    0  0  0  1  1  0  0  0  0  
  0 -1 -1  0 -1 -1 -1 -1  0    0  0 -1  1 -1 -1  0 -1  0    0  1  0  2  1  0  1  0  0  
  0  0  1  2  0 -1 -1  0  0    0 -1  1  8  6  1  0  0  0    0  0  4 16  9  2  1  0  0  
  0  1  2  2  0  0  0  0  0    0  2  3 11  7  1 -1  0  0    0  2 14 30 11  2  0  0  0  
  0  0  0  0  0  0 -1  0  0    1  2  2  1  0  0  0  0  0    0  2  8  7  1  0  0  0  0  
  0  0 -1  0  1  0  0  0  0    0  1  0  1  0  0  0 -1  0    0  0  2  2  1  0  0 -1  0  
  0  0  0  0  1  0  0  0  0    0  1  0  2  1 -1  0  0  0    0  0  0  1  1 -1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  1  0  0  0  0  0  
!Region 3: Section 4->6
  0  0  0 -1  0 -1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0 -1 -1  0  1  1  1  1  0    0  0  0  1  0  0  1  1  0    0  0  0  1  0  0  1  1  0  
  0 -1 -1  2  3  1  2  1  0    0  1  1  1  3  4  0  1  0    0  1  1  1  3  2  1  0  0  
  1  2 11 22  8  4  3  2  0    0  1  1  4 37 50  5  2  0    0  0  0  2 26 33  3  2  0  
  0  2 40 52 11  7  2  1  0    0  2  5 15100 77  6  1  0    0  2  1  9 69 49  5  1  0  
  0  2 20 15  4  2  1  0  0    1  4  1  7 32 12  2  1  0    0  2  0  6 22  8  2  1  0  
  0  1  3  2  2  1  1  0  0    0  2  1  3  5  1  1  1  0    0  1  1  2  3  1  1  1  0  
  0  0  0  0  1  0  0  0  0    0  1  1  3  2  1  1  0  0    0  0  1  2  1  0  1  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  1  0  0  0  0  0  
!Region 3: Section 7->9
  0  0 -1  0  0  0  0  0  0    0  0 -1  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0 -1  0  1  0  0  0  0    0 -1 -1  0  0 -2  0  0  0    0  0  0  0  0 -1  0 -1  0  
  0  1  2  1  1 -1  1  1  0    0  0  0  1  1 -1 -1  1  0    0 -1  0  0  1 -1  0  1  0  
  0  0  1  2  2  0  0  1  0    0 -1  0 -1  0  0 -1  1  0    0 -1  0 -1 -1  0  0  0  0  
  0  1  1  2  4  1  1  1  0    0  0  2  0  0  1  0  2  1    0  0  0 -1  0  0  0  1  0  
  0  0  1  3  4  1  1  1  0    0  2  1  1  1  1  0  1  1    0  1  0  0  0  1  0  1  0  
  0  0  0  0  1  1  1  0  0    1  0  0  0  0 -1  0 -1  0    0  1  0  0  0 -1  0  0  0  
  0 -1  0  0  0 -1  0  2  0    0  0 -1  0  0 -1  1 -1  0    0  0 -1 -1  0  0  0 -1  0  
  0  0  0  0  0  0  1  1  0    0  0  0  0  0  0  1 -1  0    0  0  0  0  0  0  0 -1  0  

I/Sigma = 17.78   Thresh = 0.020   Blend = F   #Contributing = 13   InitialProfileWt = 0.344
Region 4
Sum = 6110.57;   Maximum = 482.754;   FM = 0.761
!Region 4: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  1  1  0    0  0  1  0  0  1  0  0  0  
  0  1  1  1  0  0  1  0  0    0  1  0  0  0  0  1  1  0    0  1  1  0  0  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  1  1  0  0  1  0  0  
  0  0  0 -1  1  0  1  1  0    0  0  0  1  1  0  0  1  0    0  1  2 12  6  1  0  1  0  
  0  0  0 -1  0  0  0  1  0    0  1  1  2  1  0  0  0  0    0  1  5 31 14  1  0  0  0  
  0  1  0  0 -1  1  0  0  0    0  1  1  1  0  0  0  0  0    0  2  5 10  4  1 -1  0  0  
  0  1  0  1  0  0  1  0  0    0  1 -1  0  0  0  1  1  0    0  0  1  2  2  0  0  1  0  
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  1  0  0  0    0 -1  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 4: Section 4->6
  0  1  1  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  0  1  0  0  0  
  0  1  1  0  0  1  0  1  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  1  1  2  3  1  1  1    1  0  1  1  2  3  1  1  1    0 -1  0  1  1  1  0  0  0  
  0  0  3 16 25 19  1  0  0    0  0  2  8 47 40  2  1  0    0  0  1  5 24 15  3  0  0  
  0  0 13 60 43 23  2  1  0    0  1 10 39100 62  3  2  0    0  1  2 18 95 39  2  0  0  
  0  1 14 41 14  5  1  0  0    0  1 11 32 32 14  2  1  0    0  1  2 10 44 14  1  0  0  
  0  0  1  6  4  2  0  0  0    0  0  1  5  5  4  0  0  0    0  0  1  2  4  2  0  0  0  
  0  0  0  1  1  1  0  1  0    0  0  0  1  2  1  0  1  0    0  0  0  0  1  1  1  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 4: Section 7->9
  0  0  0  0  0  1  0  0  0    0  0  0  0  0  0  1  0  0    0  0  0  0  0  0  1  0  0  
  0  0  0  1  1  1  0  0  0    1  1 -1  0  0  0 -1 -1 -1    0  0  0  0  0  0  0  0  0  
  0  0  1  0  0  1  0  0  0    0  0  0  0  0  1  0  0  0    0  0 -1  0  1  0 -1  0  0  
  0  0  1  2  3  2  2  1  0    0  0  1  0  0 -1  1  2  1   -1 -1  0 -1  0 -1  0  1  1  
  0  1  1  5 17  6  2  0  0    0  0  0  1  0  0  1  1  0    0 -2 -1  0  0 -1  0  0  1  
  0  1  1  4 11  3  0  0  0    0  0  0  1  1  0 -1 -1  0    0 -1 -1  0  1  0 -1 -1  0  
  0  0  0  1  2  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0 -1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0 -1  0  0  0    0  0  0  0  0  0  0 -1 -1  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0 -1  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 113.25   Thresh = 0.020   Blend = F   #Contributing = 40   InitialProfileWt = 0.103
Region 5
Sum = 95761.4;   Maximum = 15189.5;   FM = 0.71
!Region 5: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  1  4  4  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  3  3  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  1  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 5: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  4 12  4  0  0  0    0  0  0  6 35 15  1  0  0    0  0  0  2 23 12  1  0  0  
  0  0  1 22 46  9  0  0  0    0  0  1 29100 28  1  0  0    0  0  0  9 53 20  1  0  0  
  0  0  1 14 21  3  0  0  0    0  0  1 16 29  6  0  0  0    0  0  0  4 10  3  0  0  0  
  0  0  0  2  1  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 5: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  1  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  3  2  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  7  3  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 160.54   Thresh = 0.020   Blend = F   #Contributing = 40   InitialProfileWt = 0.079
Region 6
Sum = 168094;   Maximum = 23976.7;   FM = 0.743
!Region 6: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  2  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  6  9  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  3  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 6: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  1  7 16  5  0  0  0    0  0  1 13 35 13  1  0  0    0  0  0  5 20 10  1  0  0  
  0  0  1 21 47 12  1  0  0    0  0  2 33100 34  2  0  0    0  0  1 14 52 20  1  0  0  
  0  0  1  7 15  4  0  0  0    0  0  1 11 33 12  1  0  0    0  0  0  5 16  6  1  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 6: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  3  2  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4  9  4  1  0  0    0  0  0  2  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  4  2  1  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 81.31   Thresh = 0.020   Blend = F   #Contributing = 52   InitialProfileWt = 0.118
Region 7
Sum = 54631.5;   Maximum = 6657.7;   FM = 0.753
!Region 7: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  0  0  0  0  0  0    0  0  1  1  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  5  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  1  8 10  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 7: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  1  0  0  0  0    0  0  0  1  2  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  2 20 25  4  0  0  0    0  0  1 18 34 10  0  0  0    0  0  1  7 19  9  0  0  0  
  0  0  2 31 61 15  1  0  0    0  0  1 27100 41  1  0  0    0  0  1 12 64 35  2  0  0  
  0  0  0  5 19  7  0  0  0    0  0  0  6 35 18  1  0  0    0  0  0  3 23 15  2  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 7: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  4  2  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  3  8  4  1  0  0    0  0  1  2  3  1  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  1  3  2  1  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 41.21   Thresh = 0.020   Blend = F   #Contributing = 18   InitialProfileWt = 0.201
Region 8
Sum = 17645.9;   Maximum = 1711.1;   FM = 0.762
!Region 8: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  0  0  0  0  0  0    0  1  2  2  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  0  1  0  0  0  0    0  0  4 13  6  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  0  3 21 10  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  1  5  4  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 8: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  0  0  0  0  0  
  0  0  1  6  3  1  0  0  0    0  0  2  6  3  1  0  0  0    0  0  1  2  3  1  0  0  0  
  0  0  6 44 21  4  1  0  0    0  0  5 29 38 17  1  0  0    0  1  2  6 37 20  1  0  0  
  0  0  6 50 42 14  1  0  0    0  1  4 21100 55  2  0  0    0  1  2  7 68 37  2  0  0  
  0  0  1  9 18  9  1  0  0    0  1  1  4 44 27  1  0  0    0  0  0  2 15 12  1  0  0  
  0  0  1  0  1  1  1  0  0    0  0  1  1  2  2  0  0  0    0  0  1  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 8: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  1  2  0  0  0  0    0  0  0  1  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  1  3  6  3  1  0  0    0  0  1  2  1  0  1  0  0    0  0  0  1  0  0  0  0  0  
  0  0  1  3  7  5  2  1  0    0  0  1  2  1  0  1  1  0    0  0  0  1  0  0  0  0  0  
  0  0  1  1  1  2  2  1  0    0  1  1  1  1  0  1  2  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  1  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 23.75   Thresh = 0.020   Blend = F   #Contributing = 1   InitialProfileWt = 0.875
Region 9
Sum = 1309.5;   Maximum = 97.6155;   FM = 0.614
!Region 9: Section 1->3
  0  0  0  0 -1  0  0  0  0    0  0  0  0 -1 -1  0  0  0    0  0  0 -2  0  0 -1 -1  0  
  0  0 -1  0 -1 -2  0 -1  0    0  0 -1  0 -1 -2  0 -1  0    0  1  1 -3  0 -1 -2  1  0  
  0  0 -1 -1  1  0  0  0  0    0  1 -1 -1  1 -1  0  0  0    0  1  3 -1 -1 -2 -1  2  0  
  0  0  0  1  0 -1  0  2  0    0  0  0  2  1 -1  0  0  0    1  2  2  8  2 -2  0  1 -1  
  0  2  2  4  0 -2 -1 -1  0    0  2  3 11  3 -2 -1 -1  0    0  3 11 70 35 -1  0  1 -1  
  0  1  1  2  2 -1 -1 -2  0    0  1  2  6  5 -1 -2 -2  0    0  0  1 41 32  0 -1  1  0  
  0  1  1  1  0 -1  0  0  0    0  1  1  1  1 -1  1  0  0    0  0  0  0  4  2  0 -1  0  
  0 -1 -1  0  2  1  4  1  0    0 -1 -1  0  2  2  5  1  0    0  1  1  0  0  3 -1  2  0  
  0 -1 -1  0  0  0  1  0  0    0 -1 -1  0  0  1  1  0  0    0  1 -1  0 -1  3  1  0  0  
!Region 9: Section 4->6
  0  0  0 -1  1  0  0  0  0    0  0  0 -1  1 -1  0  1  0    0  0  1  0  0  0  1  0  0  
  0  0  1 -1  0  0  0  1  0    0  0  1  0  0  0  1  1  0    0 -2  0  1  2 -1  0  1  0  
  0 -1  2  1  0 -1 -1  0  0    0 -2  2  2  1  0 -1  0  0    0  1  1  5  6  0  0  1  0  
  0  1  8  6  5  9  2  0  0   -1  1 12  6  8 15  2  0  0    0  1  0 19 43  6  6  3  0  
  0  3 17 28 28 62 10  1  0    0  3 23 12 29100 16  2  1    0  1  0 34 86 15  6  0  0  
  1  3  6 14 20 37  6  1  1    1  4  9  3 17 59 11  2  1    0  2  2 11 20  5  5 -1 -1  
  0  2  2  1  3  3  0  0  0    1  3  3  2  3  4  0  0  0    0  0  2  6  5 -1  1 -2 -1  
  0  2  1  1  1  1 -1  0  0    0  2  1  1  1  1 -1 -1  0    0  2  0 -2  0 -2  0 -1  0  
  0  1  0  0  0  1  1  0  0    1  0  0  0  0  0  1  0  0    0  1 -1 -1 -1 -1  1  0  0  
!Region 9: Section 7->9
  0  0  0  0 -1  0  1  0  0    0  0 -1 -1 -2 -1  0  0  0    0  0  0  0  0  0  0  0  0  
  0 -1  0  1  1 -1  0  1  0    0  0  1  1  1 -1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  2  3  3  0 -1  0  0   -1 -1  3  2  2  1 -2  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  9 19  4  2  1  0    0  0  3  0  1  3 -2  0  1    0  0  0  0  0  0  0  0  0  
  0  0  0 15 39  8  2  0  0    0 -1  1  1  4  2 -1  1  0    0  0  0  0  0  0  0  0  0  
  0  1  2  6 10  3  1 -2 -1    0 -1  1  2  3  2 -3 -3 -1    0  0  0  0  0  0  0  0  0  
  0  0  3  4  3  0 -1 -1  0    0 -1  5  3  2  0 -2  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0 -2  0  0  0 -1  0    0 -2 -1 -1  0  2  1 -1  0    0  0  0  0  0  0  0  0  0  
  0  0 -1 -1  0  0  0  0  0    0 -1 -2 -1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (338 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.500
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):         -0.0600
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  0.7107300,  0.0000089

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       338         0       338    2.1223    0.4311    19.278   111.028

Orientation ('UB') matrix:
  -0.0110004  -0.0357114   0.0857407
  -0.1293817  -0.0206286  -0.0341150
   0.0284128  -0.1077617  -0.0218832

         A         B         C     Alpha      Beta     Gamma           Vol
    7.7231    8.6667   10.8244    90.000   103.062    90.000        705.77
    0.0008    0.0008    0.0019     0.000     0.010     0.000          0.19
Corrected for goodness of fit:
    0.0007    0.0007    0.0016     0.000     0.008     0.000          0.16

Crystal system constraint:            3  (Monoclinic B-uniq)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):          -98.611     106.646      12.892
Goniometer zeros (deg):          0.0000*     0.0184      0.0000*     0.0225    (*=never refined)
Crystal translations (pixels):               0.0000      0.0000      0.0000

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.1931  -0.1979   0.0116  -0.1792  -0.0391  -0.1075

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        7.36734e+002  6.48505e+002    0.81       2         4       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 338             338             337
 Average input ESD (pix, pix, deg):          0.22438         0.23436         0.05915
 Goodness of fit:                            0.72106         0.94316         0.71463


Old XYZ spot size:              1.858   2.732   2.040
New XYZ spot size:              1.818   2.673   1.998
Average missing volume:         0.094
% with too much missing I:      6.608
Fractional overlap in H,K,L:    0.000   0.000   0.000

Integration ============================= 04/16/2019 16:17:17

Unsorted reflections will be written to D:\frames\guest\DK_Zucker2\work\unsorted.raw
Spatially corrected beam center:          386.44  506.71
Input monochromator 2Th, roll (deg):        0.00    0.00
Input spot-size bias:              1.000
Unbiased XYZ spot size (deg):      1.818   2.673   1.998
Spot size used (deg):              1.818   2.673   1.998
Scale for orientation update length:     1.00000
#Frames running average for orientation update:       24
Frames between full refinements of orientation:       50
N, where every Nth strong spot included in LS:         1

LS profile fitting will be used
   to worst resolution of 9999.000 A
   up to I/sigma(I) of       8.000
   unweighted fit

Accurate-timing indicator is set in the frame headers:
   Velocity normalization will be computed for each frame
Pixel spacing (deg):              0.176
Profile X,Y,Z spacing (deg):      0.235   0.242   0.184
Profile convolver halfwidth:       1.00    1.00    1.23
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
    0_0001    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   16 0.00 0.00 0.00 1.000
    1_0002    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   16 0.00 0.00 0.00 1.000
    2_0003    4  0.00 -0.01 -0.07  0.01  0.02  0.08  15738  97    0  0.71   23 3.08 2.38 3.58 1.000
    3_0004   30 -0.01  0.03  0.02  0.17  0.17  0.15 2590.6  25   13  0.74   27 2.19 2.01 2.39 1.000
    4_0005   38 -0.01  0.00 -0.01  0.16  0.16  0.13 2618.9  23    8  0.74   28 1.96 1.96 2.12 1.000
    5_0006   34 -0.07 -0.03  0.02  0.31  0.28  0.14 2871.1  25    3  0.74   28 1.94 1.99 2.09 1.000
    6_0007   32 -0.00  0.01  0.01  0.17  0.20  0.14 1503.1  16    9  0.71   27 1.88 1.93 2.03 1.000
    7_0008   25 -0.08  0.10  0.01  0.24  0.23  0.15 2000.1  19    4  0.73   28 1.86 1.93 2.01 1.000
    8_0009   28  0.12 -0.00 -0.03  0.28  0.13  0.08 3447.7  34    0  0.80   33 1.87 2.01 2.05 1.000
    9_0010   34 -0.03 -0.06 -0.02  0.19  0.35  0.15 2650.0  23    6  0.70   28 1.92 2.06 2.08 1.000
   10_0011   30  0.03 -0.08 -0.02  0.11  0.44  0.16 3796.0  29    7  0.73   29 1.93 2.05 2.08 1.000
   11_0012   38 -0.03  0.01  0.01  0.18  0.15  0.12 3706.3  32    3  0.79   30 1.91 2.04 2.08 1.000
   12_0013   27 -0.02 -0.00  0.06  0.16  0.13  0.13 4103.2  37    4  0.76   29 1.91 2.03 2.09 1.000
   13_0014   28  0.05 -0.01 -0.01  0.17  0.18  0.12 1514.4  18    4  0.76   31 1.93 2.08 2.10 1.000
   14_0015   33 -0.02 -0.03  0.00  0.11  0.13  0.10 3638.3  29    3  0.76   27 1.95 2.11 2.09 1.000
   15_0016   35 -0.13  0.23  0.04  0.56  1.02  0.21 2175.4  23    3  0.76   29 1.95 2.11 2.09 1.000
   16_0017   37 -0.01 -0.03 -0.01  0.20  0.17  0.13 3676.4  33    0  0.77   28 1.95 2.09 2.11 1.000
   17_0018   37 -0.06  0.12  0.03  0.23  0.39  0.14 2313.8  20    8  0.74   29 1.95 2.09 2.10 1.000
   18_0019   32 -0.00  0.03  0.03  0.29  0.37  0.15 1754.6  18    9  0.78   28 1.95 2.09 2.08 1.000
   19_0020   27 -0.02 -0.03 -0.02  0.11  0.08  0.11 2221.9  20   11  0.71   26 1.95 2.08 2.08 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   20_0021   22  0.05 -0.05 -0.05  0.21  0.16  0.17 2059.1  21    9  0.76   30 1.95 2.08 2.08 1.000
   21_0022   31 -0.01 -0.04  0.00  0.23  0.20  0.16 3143.5  27    6  0.77   29 1.94 2.08 2.09 1.000
   22_0023   33  0.05 -0.07 -0.00  0.20  0.36  0.13 1944.0  20    3  0.73   27 1.93 2.06 2.08 1.000
   23_0024   35 -0.02  0.06  0.02  0.21  0.25  0.12 2412.4  22    3  0.75   27 1.94 2.07 2.09 1.000
   24_0025   29 -0.12 -0.16  0.02  0.63  0.74  0.14 3115.3  32    0  0.80   29 1.94 2.08 2.10 1.000
   25_0026   39 -0.01  0.00  0.00  0.10  0.20  0.10 3377.6  28    5  0.78   29 1.94 2.08 2.09 1.000
   26_0027   35  0.07 -0.01  0.02  0.32  0.44  0.17 2432.1  25   11  0.77   32 1.95 2.09 2.09 1.000
   27_0028   35 -0.05  0.04  0.02  0.23  0.18  0.14 2169.4  24   11  0.75   30 1.95 2.10 2.09 1.000
   28_0029   39  0.03 -0.02 -0.01  0.19  0.17  0.11 3706.5  31    3  0.78   30 1.94 2.10 2.09 1.000
   29_0030   40 -0.01 -0.06 -0.01  0.16  0.23  0.12 2624.0  25    8  0.77   29 1.95 2.10 2.10 1.000
   30_0031   29  0.03 -0.03 -0.02  0.22  0.09  0.13 1840.0  19    3  0.76   27 1.94 2.09 2.09 1.000
   31_0032   34 -0.06 -0.01  0.00  0.25  0.30  0.13 2941.4  27    3  0.72   27 1.94 2.08 2.09 1.000
   32_0033   28 -0.14  0.14  0.07  0.64  0.96  0.18 3442.8  35    4  0.80   29 1.95 2.08 2.10 1.000
   33_0034   28 -0.05 -0.04  0.05  0.26  0.16  0.13 3003.0  25    7  0.75   26 1.95 2.08 2.10 1.000
   34_0035   34 -0.02 -0.11 -0.00  0.24  0.41  0.12 3163.0  27    6  0.77   30 1.96 2.08 2.10 1.000
   35_0036   28  0.04 -0.04 -0.04  0.19  0.14  0.15 1383.5  15    7  0.74   27 1.95 2.08 2.09 1.000
   36_0037   22 -0.07  0.00  0.05  0.19  0.23  0.13 2118.6  21    9  0.77   29 1.95 2.07 2.09 1.000
   37_0038   35 -0.06 -0.02  0.02  0.16  0.25  0.12 1715.4  18    3  0.76   28 1.94 2.06 2.08 1.000
   38_0039   34  0.07 -0.06 -0.00  0.28  0.25  0.19 2030.2  22    6  0.76   30 1.93 2.06 2.08 1.000
   39_0040   38  0.01 -0.04 -0.01  0.14  0.21  0.11 1906.8  18    5  0.76   30 1.93 2.06 2.08 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   40_0041   31  0.06 -0.03  0.01  0.42  0.20  0.13 2626.8  25   10  0.76   29 1.93 2.07 2.08 1.000
   41_0042   33 -0.04 -0.07 -0.01  0.29  0.26  0.15 2066.2  23    6  0.77   29 1.93 2.07 2.08 1.000
   42_0043   28 -0.01 -0.05  0.01  0.13  0.23  0.11 3757.4  29    4  0.78   29 1.94 2.08 2.08 1.000
   43_0044   28 -0.03 -0.06 -0.01  0.18  0.14  0.12 4058.0  31   11  0.71   27 1.94 2.08 2.08 1.000
   44_0045   38 -0.01 -0.09  0.05  0.13  0.39  0.15 2656.8  26    3  0.75   27 1.94 2.08 2.08 1.000
   45_0046   33  0.05 -0.06 -0.03  0.20  0.18  0.12 3297.8  28    6  0.76   28 1.94 2.07 2.08 1.000
   46_0047   27  0.01 -0.00  0.01  0.18  0.11  0.11 3996.4  35    4  0.79   29 1.94 2.08 2.09 1.000
   47_0048   36 -0.00 -0.11  0.00  0.15  0.22  0.11 2769.2  26    0  0.78   28 1.94 2.08 2.09 1.000
   48_0049   31 -0.01 -0.06  0.04  0.16  0.13  0.12 2299.0  27    3  0.82   30 1.94 2.09 2.10 1.000
   49_0050   35  0.02 -0.03  0.02  0.17  0.24  0.10 2766.9  26    9  0.81   30 1.94 2.09 2.10 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.500
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):         -0.0600
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  0.7107300,  0.0000089

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.5637    0.4306    15.935   111.222

Orientation ('UB') matrix:
  -0.0110138  -0.0357077   0.0857829
  -0.1294089  -0.0205967  -0.0341000
   0.0283868  -0.1077498  -0.0219096

         A         B         C     Alpha      Beta     Gamma           Vol
    7.7212    8.6681   10.8191    90.000   103.041    90.000        705.42
    0.0005    0.0007    0.0013     0.000     0.006     0.000          0.13
Corrected for goodness of fit:
    0.0005    0.0008    0.0014     0.000     0.006     0.000          0.14

Crystal system constraint:            3  (Monoclinic B-uniq)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):          -98.612     106.648      12.878
Goniometer zeros (deg):          0.0000*     0.0193      0.0000*     0.0307    (*=never refined)
Crystal translations (pixels):               0.0000      0.0000      0.0000

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.2188  -0.2359   0.0112  -0.1967  -0.0296  -0.1252

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        1.91787e+003  1.71058e+003    1.06       3         4       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             507
 Average input ESD (pix, pix, deg):          0.23116         0.24115         0.05693
 Goodness of fit:                            1.07468         1.23175         0.82184

No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   50_0051   43  0.01 -0.05 -0.01  0.17  0.20  0.12 2297.5  22    9  0.75   28 1.94 2.09 2.10 1.000
   51_0052   38  0.01 -0.05 -0.02  0.16  0.16  0.13 2778.1  29   11  0.74   31 1.94 2.10 2.10 1.000
   52_0053   33 -0.01 -0.09 -0.04  0.15  0.15  0.12 1806.3  20    3  0.77   29 1.94 2.09 2.09 1.000
   53_0054   28  0.07  0.00  0.01  0.28  0.29  0.16 1805.5  19    0  0.78   31 1.94 2.09 2.09 1.000
   54_0055   24 -0.11 -0.10  0.05  0.32  0.28  0.13 1854.6  20    4  0.75   27 1.94 2.09 2.08 1.000
   55_0056   31  0.04 -0.03 -0.02  0.21  0.25  0.12 2954.4  28    6  0.76   28 1.94 2.09 2.09 1.000
   56_0057   37 -0.03 -0.05  0.02  0.16  0.10  0.10 2915.1  27   14  0.71   27 1.94 2.08 2.09 1.000
   57_0058   28 -0.03 -0.12  0.01  0.23  0.30  0.12 3300.4  31    4  0.80   29 1.93 2.08 2.09 1.000
   58_0059   37  0.05 -0.09 -0.01  0.15  0.15  0.11 3499.1  35    5  0.77   28 1.94 2.09 2.09 1.000
   59_0060   35  0.02 -0.02 -0.04  0.27  0.40  0.16 1956.9  24    6  0.83   32 1.94 2.10 2.09 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   60_0061   23 -0.02 -0.02 -0.01  0.13  0.12  0.16 1710.7  18    0  0.78   26 1.94 2.09 2.09 1.000
   61_0062   35  0.02  0.01 -0.03  0.16  0.31  0.11 2939.3  23    3  0.77   28 1.94 2.09 2.08 1.000
   62_0063   34 -0.02 -0.02  0.02  0.17  0.40  0.17 1637.4  17    6  0.78   28 1.94 2.09 2.08 1.000
   63_0064   38  0.03 -0.06 -0.02  0.20  0.16  0.14 2912.2  26    5  0.78   29 1.94 2.09 2.08 1.000
   64_0065   40  0.02 -0.07 -0.04  0.18  0.21  0.12 2459.5  25    5  0.78   29 1.93 2.08 2.08 1.000
   65_0066   33 -0.01 -0.00  0.00  0.23  0.25  0.14 2846.5  27    3  0.77   29 1.94 2.09 2.08 1.000
   66_0067   29 -0.01 -0.08  0.00  0.14  0.16  0.09 3680.2  29    3  0.77   27 1.94 2.09 2.08 1.000
   67_0068   35 -0.13  0.15  0.06  0.62  1.02  0.20 3041.5  28    6  0.77   27 1.94 2.09 2.08 1.000
   68_0069   31 -0.01 -0.03 -0.01  0.27  0.38  0.18 2145.7  22    0  0.78   29 1.94 2.08 2.08 1.000
   69_0070   31 -0.05 -0.04  0.01  0.19  0.18  0.11 2581.2  25    0  0.81   29 1.94 2.08 2.08 1.000
   70_0071   29 -0.04 -0.11  0.04  0.14  0.27  0.13 3575.7  34    3  0.79   28 1.94 2.08 2.08 1.000
   71_0072   35 -0.03 -0.07 -0.01  0.18  0.35  0.12 3698.0  32    6  0.80   29 1.94 2.09 2.08 1.000
   72_0073   32 -0.00 -0.10  0.01  0.19  0.18  0.13 3830.6  32    6  0.78   29 1.94 2.09 2.09 1.000
   73_0074   35 -0.03  0.01  0.05  0.18  0.26  0.15 1808.3  20   11  0.73   28 1.94 2.09 2.09 1.000
   74_0075   35  0.01 -0.07  0.00  0.16  0.18  0.12 2085.2  21    6  0.78   29 1.94 2.09 2.08 1.000
   75_0076   45  0.01  0.00  0.02  0.15  0.80  0.19 2350.1  23    2  0.78   29 1.94 2.09 2.08 1.000
   76_0077   32 -0.04 -0.11 -0.02  0.19  0.18  0.12 2666.9  25    3  0.80   28 1.94 2.09 2.08 1.000
   77_0078   27  0.09 -0.16 -0.04  0.20  0.29  0.15 3298.4  30    0  0.83   29 1.94 2.09 2.08 1.000
   78_0079   27  0.01 -0.00  0.04  0.23  0.15  0.14 3806.3  35    4  0.80   28 1.94 2.10 2.08 1.000
   79_0080   25 -0.01 -0.06  0.02  0.14  0.13  0.15 2343.6  23    8  0.76   28 1.94 2.10 2.08 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   80_0081   37 -0.05 -0.02  0.04  0.30  1.13  0.28 2769.5  26    5  0.78   29 1.95 2.10 2.08 1.000
   81_0082   30 -0.04 -0.42  0.01  0.81  1.84  0.32 3332.6  27    7  0.76   26 1.95 2.10 2.08 1.000
   82_0083   41  0.02 -0.04 -0.01  0.15  0.18  0.12 2956.9  29   10  0.74   29 1.96 2.11 2.09 1.000
   83_0084   30 -0.01 -0.03 -0.00  0.18  0.17  0.13 1829.6  21    7  0.78   28 1.95 2.10 2.09 1.000
   84_0085   34 -0.06 -0.11  0.01  0.21  0.21  0.12 2148.1  24    3  0.79   32 1.96 2.11 2.09 1.000
   85_0086   32  0.04 -0.17  0.06  0.30  0.45  0.20 2952.6  30    0  0.80   30 1.96 2.11 2.09 1.000
   86_0087   36  0.01 -0.02  0.00  0.16  0.48  0.16 1718.5  19   11  0.75   29 1.95 2.11 2.08 1.000
   87_0088   37  0.04 -0.13 -0.02  0.26  0.30  0.14 2146.4  20    5  0.78   28 1.95 2.11 2.08 1.000
   88_0089   27  0.07  0.08 -0.03  0.19  0.77  0.24 2599.0  24    7  0.73   29 1.95 2.11 2.08 1.000
   89_0090   40 -0.01 -0.04 -0.01  0.18  0.20  0.12 2689.3  27    0  0.81   29 1.95 2.11 2.08 1.000
   90_0091   28  0.02 -0.06 -0.01  0.19  0.18  0.16 1572.1  18    7  0.76   29 1.95 2.11 2.08 1.000
   91_0092   35 -0.02  0.06  0.03  0.24  0.32  0.14 2064.2  21    3  0.75   28 1.95 2.11 2.08 1.000
   92_0093   24 -0.13  0.00  0.04  0.41  0.44  0.17 1490.3  19    8  0.76   30 1.95 2.11 2.08 1.000
   93_0094   35 -0.05 -0.10  0.04  0.18  0.31  0.13 2755.4  27    6  0.80   29 1.95 2.11 2.08 1.000
   94_0095   32  0.01 -0.05 -0.01  0.19  0.18  0.16 3472.8  31    6  0.77   28 1.95 2.11 2.08 1.000
   95_0096   31  0.02 -0.06  0.00  0.21  0.20  0.14 1858.7  18    3  0.74   27 1.95 2.11 2.08 1.000
   96_0097   33 -0.03 -0.07 -0.02  0.26  0.29  0.14 2118.3  24    3  0.80   30 1.95 2.11 2.08 1.000
   97_0098   33  0.02 -0.13 -0.00  0.21  0.23  0.15 1620.3  20    6  0.78   30 1.95 2.10 2.08 1.000
   98_0099   38 -0.01 -0.08  0.00  0.24  0.15  0.14 2165.9  23    8  0.74   27 1.95 2.10 2.07 1.000
   99_0100   33  0.01 -0.03  0.02  0.15  0.18  0.10 2967.9  29    0  0.80   28 1.95 2.10 2.07 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.500
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):         -0.0600
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  0.7107300,  0.0000089

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.2455    0.4309    18.211   111.132

Orientation ('UB') matrix:
  -0.0109478  -0.0356651   0.0858162
  -0.1293970  -0.0205916  -0.0339587
   0.0283346  -0.1078169  -0.0219018

         A         B         C     Alpha      Beta     Gamma           Vol
    7.7212    8.6644   10.8194    90.000   102.991    90.000        705.29
    0.0004    0.0010    0.0007     0.000     0.003     0.000          0.12
Corrected for goodness of fit:
    0.0005    0.0010    0.0008     0.000     0.004     0.000          0.13

Crystal system constraint:            3  (Monoclinic B-uniq)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):          -98.572     106.627      12.855
Goniometer zeros (deg):          0.0000*     0.0290      0.0000*     0.0308    (*=never refined)
Crystal translations (pixels):               0.0000      0.0000      0.0000

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.2107  -0.3728   0.0118  -0.1986  -0.0417  -0.1188

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        3.06815e+003  1.67960e+003    1.05       3         4       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             511
 Average input ESD (pix, pix, deg):          0.22384         0.24194         0.05637
 Goodness of fit:                            0.93947         1.23248         0.93839

No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  100_0101   34  0.00 -0.03 -0.03  0.18  0.12  0.13 2636.0  24    9  0.73   27 1.95 2.10 2.08 1.000
  101_0102   33  0.02 -0.04 -0.03  0.16  0.19  0.15 2154.6  25    6  0.80   29 1.95 2.10 2.07 1.000
  102_0103   26 -0.02  0.04 -0.02  0.17  0.39  0.15 2726.4  23    8  0.70   28 1.95 2.10 2.07 1.000
  103_0104   31 -0.03  0.08  0.01  0.20  0.54  0.17 1959.5  21    3  0.78   30 1.95 2.10 2.07 1.000
  104_0105   36  0.00 -0.06 -0.01  0.33  0.30  0.14 2915.1  26    3  0.78   28 1.95 2.10 2.08 1.000
  105_0106   35 -0.04 -0.08 -0.01  0.17  0.16  0.11 1489.4  20    3  0.80   29 1.94 2.10 2.07 1.000
  106_0107   31  0.01 -0.09 -0.03  0.14  0.22  0.15 2842.6  24    6  0.75   28 1.94 2.10 2.07 1.000
  107_0108   25 -0.01  0.02 -0.00  0.17  0.22  0.09 2551.1  27    4  0.79   28 1.95 2.10 2.07 1.000
  108_0109   35 -0.04 -0.21  0.01  0.65  1.37  0.24 3283.0  27    3  0.78   29 1.95 2.10 2.08 1.000
  109_0110   30 -0.01  0.04 -0.03  0.23  0.22  0.17 1391.3  17   20  0.70   29 1.95 2.10 2.07 1.000
  110_0111   30 -0.02 -0.04 -0.03  0.14  0.12  0.09 2723.6  27    3  0.76   29 1.95 2.10 2.08 1.000
  111_0112   26  0.03 -0.05 -0.04  0.31  0.18  0.14 1989.2  21    0  0.82   30 1.95 2.10 2.07 1.000
  112_0113   41  0.05  0.03 -0.03  0.30  0.58  0.19 1665.7  18    7  0.75   29 1.95 2.11 2.07 1.000
  113_0114   38 -0.14  0.13  0.01  0.86  0.90  0.18 2890.3  27    3  0.80   29 1.95 2.11 2.08 1.000
  114_0115   37  0.01 -0.08 -0.03  0.11  0.18  0.11 2975.4  26    3  0.78   29 1.95 2.10 2.07 1.000
  115_0116   27  0.00  0.01 -0.03  0.36  0.38  0.16 2536.8  27    4  0.78   28 1.95 2.10 2.07 1.000
  116_0117   27 -0.01 -0.08  0.00  0.14  0.20  0.12 4504.2  37    0  0.82   28 1.95 2.10 2.07 1.000
  117_0118   29 -0.06 -0.03 -0.01  0.20  0.20  0.14 1700.9  18   10  0.75   28 1.95 2.10 2.07 1.000
  118_0119   43  0.06 -0.00  0.02  0.45  0.71  0.21 2022.7  19    9  0.73   27 1.95 2.10 2.07 1.000
  119_0120   28 -0.05 -0.06  0.00  0.17  0.15  0.11 3884.5  37    0  0.80   30 1.95 2.10 2.07 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  120_0121   31 -0.13  0.10  0.01  0.50  0.82  0.15 2021.7  21    0  0.79   29 1.95 2.10 2.07 1.000
  121_0122   30 -0.04 -0.03 -0.00  0.37  0.45  0.18 4666.0  37    3  0.78   30 1.95 2.10 2.07 1.000
  122_0123   38  0.01 -0.03  0.01  0.12  0.13  0.10 3659.1  35    3  0.81   30 1.95 2.10 2.08 1.000
  123_0124   39 -0.04 -0.01 -0.01  0.15  0.17  0.12 2272.8  21    8  0.76   28 1.95 2.10 2.08 1.000
  124_0125   24  0.02 -0.07 -0.00  0.15  0.16  0.10 3934.8  35    0  0.78   28 1.95 2.10 2.08 1.000
  125_0126   28  0.01  0.02 -0.00  0.27  0.39  0.16 2236.6  21    7  0.76   28 1.95 2.10 2.08 1.000
  126_0127   37 -0.06 -0.07  0.00  0.22  0.21  0.13 2200.0  22    5  0.77   28 1.95 2.10 2.08 1.000
  127_0128   39 -0.01 -0.06 -0.03  0.15  0.16  0.14 2350.9  22    3  0.78   28 1.95 2.10 2.08 1.000
  128_0129   35 -0.01 -0.08 -0.01  0.17  0.22  0.12 3235.6  27    6  0.78   29 1.95 2.10 2.08 1.000
  129_0130   25 -0.03 -0.03  0.02  0.12  0.15  0.09 2333.6  28    0  0.81   27 1.95 2.10 2.08 1.000
  130_0131   29 -0.02 -0.05  0.02  0.19  0.37  0.14 1867.1  24    3  0.79   29 1.95 2.10 2.08 1.000
  131_0132   31  0.04  0.05 -0.01  0.17  0.42  0.15 3032.2  25    3  0.74   28 1.95 2.10 2.08 1.000
  132_0133   33  0.05 -0.05 -0.01  0.20  0.20  0.14 1388.8  15   12  0.72   27 1.95 2.10 2.08 1.000
  133_0134   42 -0.03 -0.07  0.01  0.14  0.32  0.13 2911.6  29    7  0.77   29 1.95 2.10 2.08 1.000
  134_0135   27  0.00  0.00 -0.00  0.31  0.20  0.15 1088.1  14    4  0.78   28 1.95 2.10 2.08 1.000
  135_0136   27 -0.18 -0.03  0.09  0.46  0.44  0.18 2725.6  27    7  0.73   28 1.95 2.10 2.08 1.000
  136_0137   36  0.04  0.02 -0.06  0.21  0.23  0.15 2437.2  26    6  0.78   30 1.95 2.10 2.08 1.000
  137_0138   36  0.01 -0.08 -0.03  0.18  0.22  0.13 3522.8  30   11  0.75   29 1.95 2.10 2.08 1.000
  138_0139   27  0.02 -0.03 -0.02  0.13  0.21  0.13 2870.0  30    7  0.80   31 1.95 2.10 2.08 1.000
  139_0140   35 -0.02 -0.06  0.01  0.18  0.18  0.13 3076.3  27    3  0.76   28 1.96 2.10 2.08 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  140_0141   38  0.00 -0.07 -0.01  0.12  0.14  0.09 2582.2  24    3  0.77   29 1.96 2.10 2.08 1.000
  141_0142   35  0.03 -0.09 -0.00  0.16  0.23  0.12 3527.5  32    0  0.82   31 1.96 2.10 2.08 1.000
  142_0143   28  0.06  0.05 -0.01  0.39  0.58  0.18 2012.7  24    4  0.77   29 1.96 2.10 2.08 1.000
  143_0144   37  0.01 -0.02 -0.03  0.18  0.23  0.14 2670.5  25    3  0.79   29 1.96 2.10 2.08 1.000
  144_0145   32  0.01 -0.06 -0.03  0.21  0.28  0.13 3163.9  30    3  0.82   30 1.96 2.10 2.09 1.000
  145_0146   31  0.06 -0.06 -0.04  0.21  0.13  0.13 2179.9  22    6  0.77   28 1.96 2.10 2.09 1.000
  146_0147   38 -0.02 -0.03 -0.02  0.24  0.26  0.16 2968.9  25   11  0.77   28 1.96 2.10 2.09 1.000
  147_0148   34 -0.04 -0.04  0.01  0.14  0.14  0.12 1627.5  18    3  0.77   27 1.96 2.10 2.08 1.000
  148_0149   35 -0.01 -0.03 -0.01  0.16  0.20  0.12 3417.1  29   11  0.78   28 1.96 2.10 2.09 1.000
  149_0150   28 -0.00 -0.01 -0.03  0.21  0.26  0.14 4428.9  31    4  0.77   28 1.96 2.10 2.09 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.500
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):         -0.0600
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  0.7107300,  0.0000089

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.6990    0.4302    15.132   111.394

Orientation ('UB') matrix:
  -0.0109193  -0.0356550   0.0858317
  -0.1294162  -0.0205779  -0.0339276
   0.0283131  -0.1078103  -0.0219105

         A         B         C     Alpha      Beta     Gamma           Vol
    7.7204    8.6653   10.8186    90.000   102.985    90.000        705.25
    0.0005    0.0009    0.0006     0.000     0.004     0.000          0.12
Corrected for goodness of fit:
    0.0006    0.0010    0.0006     0.000     0.004     0.000          0.13

Crystal system constraint:            3  (Monoclinic B-uniq)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):          -98.556     106.628      12.844
Goniometer zeros (deg):          0.0000*     0.0346      0.0000*     0.0314    (*=never refined)
Crystal translations (pixels):               0.0000      0.0000      0.0000

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.2235  -0.4386   0.0116  -0.2185  -0.0229  -0.1218

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        2.03415e+003  1.76192e+003    1.08       2         4       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             510
 Average input ESD (pix, pix, deg):          0.22354         0.23254         0.05535
 Goodness of fit:                            1.03179         1.22823         0.93354

No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  150_0151   28 -0.02  0.22  0.07  0.25  1.66  0.35 2820.6  28    4  0.79   29 1.96 2.10 2.08 1.000
  151_0152   27 -0.07 -0.07  0.00  0.17  0.21  0.16 4986.7  35   11  0.72   27 1.96 2.10 2.09 1.000
  152_0153   29 -0.04  0.01 -0.00  0.18  0.21  0.12 1278.8  16   10  0.75   28 1.96 2.10 2.09 1.000
  153_0154   31 -0.03 -0.04 -0.02  0.08  0.09  0.09 3033.2  27    0  0.75   27 1.96 2.10 2.09 1.000
  154_0155   32 -0.03 -0.03 -0.00  0.16  0.33  0.14 1781.7  19    6  0.76   28 1.96 2.10 2.08 1.000
  155_0156   30 -0.01 -0.02 -0.02  0.11  0.09  0.09 4192.5  34    0  0.79   28 1.96 2.10 2.08 1.000
  156_0157   34 -0.03 -0.02  0.01  0.14  0.13  0.11 2510.5  27    6  0.73   27 1.96 2.10 2.08 1.000
  157_0158   34 -0.01 -0.06 -0.02  0.24  0.21  0.15 2537.4  27   18  0.75   30 1.96 2.10 2.09 1.000
  158_0159   33  0.02 -0.02 -0.05  0.16  0.15  0.12 2413.6  26    3  0.80   31 1.96 2.10 2.09 1.000
  159_0160   31 -0.12 -0.16  0.03  0.41  0.63  0.15 4687.9  34    6  0.73   28 1.96 2.10 2.09 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  160_0161   38  0.05  0.01 -0.01  0.20  0.21  0.15 2498.1  25   11  0.79   29 1.96 2.10 2.09 1.000
  161_0162   32 -0.02 -0.11  0.00  0.21  0.33  0.15 2040.6  22    0  0.80   28 1.96 2.10 2.09 1.000
  162_0163   36 -0.04 -0.05  0.01  0.17  0.13  0.12 2461.0  27   11  0.79   29 1.96 2.10 2.09 1.000
  163_0164   32  0.05  0.10  0.06  0.43  0.83  0.23 2664.8  24   13  0.80   29 1.96 2.10 2.09 1.000
  164_0165   32 -0.09 -0.01  0.03  0.20  0.27  0.13 1962.7  20    6  0.76   28 1.96 2.10 2.09 1.000
  165_0166   28  0.03  0.03 -0.02  0.14  0.15  0.12 2838.1  28    4  0.76   29 1.96 2.10 2.09 1.000
  166_0167   28 -0.01  0.10 -0.01  0.22  0.42  0.15 1949.8  20    7  0.77   30 1.96 2.10 2.09 1.000
  167_0168   26  0.03 -0.01 -0.06  0.17  0.22  0.12 2843.6  27    4  0.80   30 1.96 2.10 2.09 1.000
  168_0169   37  0.01 -0.02 -0.01  0.20  0.18  0.13 2362.8  23    8  0.76   28 1.97 2.10 2.09 1.000
  169_0170   39  0.04 -0.06 -0.03  0.18  0.17  0.13 1875.4  21    0  0.78   30 1.96 2.10 2.09 1.000
  170_0171   36 -0.00  0.08 -0.04  0.26  0.39  0.14 2355.9  21    6  0.76   28 1.97 2.10 2.09 1.000
  171_0172   32 -0.02 -0.02 -0.03  0.19  0.15  0.13 3451.6  25    6  0.74   28 1.97 2.10 2.09 1.000
  172_0173   35 -0.00 -0.03  0.01  0.23  0.14  0.16 2707.2  26    9  0.78   29 1.97 2.10 2.10 1.000
  173_0174   21 -0.03 -0.00 -0.00  0.14  0.23  0.09 2015.1  20    5  0.78   28 1.97 2.10 2.10 1.000
  174_0175   27  0.05 -0.02  0.02  0.16  0.12  0.13 2710.5  26   11  0.73   27 1.96 2.10 2.10 1.000
  175_0176   33 -0.02  0.07  0.02  0.21  0.26  0.16 2282.2  24    6  0.77   28 1.96 2.10 2.10 1.000
  176_0177   28  0.03 -0.02 -0.02  0.19  0.25  0.12 1667.7  18    4  0.76   29 1.96 2.10 2.10 1.000
  177_0178   32 -0.04  0.02  0.01  0.19  0.19  0.11 3508.8  34    3  0.80   29 1.96 2.10 2.10 1.000
  178_0179   36 -0.03 -0.09  0.03  0.14  0.26  0.13 3607.5  31    6  0.77   29 1.96 2.10 2.10 1.000
  179_0180   45  0.01 -0.05  0.01  0.36  0.29  0.13 2945.9  29   11  0.75   32 1.97 2.10 2.10 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  180_0181   34 -0.07 -0.03 -0.00  0.16  0.12  0.12 2602.4  25   12  0.75   28 1.97 2.10 2.10 1.000
  181_0182   25 -0.06  0.02  0.08  0.17  0.21  0.14 3991.0  33   12  0.76   30 1.97 2.10 2.10 1.000
  182_0183   37 -0.03 -0.02 -0.01  0.22  0.16  0.15 2049.4  20   11  0.76   29 1.96 2.10 2.10 1.000
  183_0184   26  0.08  0.03 -0.02  0.27  0.32  0.13 2165.7  21    8  0.72   27 1.96 2.10 2.10 1.000
  184_0185   44 -0.12 -0.02  0.05  0.22  0.14  0.14 2647.0  23    7  0.79   28 1.96 2.10 2.10 1.000
  185_0186   31  0.03 -0.02 -0.01  0.21  0.20  0.10 3770.5  36    3  0.81   29 1.96 2.10 2.10 1.000
  186_0187   20 -0.03  0.09  0.06  0.18  0.60  0.16 5731.4  40   20  0.76   31 1.96 2.10 2.10 1.000
  187_0188   41 -0.00 -0.04 -0.00  0.08  0.10  0.09 3660.8  32    7  0.76   28 1.96 2.10 2.11 1.000
  188_0189   37 -0.08 -0.09  0.04  0.37  0.38  0.13 3606.8  32    5  0.80   30 1.97 2.10 2.11 1.000
  189_0190   32  0.00  0.04 -0.01  0.26  0.30  0.11 3375.8  31    0  0.82   30 1.96 2.10 2.10 1.000
  190_0191   33 -0.05 -0.01  0.01  0.21  0.21  0.11 3088.3  28    0  0.79   30 1.96 2.10 2.11 1.000
  191_0192   26 -0.07  0.05  0.05  0.30  0.48  0.15 2772.3  25    0  0.79   29 1.97 2.10 2.11 1.000
  192_0193   28 -0.02 -0.03  0.00  0.20  0.19  0.15 2042.4  23   11  0.76   29 1.96 2.10 2.11 1.000
  193_0194   38 -0.01 -0.04 -0.03  0.20  0.18  0.10 3201.5  30    0  0.79   28 1.96 2.10 2.11 1.000
  194_0195   38  0.00  0.01  0.01  0.21  0.23  0.13 2816.5  25    5  0.77   27 1.96 2.10 2.11 1.000
  195_0196   38 -0.03 -0.01  0.02  0.23  0.19  0.17 3265.8  25   13  0.74   27 1.96 2.10 2.11 1.000
  196_0197   24 -0.01  0.00 -0.01  0.11  0.07  0.09 4048.8  29    4  0.70   27 1.96 2.10 2.11 1.000
  197_0198   27 -0.04 -0.02  0.02  0.16  0.17  0.13 1525.9  17   11  0.78   29 1.96 2.10 2.11 1.000
  198_0199   39  0.03 -0.00 -0.02  0.26  0.17  0.13 4062.7  33    3  0.77   27 1.96 2.10 2.11 1.000
  199_0200   20 -0.13 -0.11  0.07  0.29  0.28  0.16 2595.1  25    0  0.83   30 1.96 2.10 2.11 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.500
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):         -0.0600
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  0.7107300,  0.0000089

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    3.8240    0.4325    10.664   110.514

Orientation ('UB') matrix:
  -0.0109195  -0.0356350   0.0858340
  -0.1294850  -0.0205467  -0.0339513
   0.0282900  -0.1077979  -0.0219032

         A         B         C     Alpha      Beta     Gamma           Vol
    7.7174    8.6671   10.8185    90.000   103.006    90.000        705.06
    0.0009    0.0006    0.0006     0.000     0.004     0.000          0.13
Corrected for goodness of fit:
    0.0009    0.0006    0.0006     0.000     0.004     0.000          0.12

Crystal system constraint:            3  (Monoclinic B-uniq)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):          -98.547     106.624      12.827
Goniometer zeros (deg):          0.0000*     0.0415      0.0000*     0.0208    (*=never refined)
Crystal translations (pixels):               0.0000      0.0000      0.0000

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.2191  -0.4706   0.0105  -0.2426  -0.0057  -0.1348

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        1.64055e+003  1.46194e+003    0.98       2         4       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             512
 Average input ESD (pix, pix, deg):          0.23435         0.25020         0.05610
 Goodness of fit:                            1.08518         0.92332         0.90842

No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  200_0201   37 -0.04  0.06  0.02  0.21  0.35  0.12 2489.7  22   11  0.76   29 1.96 2.10 2.11 1.000
  201_0202   28  0.04  0.02 -0.02  0.23  0.16  0.12 3380.4  28    0  0.78   29 1.96 2.10 2.11 1.000
  202_0203   28 -0.01 -0.00 -0.03  0.13  0.10  0.13 2156.2  22    0  0.77   29 1.96 2.10 2.11 1.000
  203_0204   31  0.02 -0.03 -0.02  0.22  0.21  0.14 2501.4  27    3  0.81   29 1.96 2.10 2.11 1.000
  204_0205   39  0.01 -0.04 -0.02  0.09  0.15  0.11 2390.5  25    5  0.79   30 1.96 2.10 2.11 1.000
  205_0206   39 -0.04  0.04 -0.01  0.27  0.35  0.15 2776.4  24    3  0.77   27 1.96 2.10 2.11 1.000
  206_0207   38 -0.00 -0.03 -0.03  0.22  0.11  0.14 2494.2  23    5  0.80   27 1.96 2.09 2.11 1.000
  207_0208   35  0.04 -0.06 -0.01  0.27  0.46  0.20 2551.4  22    9  0.78   30 1.96 2.09 2.11 1.000
  208_0209   27 -0.05 -0.07 -0.01  0.18  0.20  0.13 3048.1  26    4  0.78   28 1.96 2.09 2.11 1.000
  209_0210   23  0.01 -0.02 -0.02  0.11  0.14  0.09 3358.5  37    0  0.78   28 1.96 2.09 2.11 1.000
  210_0211   34 -0.00 -0.01  0.02  0.15  0.19  0.13 2091.8  20    3  0.74   28 1.96 2.09 2.12 1.000
  211_0212   26 -0.05  0.01  0.01  0.19  0.15  0.10 4266.8  33    0  0.80   27 1.96 2.09 2.12 1.000
  212_0213   33 -0.02 -0.14  0.02  0.18  0.40  0.18 2967.0  28    6  0.79   31 1.96 2.09 2.12 1.000
  213_0214   40 -0.02 -0.02  0.00  0.14  0.14  0.13 2764.6  29    3  0.79   31 1.96 2.09 2.12 1.000
  214_0215   29  0.11 -0.11 -0.07  0.31  0.34  0.16 2493.2  25    3  0.81   31 1.96 2.10 2.12 1.000
  215_0216   34 -0.03 -0.02  0.01  0.16  0.17  0.09 4384.9  31    3  0.76   27 1.96 2.09 2.12 1.000
  216_0217   34 -0.04 -0.08 -0.01  0.13  0.20  0.13 2406.1  24    0  0.79   28 1.96 2.09 2.12 1.000
  217_0218   34 -0.00 -0.04 -0.01  0.17  0.12  0.14 2501.6  24    3  0.77   28 1.96 2.09 2.12 1.000
  218_0219   35 -0.03 -0.05 -0.02  0.17  0.15  0.10 2805.1  27    3  0.78   30 1.96 2.09 2.12 1.000
  219_0220   43  0.03 -0.03 -0.02  0.19  0.52  0.14 2497.4  26    7  0.82   29 1.96 2.09 2.12 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  220_0221   35 -0.03 -0.07  0.00  0.21  0.18  0.13 2002.6  20   11  0.76   28 1.96 2.09 2.12 1.000
  221_0222   29 -0.05  0.04 -0.02  0.23  0.41  0.16 3186.3  28    3  0.78   28 1.96 2.09 2.12 1.000
  222_0223   28 -0.09 -0.02  0.07  0.19  0.30  0.14 3061.6  26    7  0.77   26 1.96 2.09 2.12 1.000
  223_0224   30 -0.14  0.04  0.03  0.69  0.71  0.19 2051.9  21    7  0.76   28 1.96 2.09 2.12 1.000
  224_0225   24 -0.00 -0.09 -0.00  0.13  0.19  0.11 3237.6  27    8  0.75   28 1.96 2.09 2.12 1.000
  225_0226   27 -0.04 -0.09  0.01  0.18  0.18  0.12 2723.4  23   11  0.78   30 1.96 2.09 2.12 1.000
  226_0227   31  0.04 -0.08 -0.01  0.15  0.20  0.13 1980.1  21    6  0.76   29 1.96 2.09 2.12 1.000
  227_0228   34 -0.02 -0.08  0.01  0.15  0.21  0.14 2870.2  25    9  0.77   28 1.96 2.09 2.13 1.000
  228_0229   34 -0.05 -0.10 -0.01  0.13  0.21  0.11 4253.0  31    6  0.79   30 1.96 2.09 2.13 1.000
  229_0230   34 -0.04 -0.12  0.01  0.30  0.31  0.15 3870.4  34    6  0.79   30 1.96 2.09 2.13 1.000
  230_0231   35 -0.01 -0.03  0.02  0.20  0.13  0.14 5015.6  37   17  0.75   28 1.96 2.09 2.13 1.000
  231_0232   32  0.01 -0.12  0.01  0.39  0.23  0.12 3497.8  30    3  0.80   31 1.96 2.09 2.13 1.000
  232_0233   33  0.01 -0.12 -0.01  0.16  0.19  0.12 2257.5  22    0  0.79   29 1.96 2.09 2.13 1.000
  233_0234   39 -0.01 -0.05  0.01  0.22  0.24  0.13 2616.3  24    3  0.82   28 1.96 2.09 2.13 1.000
  234_0235   36  0.01 -0.05 -0.01  0.19  0.45  0.18 3504.5  28    6  0.77   28 1.96 2.09 2.13 1.000
  235_0236   37 -0.09  0.10  0.05  0.47  0.85  0.20 4204.3  35    3  0.78   29 1.96 2.09 2.13 1.000
  236_0237   26 -0.01 -0.08 -0.01  0.36  0.34  0.13 3344.0  26    8  0.76   30 1.96 2.09 2.13 1.000
  237_0238   20  0.01 -0.04 -0.07  0.12  0.13  0.14 3127.0  24   10  0.73   30 1.96 2.09 2.13 1.000
  238_0239   36 -0.00 -0.10  0.01  0.14  0.15  0.11 2527.0  25    3  0.78   29 1.96 2.09 2.13 1.000
  239_0240   33 -0.05 -0.13 -0.01  0.17  0.28  0.14 3588.9  27    3  0.80   28 1.96 2.09 2.13 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  240_0241   27  0.07 -0.04 -0.04  0.29  0.28  0.21 2046.9  19    4  0.76   28 1.96 2.09 2.13 1.000
  241_0242   34 -0.03 -0.07  0.03  0.25  0.13  0.13 4370.6  36    6  0.79   30 1.96 2.09 2.14 1.000
  242_0243   43 -0.03 -0.08  0.04  0.23  0.24  0.13 3757.3  29    2  0.78   28 1.96 2.09 2.14 1.000
  243_0244   25  0.01 -0.10 -0.02  0.09  0.16  0.08 3675.6  33    4  0.78   29 1.96 2.09 2.14 1.000
  244_0245   33 -0.10 -0.07  0.05  0.28  0.38  0.14 3107.6  28    0  0.81   28 1.96 2.09 2.14 1.000
  245_0246   36 -0.01 -0.08  0.00  0.14  0.14  0.14 2084.2  21   11  0.78   29 1.96 2.09 2.14 1.000
  246_0247   35 -0.01 -0.08 -0.02  0.13  0.16  0.11 4435.0  32    0  0.80   28 1.96 2.08 2.14 1.000
  247_0248   32  0.04 -0.00 -0.02  0.18  0.22  0.13 3843.9  33    0  0.76   29 1.96 2.08 2.14 1.000
  248_0249   26 -0.07 -0.06  0.03  0.24  0.19  0.14 2858.9  27    4  0.76   30 1.96 2.08 2.14 1.000
  249_0250   28  0.02  0.04 -0.01  0.35  0.45  0.11 3252.1  29    0  0.78   29 1.96 2.08 2.14 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.500
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):         -0.0600
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  0.7107300,  0.0000089

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.5206    0.4303    16.209   111.363

Orientation ('UB') matrix:
  -0.0108119  -0.0356507   0.0858724
  -0.1295232  -0.0205602  -0.0339063
   0.0282739  -0.1078194  -0.0219283

         A         B         C     Alpha      Beta     Gamma           Vol
    7.7164    8.6650   10.8162    90.000   103.018    90.000        704.61
    0.0012    0.0005    0.0009     0.000     0.006     0.000          0.17
Corrected for goodness of fit:
    0.0012    0.0005    0.0009     0.000     0.006     0.000          0.17

Crystal system constraint:            3  (Monoclinic B-uniq)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):          -98.499     106.638      12.818
Goniometer zeros (deg):          0.0000*     0.0852      0.0000*     0.0500    (*=never refined)
Crystal translations (pixels):               0.0000      0.0000      0.0000

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.0963  -0.5394   0.0076  -0.2637  -0.0031  -0.1511

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        1.98821e+003  1.51696e+003    1.00       6         4       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             511
 Average input ESD (pix, pix, deg):          0.21731         0.23094         0.05417
 Goodness of fit:                            1.18292         0.95500         0.80795

No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  250_0251   28 -0.03 -0.01  0.02  0.15  0.23  0.13 3225.6  26    0  0.80   29 1.96 2.08 2.14 1.000
  251_0252   36  0.01 -0.05 -0.03  0.30  0.20  0.15 1765.1  18    8  0.77   29 1.96 2.08 2.14 1.000
  252_0253   39 -0.06 -0.05 -0.00  0.25  0.22  0.14 1898.4  21    3  0.77   31 1.96 2.08 2.14 1.000
  253_0254   34 -0.10 -0.00  0.04  0.28  0.77  0.16 2859.0  26    3  0.78   29 1.96 2.08 2.14 1.000
  254_0255   25 -0.02 -0.07 -0.01  0.22  0.14  0.15 3538.7  26   12  0.74   27 1.96 2.08 2.14 1.000
  255_0256   31 -0.06 -0.06  0.02  0.17  0.17  0.12 4173.9  39    3  0.81   32 1.96 2.08 2.14 1.000
  256_0257   32 -0.04 -0.04 -0.00  0.20  0.15  0.12 4084.9  32    9  0.77   28 1.96 2.08 2.15 1.000
  257_0258   43 -0.01 -0.06  0.01  0.28  0.23  0.10 3621.9  30    5  0.80   28 1.96 2.08 2.15 1.000
  258_0259   39 -0.00 -0.04 -0.00  0.14  0.14  0.10 2578.0  24    3  0.80   31 1.96 2.08 2.15 1.000
  259_0260   30 -0.01  0.01  0.02  0.13  0.16  0.12 3573.0  33   10  0.78   29 1.96 2.08 2.15 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  260_0261   30 -0.19 -0.41  0.07  0.78  1.51  0.24 1996.9  23    0  0.83   30 1.96 2.08 2.15 1.000
  261_0262   36 -0.04 -0.08  0.02  0.17  0.18  0.11 3249.7  29    3  0.82   28 1.96 2.08 2.15 1.000
  262_0263   28  0.04  0.00 -0.02  0.14  0.10  0.12 2271.6  19    7  0.72   26 1.96 2.08 2.15 1.000
  263_0264   24  0.01 -0.01  0.00  0.16  0.18  0.12 2317.0  22    8  0.74   29 1.96 2.08 2.15 1.000
  264_0265   36 -0.02 -0.01 -0.00  0.17  0.24  0.10 4100.7  30    6  0.79   29 1.96 2.07 2.15 1.000
  265_0266   32 -0.02  0.02  0.03  0.21  0.23  0.13 4078.4  32    6  0.78   29 1.96 2.08 2.15 1.000
  266_0267   25 -0.01  0.03  0.02  0.16  0.27  0.12 3205.0  25    8  0.74   29 1.96 2.07 2.15 1.000
  267_0268   27  0.04 -0.10 -0.02  0.20  0.21  0.10 3159.0  28    0  0.74   26 1.96 2.07 2.15 1.000
  268_0269   41 -0.06 -0.09  0.03  0.20  0.21  0.13 2966.3  26    5  0.80   30 1.96 2.07 2.15 1.000
  269_0270   41 -0.03 -0.12 -0.01  0.18  0.23  0.11 4390.0  34    5  0.81   30 1.96 2.08 2.15 1.000
  270_0271   38 -0.13 -0.08  0.06  0.32  0.60  0.15 4202.9  30    5  0.78   28 1.96 2.08 2.15 1.000
  271_0272   30 -0.09 -0.04  0.03  0.28  0.43  0.15 1940.1  19    3  0.79   30 1.96 2.08 2.15 1.000
  272_0273   29 -0.02 -0.08  0.00  0.18  0.16  0.13 2883.2  26    3  0.78   29 1.96 2.08 2.15 1.000
  273_0274   29 -0.07 -0.02  0.05  0.21  0.22  0.14 3984.3  34    7  0.76   27 1.96 2.07 2.15 1.000
  274_0275   27 -0.05 -0.08  0.04  0.11  0.17  0.12 5034.2  39    0  0.78   28 1.96 2.07 2.16 1.000
  275_0276   39 -0.07 -0.14  0.04  0.26  0.31  0.13 3844.2  34    3  0.81   31 1.96 2.07 2.16 1.000
  276_0277   39 -0.04 -0.06  0.02  0.20  0.18  0.14 3979.6  32    8  0.74   27 1.96 2.07 2.16 1.000
  277_0278   35 -0.12 -0.18  0.04  0.63  0.83  0.15 2686.3  24    9  0.75   27 1.96 2.07 2.16 1.000
  278_0279   35 -0.06 -0.14  0.03  0.20  0.41  0.13 2684.9  21   11  0.74   27 1.96 2.07 2.16 1.000
  279_0280   20 -0.03 -0.02  0.07  0.17  0.36  0.19 3049.4  26    5  0.79   30 1.96 2.07 2.16 1.000
No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  280_0281   35 -0.06 -0.09  0.04  0.21  0.48  0.16 4109.3  32    0  0.79   29 1.96 2.07 2.16 1.000
  281_0282   32 -0.16 -0.07  0.07  0.36  0.39  0.17 2015.2  19    6  0.78   30 1.96 2.07 2.16 1.000
  282_0283   35 -0.03 -0.10 -0.01  0.30  0.28  0.14 2290.6  24   11  0.75   29 1.96 2.07 2.16 1.000
  283_0284   25 -0.06 -0.04  0.03  0.17  0.16  0.11 3160.0  30    0  0.79   28 1.96 2.07 2.16 1.000
  284_0285   34 -0.05 -0.04  0.03  0.21  0.27  0.14 2976.4  26    6  0.79   28 1.96 2.07 2.16 1.000
  285_0286   34 -0.03 -0.09  0.04  0.18  0.16  0.12 3455.7  32    6  0.80   29 1.96 2.07 2.17 1.000
  286_0287   32 -0.01 -0.08  0.01  0.19  0.17  0.13 1442.1  15   13  0.70   27 1.96 2.07 2.16 1.000
  287_0288   35 -0.05 -0.12  0.04  0.15  0.21  0.13 5104.9  34    3  0.75   27 1.96 2.07 2.17 1.000
  288_0289   32 -0.00 -0.06 -0.00  0.24  0.31  0.12 2452.0  23    6  0.78   28 1.96 2.07 2.17 1.000
  289_0290   32 -0.14  0.04  0.07  0.34  0.68  0.18 2234.2  23    6  0.81   31 1.96 2.07 2.17 1.000
  290_0291   27 -0.03 -0.09  0.02  0.25  0.19  0.15 3168.5  27   11  0.77   29 1.96 2.07 2.17 1.000
  291_0292   35  0.00 -0.07  0.01  0.11  0.19  0.10 3263.0  29    3  0.78   30 1.96 2.07 2.17 1.000
  292_0293   39 -0.05 -0.09  0.07  0.18  0.21  0.16 3236.5  28    5  0.80   29 1.96 2.07 2.17 1.000
  293_0294   38  0.01 -0.03  0.03  0.18  0.19  0.11 3272.4  29    0  0.82   28 1.96 2.07 2.17 1.000
  294_0295   35  0.01 -0.06  0.01  0.27  0.18  0.12 3575.9  29    9  0.78   27 1.96 2.07 2.17 1.000
  295_0296   27 -0.09 -0.10  0.02  0.17  0.22  0.15 3018.1  24   11  0.77   29 1.96 2.07 2.17 1.000
  296_0297   29 -0.05 -0.11  0.00  0.19  0.22  0.15 2666.9  20   10  0.74   30 1.96 2.07 2.17 1.000
  297_0298   33 -0.04 -0.15  0.02  0.15  0.21  0.11 2988.0  28    3  0.80   30 1.96 2.07 2.17 1.000
  298_0299   38 -0.08 -0.08  0.03  0.19  0.27  0.11 2757.6  24    0  0.81   29 1.96 2.06 2.17 1.000
  299_0300   25 -0.09 -0.11  0.03  0.22  0.26  0.09 4343.3  29    4  0.78   28 1.96 2.07 2.17 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.500
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):         -0.0600
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  0.7107300,  0.0000089

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    3.2431    0.4317    12.582   110.802

Orientation ('UB') matrix:
  -0.0108853  -0.0356223   0.0859054
  -0.1295383  -0.0205824  -0.0339426
   0.0283180  -0.1078452  -0.0218974

         A         B         C     Alpha      Beta     Gamma           Vol
    7.7141    8.6636   10.8115    90.000   103.003    90.000        704.03
    0.0014    0.0006    0.0017     0.000     0.010     0.000          0.24
Corrected for goodness of fit:
    0.0014    0.0006    0.0017     0.000     0.009     0.000          0.23

Crystal system constraint:            3  (Monoclinic B-uniq)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):          -98.530     106.612      12.834
Goniometer zeros (deg):          0.0000*     0.1114      0.0000*     0.0774    (*=never refined)
Crystal translations (pixels):               0.0000      0.0000      0.0000

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                      -0.1045  -0.6956   0.0067  -0.2858   0.0070  -0.1618

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        2.01815e+003  1.43477e+003    0.97      11         4       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             512
 Average input ESD (pix, pix, deg):          0.22336         0.22368         0.05529
 Goodness of fit:                            1.02568         1.03727         0.82118

No BG pixels updated (best-plane BG selected)            Port, connections: 2000, 1
Integration of DK_zucker
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  300_0301   29 -0.04 -0.07  0.00  0.21  0.16  0.14 3753.3  30    0  0.75   27 1.96 2.06 2.17 1.000
  301_0302    1 -0.12 -0.02  0.10  0.12  0.02  0.10 1032.7  13    0  0.75   22 1.96 2.06 2.17 1.000
  302_0303    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   16 1.96 2.06 2.17 1.000
  303_0304    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   18 1.96 2.06 2.17 1.000

Requested number of frames processed: D:\frames\guest\DK_Zucker2\mo_DK_Zucker2_01_0304.sfrm


I/Sigma = 32.51   Thresh = 0.020   Blend = F   #Contributing = 3422   InitialProfileWt = 0.000
Region 1
Sum = 16836.1;   Maximum = 1054.63;   FM = 0.856
!Region 1: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  1  1  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  2  2  1  0  0  0    0  1  3 13 14  4  1  0  0  
  0  0  0  0  0  0  0  0  0    1  1  2  4  3  1  0  0  0    0  1  6 26 28  7  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  1  2  8  9  3  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  1  3  3  3  1  0  0    0  0  1  3  6  5  1  0  0    0  0  1  2  5  4  1  0  0  
  0  0  6 26 32 23  4  0  0    0  1  7 28 54 47  8  1  0    0  1  3 16 47 30  4  1  0  
  0  1 12 49 59 39  7  0  0    0  1 12 51100 81 13  1  0    0  0  4 27 85 55  7  1  0  
  0  0  4 15 19 14  3  0  0    0  0  4 16 31 27  5  1  0    0  0  2  9 26 17  3  1  0  
  0  0  1  1  2  1  0  0  0    0  0  1  2  3  2  1  0  0    0  0  1  1  2  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  3  2  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  6 16  9  2  1  0    0  0  1  3  4  2  1  1  0    0  0  0  1  1  0  0  0  0  
  0  0  2  8 27 15  4  2  0    0  0  1  4  7  4  2  2  1    0  0  0  1  1  0  0  0  0  
  0  0  1  4  9  5  1  1  0    0  0  1  3  5  2  1  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  2  2  1  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 0.00   Thresh = 0.020   Blend = F   #Contributing = 0   InitialProfileWt = 1.000
Region 2
Sum = 1.16635;   Maximum = 0.0777358;   FM = 0.775
!Region 2: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  0  0  1  1  1  0    0  0  1  0  0  1  1  1  0    0  0  1  1  0  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  1  0  0    0  0  1  3  3  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  4  5  1  0  0  0    0  0  7 27 20  3  1  1  0  
  0  1  0  0  0  0  0  0  0    0  1  2  7  7  1  0  0  0    0  1 11 46 28  3  1  0  0  
  0  0  0  0  0  1  1  0  0    0  1  1  2  3  1  0  0  0    0  1  3 12  9  1  1  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  1  0    0  0  0  1  2  1  1  1  0  
  0  0  0 -1  0  0  0  0  0    0  0 -1 -1  0  0  0  0  0    0  0  0  0  1  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 2: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  0  0  0  0  0  
  0  1  1  1  1  1  0  0  0    0  1  1  1  2  1  1  1  0    0  0  0  1  2  1  1  0  0  
  0  0  2  3  3  3  1  0  0    0  1  2  3  5  6  2  1  0    0  1  1  2  6  4  2  1  0  
  0  0 12 29 18 22  6  1  0    0  1  8 13 35 57 12  1  0    0  1  2 10 48 29  5  1  0  
  0  1 20 51 29 33  7  0  0    0  1 12 23 62100 16  1  0    0  1  2 14 85 51  6  1  0  
  0  1  6 13  9  9  3  1  0    0  1  4  7 17 26  6  1  0    0  1  1  5 21 13  3  1  0  
  0  0  1  1  2  2  1  1  0    0  1  1  1  1  2  1  1  0    0  1  1  1  2  1  1  1  0  
  0  0  1  1  1  1  1  0  0    0  1  1  1  1  1  1  1  0    0  0  1  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 2: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0 -1  0  0  0  
  0  0  0  2  3  1  1  0  0    0  0  1  1  1  0  0  0  0    0  0  1  0  0 -1  0  0  0  
  0  0  1  6 16  6  2  0  0    0  0  2  2  2  1  1  0  0    0  0  1  0  0  0  0  0  0  
  0  0  1  7 25  9  2  1  0    0  0  2  2  2  1  2  1  0    0  0  0  0  0  0  1  0  0  
  0  0  1  4  7  3  1  0  0    0  0  1  2  1  1  1  1  0    0  0  0  0  0  1  0  0  0  
  0  0  1  2  1  1  0  0  0    0  0  1  1  1  1  0 -1  0    0  0  0  0  0  1  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0 -1  0    0  0  0  0  0  0  0 -1  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 18.66   Thresh = 0.020   Blend = F   #Contributing = 57   InitialProfileWt = 0.001
Region 3
Sum = 7271.75;   Maximum = 479.036;   FM = 0.735
!Region 3: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  2  0  0  1  1  1  0    0  0  1  0  0  1  1  1  0    0  0  1  1  1  1  0  0  0  
  0  0  0  0  0  0  1  0  0    0  0  0  1  1  1  1  0  0    0  0  1  4  7  3  1  1  0  
  0  0  0  0  0  0  0  0  0    0  1  1  6  8  1  0  0  0    0  0  5 35 35  3  2  1  0  
  0  1  0  0  0  1  0  0  0    0  1  1  6  7  1  0  0  0    0  1 11 47 28  3  1  0  0  
  0  1  0  0  0  1  1  0  0    0  1  0  1  2  1  0  0  0    0  1  4  8  3  2  1  1  0  
  0  0  0 -1  0  1  0  0  0    0  0  0  0  1  0  0  1  0    0  1  1  2  2  2  1  1  0  
  0  0  0 -1  0  0  0  0  0    0  0  0 -1  0  0  0  0  0    0  1  1  1  1  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0 -1  0  0  0  0  0    0  0  0  1  0  0  0  0  0  
!Region 3: Section 4->6
  0  0  0  0  1  1  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  1  1  1  2  2  1  0  0    0  1  1  2  2  2  2  0  0    0  0  1  2  2  1  1  1  0  
  0  0  2  3  4  5  3  0  0    0  1  2  3  3  8  3  1  0    0  1  2  1  3  4  2  2  0  
  0  0  8 29 21 33 11  1  0    0  0  6 10 23 70 19  1  0    0  0  1  6 34 29  7  2  1  
  0  0 21 46 24 35  9  0  0    0  0 15 24 53 82 16  1  0    0  1  1 15100 48  6  1  1  
  0  1  8 10  5  5  1  0  0    0  1  6  8 16 13  2  1  0    0  1  1  7 30 10  2  1  0  
  0  1  1  2  2  2  1  0  0    0  1  1  1  2  2  1  1  0    0  1  1  2  2  1  1  1  0  
  0  1  1  1  1  1  2  1  0    0  1  1  1  1  1  1  1  0    0  1  1  2  1  1  0  0  0  
  0  0  0  1  0  0  1  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  0  0  0  0  
!Region 3: Section 7->9
  0  0  0  0  1  1  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  2  1  0  0  0    0  0  0  1  0 -1  0  0  0    0  0  0  0  0 -1  0  0  0  
  0  0  0  0  2  1  1  1  0    0  0  1  1  1  0  0  0  0    0  0  0  1  0 -1  0  0  0  
  0  0  1  3 11  5  2  1  0    0  0  1  1  0  0  0  0  0    0  1  0  0 -1 -1  0 -1  0  
  0  0  1  7 33 10  3  0  0    0  0  1  1  0  1  2  1  0    0 -1 -1 -1  0  1  0  0  0  
  0  0  2  7 12  4  1  0  0    0  0  2  3  1  1  1  1  0    0  0  0  0  0  1  0  1  0  
  0  0  2  3  2  1  0 -1  0    0  0  1  2  1  0  0 -1  0    0  0  0  0  0  1  0  0  0  
  0  1  1  1  0  0  0 -1  0    0  0  1  1  0  0 -1 -2  0    0  0  1  0  0  0 -1 -1  0  
  0  0  0  0  1  0 -1 -1  0    0  0  0  1  1  0  0 -1  0    0  0  0  1  0  0  0  0  0  

I/Sigma = 23.69   Thresh = 0.020   Blend = F   #Contributing = 305   InitialProfileWt = 0.000
Region 4
Sum = 11598.1;   Maximum = 865.491;   FM = 0.773
!Region 4: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0 -1  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0 -1 -1  1  1  0  1  0    0  0 -1  0  1  1  0  0  0  
  0  0 -1  0  0  0  1  0  0    0  0  0  0  1  1  0  0  0    0  0  0  2  2  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  1  1  0  0  0    0  0  2 17 11  2  1  0  0  
  0  1  0  0  0  0  0  0  0    0  1  1  3  1  0  0  0  0    0  1  6 30 13  2  1  0  0  
  0  0  0  0 -1  0  0  0  0    0  1  1  1  0  0  1  1  0    0  1  3  6  3  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  1  0  0    0  0  0  0  0  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 4: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  1  1  0    0  0  0  1  1  1  1  1  0    0  0  0  0  1  1  0  0  0  
  0  0  0  2  4  3  1  1  0    0  0  0  1  4  6  2  1  0    0  0  1  1  2  3  1  1  0  
  0  0  4 27 27 18  3  0  0    0  0  3 10 48 57  6  1  0    0  0  1  5 34 31  4  1  0  
  0  1 17 63 32 14  2  0  0    0  1 11 35 77 58  4  0  0    0  1  2 16100 52  3  0  0  
  0  1 10 24  7  2  1  0  0    0  1  8 24 19  7  1  0  0    0  1  3 10 36 13  1  0  0  
  0  0  2  2  1  1  1  0  0    0  1  2  3  2  1  1  0  0    0  1  1  3  4  2  0  1  0  
  0  0  1  0  0  0  1  0  0    0  0  2  0  0  1  0  0  0    0  0  1  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  0  0  0  0  0  
!Region 4: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0 -1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  0  0  0  0  0    0  0  0  0  0 -1  0  0  0  
  0  0  0  0  1  1  1  0  0    0  0  1  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  1  1  3  7  4  2  1  0    0  0  1  2  1  1  2  2  0    0  0  0  1  0  0  0  1  0  
  0  1  1  7 31 12  2  0  0    0  0  1  3  2  1  1  1  0    0  0  0  1  1  1  0  1  0  
  0  1  1  5 16  5  0  0  0    0  0  0  2  3  1  0  1  0    0  0  0  0  0  1  0  0  0  
  0  0  1  3  4  1  0  0  0    0  0  1  2  2  1  0  1  0    0  0  1  0  0  0  0  0  0  
  0  0  1  2  1  0  0  0  0    0  0  1  2  1  0  0  0  0    0  0  1  1  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 99.58   Thresh = 0.020   Blend = F   #Contributing = 795   InitialProfileWt = 0.000
Region 5
Sum = 88657.5;   Maximum = 12535.1;   FM = 0.725
!Region 5: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  2  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  0  0  0  0  0    0  0  1  8  6  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  6  3  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  0  0  0  0  0  0    0  0  1  1  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 5: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  1  0  0  
  0  0  0  4 12  4  0  0  0    0  0  0  6 39 16  1  0  0    0  0  0  3 24 14  1  0  0  
  0  0  2 26 36  6  0  0  0    0  0  1 30100 28  1  0  0    0  0  0 10 56 27  1  0  0  
  0  0  2 18 16  1  0  0  0    0  0  1 17 30  5  0  0  0    0  0  0  5 14  6  1  0  0  
  0  0  1  2  1  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 5: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  1  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  5  5  1  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2 12 10  1  0  0    0  0  0  1  3  2  1  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  2  4  3  1  0  0    0  0  0  1  2  2  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 124.06   Thresh = 0.020   Blend = F   #Contributing = 837   InitialProfileWt = 0.000
Region 6
Sum = 114121;   Maximum = 12521.1;   FM = 0.775
!Region 6: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  5  6  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  2 13 16  3  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  5  6  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 6: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  2 13 25  8  0  0  0    0  0  1 12 38 16  1  0  0    0  0  0  6 26 12  1  0  0  
  0  0  3 34 68 23  1  0  0    0  0  2 35100 38  2  0  0    0  0  1 15 63 28  2  0  0  
  0  0  1 11 21  7  0  0  0    0  0  1 12 28 11  1  0  0    0  0  0  5 19  9  1  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 6: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  8  5  1  0  0    0  0  0  1  3  2  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  4 19 12  2  0  0    0  0  0  2  7  4  1  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  2  7  4  1  0  0    0  0  0  1  4  2  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 76.07   Thresh = 0.020   Blend = F   #Contributing = 976   InitialProfileWt = 0.000
Region 7
Sum = 59270.5;   Maximum = 7236.4;   FM = 0.762
!Region 7: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  0  0  0  0  0    0  0  2  7  6  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  9  9  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  2  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 7: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  2  0  0  0  0    0  0  0  2  3  1  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  2 19 25  6  1  0  0    0  0  2 20 39 14  1  0  0    0  0  0  5 15 11  1  0  0  
  0  0  2 26 53 24  1  0  0    0  0  2 28100 58  3  0  0    0  0  0  6 39 32  3  0  0  
  0  0  0  5 17 11  1  0  0    0  0  0  6 35 25  2  0  0    0  0  0  2 13 12  2  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 7: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  4  4  1  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  8  8  1  0  0    0  0  0  1  3  2  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  3  3  1  1  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  1  1  0    0  0  0  0  0  0  0  1  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 31.77   Thresh = 0.020   Blend = F   #Contributing = 433   InitialProfileWt = 0.000
Region 8
Sum = 16419.5;   Maximum = 1196.9;   FM = 0.785
!Region 8: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  0  1  0  0  0  0  0    0  0  1  3  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  2  2  1  0  0  0    0  1  4 20 12  2  1  0  0  
  0  0  0  0  1  0  0  0  0    0  0  1  4  3  1  0  0  0    0  0  4 33 22  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  1  0    0  0  1  9  7  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 8: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  2  7  5  2  1  0  0    0  1  2  7  8  4  1  0  0    0  0  1  4  8  4  1  0  0  
  0  0 10 46 29 11  2  0  0    0  0  7 30 57 38  3  0  0    0  1  2  8 54 37  2  0  0  
  0  0  9 52 51 35  3  0  0    0  0  4 21 93100  7  1  0    0  0  1  6 63 54  5  1  0  
  0  0  2 10 20 17  2  0  0    0  0  1  4 33 40  3  1  0    0  0  1  2 10 13  3  1  0  
  0  0  0  1  1  1  1  1  0    0  0  0  1  2  2  1  1  0    0  0  0  0  1  1  1  1  0  
  0  0  0  1  1  0  1  0  0    0  0  0  0  1  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0  
!Region 8: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  3  5  2  0  0  0    0  0  0  2  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4 13  7  1  0  0    0  0  1  2  2  1  0  0  0    0  0  1  1  0  0  0  0  0  
  0  0  0  2  9  7  3  1  0    0  0  0  1  1  1  1  1  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  1  1  0    0  0  0  0  0  0  1  1  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 26.93   Thresh = 0.020   Blend = F   #Contributing = 66   InitialProfileWt = 0.000
Region 9
Sum = 11421.3;   Maximum = 952.4;   FM = 0.727
!Region 9: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  1  0  0  
  0  0  0  0  0  1  1  1  0    0  0  0  0  0  1  1  0  0    0  0  1  0  0  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  2  2  1  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  2  0  0  0  0    0  0  8 19  6  1  1  0  0  
  0  1  0  1  0  0  0  0  0    0  2  2  7  7  1  0  1  0    0  1 10 41 23  2  1  0  0  
  0  0  1  1  0  0  0  0  0    0  0  1  3  3  0  0  1  0    0  0  2 13 11  1  1  1  0  
  0  0  0  0  0  0  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  1  1  0  
  0  0  0  0  0  0  1  0  0    0  0 -1  0  0  0  0  0  0    0  0  0  0  0  0  1  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 9: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  1  0  1  0  0  0    0  0  1  1  1  0  0  1  0    0  0  0  1  1  0  0  0  0  
  0  1  3  3  2  2  0  0  0    0  2  2  2  5  3  1  0  0    0  1  1  3  7  2  1  0  0  
  0  1 15 24  8  9  3  1  0    0  2  8  9 34 39  5  1  0    0  2  2 10 51 23  2  0  0  
  0  1 18 46 21 23  5  0  0    0  1  7 12 50100 15  1  0    0  1  2  8 57 44  6  0  0  
  0  1  3 13  9  9  3  1  0    0  1  2  3 11 32  7  1  0    0  1  1  2  9 11  3  0  0  
  0  0  0  1  1  1  1  1  0    0  0  1  1  1  2  2  1  0    0  0  0  1  1  1  1  0  0  
  0  0  1  1  1  1  1  0  0    0  0  1  1  1  1  0  0  0    0  0  1  1  1  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  1  1  0  0  0  0  0    0  0  0  1  0  0  0  0  0  
!Region 9: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  3  3  1  1  0  0    0  0  1  1  0  0  0  0  0    0  0  1  0  0  0  0  0  0  
  0  0  1  8 17  4  1  0  0    0  0  2  3  2  1  1  0  0    0  0  1  1  0  0  1  0  0  
  0  0  1  5 14  5  2  1  0    0  0  2  1  1  1  2  1  0    0  0  1  0  0  0  1  0  0  
  0  0  1  2  2  1  1  0  0    0  0  0  0  1  0  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  1  1  0  0    0  0  0  0  1  0  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  0  1  0  0  0    0  0  0  0  0  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

Overall Integration Statistics for this run ("*" => excluded from output)

Spots with topped/rescanned pixels:           184
Total topped/rescanned pixels:               1490
Minimum pixel ceiling(frame):              163809(mo_DK_Zucker2_01_0001.sfrm)
Maximum pixel ceiling(frame):              163809(mo_DK_Zucker2_01_0001.sfrm)

Total spots predicted:                      11114
Spots with absolute HKL > 511:                  0*
Spots outside resolution limit:                 0*
Spots outside active detector area:          1091*
Outside frame limits:                         172*
Spots exceeding frame queue size:               0*
Collisions(same XY, adjacent frame):            0*
Spots exceeding dynamic range:                140*
Spots with too many spot components:            0*
Spots with large Lorentz factor:                0*
Spots with too much missing I:                  0*
Spots with too few BG pixels:                   0*
Spots below I/sigma threshold:                  0*
Spots left in Write-Behind Cache:               0*
Spots with unwanted components:                 0*
Total unwanted components:                      0*
Good spots written:                          9674
Total spot components written:               9674
Twin overlaps integrated:                       0
Partial, strong, full overlaps:                 0       0       0
Full overlaps collapsed to singlet:             0
Singlets (used in stats below):              9674
Twin overlaps written:                          0

Average Intensity:                       2847.139
Average I/sigma:                            34.26
% over "strong" threshold:                  67.74
% less than 2 sigma:                         5.33
% which spanned more than 1 frame:          93.15

Average X,Y,Z positional errors:            -0.02   -0.04    0.00
RMS X,Y,Z positional errors:                 0.25    0.37    0.14
% X,Y,Z more than 0.5 pixel:                 4.22    4.58    0.52
% X,Y,Z more than 1.0 pixel:                 0.67    1.41    0.07

Avg % profile volume populated:             94.78
Avg % profile volume integrated:             9.19
Avg % profile missing I:                     5.00
Avg % profile missing volume:                5.22
Avg % volume overlap in H,K,L:               0.00    0.00    0.00
Percent of profile used in X,Y,Z:           77.78   66.67   88.89
Max % intensity on XYZ boundaries:           0.79    1.45    2.72

Average spot-shape correlation:             0.753
RMS spot-shape correlation:                 0.773

Profile Shape Correlation
I/sigma from     to    Correl       +/-       #
         0.0    1.0     0.210     0.157     262
         1.0    2.0     0.410     0.138     254
         2.0    4.0     0.618     0.116     546
         4.0    8.0     0.745     0.109    1377
         8.0   16.0     0.795     0.107    2337
        16.0   32.0     0.811     0.111    2429
        32.0   64.0     0.819     0.126    1639
        64.0  128.0     0.835     0.146     638
       128.0  256.0     0.857     0.140     192

Write-behind Cache Diagnostics
Entered in Write-Behind Cache:                  0
Removed from WBC:                               0
Partial overlaps from WBC:                      0
Exceeding queue size from WBC:                  0
With > 12 components from WBC:                  0

Elapsed since program start (sec):          9.076
Elapsed since INTEGRATE command (sec):      7.436
Integration time, this run (sec):           5.348
Time in unit-cell LS (sec):                 0.125
Per-frame integration time (sec):           0.017


Integration completed normally ======================== 04/16/2019 16:17:22


Applying profile correlation filter from D:\frames\guest\DK_Zucker2\work\unsorted.raw to D:\frames\guest\DK_Zucker2\work\corrfilt.raw
Scale of 1.0752647 will be applied to LS-fit intensities

Number of spots read:                         9674
Number of LS-fit intensities scaled:          2533
Number rejected due to poor spot shape:         37
Number unwritable (I, sigma too large):          0
Number written:                               9637

Sorting Reflection File ============================== 04/16/2019 16:17:23
Integration of DK_zucker

Sorting input files:
              1 D:\frames\guest\DK_Zucker2\work\corrfilt.raw

Sorting to output file \frames\guest\DK_Zucker2\work\DK_Zucker2_01.raw

Component 1 in sample 1 (1 in file):
Point group "2/m(B-unique)", #3 (internal number)
4 symmetry operators
    1 0 0   -1 0 0   -1 0 0    1 0 0
    0 1 0    0 1 0    0-1 0    0-1 0
    0 0 1    0 0-1    0 0-1    0 0 1

Beginning sort with 128MB memory requested...
      9637 spot components in 9637 spots read from file   1--D:\frames\guest\DK_Zucker2\work\corrfilt.raw
      9637 spot components in 9637 spots written to file D:\frames\guest\DK_Zucker2\work\DK_Zucker2_01.raw

Computing Reflection File Statistics ========== 04/16/2019 16:17:23
Integration of DK_zucker

...................................................................................
Statistics for reflections in DK_Zucker2_01.raw
File is in BrukerAXS area detector ASCII format

Number of lines read (incl comments) =             9637
Number of reflection records read =                9637
Number of records with bad component number =         0
Number of records with bad status value =             0
Number of spots used =                             9637
Number of spot components used =                   9637

...................................................................................
Integration of DK_zucker
Statistics for sample 1 of 1 in DK_Zucker2_01.raw

Lattice:  P (Primitive)
Point group "2/m(B-unique)", #3 (internal number)
4 symmetry operators
    1 0 0   -1 0 0   -1 0 0    1 0 0
    0 1 0    0 1 0    0-1 0    0-1 0
    0 0 1    0 0-1    0 0-1    0 0 1


Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file
Cell constants are constrained so that consistent sin(theta) is computed for symmetry equivalents.
Components in the sample map (* marks current component)
   Component   Wanted        A        B        C    Alpha     Beta    Gamma   PointGp         Constraints
     1.1(1)*        Y    7.714    8.664   10.812   90.000  103.003   90.000      2/mB   Monoclinic B-uniq

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
     Det X      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000     56     21     55     23  1.8  9236.962 154.20   12.20 0.068  0.017  6.3 0.000 0.138  0.00 .10-.00 .06 .23 .22 .13
    32.000    169     69    164     78  0.6 10047.866 132.95   12.67 0.056  0.009  6.2 0.000 0.117  0.00 .03-.07 .07 .20 .34 .16
    64.000    334    167    312    193  0.0  8610.683 102.28   13.53 0.075 -0.004  5.9 0.000 0.155  0.00-.03-.04 .04 .08 .13 .10
    96.000    632    350    563    421  0.8  8147.604  83.84   14.80 0.089 -0.008  5.8 0.000 0.182  0.00-.02-.04 .03 .09 .22 .10
   128.000    957    573    802    728  1.6  4033.248  47.31   15.07 0.096 -0.003  4.6 0.000 0.194  0.00 .01-.04 .02 .21 .23 .11
   160.000   1544    814   1215   1143  1.5  3459.130  36.24   15.26 0.084  0.004  2.4 0.000 0.180  0.00-.00-.03 .02 .07 .27 .11
   192.000   1735    710   1315   1130  4.4  2142.292  23.41   14.42 0.078  0.004  1.5 0.000 0.166  0.00-.02-.05 .00 .11 .30 .13
   224.000   1643    492   1230    906  8.6  1150.791  14.71   13.15 0.062  0.002  0.8 0.000 0.130  0.00-.01-.03-.01 .18 .30 .16
   256.000   1303    330   1030    603  8.7  1019.199  13.34   11.99 0.058  0.002  0.7 0.000 0.123  0.00-.03-.04-.02 .24 .28 .16
   288.000    900    235    776    359 11.6   842.793  11.29   11.11 0.073 -0.001  0.8 0.000 0.150  0.00-.02-.07-.02 .44 .63 .19
   320.000    340     94    315    119  9.4   641.289  11.25   10.08 0.074 -0.007  0.8 0.000 0.147  0.00-.15-.00 .02 .64 .83 .19
   352.000     24      9     24      9 12.5   509.150   8.35    9.36 0.115 -0.054  1.1 0.000 0.230  0.00-.54 .15 .05 1.7 2.0 .27
   384.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   416.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   448.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   480.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   512.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
     Det Y      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000     93     65     93     66  1.1  1288.938  23.20    9.47 0.050 -0.011  1.2 0.000 0.100  0.00-.27 1.3 .26 .85 2.3 .45
    32.000    181    118    181    118  4.4  1598.312  28.96    9.70 0.041 -0.006  1.1 0.000 0.081  0.00-.10-.03-.01 .56 .77 .17
    64.000    270    171    270    172  3.7  1868.502  29.76   10.11 0.045  0.017  1.3 0.000 0.091  0.00-.01-.13-.03 .29 .43 .14
    96.000    384    249    384    249  3.9  2388.856  34.07   10.76 0.044  0.023  1.4 0.000 0.089  0.00-.02-.07-.03 .23 .29 .13
   128.000    619    393    616    396  5.7  2635.639  34.79   11.75 0.058  0.035  1.8 0.000 0.116  0.00-.01-.03-.02 .19 .19 .12
   160.000    913    542    902    553  5.6  3221.384  38.08   13.19 0.069  0.042  2.1 0.000 0.138  0.00-.03 .01-.01 .18 .13 .13
   192.000   1233    688   1206    715  4.5  3233.896  35.22   14.76 0.068  0.037  1.9 0.000 0.138  0.00-.02 .00-.01 .17 .09 .13
   224.000   1392    770   1358    804  4.8  2959.009  31.51   15.75 0.073  0.023  2.0 0.000 0.149  0.00-.03-.02-.00 .15 .08 .11
   256.000   1373    780   1335    821  5.8  3118.283  32.89   15.62 0.090 -0.016  2.6 0.000 0.190  0.00-.02-.05 .01 .16 .09 .12
   288.000   1146    662   1123    689  6.5  3086.239  34.77   14.45 0.095 -0.033  2.6 0.000 0.202  0.00-.00-.07 .01 .19 .12 .14
   320.000    823    473    814    484  6.1  2957.390  35.88   12.84 0.106 -0.043  4.0 0.000 0.218  0.00 .01-.09 .01 .23 .16 .12
   352.000    557    301    556    303  5.7  2300.206  31.97   11.45 0.117 -0.048  2.9 0.000 0.234  0.00 .02-.08 .01 .23 .22 .14
   384.000    358    196    358    196  6.7  2261.979  33.63   10.58 0.148 -0.073  3.6 0.000 0.297  0.00-.01-.11 .03 .29 .34 .14
   416.000    199    103    199    103  5.5  1768.881  28.01   10.00 0.174 -0.074  4.1 0.000 0.348  0.00 .03-.20 .06 .40 .77 .23
   448.000     75     33     75     33  4.0  1767.472  29.51    9.53 0.174 -0.052  4.8 0.000 0.348  0.00 .06-.02 .01 .44 .78 .18
   480.000     21     10     21     10  0.0  1338.442  19.76    9.37 0.254 -0.159  5.6 0.000 0.508  0.00-1.1-2.6 .40 2.0 3.8 .60
   512.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
     Det R      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    645    286    621    310  8.5  1114.788  13.33   13.97 0.055  0.008  0.7 0.000 0.114  0.00-.04-.04-.02 .18 .10 .14
    30.000   1649    739   1550    838  7.9  1446.701  16.26   14.18 0.063  0.012  0.9 0.000 0.130  0.00-.02-.04-.02 .20 .11 .15
    60.000   2042   1077   1894   1225  7.4  2155.903  24.05   14.49 0.073  0.013  1.5 0.000 0.154  0.00-.02-.03-.01 .19 .13 .13
    90.000   1791   1062   1667   1186  3.0  2599.753  30.15   14.22 0.094  0.002  2.3 0.000 0.191  0.00-.01-.04 .01 .17 .16 .12
   120.000   1316    780   1251    846  4.7  3878.983  45.57   13.30 0.090 -0.009  3.5 0.000 0.181  0.00 .01-.05 .00 .21 .19 .12
   150.000    988    578    959    611  3.7  4488.139  57.01   12.40 0.087 -0.010  4.4 0.000 0.178  0.00-.01-.08 .02 .25 .29 .13
   180.000    614    341    606    353  2.3  4668.918  64.24   11.62 0.077 -0.003  3.6 0.000 0.157  0.00-.01-.11 .03 .26 .52 .16
   210.000    360    194    359    198  3.1  4510.837  70.43   10.75 0.068 -0.002  3.4 0.000 0.137  0.00 .00 .04 .02 .33 .63 .15
   240.000    176    105    176    107  0.6  4998.844  80.88   10.34 0.059  0.000  3.4 0.000 0.117  0.00-.35 .17 .15 .00 2.0 .35
   270.000     56     38     56     38  0.0  5234.714  99.38    9.74 0.092 -0.005  4.9 0.000 0.184  0.00 .12 .06 .10 .43 .98 .30
   300.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   Quadrnt      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     1.000   3313   1626   2837   2108  4.1  3551.134  40.26   14.34 0.105 -0.037  3.6 0.000 0.235  0.00 .01-.08 .02 .16 .21 .13
     2.000   1238    413   1121    530 11.1   880.531  12.10   11.39 0.068 -0.010  0.8 0.000 0.142  0.00-.05-.12-.01 .43 .59 .18
     3.000   3757   1835   3079   2514  3.4  3535.813  40.29   14.32 0.065  0.033  2.1 0.000 0.156  0.00-.03-.00-.00 .12 .32 .13
     4.000   1329    428   1197    560  8.7   923.017  12.58   11.41 0.060  0.009  0.7 0.000 0.125  0.00-.05 .03-.02 .42 .51 .17
     5.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
    Region      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     1.000   4555   1864   3910   2509  7.5  1766.826  19.95   14.30 0.070  0.012  1.2 0.000 0.152  0.00-.02-.04-.01 .19 .12 .14
     2.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     3.000    189     63    184     68 11.1   625.184  10.68   10.19 0.063 -0.020  0.7 0.000 0.129  0.00-.10-.17 .00 .65 .70 .19
     4.000    631    326    616    341  7.9  1058.993  15.46   10.61 0.107 -0.052  1.5 0.000 0.219  0.00-.02-.18 .02 .39 .80 .19
     5.000   1028    578    947    660  1.8  4120.530  50.63   12.87 0.133 -0.058  5.9 0.000 0.284  0.00 .04-.08 .04 .21 .23 .13
     6.000   1021    494    833    688  0.7  7936.360  78.97   16.98 0.088 -0.002  5.3 0.000 0.189  0.00 .00-.03 .05 .09 .05 .09
     7.000   1208    786   1081    913  0.9  4248.766  51.67   12.99 0.058  0.037  2.3 0.000 0.130  0.00-.03-.03-.01 .11 .27 .11
     8.000    795    415    762    449  5.7  1137.509  17.02   10.54 0.053  0.011  0.8 0.000 0.106  0.00-.04 .09 .01 .37 .82 .20
     9.000    210     78    204     84 11.0   741.455  11.88   10.22 0.066  0.003  0.7 0.000 0.135  0.00-.09 .06 .00 .62 .61 .18
    10.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
    Frame#      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     2.120    470     63    468     71  4.9  2925.299  34.81   13.84 0.065 -0.012  2.4 0.000 0.170  0.00-.02 .01 .00 .24 .35 .14
    17.053    485     96    481    101  6.2  2578.722  32.03   13.50 0.088 -0.019  2.5 0.000 0.186  0.00-.01-.01 .01 .26 .32 .13
    31.986    469    144    457    158  5.5  2746.193  33.84   13.33 0.080 -0.027  2.8 0.000 0.193  0.00-.01-.04 .01 .27 .34 .13
    46.919    488    245    470    264  5.5  2496.301  31.17   13.06 0.095 -0.034  2.2 0.000 0.197  0.00 .01-.06-.00 .20 .24 .13
    61.852    509    401    482    428  4.5  2803.294  33.96   12.95 0.071 -0.042  1.8 0.000 0.150  0.00-.02-.04 .01 .24 .43 .15
    76.785    475    411    459    427  5.5  2472.529  31.46   12.81 0.087 -0.061  1.9 0.000 0.178  0.00 .01-.07 .01 .29 .64 .18
    91.718    484    429    477    436  5.0  2369.508  30.66   12.88 0.085 -0.062  1.9 0.000 0.171  0.00-.01-.05-.00 .22 .28 .14
   106.651    478    429    471    436  4.8  2706.537  33.34   12.83 0.074 -0.057  2.0 0.000 0.149  0.00-.02-.01-.01 .39 .59 .16
   121.584    483    418    473    428  5.2  2526.045  32.09   12.91 0.084 -0.065  2.0 0.000 0.169  0.00-.02-.04-.00 .23 .28 .14
   136.517    488    414    481    421  5.3  3032.729  36.12   13.06 0.067 -0.037  2.3 0.000 0.134  0.00 .00-.04-.02 .20 .25 .13
   151.450    476    404    474    406  6.9  2610.295  32.81   13.06 0.065 -0.032  2.4 0.000 0.131  0.00-.02-.00 .00 .23 .52 .16
   166.383    483    396    482    397  6.8  2712.658  33.49   13.20 0.050 -0.000  1.5 0.000 0.100  0.00-.01-.01-.00 .21 .22 .13
   181.316    487    373    487    373  6.4  3031.563  35.52   13.38 0.057  0.014  1.6 0.000 0.114  0.00-.03-.01 .01 .23 .27 .13
   196.249    470    299    470    299  4.0  2828.644  33.20   13.65 0.066  0.027  1.8 0.000 0.131  0.00-.01-.01-.00 .21 .24 .14
   211.182    481    276    481    276  5.2  2735.171  32.14   13.79 0.079  0.047  2.4 0.000 0.158  0.00-.02-.05-.00 .25 .33 .14
   226.115    492    230    492    230  5.7  3330.751  37.53   14.13 0.091  0.055  3.3 0.000 0.182  0.00-.02-.07 .00 .25 .34 .15
   241.048    472    180    472    180  3.4  3254.227  35.41   14.27 0.100  0.048  3.8 0.000 0.201  0.00-.03-.05 .01 .22 .31 .13
   255.981    493    156    493    156  5.3  3253.192  35.33   14.53 0.115  0.070  5.5 0.000 0.230  0.00-.04-.07 .02 .28 .45 .13
   270.914    472    123    472    123  5.7  3201.872  35.63   14.76 0.116  0.063  6.1 0.000 0.231  0.00-.06-.08 .03 .28 .37 .14
   285.847    482    100    481    102  5.2  3170.267  34.08   15.05 0.120  0.051  6.3 0.000 0.241  0.00-.04-.08 .03 .21 .27 .13
   300.780

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   Rot.Ang      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    10.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    20.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    30.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    40.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    50.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    60.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    70.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    80.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    90.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   100.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   110.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   120.000      5      0      5      1  0.0 12611.270  92.83   17.17 0.039  0.009  4.8 0.000 0.000  0.00-.05 .01-.06 .13 .03 .07
   130.000    626     86    624     93  5.8  2664.172  32.44   13.73 0.075 -0.013  2.3 0.000 0.184  0.00-.01 .01 .01 .24 .34 .14
   140.000    654    181    645    192  5.5  2596.214  32.14   13.36 0.086 -0.023  2.7 0.000 0.187  0.00-.01-.03 .01 .29 .35 .13
   150.000    650    298    625    325  5.5  2683.597  33.27   13.17 0.085 -0.032  2.2 0.000 0.187  0.00 .00-.05 .00 .19 .25 .13
   160.000    663    535    629    569  4.8  2875.574  34.59   12.94 0.078 -0.049  1.9 0.000 0.164  0.00-.01-.05 .00 .24 .47 .15
   170.000    648    559    622    585  5.2  2247.037  29.44   12.85 0.083 -0.062  1.9 0.000 0.171  0.00-.01-.07 .00 .27 .50 .16
   180.000    645    566    625    586  4.5  2725.130  33.67   12.84 0.078 -0.059  2.0 0.000 0.158  0.00-.02-.02-.01 .36 .54 .16
   190.000    651    547    629    569  5.1  2585.671  32.52   12.93 0.079 -0.056  2.2 0.000 0.160  0.00-.01-.04-.01 .22 .25 .14
   200.000    653    546    635    564  6.7  2873.275  35.11   13.05 0.064 -0.031  2.3 0.000 0.129  0.00-.01-.03-.01 .21 .44 .15
   210.000    638    521    631    528  6.9  2596.271  32.24   13.15 0.054 -0.006  1.5 0.000 0.108  0.00-.01 .00 .00 .22 .30 .14
   220.000    635    456    632    459  5.4  3086.516  36.15   13.48 0.057  0.017  1.6 0.000 0.115  0.00-.03-.01 .01 .22 .25 .13
   230.000    660    397    660    397  4.2  2794.860  32.50   13.76 0.074  0.039  2.2 0.000 0.147  0.00-.01-.03-.00 .20 .28 .14
   240.000    644    309    644    309  5.7  3294.795  37.02   14.09 0.090  0.056  3.2 0.000 0.180  0.00-.02-.07 .01 .27 .34 .14
   250.000    642    229    642    229  4.2  3068.895  33.91   14.38 0.107  0.053  4.3 0.000 0.214  0.00-.03-.06 .01 .27 .42 .13
   260.000    644    178    644    178  5.6  3315.007  36.21   14.61 0.117  0.067  5.9 0.000 0.234  0.00-.05-.08 .02 .26 .37 .14
   270.000    579    126    578    128  5.2  3151.861  34.15   15.03 0.118  0.053  6.3 0.000 0.238  0.00-.04-.07 .03 .21 .26 .13
   280.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   290.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   300.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   310.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   320.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   330.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   340.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   350.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   360.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
     Hours      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.020    459     61    457     69  4.6  2919.210  34.72   13.82 0.060 -0.010  2.3 0.000 0.158  0.00-.02 .01 .01 .25 .35 .14
     0.144    476     95    473     99  6.5  2594.160  32.20   13.52 0.095 -0.022  2.6 0.000 0.200  0.00-.01-.01 .00 .26 .32 .14
     0.269    489    148    477    162  5.5  2737.828  33.75   13.34 0.078 -0.026  2.8 0.000 0.187  0.00-.01-.04 .01 .27 .33 .13
     0.393    473    233    456    251  5.7  2517.816  31.50   13.07 0.095 -0.033  2.2 0.000 0.196  0.00 .01-.05-.00 .20 .24 .13
     0.518    529    416    499    446  4.3  2757.388  33.40   12.95 0.072 -0.043  1.7 0.000 0.151  0.00-.02-.04 .01 .24 .42 .15
     0.642    461    401    448    414  5.2  2498.585  31.70   12.82 0.086 -0.060  1.9 0.000 0.176  0.00 .01-.07 .01 .29 .65 .18
     0.767    497    438    488    447  5.2  2372.489  30.71   12.88 0.086 -0.063  1.9 0.000 0.173  0.00-.01-.05-.00 .22 .28 .14
     0.891    464    416    457    423  5.0  2695.424  33.20   12.87 0.072 -0.055  2.0 0.000 0.145  0.00-.02-.01-.01 .40 .60 .16
     1.016    507    439    497    449  5.3  2532.542  32.10   12.87 0.085 -0.065  2.0 0.000 0.171  0.00-.02-.04-.00 .22 .28 .14
     1.140    464    395    458    401  5.2  2992.399  35.76   13.06 0.068 -0.039  2.4 0.000 0.135  0.00 .00-.04-.01 .20 .25 .13
     1.265    469    397    467    399  6.8  2683.362  33.65   13.08 0.066 -0.031  2.5 0.000 0.132  0.00-.02-.01 .00 .23 .52 .16
     1.389    500    412    499    413  6.8  2701.300  33.30   13.19 0.050 -0.001  1.5 0.000 0.099  0.00-.01-.01-.00 .21 .24 .13
     1.514    472    362    472    362  6.4  3056.457  35.87   13.38 0.057  0.013  1.6 0.000 0.114  0.00-.03-.01 .01 .23 .27 .13
     1.638    488    313    488    313  4.1  2812.582  32.94   13.66 0.065  0.027  1.8 0.000 0.130  0.00-.01-.01-.01 .20 .24 .13
     1.763    461    264    461    264  5.2  2787.626  32.54   13.76 0.079  0.048  2.4 0.000 0.158  0.00-.03-.05-.00 .25 .33 .14
     1.887    515    242    515    242  5.6  3354.196  37.78   14.14 0.090  0.055  3.3 0.000 0.181  0.00-.02-.07 .00 .25 .33 .14
     2.012    459    174    459    174  3.5  3159.472  34.74   14.25 0.101  0.048  3.8 0.000 0.203  0.00-.03-.05 .01 .23 .31 .13
     2.136    516    161    516    161  5.2  3196.383  34.88   14.48 0.114  0.069  5.5 0.000 0.228  0.00-.04-.06 .01 .28 .45 .13
     2.261    453    120    453    120  5.7  3266.037  36.05   14.82 0.117  0.064  6.1 0.000 0.235  0.00-.06-.09 .03 .28 .37 .14
     2.385    485    101    484    103  5.2  3160.023  34.02   15.06 0.119  0.051  6.2 0.000 0.239  0.00-.04-.08 .03 .21 .27 .13
     2.510

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
    Batch#      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     1.000   9637   2849   6781   5712  5.4  2839.654  33.81   13.55 0.081  0.000  2.4 0.000 0.177  0.00-.02-.04 .00 .25 .37 .14
     2.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
    Correl      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000     95     36     87     44100.0     3.102   0.10   12.0012.209-22.943 14.3 0.00027.887  0.00 .04-.09 .03 .63 .41 .23
     0.100     94     32     90     37100.0    20.031   0.54   12.52 0.638 -0.130  0.4 0.000 1.329  0.00-.04-.04 .02 .39 .31 .21
     0.200     93     43     89     47100.0    33.828   0.94   12.43 1.967 -0.786  5.3 0.000 4.302  0.00-.04-.04 .00 .38 .30 .22
     0.300    119     41    114     46 84.0    57.204   1.47   12.61 0.311 -0.035  0.4 0.000 0.640  0.00-.01 .02-.05 .35 .25 .23
     0.400    224    116    217    125 32.6  2192.026  37.10   14.00 0.107 -0.013  2.4 0.000 0.235  0.00 .01 .02-.01 .31 .23 .20
     0.500    596    319    580    336  7.7  2217.315  30.02   14.32 0.079 -0.004  1.9 0.000 0.159  0.00-.01-.02-.02 .31 .34 .17
     0.600   1720    884   1631    973  0.9  2149.605  25.08   14.30 0.073  0.004  1.6 0.000 0.147  0.00 .01-.03-.04 .19 .16 .13
     0.700   2108   1095   1967   1238  0.0  2700.835  29.21   14.43 0.081  0.004  2.0 0.000 0.168  0.00-.03-.04-.00 .20 .28 .13
     0.800   2923   1506   2617   1816  0.0  3350.259  36.74   13.74 0.083  0.003  2.5 0.000 0.168  0.00-.04-.04 .03 .21 .27 .12
     0.900   1665    975   1593   1050  0.0  3818.373  49.33   11.26 0.080 -0.007  3.1 0.000 0.166  0.00-.02-.07 .02 .31 .68 .16
     1.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   Missing      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000   8626   2772   6213   5192  5.0  2967.344  35.48   13.73 0.080  0.001  2.3 0.000 0.174  0.00-.01-.04-.00 .18 .20 .13
     0.050    126     59    124     61  6.3  1441.534  19.76   11.98 0.065  0.005  1.4 0.000 0.135  0.00-.10-.04 .01 .34 .54 .16
     0.100    115     56    113     58  4.3  1713.569  21.70   12.55 0.064 -0.016  1.6 0.000 0.130  0.00-.01-.11-.02 .34 .49 .18
     0.150     83     51     83     51  8.4  1785.587  23.84   11.72 0.099  0.006  2.1 0.000 0.198  0.00-.19-.01 .08 .51 .94 .22
     0.200    122     68    121     69  8.2  3819.611  46.79   13.09 0.132 -0.021 10.7 0.000 0.239  0.00-.07-.10 .06 .59 .70 .18
     0.250    180     87    176     91  6.7  1504.308  17.33   12.07 0.124 -0.028  4.4 0.000 0.255  0.00-.03 .02 .03 .37 .51 .18
     0.300     41     17     41     17  0.0  1772.369  20.68   11.43 0.133 -0.038  2.4 0.000 0.267  0.00-.05-.12 .06 .40 .74 .22
     0.350     70     32     70     32 12.9  1328.953  15.03   11.94 0.089 -0.037  1.6 0.000 0.178  0.00-.21-.09 .09 .62 1.1 .25
     0.400     85     43     85     44  9.4  1305.571  13.92   11.89 0.100 -0.001  1.1 0.000 0.203  0.00-.12 .42 .05 .57 1.5 .34
     0.450     49     24     49     24 12.2  1141.821  11.66   11.49 0.095 -0.014  1.1 0.000 0.190  0.00 .02 .12 .03 .41 .96 .26
     0.500     68     35     67     36 13.2   998.115   9.45   11.62 0.108 -0.000  1.1 0.000 0.216  0.00-.10-.18 .07 .77 1.4 .30
     0.550     72     36     71     37 12.5  1462.239  12.52   11.20 0.158 -0.029  4.0 0.000 0.316  0.00-.18-.21 .09 1.1 1.9 .34
     0.600      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.650      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.700      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.750      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.800      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.850      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.900      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.950      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     1.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
    Frac Z      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    586    296    576    308  5.5  2429.271  31.07   13.02 0.087 -0.002  1.9 0.000 0.177  0.00-.03-.07 .02 .30 .50 .14
     0.050    519    307    503    324  6.7  2048.328  27.20   12.73 0.069  0.002  1.7 0.000 0.142  0.00-.03-.03 .01 .25 .33 .13
     0.100    407    227    402    233  4.4  2955.079  35.40   13.33 0.080  0.003  2.4 0.000 0.162  0.00-.03-.03 .02 .21 .39 .13
     0.150    304    189    300    193  4.6  3452.392  39.01   13.38 0.078 -0.017  2.4 0.000 0.154  0.00-.03-.04 .03 .24 .44 .14
     0.200    311    185    308    188  5.5  3471.974  36.04   13.61 0.083 -0.002  3.0 0.000 0.162  0.00 .01-.07 .03 .23 .23 .13
     0.250    406    234    399    241  1.7  3338.366  33.49   13.95 0.082 -0.001  3.5 0.000 0.167  0.00-.02-.04 .03 .18 .18 .11
     0.300    565    343    555    354  2.3  2738.770  30.04   13.43 0.075  0.001  2.1 0.000 0.150  0.00-.03-.08 .03 .24 .49 .14
     0.350    705    379    692    394  2.8  2464.706  28.52   13.44 0.074  0.004  1.9 0.000 0.150  0.00-.03-.05 .01 .21 .25 .15
     0.400    816    483    794    506  6.0  2317.913  28.84   13.55 0.076  0.003  1.9 0.000 0.154  0.00-.02-.05-.00 .21 .23 .15
     0.450    686    368    673    381  7.1  2251.916  29.00   13.63 0.086 -0.005  2.4 0.000 0.172  0.00-.02-.03-.00 .26 .30 .15
     0.500    836    440    814    462  8.6  2713.984  34.61   13.74 0.091 -0.003  2.4 0.000 0.179  0.00-.02-.01-.00 .24 .29 .16
     0.550    650    392    634    408  8.5  2982.231  37.62   13.74 0.078 -0.004  2.4 0.000 0.160  0.00-.01-.02-.02 .26 .36 .16
     0.600    515    285    507    295  7.4  3109.286  37.24   14.01 0.092  0.015  2.8 0.000 0.185  0.00-.03-.02-.03 .38 .47 .16
     0.650    364    219    363    221  6.6  3577.668  40.59   13.92 0.082  0.010  2.4 0.000 0.165  0.00-.00-.04-.03 .18 .26 .14
     0.700    263    146    261    148  2.3  3150.392  35.67   14.45 0.082  0.009  2.7 0.000 0.169  0.00-.00 .00-.02 .17 .58 .17
     0.750    293    191    289    196  1.4  4190.459  42.16   14.34 0.078 -0.010  2.9 0.000 0.158  0.00-.02-.03-.01 .16 .42 .12
     0.800    259    180    257    182  1.2  3649.485  39.02   13.68 0.085 -0.010  2.7 0.000 0.171  0.00 .02-.07-.00 .18 .34 .11
     0.850    314    184    309    189  5.4  3791.773  43.98   13.49 0.085  0.011  4.2 0.000 0.165  0.00-.02-.05 .01 .32 .48 .12
     0.900    446    261    439    269  5.6  2721.568  34.12   13.10 0.087 -0.008  2.4 0.000 0.175  0.00 .00-.03 .00 .27 .34 .11
     0.950    392    214    387    220  4.6  2432.508  31.17   13.14 0.077  0.001  2.0 0.000 0.155  0.00-.01-.06 .01 .28 .47 .12
     1.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   PeakCts      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   745.334      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
  1490.668      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
  2981.336     53     44     53     44 26.4   200.622   4.62   15.53 0.124 -0.077  0.6 0.000 0.248  0.00-.02-.01 .01 .18 .13 .12
  5962.672   3869   1764   3279   2355  6.8  1337.113  16.95   14.78 0.070  0.001  1.4 0.000 0.148  0.00-.02-.03-.01 .17 .11 .13
 11925.344   3401   1566   3002   1965  4.8  2632.370  29.59   13.25 0.088  0.003  2.5 0.000 0.181  0.00-.01-.04-.00 .21 .16 .12
 23850.688   1542    822   1454    914  3.6  4167.517  49.77   12.03 0.088 -0.010  3.6 0.000 0.184  0.00-.01-.08 .02 .25 .37 .14
 47701.375    632    322    594    363  2.5  7891.344  87.22   11.76 0.076  0.005  4.8 0.000 0.161  0.00-.06-.01 .05 .44 .82 .18
 95402.750    124     60    123     62  0.8 13009.874 135.64   10.98 0.064  0.010  5.8 0.000 0.136  0.00-.22 .26 .15 .95 2.1 .38
190805.500     16      9     16      9  0.0 12641.531 161.28    9.93 0.089 -0.022  8.6 0.000 0.178  0.00 .27-.32 .14 .62 .97 .34
381611.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   BgndCts      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     2.796      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     5.593      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     8.389   2147   1102   1976   1274  6.8  1580.245  24.80   10.32 0.085 -0.027  2.2 0.000 0.172  0.00-.03-.05 .01 .44 .76 .19
    11.185   3546   1626   3183   1994  7.2  2114.969  26.78   12.54 0.075 -0.007  1.9 0.000 0.159  0.00-.01-.04-.01 .20 .14 .14
    13.982   2683   1362   2375   1673  3.5  3467.835  36.79   15.33 0.078 -0.010  2.4 0.000 0.159  0.00-.02-.03 .01 .11 .09 .11
    16.778   1113    605   1056    665  1.6  5277.047  48.97   17.79 0.083  0.021  3.6 0.000 0.175  0.00-.01-.03 .03 .07 .06 .08
    19.574    142    100    141    102  0.7  8735.644  65.59   20.34 0.119  0.092  7.3 0.000 0.237  0.00-.02-.04 .05 .05 .05 .08
    22.370      5      4      5      4  0.0  7475.400  61.81   23.86 0.098 -0.023  4.0 0.000 0.197  0.00 .04-.09 .03 .18 .12 .13
    25.167      1      0      1      0  0.0 17883.199  87.41   27.96 0.000  0.000  0.0 0.000 0.000  0.00 .03-.04 .03 .03 .04 .03
    27.963

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
      ErrX      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
    -1.500     20     11     20     11  0.0   617.592   9.75    9.38 0.135 -0.064  1.1 0.000 0.271  0.00-2.8-.22 .71 2.9 5.0 .77
    -1.380      4      3      4      3 25.0   669.492  12.47    9.65 0.089  0.024  0.6 0.000 0.177  0.00-1.3 1.9 .48 1.3 2.0 .48
    -1.260      8      2      8      2 12.5   455.720   8.80    9.88 0.188 -0.021  1.8 0.000 0.375  0.00-1.2 .34 .35 1.2 1.4 .36
    -1.140      4      1      4      1  0.0   677.255  10.75    9.68 0.108 -0.035  1.5 0.000 0.216  0.00-1.1 1.3 .39 1.1 2.3 .44
    -1.020     19      5     19      5 31.6   301.438   6.25   10.11 0.101 -0.007  0.7 0.000 0.202  0.00-.95-.13 .33 .95 1.2 .34
    -0.900     26     11     26     12 34.6   262.906   5.36   10.43 0.087 -0.050  0.6 0.000 0.220  0.00-.85 .36 .32 .85 1.2 .35
    -0.780     55     19     55     19 14.5   319.604   5.84   10.91 0.108  0.006  0.5 0.000 0.216  0.00-.72 .06 .29 .72 1.3 .37
    -0.660     68     28     67     29 19.1   370.327   6.72   11.42 0.096  0.000  0.6 0.000 0.195  0.00-.59 .03 .24 .59 .54 .28
    -0.540    128     46    127     47 21.9   402.742   6.89   11.59 0.098 -0.006  0.7 0.000 0.192  0.00-.48-.05 .22 .48 .54 .25
    -0.420    241    113    237    117 15.4   642.975  10.25   12.08 0.070  0.003  0.7 0.000 0.144  0.00-.35-.04 .17 .35 .53 .22
    -0.300    527    242    517    252 12.1   877.981  13.50   12.52 0.076  0.008  1.0 0.000 0.153  0.00-.23-.05 .10 .23 .28 .16
    -0.180   1651    881   1551    983  5.3  2142.324  27.63   13.26 0.068  0.025  1.7 0.000 0.140  0.00-.11-.04 .04 .11 .25 .11
    -0.060   4692   2028   3736   2989  2.0  4305.107  43.82   14.62 0.081  0.001  2.9 0.000 0.173  0.00-.00-.04 .00 .03 .12 .09
     0.060   1293    709   1216    787  3.9  1633.756  22.12   12.69 0.099 -0.033  1.8 0.000 0.205  0.00 .11-.05-.06 .11 .21 .13
     0.180    455    227    444    239  7.0   995.168  14.81   12.02 0.086 -0.017  1.1 0.000 0.174  0.00 .23-.04-.13 .23 .30 .18
     0.300    210    108    208    110 18.1   742.061  12.47   11.87 0.117 -0.041  1.1 0.000 0.237  0.00 .35-.03-.17 .35 .43 .22
     0.420    101     36     99     38 13.9   717.714  11.30   11.00 0.069 -0.008  0.8 0.000 0.147  0.00 .47 .00-.22 .47 .50 .27
     0.540     48     26     48     26 22.9   855.289  13.21   10.99 0.204 -0.110  2.5 0.000 0.409  0.00 .58 .01-.24 .58 .49 .28
     0.660     30     13     30     13 26.7   549.751   9.62   10.74 0.304 -0.134  3.0 0.000 0.608  0.00 .73-.03-.31 .73 .59 .32
     0.780     21      8     21      8 19.0   707.006  11.56   10.66 0.549 -0.085  3.7 0.000 1.098  0.00 .83-.13-.30 .83 .73 .32
     0.900     11      6     11      6 18.2   546.034  10.73   10.91 0.567 -0.340  9.2 0.000 1.133  0.00 .95 .03-.28 .95 .53 .31
     1.020      9      5      9      5  0.0   416.558   9.69    9.93 0.091 -0.041  1.0 0.000 0.182  0.00 1.1 .77-.22 1.1 1.4 .43
     1.140      5      2      5      2 20.0   701.932  16.65    9.44 0.085 -0.058  2.4 0.000 0.170  0.00 1.2 .07 .08 1.2 1.6 .46
     1.260      3      2      3      2 33.3   334.067   9.93   11.20 0.533  0.016  2.0 0.000 1.065  0.00 1.3 .94 .28 1.3 2.8 .66
     1.380      8      6      8      6 75.0   382.667  17.40   10.55 3.110 -3.050141.6 0.000 6.220  0.00 1.9-.52 .05 1.9 1.3 .42
     1.500

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
      ErrY      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
    -1.500     34     20     34     20  5.9   772.625  13.18    9.69 0.271 -0.160  6.2 0.000 0.542  0.00-.81-2.8 .52 1.7 3.4 .63
    -1.380      4      1      4      1  0.0   964.531  14.78    9.82 0.092 -0.007  0.6 0.000 0.184  0.00-.56-1.3 .29 .67 1.3 .30
    -1.260     10      4     10      4 20.0   307.147   6.84    9.65 0.174 -0.134  1.7 0.000 0.347  0.00-.21-1.2 .10 .85 1.2 .31
    -1.140      7      3      7      3 14.3   925.179  14.81    9.54 0.116 -0.036  1.1 0.000 0.232  0.00-.33-1.1 .09 .78 1.1 .23
    -1.020     15      6     15      6  0.0   552.625  10.82    9.85 0.087 -0.016  0.8 0.000 0.175  0.00 .02-.96 .03 .61 .96 .30
    -0.900     26     12     26     12 15.4  1256.024  20.86    9.92 0.217 -0.108  3.8 0.000 0.435  0.00-.05-.82 .06 .53 .82 .28
    -0.780     44     24     44     24  6.8   975.816  16.78    9.97 0.069 -0.001  1.0 0.000 0.138  0.00-.10-.72 .01 .51 .72 .25
    -0.660     82     42     82     42  8.5  1468.404  22.72   10.08 0.095 -0.030  3.9 0.000 0.190  0.00-.01-.60-.02 .45 .60 .22
    -0.540    122     58    121     59 11.5  1316.303  20.68   10.47 0.069 -0.012  2.4 0.000 0.137  0.00-.04-.48 .01 .39 .48 .21
    -0.420    248    133    247    135 11.3  1316.624  20.40   10.87 0.050 -0.011  1.2 0.000 0.100  0.00-.03-.35-.02 .30 .35 .18
    -0.300    683    385    661    407  7.0  1637.367  22.51   11.93 0.083 -0.018  2.5 0.000 0.167  0.00-.01-.23-.00 .23 .23 .15
    -0.180   2536   1288   2346   1480  4.2  2765.724  31.03   13.70 0.089 -0.016  2.5 0.000 0.180  0.00-.00-.11-.00 .15 .11 .11
    -0.060   4324   1994   3618   2705  2.9  3993.075  42.50   14.68 0.077  0.010  2.7 0.000 0.163  0.00-.01-.01-.00 .12 .03 .10
     0.060    839    440    817    464  9.8  1021.200  15.43   12.80 0.104 -0.019  1.4 0.000 0.209  0.00-.01 .11-.01 .19 .11 .14
     0.180    301    156    295    162 14.6   555.218  10.05   11.82 0.090 -0.022  0.8 0.000 0.181  0.00-.01 .23 .00 .30 .23 .19
     0.300    121     66    120     67 19.0   669.494  12.54   10.96 0.105 -0.027  1.0 0.000 0.209  0.00-.06 .35 .04 .36 .36 .22
     0.420     69     33     69     33 17.4   633.460  12.58   10.41 0.127 -0.060  1.2 0.000 0.254  0.00-.01 .47 .04 .43 .47 .22
     0.540     40     19     40     19 17.5   469.710  10.04   10.01 0.099 -0.030  1.1 0.000 0.199  0.00-.10 .59 .08 .46 .59 .25
     0.660     22     10     22     10 27.3   285.318   6.63    9.86 0.128 -0.029  0.9 0.000 0.257  0.00-.19 .71 .14 .60 .71 .29
     0.780     19      7     19      7  0.0   467.511   9.75    9.96 0.116 -0.048  1.3 0.000 0.231  0.00-.02 .82 .07 .59 .82 .29
     0.900     15      6     15      6  6.7   490.685  10.76    9.60 0.043  0.005  0.5 0.000 0.086  0.00-.49 .96 .21 .66 .96 .24
     1.020     16      6     16      6  6.3   330.654   7.34    9.62 0.069 -0.032  0.7 0.000 0.138  0.00 .02 1.1-.03 .70 1.1 .31
     1.140      4      2      4      2  0.0   508.951  12.99    9.60 0.027 -0.020  0.8 0.000 0.055  0.00 .51 1.2 .13 .80 1.2 .33
     1.260      2      1      2      1  0.0  1020.591  14.12    9.35 0.280 -0.215  4.7 0.000 0.561  0.00 1.1 1.4-.25 1.1 1.4 .25
     1.380     54     36     54     37  1.9   687.174  12.65    9.45 0.066 -0.026  0.8 0.000 0.136  0.00-.71 2.8 .47 1.5 3.2 .61
     1.500

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
      ErrZ      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
    -1.500      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -1.380      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -1.260      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -1.140      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -1.020      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -0.900      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -0.780      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -0.660      2      1      2      1100.0    53.885   1.38   13.32 1.065 -0.420  1.2 0.000 2.130  0.00 .53-.05-.60 .53 .12 .61
    -0.540     29     17     29     17 48.3   164.127   3.90   12.16 0.849 -0.483 14.1 0.000 1.699  0.00 .53 .11-.47 .69 .54 .47
    -0.420    135     73    132     76 28.9   289.749   6.28   12.23 0.233 -0.111  1.3 0.000 0.474  0.00 .42 .01-.35 .53 .51 .35
    -0.300    578    305    562    321  8.8   753.573  11.51   12.15 0.094 -0.018  2.1 0.000 0.189  0.00 .23-.07-.22 .33 .33 .23
    -0.180   1887    954   1743   1099  4.4  1715.559  21.48   12.90 0.058  0.002  1.2 0.000 0.119  0.00 .06-.06-.11 .15 .18 .11
    -0.060   4235   1948   3534   2652  2.4  3708.827  39.13   14.11 0.082  0.006  2.8 0.000 0.169  0.00-.01-.04 .00 .10 .11 .03
     0.060   2026   1026   1889   1169  4.7  3637.751  43.21   13.96 0.087 -0.010  2.9 0.000 0.179  0.00-.08-.04 .11 .18 .18 .11
     0.180    493    234    482    246 15.2   948.175  16.43   12.61 0.100 -0.020  1.1 0.000 0.200  0.00-.26-.03 .23 .37 .47 .23
     0.300    173     83    172     84 20.8   391.511   7.45   12.00 0.143 -0.047  0.9 0.000 0.284  0.00-.48 .11 .35 .66 .89 .35
     0.420     46     23     46     24 34.8   237.463   5.63   11.55 0.371 -0.153  3.9 0.000 0.741  0.00-.50-.20 .47 .89 1.3 .47
     0.540     11      7     11      7 18.2   725.835  12.19   10.31 0.083 -0.056  1.1 0.000 0.167  0.00-.99 .32 .61 1.6 2.9 .61
     0.660      9      4      9      5  0.0   811.246  13.90    9.59 0.077 -0.048  1.3 0.000 0.196  0.00-1.2 2.0 .73 2.3 3.7 .73
     0.780      3      3      3      3  0.0  1291.118  22.72    9.33 0.239 -0.225  5.2 0.000 0.478  0.00-.54 2.4 .84 2.2 4.2 .84
     0.900      3      2      3      2  0.0   628.586  10.83    9.39 0.020 -0.015  0.2 0.000 0.041  0.00-1.4 5.1 .96 1.9 5.1 .96
     1.020      2      2      2      2  0.0   448.298  10.73    9.42 0.152 -0.048  1.7 0.000 0.305  0.00 .59 4.9 1.1 .91 4.9 1.1
     1.140      3      2      3      2  0.0  1228.890  13.46    9.59 0.228 -0.094  1.8 0.000 0.457  0.00-2.6-6.7 1.2 3.1 6.9 1.2
     1.260      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     1.380      2      2      2      2  0.0   117.450   2.89    9.38 0.142 -0.124  0.3 0.000 0.284  0.00-2.4-.61 1.7 2.9 9.3 1.7
     1.500

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   #Equivs      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000   3925      0   3925      0  7.1  2601.960  31.46   13.42 0.000  0.000  0.0 0.000 0.000  0.00-.03-.04 .01 .28 .35 .14
     1.000   5712   2849   2856   5712  4.1  3002.985  35.38   13.64 0.081  0.000  2.4 0.000 0.177  0.00-.01-.04 .00 .23 .38 .14
     2.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     3.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     4.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     5.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     6.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     7.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     8.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     9.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    10.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   Compon#      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     1.000   9637   2849   6781   5712  5.4  2839.654  33.81   13.55 0.081  0.000  2.4 0.000 0.177  0.00-.02-.04 .00 .25 .37 .14
     2.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     3.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     4.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     5.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     6.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     7.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     8.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     9.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   Angstms      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
  9999.000   1051    297    748    606  0.9  9416.667  97.75   15.41 0.079  0.000  6.0 0.000 0.173  0.00-.00-.03 .05 .09 .06 .09
     0.922   1256    473    783    946  1.0  4027.177  46.34   15.09 0.093  0.000  4.3 0.000 0.203  0.00-.00-.04 .02 .18 .17 .10
     0.733   1178    436    742    872  1.5  3460.428  36.46   15.00 0.086  0.000  2.6 0.000 0.186  0.00-.01-.04 .01 .11 .20 .10
     0.641   1113    389    724    778  3.4  2298.139  25.97   14.27 0.080  0.000  1.7 0.000 0.173  0.00-.00-.04 .00 .09 .30 .13
     0.583    992    299    693    598  6.0  1789.293  20.25   13.69 0.076  0.000  1.3 0.000 0.163  0.00-.02-.04 .00 .13 .43 .16
     0.541    944    265    679    530  8.3  1207.234  15.51   13.01 0.069  0.000  0.9 0.000 0.144  0.00-.01-.05-.01 .16 .26 .15
     0.509    891    233    657    468  8.6  1002.852  13.57   12.35 0.051  0.000  0.7 0.000 0.105  0.00-.01-.02-.02 .21 .38 .17
     0.484    828    194    634    388  8.3  1033.566  13.62   11.81 0.064  0.000  0.8 0.000 0.133  0.00-.03-.04-.02 .26 .33 .16
     0.463    700    138    562    276 10.3   917.303  11.57   11.21 0.078  0.000  0.8 0.000 0.158  0.00-.09-.05 .00 .52 .83 .20
     0.445    684    125    559    250 12.1   687.755  10.83   10.79 0.065  0.000  0.7 0.000 0.134  0.00-.06-.04-.01 .53 .52 .17
     0.430

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
    Intens      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    585    183    479    290 85.8    39.598   1.13   12.56 1.022 -0.453  3.3 0.000 2.655  0.00-.04 .00 .02 .43 .52 .24
    90.953    509    208    433    284  2.8   135.451   3.27   12.62 0.148 -0.009  0.5 0.000 0.348  0.00-.06-.02 .02 .42 .65 .22
   181.906    887    298    738    447  0.0   269.011   5.43   12.70 0.116 -0.008  0.7 0.000 0.267  0.00-.04-.01 .01 .31 .41 .19
   363.812   1375    456   1087    744  0.0   540.903   8.75   12.73 0.086 -0.006  0.8 0.000 0.195  0.00-.04-.02 .00 .29 .41 .16
   727.623   1859    644   1425   1079  0.0  1061.627  14.04   12.96 0.073 -0.007  1.2 0.000 0.169  0.00-.01-.04-.01 .27 .45 .13
  1455.247   1776    670   1345   1102  0.0  2082.179  22.63   13.73 0.075 -0.005  1.9 0.000 0.173  0.00 .00-.07-.01 .16 .29 .10
  2910.494   1423    593   1039    977  0.0  4099.241  37.08   14.52 0.081 -0.003  3.3 0.000 0.185  0.00-.01-.06 .01 .09 .14 .07
  5820.987    765    324    572    518  0.0  8038.775  60.10   15.26 0.082  0.002  5.1 0.000 0.187  0.00-.01-.05 .03 .06 .11 .07
 11641.975    365    134    283    219  0.0 16163.407 102.17   15.78 0.086  0.002  8.6 0.000 0.198  0.00-.01-.04 .04 .05 .07 .08
 23283.949     93     33     74     52  0.0 29432.657 155.79   15.70 0.074  0.016 10.6 0.000 0.171  0.00-.02-.03 .05 .05 .06 .08
 46567.898

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   #Sigmas      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    456    134    380    211100.0    30.070   0.83   12.52 1.734 -0.722  4.4 0.000 4.716  0.00-.04-.03 .02 .43 .31 .23
     1.759    331    137    297    171 18.1   104.486   2.47   12.67 0.204 -0.016  0.5 0.000 0.445  0.00-.05 .03 .00 .43 .69 .24
     3.094    761    272    656    377  0.0   210.580   4.35   12.85 0.128 -0.004  0.6 0.000 0.275  0.00-.06-.02 .02 .36 .55 .21
     5.442   1443    485   1199    729  0.0   470.811   7.53   12.73 0.090  0.001  0.7 0.000 0.184  0.00-.05-.01-.00 .31 .40 .17
     9.571   1949    724   1556   1118  0.0  1001.824  13.12   12.99 0.071 -0.001  1.0 0.000 0.152  0.00-.01-.03-.01 .27 .46 .14
    16.835   2033    825   1569   1289  0.0  2096.031  22.54   13.61 0.073 -0.001  1.7 0.000 0.156  0.00 .01-.06-.01 .16 .32 .10
    29.610   1498    690   1118   1071  0.0  4322.952  39.30   14.82 0.083 -0.002  3.3 0.000 0.175  0.00-.00-.06 .01 .10 .15 .07
    52.082    732    346    568    511  0.0  8229.029  67.11   14.88 0.086  0.001  5.6 0.000 0.178  0.00-.02-.06 .03 .07 .13 .07
    91.607    372    134    297    213  0.0 16476.610 120.27   15.18 0.083  0.000  9.5 0.000 0.177  0.00-.01-.03 .06 .06 .08 .09
   161.127     62     20     60     22  0.0 26375.763 192.36   12.62 0.055  0.013 10.3 0.000 0.124  0.00 .01-.05 .04 .09 .08 .08
   283.406

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
      Rsym      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000   1370    700    704   1370  1.3  3252.012  36.86   13.30 0.014  0.001  0.4 0.000 0.030  0.00-.02-.01-.01 .17 .39 .13
     0.030   1018    587    589   1018  0.8  3067.748  34.42   13.52 0.044  0.006  1.2 0.000 0.092  0.00-.01-.03-.00 .16 .25 .12
     0.060    846    597    597    846  0.6  2746.187  31.75   13.77 0.075  0.015  1.9 0.000 0.155  0.00-.01-.04-.00 .17 .22 .12
     0.090    774    680    680    774  0.9  3238.857  35.88   14.25 0.105  0.039  3.0 0.000 0.213  0.00-.02-.02 .01 .25 .44 .14
     0.120    664    664    664    664  0.9  4048.313  42.96   14.62 0.133  0.038  4.4 0.000 0.266  0.00-.01-.05 .01 .20 .31 .12
     0.150    386    386    386    386  2.3  3125.018  37.70   13.75 0.165 -0.094  4.6 0.000 0.330  0.00-.01-.04 .01 .20 .28 .13
     0.180    203    203    203    203  3.0  2613.499  36.56   12.85 0.192 -0.157  5.1 0.000 0.385  0.00-.05-.15 .02 .43 .80 .19
     0.210    119    119    119    119  7.6  1441.635  24.33   12.17 0.222 -0.195  4.0 0.000 0.443  0.00-.01-.07 .02 .29 .36 .16
     0.240     65     65     65     65 18.5   648.534  12.73   12.23 0.252 -0.223  2.5 0.000 0.504  0.00-.10-.14 .06 .50 1.1 .24
     0.270     40     40     40     40 25.0   937.441  19.88   12.16 0.283 -0.089  3.7 0.000 0.567  0.00 .10-.05 .03 .38 .53 .23
     0.300     24     24     24     24 29.2   342.671   7.32   12.70 0.311 -0.213  2.0 0.000 0.622  0.00 .11-.04-.07 .25 .26 .19
     0.330     29     29     29     29 20.7   902.807  17.84   12.89 0.340 -0.080  4.1 0.000 0.680  0.00 .15 .17 .00 .37 .90 .29
     0.360      9      9      9      9 55.6    86.062   2.12   12.87 0.378 -0.249  0.9 0.000 0.756  0.00-.08 .08 .02 .41 .21 .23
     0.390     14     14     14     14 50.0   319.928   7.80   11.79 0.412 -0.348  2.0 0.000 0.824  0.00-.06 .02-.05 .22 .22 .16
     0.420     15     15     15     15 53.3    73.692   2.01   12.34 0.436 -0.132  0.9 0.000 0.872  0.00 .07 .10-.05 .28 .19 .22
     0.450      7      7      7      7 71.4    66.396   1.59   12.26 0.466 -0.493  0.9 0.000 0.932  0.00-.26 .13-.02 .53 .30 .29
     0.480     15     15     15     15 46.7  1182.462  20.54   14.69 0.500  0.468  5.7 0.000 0.999  0.00-.00 .01-.02 .21 .22 .21
     0.510      7      7      7      7 85.7    40.105   1.22   12.10 0.525 -0.110  0.7 0.000 1.049  0.00 .04 .46-.07 .58 .86 .31
     0.540      4      3      4      4 75.0    44.149   1.61   13.29 0.558 -0.204  0.9 0.000 1.119  0.00-.15-.14 .11 .32 .21 .26
     0.570    103     83     84    103 89.3    89.026   2.79   12.54 1.764 -1.798 10.0 0.000 3.563  0.00 .10-.08 .01 .60 .36 .25
     0.600

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
      dI/I      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
    -0.500    100     99    100    100 84.0   101.345   3.09   12.52 1.638 -1.719 10.3 0.000 3.275  0.00 .09-.07 .02 .61 .36 .26
    -0.460     10     10     10     10 60.0    69.625   1.79   11.97 0.438 -0.531  0.9 0.000 0.875  0.00 .11 .17-.13 .38 .32 .22
    -0.420     11     11     11     11 36.4   404.526   9.00   11.72 0.411 -0.411  2.6 0.000 0.823  0.00-.08 .11 .01 .34 .25 .18
    -0.380     13     13     13     13 38.5   422.467   9.44   12.41 0.353 -0.353  2.2 0.000 0.707  0.00 .15 .11-.14 .33 .25 .23
    -0.340     22     22     22     22 27.3   821.532  16.66   12.26 0.322 -0.322  3.7 0.000 0.645  0.00 .15-.11-.05 .23 .32 .18
    -0.300     41     41     41     41 17.1   818.947  16.53   12.24 0.277 -0.277  3.2 0.000 0.553  0.00 .11-.10 .00 .41 .53 .24
    -0.260     93     93     93     93  8.6  1130.681  19.62   12.03 0.234 -0.234  3.7 0.000 0.469  0.00-.02-.13 .02 .42 .86 .19
    -0.220    193    193    193    193  1.6  2950.862  40.50   12.50 0.196 -0.196  6.0 0.000 0.391  0.00-.04-.17 .02 .43 .83 .18
    -0.180    343    343    343    343  1.2  3585.561  42.56   13.26 0.161 -0.161  5.3 0.000 0.323  0.00 .03-.07 .01 .16 .26 .12
    -0.140    401    401    401    401  1.2  2787.834  33.45   13.21 0.121 -0.121  3.2 0.000 0.243  0.00-.02-.05 .03 .36 .61 .17
    -0.100    496    496    496    496  0.6  2559.936  30.65   13.51 0.080 -0.080  1.9 0.000 0.160  0.00 .01-.05 .00 .17 .31 .13
    -0.060    678    676    678    678  1.3  2970.323  33.97   13.43 0.038 -0.038  1.1 0.000 0.076  0.00-.01-.01-.00 .18 .37 .13
    -0.020    929    470    474    929  1.1  3303.155  37.33   13.23 0.010  0.000  0.3 0.000 0.019  0.00-.02-.02-.01 .16 .30 .12
     0.020    781    779    781    781  0.9  3195.537  35.60   13.54 0.039  0.039  1.1 0.000 0.077  0.00-.02-.03-.00 .15 .35 .13
     0.060    628    628    628    628  0.5  2965.368  33.25   14.15 0.081  0.081  2.1 0.000 0.161  0.00-.03-.03 .00 .16 .19 .11
     0.100    572    572    572    572  0.9  4595.971  45.51   15.29 0.120  0.120  4.3 0.000 0.239  0.00-.03-.02 .00 .14 .22 .10
     0.140    230    230    230    230  3.0  2677.575  30.63   15.28 0.151  0.151  3.4 0.000 0.302  0.00-.04-.02 .01 .21 .22 .14
     0.180     54     54     54     54  9.3   916.814  15.18   13.55 0.196  0.196  1.8 0.000 0.392  0.00-.05 .01 .02 .25 .20 .16
     0.220     31     31     31     31 29.0   356.607   7.85   12.42 0.232  0.232  1.2 0.000 0.464  0.00-.17-.00 .08 .47 .70 .24
     0.260     15     15     15     15 33.3   862.543  20.31   12.54 0.288  0.288  3.6 0.000 0.575  0.00-.04-.00 .05 .16 .17 .15
     0.300     11     11     11     11 36.4   144.016   3.17   13.17 0.321  0.321  1.0 0.000 0.642  0.00 .10-.00-.03 .30 .23 .21
     0.340     13     13     13     13 15.4   746.094  14.81   13.80 0.345  0.345  3.7 0.000 0.689  0.00-.01 .41 .14 .44 1.3 .35
     0.380      6      6      6      6 66.7    60.013   1.68   12.53 0.399  0.399  0.7 0.000 0.799  0.00 .01-.05-.14 .13 .16 .22
     0.420      8      8      8      8 62.5    55.896   1.62   12.75 0.438  0.438  0.7 0.000 0.877  0.00-.07 .08-.00 .26 .13 .24
     0.460     33     32     33     33 78.8   535.033  12.70   13.55 0.508  0.508  2.7 0.000 1.016  0.00 .02 .04-.00 .37 .46 .23
     0.500

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
    dI/sig      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000   2732   1456   1458   2732  7.7  1340.222  19.22   12.96 0.024  0.002  0.5 0.000 0.050  0.00-.03-.02-.00 .24 .42 .16
     1.000   1180    747    749   1180  1.6  2416.909  29.19   13.41 0.049  0.002  1.4 0.000 0.103  0.00-.01-.02-.01 .25 .43 .13
     2.000    525    385    387    525  0.2  3471.169  35.60   14.22 0.069  0.006  2.5 0.000 0.149  0.00-.01-.08-.00 .19 .28 .10
     3.000    348    287    287    348  0.0  4423.993  41.60   14.90 0.084  0.015  3.5 0.000 0.177  0.00-.01-.09 .02 .21 .48 .11
     4.000    245    213    214    245  0.0  5035.509  47.85   14.87 0.094 -0.008  4.5 0.000 0.197  0.00 .01-.06 .02 .10 .15 .07
     5.000    184    160    160    184  0.0  5776.276  52.23   15.17 0.105  0.011  5.5 0.000 0.216  0.00-.00-.06 .03 .06 .09 .06
     6.000    109    101    102    109  0.0  7322.701  62.46   15.39 0.104  0.002  6.5 0.000 0.221  0.00-.01-.06 .03 .08 .10 .07
     7.000     81     76     76     81  0.0  8085.938  62.73   15.51 0.120  0.020  7.5 0.000 0.245  0.00-.01-.05 .02 .07 .09 .06
     8.000     57     53     53     57  0.0  7506.782  65.26   15.54 0.129  0.004  8.5 0.000 0.262  0.00 .00-.04 .04 .06 .08 .07
     9.000     42     41     41     42  0.0  9177.148  74.15   14.92 0.128 -0.003  9.5 0.000 0.266  0.00 .01-.06 .05 .08 .10 .08
    10.000     30     28     28     30  0.0  9266.007  75.12   15.09 0.140 -0.003 10.5 0.000 0.284  0.00 .00-.05 .03 .06 .08 .07
    11.000     35     32     32     35  0.0 11881.240  82.84   15.76 0.138  0.000 11.5 0.000 0.285  0.00 .01-.05 .04 .06 .07 .07
    12.000     21     19     19     21  0.0 12918.262  91.92   15.61 0.136  0.002 12.5 0.000 0.279  0.00 .00-.07 .06 .06 .20 .10
    13.000     18     17     17     18  0.0 10413.890  90.66   14.71 0.147 -0.048 13.3 0.000 0.305  0.00 .14-.18 .08 .43 .56 .22
    14.000      7      7      7      7  0.0 11870.171  94.63   15.32 0.153 -0.095 14.4 0.000 0.305  0.00 .00-.05 .08 .04 .05 .10
    15.000     16     15     15     16  0.0 14222.125  98.84   14.10 0.156 -0.017 15.4 0.000 0.321  0.00 .02-.08 .05 .10 .18 .08
    16.000     12     12     12     12  0.0 14530.183 107.07   14.55 0.153 -0.038 16.4 0.000 0.307  0.00 .01-.04 .05 .08 .07 .08
    17.000     14     14     14     14  0.0 14459.023 113.74   16.30 0.154  0.013 17.5 0.000 0.307  0.00 .12-.04 .03 .32 .07 .09
    18.000      8      8      8      8  0.0 15089.615 118.38   15.02 0.157 -0.020 18.6 0.000 0.314  0.00 .12-.01 .03 .33 .04 .17
    19.000     11     10     10     11  0.0 18416.255 135.93   15.28 0.143  0.016 19.4 0.000 0.290  0.00-.03-.03 .02 .07 .06 .09
    20.000      8      8      8      8  0.0 13774.575 106.76   13.84 0.192 -0.098 20.5 0.000 0.383  0.00-.04 .04 .03 .07 .24 .10
    21.000     11      9      9     11  0.0 21383.164 144.29   14.48 0.148  0.000 21.4 0.000 0.310  0.00-.01 .01 .04 .03 .04 .07
    22.000      4      4      4      4  0.0 14682.075  95.54   14.83 0.235 -0.114 22.5 0.000 0.471  0.00 .11-.23 .13 .27 .40 .18
    23.000      3      3      3      3  0.0 21062.400 144.99   14.35 0.163 -0.079 23.6 0.000 0.326  0.00-.01-.02 .08 .02 .03 .11
    24.000     11     10     10     11 45.5  7644.456 114.60   11.90 0.315 -0.180 90.8 0.000 0.598  0.00 1.1-.31-.05 1.4 .69 .26
    25.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   Overall      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000   9637   2849   6781   5712  5.4  2839.654  33.81   13.55 0.081  0.000  2.4 0.000 0.177  0.00-.02-.04 .00 .25 .37 .14
     1.000

Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
   Centric      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    435      0    435      0 10.3  3549.796  46.40   13.53 0.000  0.000  0.0 0.000 0.000  0.00 .00-.05 .01 .20 .23 .14
     1.000

Coverage Statistics
Integration of DK_zucker
 ...1.1(1):  component 1 in sample 1 (component 1 in DK_Zucker2_01.raw)
                                                           .......Shell......
  Angstrms   #Obs Theory %Compl Redund   Rsym Pairs %Pairs Rshell #Sigma %<2s
 to  0.922    748   1021  73.26   1.41  0.079   297  29.09  0.079  97.75  0.9
 to  0.733   1531   1991  76.90   1.51  0.085   770  38.67  0.093  46.34  1.0
 to  0.641   2273   2956  76.89   1.53  0.085  1206  40.80  0.086  36.46  1.5
 to  0.583   2997   3915  76.55   1.53  0.084  1595  40.74  0.080  25.97  3.4
 to  0.541   3690   4870  75.77   1.51  0.084  1894  38.89  0.076  20.25  6.0
 to  0.509   4369   5827  74.98   1.50  0.083  2159  37.05  0.069  15.51  8.3
 to  0.484   5026   6777  74.16   1.48  0.082  2392  35.30  0.051  13.57  8.6
 to  0.463   5660   7742  73.11   1.46  0.082  2586  33.40  0.064  13.62  8.3
 to  0.445   6222   8707  71.46   1.44  0.082  2724  31.29  0.078  11.57 10.3
 to  0.430   6781   9637  70.36   1.42  0.081  2849  29.56  0.065  10.83 12.1
