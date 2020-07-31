SAINT V8.40A
C:\bn\SAINT\saint.exe vqmoxl.slm /BATCH /CONFIG:vqmoxl.ini /NOPROMPT /PLAIN /PRI&
ORITY:4 /SOCKET:2000

!====================================================
!01/23/2020 16:55:02 
INTEGRATE &
 "D:\frames\guest\BruecknerJK_153F40\cu_BruecknerJK_153F40_[1-11]_0001.sfrm,cu_fastscan_01_0001" &
 "d:\Frames\guest\BruecknerJK_153F40\work\cu_BruecknerJK_153F40_[1-11].raw,cu_BruecknerJK_153F40_01A" &
 /2THETA=-9999.0000 /ACTTHRESH=0.0000 /ALPHA12 /AMNAME=$NEW /BATCH=1 &
 /BGCSCALE=0 /BGQSCALE=1 /BGSIG=1.000 /CHI=-9999.0000 /CRYSTAL=1 &
 /CYCLIM=25 /DAAP=0.0000 /DAPHI=0.00000 /DFRAME /ESDSCALE=1.00000 &
 /EXPOSURE=0.000 /GLOBAL /GMARQ=2.000000e-003 /GMIN=0 /GREFLIM=9999 &
 /GRLVERR=0.0250 /GSVD=1.000000e-006 /IAXIS=-9999 /IOVSIGMA=-3.00000 &
 /K1=5 /K2=5 /L1=T /L2=0 /LATTICE=0 /LMARQ=2.000000e-003 /LMIN=0 &
 /LORENTZ=0.02000 /LORMODEL=0.07500 /LRES=9999.00000 /LSFIT /LSFREQ=50 &
 /LSVD=5.000000e-005 /LTHR=8.000 /LWT=0.000 /MACHINE_ERROR=0.0000 &
 /MAXSATIND=1 /MCESDS /MCREFLIM=4096 /MCVERB=1 /MEDMSK=-1 &
 /MISSING=0.6000 /MMIC=20.00000 /NEXP=-9999 &
 /NFRAMES="508,508,508,508,900,508,508,508,508,481,508,180" /NODECAY &
 /NSIM=20 /OMEGA=-9999.0000 &
 /ORIENTATION=d:\Frames\guest\BruecknerJK_153F40\work\vqmoxl.p4p &
 /ORTUPDSCALE=1.000 /OVRTIME=-9999.00000 /PHI=-9999.0000 &
 /POINTGROUP=mmm /PROFXHALF=4 /PROFYHALF=4 /PROFZHALF=4 /QUEUEHALF=7 &
 /RESOLUTION=0.77 /ROLL=0.000 /SEED=0 /SHRMSK=-1 /SMAP=$P4P &
 /SMIC=20.00000 /SNAP=999 /SPATIAL=$NULL /SSBIAS=1.0000 /STRONG=10.000 &
 /TIMEOUT=0.000 /TITLE="Integration of BruecknerJK_153F40" /TOPFILT &
 /TPROF=0.0500 /TTM=0.000 /TWINBOXRATIO=1.30000 /TWINMINCOMVOL=0.04000 &
 /TWINSEPARATION=1.00000 /VERBOSITY=2 /VOLANGSTROMS=1.00000 &
 /VOLTARGET=1.00000 /WIDTH=-9999.0000 /WTMETH=2 /XSIZE=0.4400 &
 /YSIZE=0.4400 /ZSIZE=0.9400 /ZW=1.000


Saving spots >    10.00 sigma(I) in d:\Frames\guest\BruecknerJK_153F40\work\cu_BruecknerJK_153F40_01._ma

Multiple runs have been specified:
  (current run indicated with "*")
 FRAME                  MATRIX                 OUTPUT                 #FRAMES                 RESOLUTIONS
*cu_BruecknerJK_153F40_01_0001vqmoxl.p4p             cu_BruecknerJK_153F40_01    508      0.77
 cu_BruecknerJK_153F40_02_0001vqmoxl.p4p             cu_BruecknerJK_153F40_02    508      0.77
 cu_BruecknerJK_153F40_03_0001vqmoxl.p4p             cu_BruecknerJK_153F40_03    508      0.77
 cu_BruecknerJK_153F40_04_0001vqmoxl.p4p             cu_BruecknerJK_153F40_04    508      0.77
 cu_BruecknerJK_153F40_05_0001vqmoxl.p4p             cu_BruecknerJK_153F40_05    900      0.77
 cu_BruecknerJK_153F40_06_0001vqmoxl.p4p             cu_BruecknerJK_153F40_06    508      0.77
 cu_BruecknerJK_153F40_07_0001vqmoxl.p4p             cu_BruecknerJK_153F40_07    508      0.77
 cu_BruecknerJK_153F40_08_0001vqmoxl.p4p             cu_BruecknerJK_153F40_08    508      0.77
 cu_BruecknerJK_153F40_09_0001vqmoxl.p4p             cu_BruecknerJK_153F40_09    508      0.77
 cu_BruecknerJK_153F40_10_0001vqmoxl.p4p             cu_BruecknerJK_153F40_10    481      0.77
 cu_BruecknerJK_153F40_11_0001vqmoxl.p4p             cu_BruecknerJK_153F40_11    508      0.77
 cu_fastscan_01_0001    vqmoxl.p4p             cu_BruecknerJK_153F40_01A    180      0.77
Current batch number is 1

Integration of BruecknerJK_153F40

Logical CPUs detected:             8
Number of threads to be used:      8
Additional read-ahead threads:     0

Input linear pixel scale:         1.00000
Input frame rows, columns:      1024  768
Frame queue half-size:             7
Number of frames in queue:        15
Profile X,Y,Z half-widths:         4  4  4
Number of X,Y,Z profile points:    9  9  9
Fraction-of-maximum method will be used to determine summation volume

SMART CCD DETECTOR PARAMETERS ------------
Detector type = 1 was obtained from CONFIGURE menu
Multiwire reference correction will be disabled
Detector is a single tile            (from CONFIGURE menu)
Read noise (e-):              103.93 (from frame cu_BruecknerJK_153F40_01_0001.sfrm)
Electrons per A/D unit:        36.60 (from frame cu_BruecknerJK_153F40_01_0001.sfrm)
Electrons per x-ray photon:   119.82 (from frame cu_BruecknerJK_153F40_01_0001.sfrm)
Base offset per exposure:         64 (from frame cu_BruecknerJK_153F40_01_0001.sfrm)
Per-exposure full scale:      163809 (from frame cu_BruecknerJK_153F40_01_0001.sfrm)
Nominal pixels per CM:        36.955 (from CONFIGURE menu)
CM from face to imaging plane: 1.004 (from CONFIGURE menu)
Fiducial spot spacing(CM):     0.425 (from CONFIGURE menu)
Faceplate transmittance:      0.8168 (from CONFIGURE menu)
Phosphor absorption:          0.9900 (from CONFIGURE menu)
Air absorption (per CM):      0.0106 (from CONFIGURE menu)
Active pixel threshold:        0.000 (from Advanced menu)

Frames were acquired with BIS V6.2.12/2019-08-12
   Booster system: rescan threshold is 60,000 ADU

Starting swing angle will be obtained from frame header
Starting omega will be obtained from frame header
Starting phi will be obtained from frame header
Starting chi will be obtained from frame header
Number of exposures summed will be obtained from frame header
Scan axis will be obtained from frame header
Scan width will be obtained from frame header
Exposure time will be obtained from frame header

Initial background ================== 01/23/2020 16:55:02

Initial background range (deg) =      16.00, interleave = 2
Number of BG pixels >= 64K:               0
 
Initial BG frame written to cu_BruecknerJK_153F40_ib_01_0001.sfrm
 
Nominal time per frame (s):          4.2
Intensity normalization in deg/min:  5.71429
Output intensities are multiplied by this value
   to place on scale of 1 min/deg

Reading orientation and spatial calibration ========== 01/23/2020 16:55:02
INFO:  No spatial correction will be used
Orientation for 1 component read from d:\Frames\guest\BruecknerJK_153F40\work\vqmoxl.p4p
Detector distance of 4.996 cm was obtained from header of cu_BruecknerJK_153F40_01_0001.sfrm

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file
... Input P4P data for sample 1 of 1:
... This sample is a single crystal with 3 indices (HKL)

... Component 1.1(1) (component 1 in sample 1, 1 of 1 in file)
Orientation ("UB") matrix:
  -0.0355953   0.0175752   0.0626516
  -0.0282727  -0.0062733  -0.1678359
  -0.0228773  -0.0195929   0.1099373

Unit Cell: A           B           C       Alpha        Beta       Gamma
     19.6504     36.9579      4.7576      90.000      90.000      90.000

Detector corrections:      X-Cen   Y-Cen    Dist   Pitch    Roll     Yaw
                          -0.229   0.313   0.003  -0.270  -0.151  -0.240

Goniometer zeros (deg):       0.0000      0.1365      0.0000      0.1036
Crystal translations (pixels):            0.1101      0.0978     -0.0162
... End component 1.1(1)
... End sample 1 of 1

Mean, a1, a2 wavelength (Angstroms):     1.54184     1.54056     1.54439
Alpha1:alpha2 ratio:                     2.00000
Nominal detector distance (cm):            4.996
X,Y beam center @swing=0 (pixels):        386.24      506.40

Input sample map:    1

Input components will be treated as follows:

 Component   Lattice      PointGroup    Wanted    Indices  Subsystems
    1.1(1)       0=P             mmm         Y      3=HKL           1

Active pixel mask ================== 01/23/2020 16:55:02

Median filter size:   input, used    -1,  4
Mask shrinkage (pix): input, used    -1,  6
No diamond-anvil cell occlusions will be computed
Active area will be limited according to x-ray aperture file:
   cu_BruecknerJK_153F40_xa_01_0001.sfrm
Active pixel mask written to cu_BruecknerJK_153F40_am_01_0001.sfrm
Fraction of mask marked active:  0.9443

Scan axis is OMEGA
Spatially corrected beam center:       386.24  506.40
Direction cosines of rotation axis:     0.002   0.000   1.000
Starting frame angles (degrees):       73.305 241.854   0.000  54.736
Vertical tilt of beam (degrees):       0.1000
Exposures per frame:                        1
Output sigma(I)'s will be scaled by:                   1.0000
Fraction of I to be combined with sigma(I)'s:          0.0000
Maximum number of frames to be processed:                 508
Mark-up frames will not be written
Narrow-frame algorithm will be used.
Per-frame BG offsets will be used.
Recurrence-method BG will be used.
Direct beam monitor will not be used.
Alpha1,2 splitting will be added to box sizes
Box volumes will be multiplied by exp(0.00000 * [sin(theta)/lambda]^2
Target volume factor is 1.000 at 1.000 angstroms
Max allowed missing profile intensity:                  0.600
Lorentz cutoff for exclusion from output:              0.0200
Lorentz cutoff for exclusion from model profiles:      0.0750
LS will use individual reflection weights

Initial orientation and spot-shape refinement ============== 01/23/2020 16:55:02
Input X,Y,Z spot size (deg):    0.440   0.440   0.940
Scale for orientation update length:            1.00000
#Frames running average for orientation update:      15
Frames between full refinements of orientation:      50
Frames in BG running avg (correlation length):       16
Nominal frame width in degrees:                   0.400
Accurate-timing indicator is set in the frame headers:
   Velocity normalization will be computed for each frame
Pixel spacing (deg):              0.111
Profile X,Y,Z spacing (deg):      0.079   0.079   0.171
Profile convolver halfwidth:       1.23    1.23    1.75
Background pixels updated = 94.63%            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
    0_0001    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   21 0.44 0.44 0.94 1.000
    1_0002    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   20 0.44 0.44 0.94 1.000
    2_0003    1  0.06 -0.51 -0.33  0.06  0.51  0.33  23912  32    0  0.30   27 0.44 0.44 0.94 1.000
    3_0004    9 -0.07 -0.67 -0.25  0.26  0.70  0.28  67475  40    0  0.74   32 0.44 0.44 0.94 1.000
    4_0005   11  0.11 -0.57 -0.27  0.29  0.66  0.30  98919  39    0  0.79   31 0.44 0.44 0.94 1.000
    5_0006   10 -0.01 -0.49 -0.24  0.13  0.53  0.26  41793  31    0  0.84   34 0.44 0.44 0.94 1.000
    6_0007   15 -0.09 -0.66 -0.24  0.23  0.73  0.25  88865  37    7  0.83   32 0.44 0.44 0.94 1.000
    7_0008    5 -0.21 -0.39 -0.06  0.24  0.56  0.23  17926  22   20  0.82   35 0.44 0.44 0.94 1.000
    8_0009    8  0.08 -0.50 -0.24  0.20  0.51  0.26  63397  34    0  0.81   33 0.44 0.44 0.94 1.000
    9_0010    7 -0.01 -0.58 -0.20  0.14  0.64  0.23  41942  28    0  0.88   30 0.44 0.44 0.94 1.000
   10_0011   13 -0.09 -0.48 -0.18  0.18  0.53  0.22  50401  35    0  0.84   31 0.44 0.44 0.94 1.000
   11_0012   14 -0.04 -0.57 -0.21  0.30  0.63  0.23  71568  39    0  0.89   34 0.44 0.44 0.94 1.000
   12_0013    8 -0.13 -0.41 -0.15  0.33  0.54  0.22  51083  38   13  0.83   29 0.44 0.44 0.94 1.000
   13_0014    9  0.04 -0.52 -0.23  0.15  0.54  0.24  36675  33    0  0.91   34 0.44 0.44 0.94 1.000
   14_0015    6 -0.01 -0.46 -0.17  0.07  0.52  0.18  29090  27    0  0.86   31 0.44 0.44 0.94 1.000
   15_0016   14  0.07 -0.47 -0.23  0.24  0.51  0.24  58348  36    0  0.91   31 0.44 0.44 0.94 1.000
   16_0017    6 -0.09 -0.72 -0.19  0.16  0.75  0.19 102874  44    0  0.95   35 0.44 0.44 0.94 1.000
   17_0018    6 -0.11 -0.52 -0.19  0.29  0.57  0.19 119583  61    0  0.91   30 0.44 0.44 0.94 1.000
   18_0019   11  0.06 -0.49 -0.21  0.17  0.50  0.22 103878  52    0  0.93   31 0.44 0.44 0.94 1.000
   19_0020    7  0.01 -0.36 -0.17  0.11  0.39  0.18  49609  33    0  0.91   35 0.44 0.44 0.94 1.000
Background pixels updated = 97.34%            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   20_0021    9 -0.15 -0.55 -0.13  0.23  0.57  0.17  99350  49    0  0.92   31 0.44 0.44 0.94 1.000
   21_0022    6  0.08 -0.45 -0.16  0.21  0.47  0.18  40543  35    0  0.87   31 0.44 0.44 0.94 1.000
   22_0023    7 -0.06 -0.40 -0.13  0.17  0.44  0.17  29410  28    0  0.89   33 0.44 0.44 0.94 1.000
   23_0024    9  0.03 -0.44 -0.14  0.12  0.46  0.16  81069  47   11  0.89   31 0.44 0.44 0.94 1.000
   24_0025    5  0.03 -0.28 -0.20  0.21  0.38  0.25  93483  50    0  0.92   30 0.44 0.44 0.94 1.000
   25_0026   11 -0.00 -0.33 -0.16  0.20  0.46  0.22  59027  40    0  0.84   29 0.44 0.44 0.94 1.000
   26_0027   11  0.06 -0.43 -0.15  0.22  0.48  0.16  41897  34    9  0.84   32 0.44 0.44 0.94 1.000
   27_0028    7  0.00 -0.52 -0.15  0.21  0.54  0.15  75373  48    0  0.93   33 0.44 0.44 0.94 1.000
   28_0029   17  0.05 -0.32 -0.16  0.28  0.47  0.18  61749  38    0  0.91   31 0.44 0.44 0.94 1.000

I/Sigma = 109.02   Thresh = 0.020   Blend = F   #Contributing = 58   InitialProfileWt = 0.041
Region 1
Sum = 33715.3;   Maximum = 573.638;   FM = 0.697
!Region 1: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  1  0  0    0  0  1  3  4  4  2  1  0  
  0  0  0  0  0  0  0  0  0    0  1  1  2  3  3  2  1  0    0  2  5  9 13 13  8  4  1  
  0  0  0  0  0  0  0  0  0    0  1  1  3  4  5  3  1  0    0  2  5 10 16 17 12  5  1  
  0  0  0  0  0  0  0  0  0    0  1  1  3  5  5  3  1  0    0  2  5 10 17 18 13  6  1  
  0  0  0  0  0  0  0  0  0    0  1  1  2  3  3  2  1  0    0  2  4  8 12 12  7  3  1  
  0  0  0  0  0  0  0  0  0    0  0  1  1  2  2  1  0  0    0  1  3  5  7  6  3  1  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0    0  1  2  2  3  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 4->6
  0  2  5 11 13 12  8  4  1    1  4 13 24 27 24 20 11  3    1  3 11 20 23 23 20 12  4  
  1  5 13 27 39 40 28 14  4    2  9 27 56 81 83 59 30  8    1  7 22 47 69 71 52 27  7  
  1  5 15 30 45 48 36 18  5    2 11 31 63 94100 74 38 10    2  9 26 53 80 84 63 33  9  
  1  6 15 30 44 47 34 17  4    2 11 31 61 90 92 66 32  9    2  9 25 51 76 78 55 27  7  
  1  5 12 24 34 33 22 10  2    2  9 26 52 75 72 46 21  5    1  7 21 44 65 62 40 18  5  
  1  3  9 17 22 18 10  4  1    1  6 19 37 48 39 22  9  2    1  4 14 30 40 34 19  8  2  
  0  2  4  8  9  7  4  2  0    1  3  9 18 21 16  9  3  1    0  2  7 15 18 15  8  4  1  
  0  1  2  3  3  2  1  1  0    0  1  4  6  7  6  3  1  0    0  1  3  5  6  5  3  1  0  
  0  0  1  1  1  1  0  0  0    0  0  1  1  1  1  1  0  0    0  0  0  1  1  1  0  0  0  
!Region 1: Section 7->9
  0  1  4  7 11 14 12  7  2    0  0  1  3  5  6  4  2  1    0  0  0  0  0  0  0  0  0  
  0  3  9 20 30 33 25 14  4    0  1  4  8 12 12  9  5  1    0  0  1  1  1  1  1  0  0  
  1  3 11 24 35 37 28 15  5    0  1  5 11 14 14 10  5  1    0  0  1  1  2  1  1  0  0  
  1  3 10 23 34 35 25 13  4    0  1  4 10 15 14  9  5  1    0  0  1  1  2  1  1  0  0  
  0  2  8 19 28 28 19 10  3    0  1  3  8 12 11  7  4  1    0  0  0  1  1  1  1  0  0  
  0  1  4 10 17 16 11  5  1    0  1  1  4  7  7  4  2  1    0  0  0  0  1  1  0  0  0  
  0  1  2  5  7  7  5  3  1    0  0  1  1  3  3  2  1  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  2  2  2  1  0    0  0  0  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 132.46   Thresh = 0.020   Blend = F   #Contributing = 2   InitialProfileWt = 0.766
Region 2
Sum = 48714.5;   Maximum = 882.643;   FM = 0.501
!Region 2: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  3  8  4  1  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  1  1  0  0    0  0  1  4 12 21 23 14  4  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  1  0  0    0  0  1  6 16 26 27 18  5  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  1  0  0    0  0  1  8 17 24 22 14  5  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  1  7 14 16 11  5  1  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  1  5  8  7  4  2  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  2  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 2: Section 4->6
  0  0  0  2  3  5 18 10  2    0  0  1 11 24 29 28 13  3    0  0  3 28 64 76 55 24  5  
  0  0  1  9 28 48 53 33  9    0  1  6 21 43 58 54 31  8    0  2 14 44 82100 83 44 11  
  0  0  2 14 37 60 62 41 13    0  1  8 26 49 64 60 38 11    0  3 18 52 87100 88 52 15  
  0  0  3 17 39 54 50 33 10    0  1  8 26 48 57 51 30  9    0  2 16 49 82 89 76 42 11  
  0  0  3 16 32 36 25 11  3    0  1  5 21 39 42 31 15  4    0  1 10 37 64 67 52 26  7  
  0  0  2 11 18 15  8  4  1    0  0  2 11 21 22 14  6  2    0  0  3 14 33 40 28 13  3  
  0  0  1  3  5  5  3  1  0    0  0  1  3  7  8  5  2  0    0  0  1  5 12 16 11  4  1  
  0  0  0  1  2  1  1  0  0    0  0  0  1  2  2  1  0  0    0  0  0  1  3  3  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  1  0  0  0  
!Region 2: Section 7->9
  0  0  2 18 42 49 34 15  3    0  0  1  2  4  3  1  0  0    0  0  0  1  1  1  0  0  0  
  0  2 10 30 53 62 51 27  7    0  0  2  6  6  3  1  0  0    0  0  1  2  2  1  0  0  0  
  0  2 12 35 56 61 53 31  9    0  1  3  7  6  3  1  0  0    0  0  1  2  2  1  0  0  0  
  0  2 11 33 52 54 45 25  7    0  0  2  5  5  2  1  0  0    0  0  1  2  2  1  0  0  0  
  0  1  7 23 40 40 31 16  4    0  0  1  2  2  1  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  2  9 20 24 17  8  2    0  0  0  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  3  7 10  7  3  1    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  2  1  1  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 161.96   Thresh = 0.020   Blend = F   #Contributing = 5   InitialProfileWt = 0.513
Region 3
Sum = 58056.8;   Maximum = 906.243;   FM = 0.647
!Region 3: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  1  1  0    0  0  1  2  5  8  7  4  1  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  3  4  2  1    0  0  2  5 12 19 20 11  3  
  0  0  0  0  0  0  0  0  0    0  0  1  1  2  3  4  2  1    0  1  3  8 16 23 23 15  4  
  0  0  0  0  0  0  0  0  0    0  0  1  1  3  4  3  2  1    0  1  4 11 19 22 19 11  3  
  0  0  0  0  0  0  0  0  0    0  0  1  2  3  3  2  1  0    0  1  4 11 17 17 12  7  2  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  1  1  0    0  1  2  6 11 11  7  3  1  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  1  2  4  4  3  1  1  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  1  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 3: Section 4->6
  0  0  2  7 14 24 22  8  1    0  1  4 12 21 33 31 10  1    0  1  4 12 21 34 26  7  1  
  0  1  6 17 36 55 54 29  6    0  2 10 28 58 86 78 38  8    0  2 10 29 61 88 68 28  5  
  0  2  9 25 46 64 65 44 11    0  3 15 38 71100 99 63 16    1  4 15 38 70100 91 48 10  
  0  3 12 31 52 62 56 38 10    0  4 17 44 77 97 91 60 16    0  3 16 42 70 90 82 48 12  
  0  2 10 28 48 51 40 23  5    0  3 13 40 70 82 67 39  9    0  2 12 36 62 72 58 32  8  
  0  1  5 17 30 33 24 11  2    0  1  7 24 48 56 41 20  4    0  1  6 22 44 50 35 16  4  
  0  0  1  5 11 14 10  5  1    0  0  2  8 20 27 20  8  2    0  0  2  8 21 26 17  7  1  
  0  0  0  1  3  4  3  2  1    0  0  1  2  5  8  6  3  1    0  0  0  2  6  9  6  2  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  1  1  0    0  0  0  0  1  1  1  0  0  
!Region 3: Section 7->9
  0  1  2  6 12 21 15  4  0    0  0  0  2  4  6  4  1  0    0  0  0  0  0  1  0  0  0  
  0  1  5 16 37 54 39 13  2    0  0  1  4 11 16 11  4  1    0  0  0  1  2  2  1  0  0  
  0  2  8 22 42 59 50 22  4    0  0  2  6 13 18 13  5  1    0  0  0  1  2  2  1  0  0  
  0  2  8 23 39 48 40 20  4    0  0  2  7 12 13 10  4  1    0  0  0  1  2  2  1  0  0  
  0  1  6 19 32 33 25 12  3    0  0  2  5  8  7  5  2  0    0  0  0  1  1  1  1  0  0  
  0  0  3 11 20 21 13  6  1    0  0  1  3  4  3  2  1  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4  9 10  6  2  0    0  0  0  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  3  2  1  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 97.35   Thresh = 0.020   Blend = F   #Contributing = 13   InitialProfileWt = 0.201
Region 4
Sum = 17740.5;   Maximum = 274.07;   FM = 0.668
!Region 4: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  1  1  2  1  1  0  0    0  1  2  5  8  8  4  1  0  
  0  0  0  0  0  0  0  0  0    0  1  1  3  4  4  2  1  0    0  2  5 11 15 16 11  4  1  
  0  0  0  0  0  0  0  0  0    0  1  1  3  3  3  1  1  0    0  2  6 12 16 15 11  6  1  
  0  0  0  0  0  0  0  0  0    0  1  2  2  3  2  1  0  0    0  2  6 11 14 13  9  5  1  
  0  0  0  0  0  0  0  0  0    0  1  1  2  2  1  1  0  0    0  2  5  9 11  9  6  3  1  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0    0  1  3  6  7  6  4  2  1  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  1  1  2  3  3  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 4: Section 4->6
  0  2  8 18 29 28 17  6  1    0  3 11 24 39 37 23  9  2    0  2  7 17 27 27 19  8  1  
  1  5 15 32 51 59 44 21  5    1  6 20 44 76 89 66 31  8    1  4 14 35 65 77 57 26  6  
  1  6 19 37 56 65 53 30  9    1  8 24 50 82100 84 46 14    1  5 17 39 68 88 76 40 10  
  1  7 20 38 54 57 44 26  9    1  8 26 52 79 89 72 43 15    1  5 17 39 64 79 70 40 11  
  1  5 17 33 46 43 31 18  6    1  7 21 45 68 70 54 31 11    1  4 14 33 55 65 54 30 10  
  0  3 10 22 30 29 21 12  4    1  4 13 30 46 49 38 21  6    0  2  8 22 39 48 38 19  5  
  0  1  4  9 14 15 12  6  2    0  2  5 14 24 28 22 12  3    0  1  3 10 22 29 23 10  3  
  0  0  1  3  4  6  5  3  1    0  0  1  4  8 11 10  5  1    0  0  1  3  8 12 10  5  1  
  0  0  0  0  1  1  1  1  0    0  0  0  1  1  2  2  1  0    0  0  0  1  1  2  2  1  0  
!Region 4: Section 7->9
  0  1  2  7 12 15 13  5  1    0  0  1  1  3  4  4  2  0    0  0  0  0  0  0  0  0  0  
  1  2  6 18 35 44 34 16  3    0  1  1  4  8 12 10  5  1    0  0  0  0  1  1  1  1  0  
  1  2  8 20 38 52 46 24  5    0  1  2  4  9 14 13  7  1    0  0  0  0  1  1  1  1  0  
  1  2  8 20 35 47 43 23  5    0  0  1  4  9 13 11  6  1    0  0  0  0  1  1  1  1  0  
  0  2  6 16 30 38 32 17  5    0  0  1  4  7  9  8  4  1    0  0  0  0  1  1  1  0  0  
  0  1  3 10 21 28 22 10  3    0  0  1  2  5  6  5  2  1    0  0  0  0  0  0  0  0  0  
  0  0  1  5 12 17 13  5  1    0  0  0  1  2  4  2  1  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  5  7  5  2  1    0  0  0  0  1  1  1  1  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  1  1  1  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 68.22   Thresh = 0.020   Blend = F   #Contributing = 35   InitialProfileWt = 0.053
Region 5
Sum = 13918.3;   Maximum = 173.169;   FM = 0.597
!Region 5: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  1  2  2  1  1  0  0    1  3  8 11 12 10  6  3  1  
  0  0  0  0  0  0  0  0  0    0  1  3  4  4  3  2  1  0    2  8 16 22 22 18 13  7  2  
  0  0  0  0  0  0  0  0  0    0  2  3  4  4  2  2  1  0    2  8 16 20 20 17 12  7  2  
  0  0  0  0  0  0  0  0  0    1  2  3  4  3  2  1  1  1    2  8 14 18 17 14 10  5  2  
  0  0  0  0  0  0  0  0  0    0  1  2  3  2  1  1  1  0    1  6 10 13 13 12  8  4  1  
  0  0  0  0  0  0  0  0  0    0  1  1  2  1  1  1  0  0    1  4  7  8  9  8  5  2  1  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  1  0  0    1  2  3  4  5  4  3  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  1  1  1  2  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0  
!Region 5: Section 4->6
  1  7 16 25 33 31 23 12  4    2  7 17 33 52 55 42 22  6    1  4 11 25 44 53 44 24  6  
  4 17 35 53 63 59 44 26  8    4 17 39 70 97100 79 49 15    2  9 24 51 83 97 84 54 17  
  4 18 36 52 60 57 44 26  8    4 17 40 68 94 99 81 53 17    2  9 24 50 80 95 87 59 19  
  4 17 33 46 52 48 37 22  7    3 16 37 63 83 86 71 46 15    1  8 21 45 71 84 77 52 17  
  3 13 25 36 41 39 30 17  5    2 12 29 50 66 69 57 37 12    1  5 16 36 57 68 63 42 14  
  2  8 16 23 27 27 21 12  4    1  7 19 34 46 49 41 27  9    0  3 10 24 40 50 47 32 10  
  1  4  7 11 14 15 12  7  2    1  3  8 17 25 28 25 17  6    0  2  5 12 22 29 29 20  7  
  0  1  3  4  6  6  5  3  1    0  1  3  6 10 12 11  8  3    0  1  2  5  9 12 13 10  4  
  0  0  1  1  1  1  1  1  0    0  0  1  1  2  3  3  2  1    0  0  0  1  2  3  3  3  1  
!Region 5: Section 7->9
  0  1  3 10 18 27 28 16  4    0  0  1  2  4  7  9  6  2    0  0  0  0  0  1  1  1  0  
  1  3  8 20 37 51 52 36 11    0  1  2  4  8 14 18 14  4    0  0  0  1  1  1  2  2  1  
  1  3  8 19 35 49 53 39 12    0  1  2  4  8 14 17 14  4    0  0  0  0  1  1  2  2  1  
  1  3  7 17 31 44 46 33 10    0  1  2  3  7 12 15 11  3    0  0  0  0  1  1  2  1  0  
  0  2  5 13 24 36 38 26  8    0  1  1  3  5 10 12  8  2    0  0  0  0  1  1  1  1  0  
  0  1  3  8 16 25 28 19  5    0  1  1  2  3  6  8  5  1    0  0  0  0  0  1  1  0  0  
  0  1  2  4  8 14 17 12  3    0  0  0  1  2  3  4  3  1    0  0  0  0  0  0  0  0  0  
  0  1  1  1  3  6  8  6  2    0  0  0  0  0  1  2  2  1    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  1  2  2  1    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 62.27   Thresh = 0.020   Blend = F   #Contributing = 28   InitialProfileWt = 0.079
Region 6
Sum = 10466.1;   Maximum = 123.372;   FM = 0.609
!Region 6: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  1  2  2  1  1  0  0    1  3  7 10 11 10  7  4  1  
  0  0  0  1  1  0  0  0  0    1  1  3  5  5  3  2  1  0    2  8 16 22 23 20 15  8  2  
  0  0  0  1  1  0  0  0  0    1  2  3  5  5  3  2  1  1    2  9 17 23 24 20 15  8  2  
  0  0  0  1  1  0  0  0  0    1  2  3  5  4  3  2  1  1    2  9 18 23 22 17 11  6  2  
  0  0  0  0  0  0  0  0  0    1  1  2  3  3  2  1  1  0    2  7 13 16 15 11  7  4  1  
  0  0  0  0  0  0  0  0  0    0  1  2  2  2  1  1  1  0    2  6 10 12 11  7  4  2  1  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  0  0  0    1  4  6  7  6  3  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    1  2  3  3  3  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  0  0  0  
!Region 6: Section 4->6
  2  7 18 27 31 30 25 17  5    2  8 20 34 47 50 43 29 10    1  5 12 26 44 53 43 27  9  
  5 19 40 56 63 59 48 31  9    5 19 42 68 90 94 82 57 20    2  9 22 45 75 93 90 67 25  
  5 20 41 59 66 60 49 31 10    5 20 44 73 98 99 83 57 20    2  9 24 51 84100 92 66 24  
  5 21 42 56 58 49 37 21  6    5 19 42 68 85 81 65 42 15    2  9 23 48 78 90 79 55 21  
  5 19 35 44 44 36 27 14  4    5 19 38 57 69 64 49 30 11    2  8 20 41 65 70 59 40 16  
  4 14 24 28 27 23 15  8  2    3 13 27 38 44 39 28 16  5    1  6 15 31 45 45 35 23  8  
  3 10 16 17 15 12  7  3  1    2  9 17 22 23 20 14  8  3    1  3  8 16 22 21 17 12  4  
  1  5  6  7  7  6  4  2  1    1  4  7 10 11 10  7  4  1    0  2  4  8 10 10  7  5  2  
  0  1  2  2  2  1  1  0  0    0  1  2  2  2  2  1  1  0    0  0  1  1  2  2  2  2  1  
!Region 6: Section 7->9
  0  2  5 12 21 28 23 14  4    0  0  1  2  3  5  5  4  1    0  0  0  0  0  1  1  1  0  
  1  3  7 18 35 50 55 44 17    0  1  2  3  6 12 15 13  5    0  0  0  0  1  2  2  2  1  
  1  3  8 21 39 54 58 45 16    0  1  2  3  7 13 17 14  5    0  0  0  0  1  2  3  3  1  
  1  3  8 20 39 54 55 41 15    0  1  1  3  7 13 16 14  5    0  0  0  0  1  2  3  2  1  
  1  2  6 16 31 41 40 29 11    0  1  1  2  5  9 12 10  4    0  0  0  1  1  1  2  2  1  
  0  2  5 12 23 28 26 19  7    0  0  1  1  4  6  8  7  3    0  0  0  0  0  1  1  1  0  
  0  1  2  6 11 13 13 10  4    0  0  0  0  2  3  4  4  2    0  0  0  0  0  0  0  0  0  
  0  0  1  3  5  6  5  4  2    0  0  0  0  1  2  2  2  1    0  0  0  0  0  1  0  0  0  
  0  0  0  1  2  2  2  2  1    0  0  0  0  0  0  1  1  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 57.62   Thresh = 0.020   Blend = F   #Contributing = 32   InitialProfileWt = 0.079
Region 7
Sum = 9722.48;   Maximum = 153.499;   FM = 0.604
!Region 7: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  1  2  4  7  9  7  3  1  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  2  1  0  0    0  2  6 11 15 17 14  6  1  
  0  0  0  0  0  0  0  0  0    0  0  1  1  2  2  1  1  0    0  2  7 13 17 18 13  6  1  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  2  1  1  0    0  2  7 13 17 15 10  4  1  
  0  0  0  0  0  0  0  0  0    0  0  1  1  2  2  1  0  0    0  2  6 11 14 11  6  2  1  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  1  0  0    0  2  5  8 10  7  3  1  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  0  0  0    0  2  3  5  6  4  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0    0  1  2  3  3  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0  
!Region 7: Section 4->6
  0  2  7 15 26 30 24 12  3    0  2 10 26 43 50 41 23  6    0  1  7 22 38 49 43 25  6  
  1  5 18 37 53 57 45 23  5    1  6 22 55 89 98 76 42 11    1  4 16 45 84100 80 45 13  
  1  5 20 42 57 56 41 19  4    1  7 25 61 93 93 67 34  9    1  5 18 50 89 97 70 36 10  
  1  5 20 42 52 45 30 12  2    1  7 26 59 82 73 48 22  5    1  5 19 50 80 76 49 23  6  
  1  5 18 34 39 31 18  7  1    1  7 24 50 61 48 28 12  2    1  5 19 44 60 49 28 12  3  
  1  4 13 24 25 19 10  4  1    1  5 19 36 37 27 15  6  1    1  5 16 32 36 26 14  5  1  
  1  3  9 15 15 10  5  2  0    1  4 13 21 20 13  6  2  0    0  3 11 19 18 11  6  2  0  
  0  2  5  8  7  4  2  0  0    0  2  7 11  9  5  2  1  0    0  2  6  9  7  4  2  1  0  
  0  0  1  2  2  1  0  0  0    0  1  2  3  2  1  1  0  0    0  1  2  3  2  1  0  0  0  
!Region 7: Section 7->9
  0  1  3  9 17 26 24 14  4    0  1  1  2  4  7  7  4  1    0  0  0  0  0  1  1  1  0  
  1  2  7 19 39 54 48 27  7    0  1  2  3  9 16 16  9  2    0  0  1  1  1  3  3  2  0  
  1  3  8 21 43 54 42 22  6    0  1  2  4  9 16 14  7  2    0  0  1  1  1  3  3  1  0  
  1  3  8 22 39 43 29 14  3    0  1  2  3  8 12 10  4  1    0  0  0  1  1  2  2  1  0  
  1  3  8 19 30 27 15  7  2    0  1  2  3  5  7  5  2  1    0  0  0  0  1  1  1  1  0  
  0  2  6 13 18 14  7  3  1    0  0  1  2  4  4  2  1  0    0  0  0  1  1  1  1  1  0  
  0  1  4  8  9  6  4  2  0    0  0  1  1  2  2  2  1  0    0  0  0  1  1  1  1  1  0  
  0  1  2  4  4  2  2  1  0    0  0  0  1  1  2  1  1  0    0  0  0  1  1  1  1  0  0  
  0  1  1  1  1  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 96.40   Thresh = 0.020   Blend = F   #Contributing = 24   InitialProfileWt = 0.118
Region 8
Sum = 25601.3;   Maximum = 476.075;   FM = 0.603
!Region 8: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  2  5  6  5  4  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    1  3  8 12 12  9  4  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  2  7 12 15 12  6  2  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  1  5 10 14 12  5  2  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  1  0  0    0  1  3  7 10  9  4  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  1  4  5  5  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  1  2  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 8: Section 4->6
  1  6 17 24 21 13  6  2  1    3 13 31 42 36 21  9  3  1    3 15 31 41 32 18  7  2  1  
  2 12 32 48 48 34 16  5  1    5 26 62 89 84 54 23  7  1    7 30 66 88 78 46 17  5  1  
  2  9 28 48 56 42 19  5  1    4 22 59 95 98 64 25  7  1    6 28 68100 93 53 17  4  1  
  1  6 20 41 53 39 17  4  1    3 16 47 84 90 55 20  5  1    4 21 58 92 86 43 12  3  0  
  0  3 12 28 37 27 11  3  1    2 10 32 60 62 35 12  3  1    2 13 41 68 59 26  7  1  0  
  0  2  6 15 18 14  6  1  0    1  5 17 33 32 17  6  1  0    1  7 22 38 30 12  3  1  0  
  0  1  3  6  7  5  2  1  0    0  2  8 14 12  6  2  1  0    0  3  9 16 11  4  1  0  0  
  0  0  1  2  2  2  1  0  0    0  1  3  4  4  2  1  0  0    0  1  3  4  3  1  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  1  1  0  0  0  0  
!Region 8: Section 7->9
  2  8 17 20 15  8  3  1  0    1  2  4  4  3  2  1  0  0    0  0  0  0  0  0  0  0  0  
  4 19 38 46 37 21  8  2  0    1  6 10 11  8  4  2  0  0    0  0  1  1  1  0  0  0  0  
  4 19 43 56 45 24  8  2  0    1  6 13 14 10  4  2  0  0    0  0  1  1  1  0  0  0  0  
  2 15 39 53 41 19  5  1  0    1  5 12 14  8  3  1  0  0    0  0  1  1  1  0  0  0  0  
  2  9 26 37 28 11  3  1  0    1  3  7  9  5  2  0  0  0    0  0  0  0  0  0  0  0  0  
  1  4 12 19 13  5  1  0  0    0  1  3  4  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  2  5  7  5  2  1  0  0    0  1  1  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  1  2  1  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 78.34   Thresh = 0.020   Blend = F   #Contributing = 5   InitialProfileWt = 0.586
Region 9
Sum = 16274;   Maximum = 287.091;   FM = 0.633
!Region 9: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  1  3  3  3  4  3  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  2  5 10 14 14  9  3  1  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  1  4 11 19 20 14  5  1  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  2  9 18 21 14  4  1  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  6 13 14  7  2  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  3  6  6  3  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  2  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 9: Section 4->6
  0  4 12 10 10 12  9  3  1    1  8 18 20 21 19 11  3  0    2  8 19 33 42 36 17  3  0  
  1  7 18 34 45 42 27 10  2    3 16 37 57 63 50 27  9  1    4 21 53 83 89 65 29  7  1  
  1  5 15 37 58 60 41 15  2    3 13 34 63 78 67 38 13  2    4 22 56 90100 76 35  9  1  
  0  3 10 31 56 62 39 12  2    2  9 28 56 75 66 36 10  1    3 17 51 86 96 73 30  7  1  
  0  2  6 21 39 39 20  5  0    1  5 18 41 55 43 18  4  0    2 11 37 71 77 49 16  3  0  
  0  1  3 10 19 17  7  2  0    0  2  9 22 29 19  6  1  0    1  5 20 42 45 23  4  1  0  
  0  0  1  3  5  4  2  0  0    0  1  3  8 10  5  2  0  0    0  2  7 16 17  7  1  0  0  
  0  0  0  1  1  1  1  0  0    0  0  1  2  2  1  0  0  0    0  0  1  3  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 9: Section 7->9
  1  5 12 22 30 26 12  2  0    0  1  3  3  3  2  1  0  0    0  0  0  0  0  0  0  0  0  
  3 14 36 57 61 46 22  5  1    1  4  8  8  6  4  2  0  0    0  1  1  1  0  0  0  0  0  
  3 16 41 63 69 54 26  7  1    1  5 10 11  8  5  2  1  0    0  1  2  2  1  0  0  0  0  
  2 14 40 62 67 52 22  5  1    1  4 10 12  9  5  2  1  0    0  0  1  2  1  0  0  0  0  
  1  9 30 52 55 35 12  2  0    0  2  6  9  8  4  1  0  0    0  0  1  1  1  0  0  0  0  
  1  4 16 32 33 17  3  1  0    0  1  3  5  4  2  0  0  0    0  0  0  1  0  0  0  0  0  
  0  2  6 12 12  5  1  0  0    0  0  1  2  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  2  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (202 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       202         0       202    2.4558    0.9413    36.591   109.972

Orientation ('UB') matrix:
  -0.0356087   0.0176087   0.0618407
  -0.0281930  -0.0063262  -0.1678873
  -0.0229774  -0.0195265   0.1101596

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6464   36.9770    4.7594    90.000    90.000    90.000       3457.58
    0.0017    0.0030    0.0004     0.000     0.000     0.000          0.62
Corrected for goodness of fit:
    0.0024    0.0043    0.0006     0.000     0.000     0.000          0.88

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.779      58.379     -32.014
Goniometer zeros (deg):          0.0000*     0.0694      0.0000*     0.1191    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                      -0.3324  -0.1436  -0.0013  -0.3675  -0.1810  -0.2213

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        1.30022e+004  1.21986e+003    1.44       5         5       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 202             202             202
 Average input ESD (pix, pix, deg):          0.11658         0.11427         0.03736
 Goodness of fit:                            1.27533         1.75066         1.16088

Average missing volume:         0.062

Repeat orientation and spot-shape refinement ============= 01/23/2020 16:55:03

Current XYZ spot size:            0.440   0.440   0.940
Accurate-timing indicator is set in the frame headers:
   Velocity normalization will be computed for each frame
Pixel spacing (deg):              0.111
Profile X,Y,Z spacing (deg):      0.079   0.079   0.171
Profile convolver halfwidth:       1.23    1.23    1.75
Background pixels updated = 98.00%            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
    0_0001    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   21 0.44 0.44 0.94 1.000
    1_0002    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   18 0.44 0.44 0.94 1.000
    2_0003    1 -0.06 -0.27 -0.03  0.06  0.27  0.03 109835  68    0  0.62   28 0.44 0.44 0.94 1.000
    3_0004    7 -0.10 -0.27 -0.05  0.11  0.28  0.08  73230  39    0  0.81   30 0.44 0.44 0.94 1.000
    4_0005   13 -0.00 -0.32 -0.03  0.13  0.39  0.10 133435  47    0  0.87   32 0.44 0.44 0.94 1.000
    5_0006   11 -0.04 -0.28 -0.01  0.11  0.30  0.08 136741  55    0  0.91   31 0.44 0.44 0.94 1.000
    6_0007   13  0.00 -0.34 -0.10  0.13  0.39  0.13  42694  29    8  0.87   33 0.44 0.44 0.94 1.000
    7_0008    4 -0.09 -0.07  0.04  0.11  0.32  0.16 106758  51   25  0.84   36 0.44 0.44 0.94 1.000
    8_0009    7 -0.04 -0.24  0.02  0.09  0.26  0.09  37342  24    0  0.92   33 0.44 0.44 0.94 1.000
    9_0010    7 -0.03 -0.33 -0.02  0.11  0.38  0.09  72496  40    0  0.94   33 0.44 0.44 0.94 1.000
   10_0011   17 -0.09 -0.26  0.01  0.13  0.32  0.07  66567  38    0  0.88   31 0.44 0.44 0.94 1.000
   11_0012   12 -0.01 -0.26 -0.02  0.11  0.29  0.09  81115  44    0  0.93   34 0.44 0.44 0.94 1.000
   12_0013    9 -0.09 -0.18 -0.00  0.17  0.23  0.06  58216  40   11  0.86   30 0.44 0.44 0.94 1.000
   13_0014    8 -0.01 -0.22 -0.04  0.03  0.23  0.09  53542  42    0  0.93   33 0.44 0.44 0.94 1.000
   14_0015    8 -0.01 -0.22 -0.01  0.08  0.25  0.09  36012  30    0  0.90   32 0.44 0.44 0.94 1.000
   15_0016   12  0.02 -0.20 -0.01  0.12  0.21  0.06  77860  41    0  0.93   31 0.44 0.44 0.94 1.000
   16_0017    7 -0.02 -0.17 -0.07  0.06  0.19  0.11 107604  46    0  0.95   33 0.44 0.44 0.94 1.000
   17_0018    8 -0.02 -0.16 -0.01  0.04  0.18  0.05 116919  60    0  0.94   31 0.44 0.44 0.94 1.000
   18_0019    9  0.01 -0.17 -0.00  0.03  0.18  0.06 132055  59    0  0.94   33 0.44 0.44 0.94 1.000
   19_0020   10 -0.02 -0.22 -0.02  0.20  0.30  0.11  99057  48    0  0.95   34 0.44 0.44 0.94 1.000
Background pixels updated = 98.18%            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   20_0021    8 -0.03 -0.16  0.03  0.09  0.18  0.08  76318  44    0  0.94   32 0.44 0.44 0.94 1.000
   21_0022    5 -0.01 -0.15  0.03  0.05  0.17  0.05  34981  30    0  0.91   31 0.44 0.44 0.94 1.000
   22_0023    8 -0.13 -0.16  0.04  0.30  0.18  0.11  83074  44    0  0.91   34 0.44 0.44 0.94 1.000
   23_0024    8  0.07 -0.13 -0.05  0.16  0.14  0.09  53328  38   13  0.91   32 0.44 0.44 0.94 1.000
   24_0025    5 -0.00 -0.12 -0.01  0.04  0.13  0.03 120200  63    0  0.93   28 0.44 0.44 0.94 1.000
   25_0026   14 -0.00 -0.10 -0.03  0.11  0.17  0.11  62867  41    0  0.89   29 0.44 0.44 0.94 1.000
   26_0027   10  0.02 -0.13 -0.02  0.11  0.16  0.08  41304  35   10  0.88   32 0.44 0.44 0.94 1.000
   27_0028    6 -0.02 -0.17  0.04  0.06  0.17  0.09 107401  58    0  0.96   34 0.44 0.44 0.94 1.000
   28_0029   17 -0.01 -0.11  0.00  0.07  0.16  0.06  66937  40    0  0.92   31 0.44 0.44 0.94 1.000

I/Sigma = 116.43   Thresh = 0.020   Blend = F   #Contributing = 62   InitialProfileWt = 0.041
Region 1
Sum = 38107.7;   Maximum = 587.216;   FM = 0.918
!Region 1: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  1  1  2  2  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  1  2  2  2  1  0  0    1  2  4  7  8  6  3  1  0  
  0  0  0  0  0  0  0  0  0    0  1  2  3  4  3  2  1  0    1  3  7 11 14 12  7  3  1  
  0  0  0  0  0  0  0  0  0    0  1  3  6  7  7  4  2  0    1  4 10 17 21 19 12  5  1  
  0  0  0  0  1  0  0  0  0    0  2  3  6  9  9  5  2  0    1  4 10 17 23 23 14  6  1  
  0  0  0  0  0  0  0  0  0    0  1  3  6  8  7  4  2  0    1  4  9 15 20 18 10  4  1  
  0  0  0  0  0  0  0  0  0    0  1  2  4  5  4  2  1  0    1  3  7 10 12 10  5  2  0  
  0  0  0  0  0  0  0  0  0    0  1  1  2  2  1  1  0  0    1  2  4  6  6  4  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  1  2  2  2  1  0  0  0  
!Region 1: Section 4->6
  0  2  6  9  9  6  3  1  0    1  3  9 15 16 11  6  3  1    0  1  4  9 11  9  5  2  1  
  2  7 17 30 34 26 14  5  1    2  9 24 45 54 42 22  9  2    1  4 13 26 35 29 17  7  2  
  2 10 25 45 56 47 28 11  3    3 13 36 66 84 72 42 18  4    1  7 20 39 52 46 28 12  3  
  3 13 30 54 70 62 39 16  3    4 17 41 76 99 90 56 24  5    2  9 23 45 59 54 35 15  3  
  3 13 31 54 70 65 41 17  4    4 18 43 75100 93 59 25  6    2  9 25 45 60 56 36 15  3  
  3 13 30 49 61 51 29 11  2    4 17 40 70 88 75 43 17  3    2  8 22 41 54 47 27 11  2  
  2 10 23 36 42 31 16  5  1    3 13 31 54 64 48 23  8  2    1  6 16 31 40 32 17  6  1  
  2  7 14 21 22 15  7  2  0    2  8 19 32 35 24 11  3  1    1  3  9 18 22 16  8  3  1  
  1  2  4  6  6  4  2  0  0    1  2  5  8  8  6  2  1  0    0  1  2  4  5  4  2  1  0  
!Region 1: Section 7->9
  0  0  1  2  4  5  3  1  0    0  0  0  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  1  4 10 15 15  9  4  1    0  0  1  3  4  4  3  1  0    0  0  0  0  0  0  0  0  0  
  0  2  8 17 23 21 13  6  1    0  1  2  5  6  6  3  2  0    0  0  0  0  0  0  0  0  0  
  1  3 11 21 27 24 15  6  1    0  1  3  7  8  7  4  2  0    0  0  0  0  0  0  0  0  0  
  1  4 11 22 28 25 15  6  1    0  1  4  7  9  7  4  2  0    0  0  0  0  0  0  0  0  0  
  1  3  8 19 25 22 12  5  1    0  1  3  6  8  6  3  1  0    0  0  0  0  0  0  0  0  0  
  0  2  5 12 18 16  9  3  1    0  1  1  4  6  5  3  1  0    0  0  0  0  0  0  0  0  0  
  0  1  2  6  9  8  5  2  0    0  0  1  2  3  2  1  1  0    0  0  0  0  0  0  0  0  0  
  0  0  1  1  2  2  1  1  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 0.00   Thresh = 0.020   Blend = F   #Contributing = 0   InitialProfileWt = 1.000
Region 2
Sum = 1.02933;   Maximum = 0.01619;   FM = 0.946
!Region 2: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  1  3  4  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  3  2  1  0  0    0  1  4 11 13 10  4  1  0  
  0  0  0  0  0  0  0  0  0    0  0  2  4  5  5  3  1  0    0  2  7 17 24 22 12  4  1  
  0  0  0  0  0  0  0  0  0    0  1  2  4  7  8  5  2  0    0  2  8 21 32 34 22  8  1  
  0  0  0  0  0  0  0  0  0    0  1  2  4  8  8  6  2  0    0  3  9 21 34 36 25  9  1  
  0  0  0  0  0  0  0  0  0    0  1  2  4  6  7  4  2  0    0  3  8 18 27 28 18  6  1  
  0  0  0  0  0  0  0  0  0    0  0  1  2  4  3  2  1  0    0  2  5 11 16 14  8  3  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  2  1  1  0  0    0  1  2  5  7  5  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  1  2  1  1  0  0  
!Region 2: Section 4->6
  0  1  4  7  8  5  2  1  0    0  2  6 10 12  8  3  1  0    0  1  4  8 10  7  3  1  0  
  0  4 12 25 30 20  8  2  0    1  6 20 40 47 31 12  3  1    0  4 16 34 40 27 10  2  0  
  1  6 19 39 52 45 23  6  1    1 10 33 62 77 61 29  8  1    1  8 28 55 67 50 22  5  1  
  1  8 23 47 66 65 41 14  2    2 13 40 74 95 85 48 15  2    2 12 36 66 83 69 35 10  1  
  1  8 24 48 69 68 44 17  3    2 14 42 77100 89 53 19  3    2 12 38 69 85 72 39 12  2  
  1  7 22 43 59 53 32 11  2    2 11 37 71 89 72 38 13  2    1  9 33 62 74 58 28  9  1  
  1  4 15 30 38 30 15  5  1    1  7 24 51 63 45 20  6  1    1  5 21 45 53 36 15  4  1  
  0  2  6 14 18 13  5  2  0    0  3 11 25 31 21  8  2  0    0  2  9 22 27 17  6  2  0  
  0  1  1  3  4  3  1  0  0    0  1  2  6  7  5  2  1  0    0  1  2  5  6  4  1  0  0  
!Region 2: Section 7->9
  0  0  1  3  3  2  1  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  6 12 15  9  3  1  0    0  0  1  2  2  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  3 10 22 28 20  8  2  0    0  1  2  5  6  4  1  0  0    0  0  0  0  1  0  0  0  0  
  1  5 14 27 35 27 12  3  0    0  1  3  6  8  5  2  1  0    0  0  0  1  1  0  0  0  0  
  1  5 16 28 33 26 13  4  1    0  1  4  7  7  5  2  1  0    0  0  0  1  1  0  0  0  0  
  0  4 13 24 27 19  9  3  0    0  1  3  5  5  3  1  0  0    0  0  0  1  1  0  0  0  0  
  0  2  8 17 18 12  5  2  0    0  0  2  3  3  2  1  0  0    0  0  0  0  0  0  0  0  0  
  0  1  3  8  9  5  2  1  0    0  0  1  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  2  1  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 167.17   Thresh = 0.020   Blend = F   #Contributing = 5   InitialProfileWt = 0.513
Region 3
Sum = 62202;   Maximum = 914.464;   FM = 0.936
!Region 3: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  2  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  2  1  0  0    0  1  3  7 11  9  3  1  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  3  4  2  1  0    0  2  5 12 20 21 11  3  0  
  0  0  0  0  0  0  0  0  0    0  1  1  3  4  4  3  1  0    0  3  8 17 26 27 17  6  1  
  0  0  0  0  0  0  0  0  0    0  1  2  3  4  4  2  1  0    1  4 12 22 26 23 15  6  1  
  0  0  0  0  0  0  0  0  0    0  1  2  4  4  2  1  1  0    1  4 13 21 22 16  9  4  1  
  0  0  0  0  0  0  0  0  0    0  1  1  2  2  1  1  0  0    0  3  9 14 14 10  5  2  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0    0  1  3  6  7  4  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  1  2  1  1  0  0  
!Region 3: Section 4->6
  0  1  2  7  8  4  1  0  0    0  1  4 10 12  5  1  0  0    0  1  4 10 10  4  1  0  0  
  0  3  9 22 31 21  7  1  0    1  4 15 36 45 27  8  1  0    0  4 15 36 42 22  6  1  0  
  1  5 16 35 56 52 25  6  1    1  8 25 56 82 69 30  6  1    1  8 25 57 80 59 21  4  0  
  1  9 24 47 68 72 47 16  2    2 13 36 69100100 60 18  2    1 12 33 66 96 87 43 11  1  
  2 12 31 56 70 65 46 20  3    2 16 43 77 99 96 66 27  3    2 14 39 68 87 81 50 17  2  
  2 11 33 55 61 48 31 14  2    2 14 43 75 87 73 47 21  3    1 12 37 62 71 59 36 14  2  
  1  6 22 40 42 31 16  6  1    1  8 30 57 64 47 26 10  1    1  7 24 46 51 38 20  7  1  
  0  2  8 18 21 15  7  3  1    0  3 12 28 34 25 11  4  1    0  2 10 24 29 20  9  3  0  
  0  0  1  4  5  4  2  1  0    0  0  2  7 10  7  3  1  0    0  0  2  7  9  5  2  1  0  
!Region 3: Section 7->9
  0  1  2  5  5  2  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  2  7 18 22 11  3  0  0    0  0  1  4  5  2  1  0  0    0  0  0  0  0  0  0  0  0  
  0  4 12 32 45 30  9  1  0    0  1  3  8 12  7  2  0  0    0  0  0  1  1  1  0  0  0  
  1  6 17 37 54 44 18  4  0    0  1  4 10 15 11  4  1  0    0  0  0  1  2  1  0  0  0  
  1  7 20 35 45 38 19  6  1    0  2  5 10 12  9  4  1  0    0  0  0  1  1  1  0  0  0  
  1  6 18 29 31 24 13  5  1    0  1  5  7  7  5  2  1  0    0  0  0  1  1  0  0  0  0  
  0  3 11 20 20 13  6  2  0    0  1  3  4  3  2  1  0  0    0  0  0  0  0  0  0  0  0  
  0  1  4  9 10  6  3  1  0    0  0  1  2  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  3  1  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 100.98   Thresh = 0.020   Blend = F   #Contributing = 14   InitialProfileWt = 0.201
Region 4
Sum = 19095.8;   Maximum = 264.507;   FM = 0.918
!Region 4: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  1  3  4  3  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  1  2  3  3  2  1  0  0    0  3  7 12 12  8  3  1  0  
  0  0  0  0  0  0  0  0  0    0  1  3  5  5  4  2  0  0    1  4 11 18 20 15  7  2  0  
  0  0  0  0  0  0  0  0  0    0  1  3  5  5  4  2  1  0    1  5 13 19 22 18 10  4  1  
  0  0  0  0  0  0  0  0  0    0  2  3  5  4  2  1  1  0    1  6 13 18 19 15  9  4  1  
  0  0  0  0  0  0  0  0  0    1  2  3  4  3  1  1  1  0    1  6 11 16 16 12  7  3  1  
  0  0  0  0  0  0  0  0  0    0  1  2  3  2  1  1  0  0    1  4  8 12 11  8  5  2  1  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  1  0  0  0    0  2  4  6  6  5  3  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  2  2  2  1  0  0  
!Region 4: Section 4->6
  1  3  8 11  9  5  2  0  0    1  4  9 13 12  7  2  1  0    0  2  5  7  8  5  2  1  0  
  1  8 20 32 33 22  8  2  0    2 10 25 42 45 30 12  3  0    1  5 15 29 34 22 10  3  1  
  2 11 28 49 59 47 22  6  1    3 13 35 65 81 66 32  9  1    1  8 23 48 65 53 27  8  1  
  3 14 33 55 71 65 39 14  2    4 17 42 74100 95 56 21  3    2 10 28 55 81 78 48 18  3  
  3 16 35 56 67 61 40 18  3    4 19 44 75 97 92 61 27  4    2 12 30 55 78 79 53 23  4  
  3 14 34 53 60 49 31 14  2    3 17 42 72 86 75 47 23  4    2 10 27 50 67 63 41 19  4  
  2 10 26 41 45 35 21  9  1    2 12 33 57 66 55 33 15  2    1  7 20 39 52 47 29 12  2  
  1  5 14 24 27 22 13  5  1    1  6 18 34 42 35 21  8  1    0  3 10 23 35 31 18  7  1  
  0  1  4  7  9  8  5  2  0    0  1  5 10 14 13  8  3  0    0  1  3  6 11 10  6  2  0  
!Region 4: Section 7->9
  0  1  1  3  4  3  1  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  2  6 13 18 12  6  2  0    0  1  1  2  4  3  1  1  0    0  0  0  0  0  0  0  0  0  
  1  3 10 24 37 30 16  5  1    0  1  2  5  8  7  4  2  0    0  0  0  0  0  1  0  0  0  
  1  5 13 29 46 46 28 11  2    0  1  3  6 10 11  7  3  1    0  0  0  0  1  1  1  0  0  
  1  5 14 29 44 46 31 13  3    0  1  3  6 10 10  7  3  1    0  0  0  0  1  1  1  0  0  
  1  5 13 25 37 36 24 11  2    0  1  2  5  8  8  5  2  1    0  0  0  0  1  1  0  0  0  
  1  3  9 19 28 26 16  7  1    0  1  2  4  6  5  3  1  0    0  0  0  0  0  0  0  0  0  
  0  1  4 11 19 17  9  4  1    0  0  1  2  3  3  2  1  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  5  5  3  1  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 74.59   Thresh = 0.020   Blend = F   #Contributing = 37   InitialProfileWt = 0.046
Region 5
Sum = 16445.3;   Maximum = 183.954;   FM = 0.839
!Region 5: Section 1->3
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  0  0  0  0    1  3  5  6  5  3  2  1  0  
  0  0  0  0  0  0  0  0  0    0  2  3  4  3  2  1  1  0    3 10 16 18 16 12  7  3  1  
  0  0  0  0  0  0  0  0  0    1  2  4  5  4  3  2  1  0    3 12 21 26 24 19 12  5  1  
  0  0  0  0  0  0  0  0  0    1  2  4  5  4  3  2  1  0    4 14 23 26 25 21 14  6  1  
  0  0  0  0  0  0  0  0  0    1  3  4  5  4  3  2  1  0    4 14 21 24 22 19 13  6  1  
  0  0  0  0  0  0  0  0  0    1  2  4  4  3  2  1  1  0    3 12 18 20 19 15 10  4  1  
  0  0  0  0  0  0  0  0  0    0  2  2  3  2  1  1  1  0    2  8 12 14 14 12  7  3  1  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  1  0  0    1  5  7  8  9  7  4  2  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  1  2  3  3  3  1  1  0  
!Region 5: Section 4->6
  2  7 12 13 13 10  6  2  0    2  8 13 18 21 18 11  5  1    1  4  8 15 20 17 12  6  1  
  5 18 32 41 40 32 19  8  2    5 18 37 56 63 53 34 16  4    2 10 24 44 56 51 35 18  4  
  6 23 42 57 60 51 33 16  3    5 22 46 74 91 83 57 29  7    3 12 29 55 78 78 58 31  8  
  7 25 45 60 65 58 41 21  5    6 23 48 79100 96 71 40 11    3 12 30 58 83 90 72 42 11  
  7 25 43 56 59 53 38 20  5    6 22 46 75 94 91 69 41 12    2 11 28 55 79 86 70 42 12  
  6 21 36 47 51 45 31 16  4    5 18 39 65 81 78 59 34 10    2  9 24 48 69 75 60 35 11  
  4 15 27 35 38 34 24 12  3    3 13 30 50 63 62 47 27  8    1  6 17 36 54 60 48 28  8  
  2  8 15 21 24 22 16  8  2    2  7 17 31 41 42 32 19  6    1  3 10 22 35 41 34 20  6  
  1  2  4  7  9  8  5  2  1    1  2  5  9 13 15 11  6  2    0  1  3  6 11 15 12  7  2  
!Region 5: Section 7->9
  0  1  2  5  8  8  7  4  1    0  0  1  1  1  2  2  1  0    0  0  0  0  0  0  0  0  0  
  1  3  7 15 24 26 21 11  2    0  1  1  2  5  7  7  4  1    0  0  0  0  0  1  1  1  0  
  1  3  9 19 33 40 34 19  4    0  1  1  3  7 11 12  7  1    0  0  0  0  1  1  1  1  0  
  1  4  9 20 34 44 41 24  6    0  1  2  4  7 12 13  8  2    0  0  0  0  1  1  1  1  0  
  1  3  9 19 32 42 38 23  6    0  1  2  4  7 11 12  7  1    0  0  0  0  1  1  1  1  0  
  1  3  7 16 27 36 32 19  5    0  1  1  3  6 10 10  5  1    0  0  0  0  1  1  1  0  0  
  0  2  5 11 21 28 26 14  3    0  1  1  2  4  7  7  4  1    0  0  0  0  0  1  1  0  0  
  0  1  3  7 13 18 17  9  2    0  1  1  1  3  4  4  2  0    0  0  0  0  0  0  0  0  0  
  0  1  1  2  4  6  6  4  1    0  0  0  1  1  1  2  1  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 66.64   Thresh = 0.020   Blend = F   #Contributing = 31   InitialProfileWt = 0.069
Region 6
Sum = 11875.7;   Maximum = 121.687;   FM = 0.837
!Region 6: Section 1->3
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  1  0  0    1  3  6  7  7  6  4  2  0  
  0  0  0  0  0  0  0  0  0    1  2  4  4  3  3  1  1  0    3 11 17 20 19 17 10  5  1  
  0  1  1  1  1  0  0  0  0    1  3  6  7  6  4  2  1  0    4 14 24 29 29 25 15  7  2  
  0  1  2  2  1  1  0  0  0    2  6  9 10  7  5  3  1  0    6 21 33 37 34 27 17  8  2  
  0  1  1  1  1  1  1  1  0    2  6  8  9  7  4  2  2  1    6 21 32 36 32 25 15  7  2  
  0  1  1  1  1  1  0  0  0    2  5  8  7  5  3  2  1  0    6 20 29 30 25 19 10  4  1  
  0  0  1  1  1  0  0  0  0    1  4  5  5  3  2  1  1  0    5 16 21 21 17 11  6  3  1  
  0  0  1  1  0  0  0  0  0    1  3  4  3  2  1  1  1  0    4 11 13 13 10  6  3  1  0  
  0  0  0  0  0  0  0  0  0    1  1  2  1  1  0  0  0  0    2  5  6  6  4  2  1  0  0  
!Region 6: Section 4->6
  2  8 15 19 20 19 14  6  2    2  8 18 29 35 32 23 12  2    1  4 11 22 32 31 22 12  2  
  5 22 37 46 49 45 30 15  4    4 18 36 56 69 67 50 29  6    2  7 19 39 59 66 55 32  6  
  7 29 52 70 73 64 45 23  6    5 25 52 82 97 91 67 37  9    2 11 28 53 76 82 67 38  7  
  9 35 61 78 79 67 46 24  7    6 28 56 86100 92 68 39  9    3 12 31 58 80 85 69 40  7  
  9 37 62 77 75 62 40 21  5    6 29 58 87 99 88 62 35  8    3 13 31 59 80 82 64 36  7  
  8 34 55 64 59 47 28 14  4    6 27 53 77 82 68 46 25  6    3 12 31 56 72 68 51 29  5  
  7 29 41 45 40 30 17  8  2    5 22 40 55 56 44 29 15  3    2  9 22 41 50 45 34 19  3  
  5 19 26 28 25 18  9  4  1    4 16 28 37 37 27 17  8  2    1  7 16 28 32 26 19 10  2  
  2  7  8  8  7  4  2  1  0    1  3  4  6  7  6  4  2  0    1  1  2  6  8  7  6  3  0  
!Region 6: Section 7->9
  0  1  3  6 11 12 10  5  1    0  0  0  0  1  1  1  1  0    0  0  0  0  0  0  0  0  0  
  0  2  6 13 25 33 31 18  3    0  1  1  2  4  6  7  4  1    0  0  0  0  0  0  1  0  0  
  1  3  8 18 30 39 36 20  3    0  1  1  2  5  7  8  4  1    0  0  0  0  1  1  1  1  0  
  1  4 10 21 34 42 38 22  3    0  1  1  3  6  9  9  5  1    0  0  0  0  1  1  1  1  0  
  1  4 10 21 33 40 36 19  3    0  1  1  3  6  9  9  5  1    0  0  0  0  1  1  1  1  0  
  1  3  9 20 31 35 30 17  3    0  1  1  2  5  7  8  4  1    0  0  0  0  1  1  1  1  0  
  0  2  6 14 23 26 23 12  2    0  0  1  2  4  6  7  4  1    0  0  0  0  0  1  1  1  0  
  0  2  4  9 13 13 12  6  1    0  0  0  1  2  3  3  2  0    0  0  0  0  0  0  1  0  0  
  0  0  1  3  5  5  5  2  0    0  0  0  0  1  1  1  1  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 67.59   Thresh = 0.020   Blend = F   #Contributing = 37   InitialProfileWt = 0.069
Region 7
Sum = 13152.9;   Maximum = 168.354;   FM = 0.877
!Region 7: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  1  1  0    0  1  4  7 10 10  6  2  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  3  2  1  1  0    1  4 11 18 23 22 14  5  1  
  0  0  0  0  0  0  0  0  0    0  1  2  3  3  3  1  1  0    1  7 17 26 30 29 17  7  1  
  0  0  1  1  0  0  0  0  0    0  1  2  3  4  3  1  1  0    1  9 21 32 36 32 19  7  1  
  0  0  1  1  0  0  0  1  0    0  1  2  4  5  3  2  1  0    2  9 24 36 38 30 16  6  1  
  0  0  0  0  0  0  0  0  0    0  1  2  4  4  3  2  1  0    2 10 24 35 33 23 11  4  1  
  0  0  0  1  1  0  0  0  0    0  1  2  4  4  2  1  0  0    2  9 20 28 24 14  6  2  0  
  0  0  0  1  1  0  0  0  0    0  1  2  3  3  2  0  0  0    1  7 14 19 15  8  3  1  0  
  0  0  0  0  0  0  0  0  0    0  1  1  1  1  1  0  0  0    1  3  6  7  6  3  1  0  0  
!Region 7: Section 4->6
  0  3  8 16 23 21 13  5  1    0  2  8 19 30 27 16  8  1    0  1  5 13 22 21 12  6  1  
  1  8 23 42 54 50 32 14  3    1  7 23 49 70 66 42 19  3    1  4 13 31 51 52 33 14  3  
  2 13 35 58 69 63 40 16  3    2 11 33 67 87 81 51 22  4    1  6 20 44 64 64 40 17  3  
  3 16 44 71 80 69 42 16  3    2 14 42 81100 86 53 22  4    1  8 25 54 75 69 42 18  3  
  3 18 48 77 81 63 35 13  2    3 16 47 87100 78 44 17  3    1  9 28 60 77 63 36 15  2  
  3 19 48 72 68 48 24  8  1    3 17 48 82 84 59 30 10  2    2 10 30 59 66 47 24  9  1  
  3 18 41 56 48 30 13  4  1    3 17 43 65 59 36 16  5  1    1 10 28 48 46 28 12  4  1  
  2 13 29 36 29 16  6  2  0    2 14 32 41 33 18  7  2  0    1  8 21 30 25 13  6  2  0  
  1  5 11 14 11  6  2  1  0    1  5 11 14 11  6  2  1  0    1  3  7 10  8  4  2  1  0  
!Region 7: Section 7->9
  0  1  2  4  7  7  4  2  1    0  0  0  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  2  4  9 16 18 11  5  1    0  1  1  1  3  4  2  1  0    0  0  0  0  0  0  0  0  0  
  1  2  6 13 22 25 16  6  1    0  1  1  2  4  6  3  1  0    0  0  0  0  0  0  0  0  0  
  1  3  7 16 28 29 18  7  1    0  1  1  2  6  8  5  1  0    0  0  0  0  1  1  0  0  0  
  1  3  8 18 28 27 16  6  1    0  1  1  2  5  7  4  1  0    0  0  0  0  0  0  0  0  0  
  1  3  8 18 23 19 10  4  1    0  1  1  2  4  5  3  1  0    0  0  0  0  0  0  0  0  0  
  1  3  7 14 15 10  5  2  0    0  1  1  1  2  2  2  1  0    0  0  0  0  1  1  0  0  0  
  0  2  6  9  8  5  2  1  0    0  1  1  1  1  1  1  1  0    0  0  0  1  0  0  0  0  0  
  0  1  2  3  3  2  1  0  0    0  0  0  0  1  1  1  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 101.61   Thresh = 0.020   Blend = F   #Contributing = 22   InitialProfileWt = 0.090
Region 8
Sum = 28059.2;   Maximum = 503.225;   FM = 0.93
!Region 8: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  1  2  5  6  4  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  2  2  1  1  0    0  2  7 14 16 11  5  2  0  
  0  0  0  0  0  0  0  0  0    0  0  1  3  3  3  1  1  0    0  3 11 21 24 18  9  3  1  
  0  0  0  0  0  0  0  0  0    0  0  1  3  4  3  2  1  0    0  3 12 23 30 25 13  5  1  
  0  0  0  0  0  0  0  0  0    0  0  1  2  4  4  2  1  0    0  3  9 21 31 28 16  5  1  
  0  0  0  0  0  0  0  0  0    0  0  1  2  3  4  2  1  0    0  2  7 17 27 26 14  4  1  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  3  2  1  0    0  1  4 12 18 17  9  3  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  2  1  1  0    0  1  3  6  9  8  4  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  1  2  3  2  1  0  0  
!Region 8: Section 4->6
  0  2  7 13 15  9  4  1  0    0  3  9 16 15  9  4  1  0    0  2  5  9  8  4  2  1  0  
  0  6 22 39 40 27 12  4  1    0  8 27 45 43 27 12  4  1    0  5 16 26 24 14  6  2  0  
  1 10 33 57 61 44 21  7  1    1 12 40 66 67 46 21  6  1    1  8 26 40 40 26 11  3  0  
  1 10 34 64 77 61 31 10  1    1 14 44 78 90 67 31  8  1    1 10 32 54 58 40 16  4  0  
  1  8 28 60 83 69 35 10  1    1 12 40 79100 75 32  8  1    1  9 32 60 68 46 17  4  0  
  1  6 21 50 72 59 28  7  1    1  9 32 70 88 62 24  5  1    1  7 27 56 62 37 12  2  0  
  0  3 14 34 47 37 16  4  1    1  6 22 49 58 37 13  3  0    1  5 18 40 41 22  6  1  0  
  0  2  8 18 24 17  7  2  0    0  3 12 27 29 17  6  1  0    0  3 10 21 20  9  3  1  0  
  0  1  2  5  7  5  2  0  0    0  1  4  7  8  5  2  0  0    0  1  3  6  5  2  1  0  0  
!Region 8: Section 7->9
  0  0  1  2  2  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  2  4  7  7  4  1  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  3  8 12 12  8  3  1  0    0  0  1  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  4 11 19 20 12  5  1  0    0  0  1  3  3  2  1  0  0    0  0  0  0  0  0  0  0  0  
  0  3 12 23 24 14  5  1  0    0  0  2  4  4  2  1  0  0    0  0  0  0  0  0  0  0  0  
  0  3 10 21 22 11  3  1  0    0  0  1  3  3  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  2  7 14 14  6  2  0  0    0  0  1  2  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  3  7  6  3  1  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  2  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 83.87   Thresh = 0.020   Blend = F   #Contributing = 5   InitialProfileWt = 0.586
Region 9
Sum = 18518.9;   Maximum = 314.166;   FM = 0.931
!Region 9: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  2  5  5  3  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  3  4  3  1  1  0    0  1  6 14 17 12  5  2  1  
  0  0  0  0  0  0  0  0  0    0  0  2  6  7  6  3  1  0    0  2  9 23 31 27 15  5  1  
  0  0  0  0  0  0  0  0  0    0  0  2  6 10 10  7  3  0    0  1  8 25 41 44 30 11  2  
  0  0  0  0  0  0  0  0  0    0  0  1  5 10 12  9  3  0    0  1  5 21 42 52 37 13  2  
  0  0  0  0  0  0  0  0  0    0  0  1  4  8 10  7  3  0    0  1  3 15 34 42 28  9  1  
  0  0  0  0  0  0  0  0  0    0  0  1  2  5  5  3  1  0    0  1  2  9 19 19 10  3  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  2  1  0  0    0  0  1  4  8  6  3  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  1  2  1  1  0  0  
!Region 9: Section 4->6
  0  1  4  7  8  5  2  1  0    0  2  6  9 11 10  4  1  0    0  1  5  6 10  9  4  1  0  
  0  3 13 25 27 18  7  2  1    0  6 23 42 46 32 13  3  0    0  4 19 35 41 30 12  3  0  
  0  5 20 40 47 37 19  6  1    1 10 38 66 69 51 24  6  1    1  9 33 57 60 45 21  5  1  
  0  5 20 45 63 59 36 12  2    2 12 43 78 90 70 34  9  1    2 12 41 71 78 58 27  7  1  
  0  4 16 40 67 71 44 14  2    1 11 40 78100 83 39 10  1    1 11 41 75 89 68 30  8  1  
  0  2 10 31 55 58 33  9  1    1  7 31 68 90 70 28  6  1    1  8 33 68 83 59 21  4  0  
  0  1  6 19 34 29 13  3  0    1  4 18 46 61 42 13  2  0    1  4 20 48 58 36 10  2  0  
  0  1  3  8 14 10  4  1  0    0  2  8 21 27 16  4  1  0    0  2  9 22 26 14  3  0  0  
  0  0  1  2  3  2  1  0  0    0  1  2  4  5  3  1  0  0    0  1  2  4  5  2  1  0  0  
!Region 9: Section 7->9
  0  0  1  1  2  2  1  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  5  8  9  7  3  1  0    0  0  1  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  3  9 14 14 10  5  1  0    0  1  1  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  4 13 20 20 13  6  2  0    0  1  3  3  1  0  0  0  0    0  0  0  1  0  0  0  0  0  
  0  4 13 23 24 16  7  2  0    0  1  3  4  2  1  0  0  0    0  0  0  1  0  0  0  0  0  
  0  3 11 22 23 15  5  1  0    0  0  2  3  3  1  0  0  0    0  0  0  1  0  0  0  0  0  
  0  1  6 15 16  9  2  0  0    0  0  1  2  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  1  3  6  7  4  1  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (213 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       213         0       213    2.4558    0.9412    36.591   109.982

Orientation ('UB') matrix:
  -0.0356031   0.0176138   0.0618630
  -0.0281852  -0.0063141  -0.1679692
  -0.0229963  -0.0195310   0.1100928

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6463   36.9719    4.7586    90.000    90.000    90.000       3456.48
    0.0015    0.0028    0.0004     0.000     0.000     0.000          0.56
Corrected for goodness of fit:
    0.0014    0.0026    0.0003     0.000     0.000     0.000          0.52

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.781      58.407     -32.033
Goniometer zeros (deg):          0.0000*     0.0670      0.0000*     0.1290    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                      -0.3746  -0.2397  -0.0004  -0.3856  -0.1646  -0.2175

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        2.35410e+003  5.32542e+002    0.92       2         5       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 213             213             213
 Average input ESD (pix, pix, deg):          0.11150         0.10782         0.03524
 Goodness of fit:                            1.10942         1.03416         0.44711


Old XYZ spot size:              0.440   0.440   0.940
New XYZ spot size:              1.373   1.300   0.950
Average missing volume:         0.062
% with too much missing I:      2.933
Fractional overlap in H,K,L:    0.000   0.000   0.000

End of pass 2.  Repeating shape determination...

Repeat orientation and spot-shape refinement ============= 01/23/2020 16:55:03

Current XYZ spot size:            1.373   1.300   0.950
Accurate-timing indicator is set in the frame headers:
   Velocity normalization will be computed for each frame
Pixel spacing (deg):              0.111
Profile X,Y,Z spacing (deg):      0.229   0.217   0.172
Profile convolver halfwidth:       1.00    1.00    1.74
Background pixels updated = 97.00%            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
    0_0001    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   20 0.00 0.00 1.09 1.000
    1_0002    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   19 0.00 0.00 1.09 1.000
    2_0003    1 -0.06 -0.10  0.01  0.06  0.10  0.01 155904  80    0  0.85   27 1.99 2.08 1.09 1.000
    3_0004    6 -0.07 -0.04 -0.02  0.15  0.13  0.07  87453  40    0  0.87   29 1.51 1.52 1.08 1.000
    4_0005   11  0.09 -0.16 -0.05  0.18  0.29  0.09 156802  49    0  0.91   32 1.43 1.52 1.06 1.000
    5_0006    9 -0.00 -0.09 -0.01  0.07  0.12  0.05 175349  67    0  0.96   31 1.47 1.64 1.04 1.000
    6_0007   12  0.09 -0.14 -0.08  0.38  0.50  0.17  51209  31    8  0.91   33 1.46 1.64 1.05 1.000
    7_0008    5 -0.04 -0.12  0.05  0.20  0.21  0.12  89778  44   20  0.86   33 1.50 1.66 1.04 1.000
    8_0009    6 -0.08  0.02 -0.01  0.18  0.16  0.03  48863  27    0  0.96   34 1.50 1.64 1.04 1.000
    9_0010    6  0.04 -0.14 -0.07  0.11  0.18  0.15  71742  39    0  0.94   33 1.48 1.69 1.04 1.000
   10_0011   15 -0.04 -0.05  0.00  0.10  0.14  0.09  84953  44    0  0.92   32 1.54 1.75 1.03 1.000
   11_0012   11 -0.06  0.03  0.03  0.11  0.27  0.07  90721  45    0  0.94   34 1.52 1.74 1.01 1.000
   12_0013    9 -0.03 -0.06 -0.00  0.08  0.08  0.06  84591  49   11  0.88   31 1.51 1.74 1.01 1.000
   13_0014    7 -0.01 -0.07  0.00  0.06  0.08  0.06  41578  37    0  0.96   33 1.49 1.72 1.00 1.000
   14_0015    8  0.01 -0.05 -0.03  0.05  0.10  0.05  44526  33    0  0.93   32 1.48 1.72 1.00 1.000
   15_0016   11  0.06 -0.03 -0.00  0.30  0.15  0.11  86701  42    0  0.95   31 1.51 1.71 0.99 1.000
   16_0017    7 -0.05 -0.00 -0.01  0.10  0.08  0.05 117779  47    0  0.97   33 1.51 1.71 0.99 1.000
   17_0018    6 -0.04 -0.03  0.02  0.05  0.07  0.03  87933  54    0  0.94   31 1.51 1.70 1.00 1.000
   18_0019    9 -0.01 -0.02 -0.01  0.06  0.06  0.04 140076  60    0  0.96   33 1.51 1.70 0.99 1.000
   19_0020    8  0.07 -0.01  0.01  0.26  0.28  0.13 118972  53    0  0.96   33 1.50 1.72 0.99 1.000
Background pixels updated = 96.82%            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   20_0021    9 -0.13 -0.05  0.04  0.22  0.17  0.13  70958  40    0  0.94   31 1.50 1.72 0.99 1.000
   21_0022    3  0.04  0.00  0.02  0.05  0.05  0.08  27369  28    0  0.97   33 1.50 1.71 0.99 1.000
   22_0023    6  0.02 -0.01  0.00  0.03  0.05  0.03 106342  52    0  0.97   34 1.49 1.71 0.99 1.000
   23_0024    7  0.06 -0.02 -0.06  0.13  0.14  0.13  67572  45    0  0.92   33 1.50 1.72 0.99 1.000
   24_0025    5  0.03 -0.00 -0.04  0.07  0.07  0.08 116103  56    0  0.96   30 1.49 1.72 1.00 1.000
   25_0026   14 -0.00  0.03 -0.02  0.12  0.18  0.12  67478  42    0  0.91   30 1.49 1.72 1.00 1.000
   26_0027    9  0.04 -0.03  0.00  0.15  0.10  0.08  43102  35   11  0.89   33 1.47 1.70 0.99 1.000
   27_0028    6  0.01 -0.03  0.01  0.05  0.05  0.03  95369  52    0  0.97   35 1.47 1.70 0.99 1.000
   28_0029   16  0.04  0.02  0.03  0.15  0.11  0.11  75423  43    0  0.94   31 1.48 1.69 0.99 1.000
   29_0030    6  0.04  0.02 -0.03  0.18  0.08  0.09 114818  46    0  0.89   33 1.48 1.70 1.00 1.000

I/Sigma = 162.82   Thresh = 0.020   Blend = F   #Contributing = 61   InitialProfileWt = 0.031
Region 1
Sum = 58598;   Maximum = 4625.68;   FM = 0.856
!Region 1: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  2  3  1  0  0  0    0  0  1  5  8  3  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  5  8  3  1  0  0    0  0  2 13 23  9  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  3  4  2  0  0  0    0  0  1  8 12  4  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  2  2  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  4  2  0  0  0    0  0  0  4  8  4  1  0  0    0  0  0  2  5  3  0  0  0  
  0  0  1 14 33 14  1  0  0    0  0  2 23 59 25  3  0  0    0  0  1 13 35 16  2  0  0  
  0  0  3 27 62 27  2  0  0    0  0  3 40100 45  4  0  0    0  0  2 22 59 27  2  0  0  
  0  0  2 18 34 11  1  0  0    0  0  2 28 57 19  1  0  0    0  0  1 15 34 12  1  0  0  
  0  0  1  3  4  1  0  0  0    0  0  1  5  8  2  0  0  0    0  0  0  3  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  2  1  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  3 11  6  1  0  0    0  0  0  1  4  2  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  7 21 10  1  0  0    0  0  0  2  8  4  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  3 11  6  1  0  0    0  0  0  1  4  2  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 0.00   Thresh = 0.020   Blend = F   #Contributing = 0   InitialProfileWt = 1.000
Region 2
Sum = 1.06658;   Maximum = 0.0858704;   FM = 0.817
!Region 2: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  3  1  0  0  0    0  0  0  5 17  6  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  2  7  4  0  0  0    0  0  1 10 37 19  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  3  2  0  0  0    0  0  0  5 17  7  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 2: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  1  0  0  0    0  0  0  2  5  1  0  0  0    0  0  0  2  4  1  0  0  0  
  0  0  0 12 34 11  1  0  0    0  0  1 19 54 15  1  0  0    0  0  1 16 47 12  0  0  0  
  0  0  1 22 69 32  2  0  0    0  0  2 35100 37  2  0  0    0  0  1 31 86 29  1  0  0  
  0  0  1 12 34 13  1  0  0    0  0  1 19 54 16  1  0  0    0  0  1 16 47 13  1  0  0  
  0  0  0  1  3  1  0  0  0    0  0  0  2  6  1  0  0  0    0  0  0  2  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 2: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  5 15  4  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 11 30  9  0  0  0    0  0  0  3  6  1  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  5 15  4  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 151.39   Thresh = 0.020   Blend = F   #Contributing = 4   InitialProfileWt = 0.586
Region 3
Sum = 48736.3;   Maximum = 3787.38;   FM = 0.824
!Region 3: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  6 19  6  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  2  3  1  0  0  0    0  0  1 14 34 14  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  8 15  5  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 3: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  3  0  0  0  0    0  0  0  2  4  1  0  0  0    0  0  0  2  3  1  0  0  0  
  0  0  1 14 42 12  0  0  0    0  0  1 20 53 13  0  0  0    0  0  1 18 46  9  0  0  0  
  0  0  2 31 77 32  2  0  0    0  0  2 39100 39  2  0  0    0  0  2 32 85 29  1  0  0  
  0  0  1 17 37 12  1  0  0    0  0  1 21 51 17  1  0  0    0  0  1 17 42 13  1  0  0  
  0  0  0  1  3  1  0  0  0    0  0  0  2  6  2  0  0  0    0  0  0  1  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 3: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  7 20  4  0  0  0    0  0  0  1  4  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 14 36 11  0  0  0    0  0  0  3  8  2  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  6 15  4  0  0  0    0  0  0  1  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  2  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 87.75   Thresh = 0.020   Blend = F   #Contributing = 12   InitialProfileWt = 0.230
Region 4
Sum = 20011.3;   Maximum = 1392.9;   FM = 0.853
!Region 4: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  2  4  1  0  0  0    0  0  1 10 17  4  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  1  3  5  1  0  0  0    0  0  1 15 27 10  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  2  1  0  0  0    0  0  1  8 13  5  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 4: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  3  4  1  0  0  0    0  0  1  4  5  1  0  0  0    0  0  0  2  3  1  0  0  0  
  0  0  2 23 42 12  1  0  0    0  0  2 26 53 15  1  0  0    0  0  1 16 40 12  1  0  0  
  0  0  3 38 78 33  2  0  0    0  0  4 43100 44  3  0  0    0  0  2 27 78 35  2  0  0  
  0  0  2 22 43 17  2  0  0    0  0  2 25 58 24  2  0  0    0  0  1 15 46 19  1  0  0  
  0  0  0  3  6  3  0  0  0    0  0  0  3 10  5  1  0  0    0  0  0  2  8  4  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 4: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  7 20  6  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 12 40 19  1  0  0    0  0  0  1  6  3  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  6 22  9  1  0  0    0  0  0  1  3  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  4  2  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 89.66   Thresh = 0.020   Blend = F   #Contributing = 33   InitialProfileWt = 0.046
Region 5
Sum = 24644.1;   Maximum = 1384.41;   FM = 0.893
!Region 5: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  2  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  4  4  1  0  0  0    0  0  3 17 19  6  1  0  0  
  0  0  0  1  0  0  0  0  0    0  0  1  5  6  2  1  0  0    0  0  4 25 29 12  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  1  3  3  1  1  0  0    0  0  3 13 15  6  1  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  2  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 5: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  1  2  1  0  0  0  
  0  0  1  5  5  2  0  0  0    0  0  1  6  8  3  0  0  0    0  0  1  4  7  3  1  0  0  
  0  0  4 30 42 16  2  0  0    0  0  4 33 61 27  3  0  0    0  0  2 21 50 26  4  0  0  
  0  0  6 44 68 32  4  1  0    0  0  5 45100 57  8  0  0    0  0  2 28 80 53  8  0  0  
  0  0  3 24 38 19  3  1  0    0  0  2 25 60 37  6  0  0    0  0  1 15 49 34  5  0  0  
  0  0  1  4  7  4  1  0  0    0  0  0  4 12  9  2  0  0    0  0  0  3 10  9  2  0  0  
  0  0  0  1  1  1  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 5: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  2  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  6 19 13  2  0  0    0  0  0  1  4  4  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  8 30 25  4  0  0    0  0  1  2  7  7  1  0  0    0  0  0  0  0  1  0  0  0  
  0  0  1  4 17 14  2  0  0    0  0  0  1  4  4  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  3  1  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 61.90   Thresh = 0.020   Blend = F   #Contributing = 33   InitialProfileWt = 0.069
Region 6
Sum = 13787.8;   Maximum = 681.4;   FM = 0.907
!Region 6: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  0  1  3  4  2  1  0  0  
  0  0  0  1  0  0  0  0  0    0  0  1  3  4  1  1  0  0    0  0  3 14 18  8  2  0  0  
  0  0  0  1  1  1  0  0  0    0  0  2  8  7  2  1  0  0    0  0  6 28 32 13  2  1  0  
  0  0  0  1  1  0  0  0  0    0  0  2  5  4  1  1  0  0    0  0  5 19 16  5  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  0  2  4  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 6: Section 4->6
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  2  1  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  1  1  1  1  0  0  
  0  0  1  6  9  5  1  0  0    0  0  1  6 13  9  2  0  0    0  0  0  4 12 10  3  0  0  
  0  0  6 32 48 25  4  0  0    0  0  5 33 67 40  7  0  0    0  0  2 17 54 41  7  0  0  
  0  0 10 56 77 36  5  1  0    0  1  8 54100 55  8  0  0    0  1  3 29 77 52  9  0  0  
  0  0  8 36 40 15  2  0  0    0  0  6 36 54 24  4  0  0    0  0  2 19 45 26  4  0  0  
  0  0  3  8  7  2  0  0  0    0  0  2  8 10  4  1  0  0    0  0  0  4  8  5  1  0  0  
  0  0  0  1  1  1  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  1  2  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0  
!Region 6: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  5  5  1  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  5 22 21  4  0  0    0  0  0  1  4  4  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  9 32 27  4  0  0    0  0  1  1  6  6  1  0  0    0  0  0  0  1  1  0  0  0  
  0  0  1  6 20 16  3  0  0    0  0  0  1  4  4  1  0  0    0  0  0  0  0  1  0  0  0  
  0  0  0  1  4  3  1  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  1  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  1  0  0  0    0  0  0  0  0  1  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 58.13   Thresh = 0.020   Blend = F   #Contributing = 32   InitialProfileWt = 0.079
Region 7
Sum = 14029.3;   Maximum = 839.009;   FM = 0.872
!Region 7: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  1  4  3  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  1  1  0    0  0  1  8 19  9  1  1  0  
  0  0  0  0  1  0  0  0  0    0  0  0  2  4  2  1  0  0    0  0  1 17 32 12  2  1  0  
  0  0  0  0  1  0  0  0  0    0  0  1  2  3  1  0  0  0    0  0  1 14 21  5  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  5  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 7: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  3 11  8  1  0  0    0  0  0  3 17 12  2  0  0    0  0  0  2 14 10  1  0  0  
  0  0  1 20 50 25  3  0  0    0  0  1 21 67 35  3  0  0    0  0  1 12 51 28  2  0  0  
  0  0  3 39 79 31  3  0  0    0  0  3 41100 41  3  0  0    0  0  2 25 77 34  3  0  0  
  0  0  3 32 47 12  1  0  0    0  0  3 35 57 15  1  0  0    0  0  2 23 44 12  1  0  0  
  0  0  1 10 10  2  0  0  0    0  0  1 11 11  2  0  0  0    0  0  1  7  8  2  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 7: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  5  3  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4 18 11  1  0  0    0  0  0  1  3  2  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  8 30 15  1  0  0    0  0  1  2  6  4  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  1  7 17  6  0  0  0    0  0  0  1  3  2  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  2  3  1  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 96.06   Thresh = 0.020   Blend = F   #Contributing = 22   InitialProfileWt = 0.090
Region 8
Sum = 30766.8;   Maximum = 2605.31;   FM = 0.816
!Region 8: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  1  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  5 16  5  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  3  2  0  0  0    0  0  0  8 27 12  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  2  1  0  0  0    0  0  0  3 15  7  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  1  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 8: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  6  2  0  0  0    0  0  0  3  8  2  0  0  0    0  0  0  2  4  1  0  0  0  
  0  0  1 17 44 13  1  0  0    0  0  1 23 53 15  1  0  0    0  0  1 15 33  8  0  0  0  
  0  0  1 24 78 29  2  0  0    0  0  1 34100 31  1  0  0    0  0  1 27 70 18  1  0  0  
  0  0  0 11 42 15  1  0  0    0  0  1 18 56 15  1  0  0    0  0  1 15 41  8  0  0  0  
  0  0  0  2  6  2  0  0  0    0  0  0  3  7  2  0  0  0    0  0  0  2  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 8: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  5 10  2  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 11 26  6  0  0  0    0  0  0  2  4  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  6 15  2  0  0  0    0  0  0  1  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 82.11   Thresh = 0.020   Blend = F   #Contributing = 4   InitialProfileWt = 0.670
Region 9
Sum = 19442.2;   Maximum = 1632.16;   FM = 0.781
!Region 9: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  4  2  0  0  0    0  0  0  4 17  7  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  9  6  0  0  0    0  0  0  6 45 28  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  5  2  0  0  0    0  0  0  3 21 11  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 9: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  1  4  1  0  0  0    0  0  0  1  4  1  0  0  0  
  0  0  0  8 27 10  1  0  0    0  0  0 16 52 15  0  0  0    0  0  0 15 51 14  0  0  0  
  0  0  0 12 63 33  2  0  0    0  0  1 31100 34  1  0  0    0  0  1 32 96 29  1  0  0  
  0  0  0  5 31 13  0  0  0    0  0  0 15 55 14  0  0  0    0  0  1 16 55 12  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  1  5  1  0  0  0    0  0  0  2  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 9: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  4 12  3  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0 10 26  7  0  0  0    0  0  0  2  3  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  5 16  3  0  0  0    0  0  0  1  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (201 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       201         0       201    2.4559    0.9411    36.590   109.999

Orientation ('UB') matrix:
  -0.0355991   0.0176189   0.0619111
  -0.0281843  -0.0063089  -0.1680303
  -0.0230001  -0.0195393   0.1100800

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6470   36.9607    4.7573    90.000    90.000    90.000       3454.61
    0.0020    0.0038    0.0005     0.000     0.000     0.000          0.76
Corrected for goodness of fit:
    0.0020    0.0038    0.0005     0.000     0.000     0.000          0.77

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.774      58.420     -32.035
Goniometer zeros (deg):          0.0000*     0.0686      0.0000*     0.1295    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                      -0.3818  -0.2481  -0.0005  -0.3679  -0.1682  -0.2280

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        8.20959e+002  6.01724e+002    1.01       2         5       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 201             201             201
 Average input ESD (pix, pix, deg):          0.20430         0.18722         0.04014
 Goodness of fit:                            1.14381         1.18336         0.53385


Old XYZ spot size:              1.373   1.300   0.950
New XYZ spot size:              1.365   1.293   1.014
Average missing volume:         0.089
% with too much missing I:      6.477
Fractional overlap in H,K,L:    0.002   0.007   0.000

End of pass 3.  Repeating shape determination...

Repeat orientation and spot-shape refinement ============= 01/23/2020 16:55:03

Current XYZ spot size:            1.365   1.293   1.014
Accurate-timing indicator is set in the frame headers:
   Velocity normalization will be computed for each frame
Pixel spacing (deg):              0.111
Profile X,Y,Z spacing (deg):      0.228   0.216   0.179
Profile convolver halfwidth:       1.00    1.00    1.67
Background pixels updated = 97.00%            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
    0_0001    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   21 0.00 0.00 1.19 1.000
    1_0002    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   21 0.00 0.00 1.19 1.000
    2_0003    1 -0.12 -0.05  0.10  0.12  0.05  0.10 6560.2  10    0  0.81   28 0.69 0.60 1.19 1.000
    3_0004    5 -0.02  0.00 -0.03  0.12  0.13  0.06 103444  44    0  0.91   30 1.40 1.21 1.19 1.000
    4_0005   12  0.10 -0.10 -0.04  0.21  0.26  0.08 138845  46    0  0.89   33 1.16 1.04 1.14 1.000
    5_0006   11  0.07  0.01 -0.04  0.17  0.11  0.09 141486  55    0  0.93   32 1.19 1.12 1.09 1.000
    6_0007   13  0.10 -0.10 -0.06  0.36  0.47  0.16  50079  32    8  0.91   34 1.17 1.10 1.10 1.000
    7_0008    3 -0.04 -0.10  0.10  0.26  0.25  0.18 134067  56   33  0.81   36 1.21 1.13 1.08 1.000
    8_0009    7 -0.04 -0.01  0.05  0.16  0.06  0.15  42547  25    0  0.94   35 1.19 1.10 1.08 1.000
    9_0010    6  0.07 -0.08 -0.08  0.13  0.14  0.14  71344  39    0  0.94   36 1.18 1.13 1.08 1.000
   10_0011   15  0.01  0.03 -0.02  0.10  0.12  0.07  84888  44    0  0.92   32 1.22 1.17 1.07 1.000
   11_0012   12 -0.04  0.07  0.05  0.09  0.26  0.08 105884  50    0  0.94   34 1.22 1.17 1.05 1.000
   12_0013    8 -0.02 -0.01 -0.00  0.07  0.06  0.05  60720  42   13  0.88   32 1.20 1.16 1.04 1.000
   13_0014    7  0.00 -0.04  0.01  0.06  0.06  0.05  41491  37    0  0.96   33 1.18 1.14 1.04 1.000
   14_0015    8  0.04 -0.02 -0.01  0.06  0.14  0.07  44575  33    0  0.94   33 1.19 1.15 1.04 1.000
   15_0016   11  0.00 -0.02  0.02  0.11  0.09  0.06  85991  42    0  0.95   31 1.21 1.14 1.03 1.000
   16_0017    7 -0.03  0.01  0.01  0.08  0.08  0.04 117101  47    0  0.97   33 1.20 1.14 1.03 1.000
   17_0018    5 -0.01  0.03  0.01  0.02  0.06  0.02  80718  52    0  0.93   30 1.21 1.13 1.03 1.000
   18_0019   10 -0.00  0.00 -0.01  0.06  0.06  0.05 138193  60    0  0.96   33 1.20 1.13 1.03 1.000
   19_0020    8  0.11  0.04 -0.02  0.29  0.28  0.12 118423  53    0  0.96   35 1.20 1.14 1.02 1.000
Background pixels updated = 96.90%            Port, connections: 2000, 1
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   20_0021    8 -0.13 -0.03  0.04  0.21  0.14  0.13  67070  37    0  0.93   30 1.20 1.14 1.03 1.000
   21_0022    4  0.00  0.01  0.04  0.06  0.06  0.06  45582  36    0  0.97   36 1.19 1.14 1.03 1.000
   22_0023    5  0.02  0.02  0.01  0.07  0.06  0.06  47983  39    0  0.97   35 1.19 1.13 1.03 1.000
   23_0024    8  0.01  0.03  0.01  0.05  0.10  0.09 108856  54    0  0.93   34 1.19 1.14 1.02 1.000
   24_0025    6  0.03  0.03 -0.03  0.06  0.06  0.06 105374  53    0  0.96   32 1.19 1.14 1.03 1.000
   25_0026   13  0.02  0.06 -0.03  0.11  0.20  0.13  68654  42    0  0.91   30 1.19 1.14 1.03 1.000
   26_0027    9  0.05 -0.03  0.01  0.16  0.10  0.07  43111  35   11  0.89   34 1.18 1.13 1.02 1.000
   27_0028    7  0.01 -0.00  0.01  0.05  0.03  0.02 100816  54    0  0.97   36 1.18 1.13 1.02 1.000
   28_0029   16  0.06  0.06  0.02  0.17  0.14  0.11  75435  43    0  0.94   33 1.19 1.12 1.02 1.000
   29_0030    6  0.06  0.05 -0.03  0.18  0.08  0.09 113974  46    0  0.89   33 1.19 1.12 1.02 1.000

I/Sigma = 162.30   Thresh = 0.020   Blend = F   #Contributing = 59   InitialProfileWt = 0.035
Region 1
Sum = 58570.3;   Maximum = 4752.94;   FM = 0.855
!Region 1: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  1  4  7  3  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  4  7  3  1  0  0    0  0  2 12 21  8  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  3  4  1  0  0  0    0  0  1  8 11  4  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  2  2  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  4  2  0  0  0    0  0  0  3  8  4  1  0  0    0  0  0  2  5  2  0  0  0  
  0  0  1 14 31 13  1  0  0    0  0  2 23 58 25  3  0  0    0  0  1 12 34 15  2  0  0  
  0  0  3 26 60 26  2  0  0    0  0  3 40100 45  4  0  0    0  0  2 21 57 26  2  0  0  
  0  0  2 18 33 11  1  0  0    0  0  3 29 58 19  2  0  0    0  0  1 15 34 12  1  0  0  
  0  0  1  4  5  1  0  0  0    0  0  1  6  8  2  0  0  0    0  0  0  3  5  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  3 10  6  1  0  0    0  0  0  1  3  2  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  6 20 10  1  0  0    0  0  0  2  6  3  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  3 11  6  1  0  0    0  0  0  1  4  2  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 0.00   Thresh = 0.020   Blend = F   #Contributing = 0   InitialProfileWt = 1.000
Region 2
Sum = 1.07421;   Maximum = 0.0891043;   FM = 0.818
!Region 2: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  5 16  5  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  4  2  0  0  0    0  0  1 10 34 17  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  5 16  7  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 2: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  1  0  0  0    0  0  0  2  5  1  0  0  0    0  0  0  2  4  1  0  0  0  
  0  0  1 12 34 11  1  0  0    0  0  1 20 54 15  1  0  0    0  0  1 17 47 12  0  0  0  
  0  0  1 22 67 31  2  0  0    0  0  2 37100 37  2  0  0    0  0  1 32 85 28  1  0  0  
  0  0  1 11 33 12  1  0  0    0  0  1 20 54 16  1  0  0    0  0  1 17 46 12  0  0  0  
  0  0  0  1  3  1  0  0  0    0  0  0  2  6  1  0  0  0    0  0  0  2  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 2: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  5 14  3  0  0  0    0  0  0  1  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 10 26  8  0  0  0    0  0  0  2  5  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  5 13  3  0  0  0    0  0  0  1  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 151.01   Thresh = 0.020   Blend = F   #Contributing = 4   InitialProfileWt = 0.586
Region 3
Sum = 48834.1;   Maximum = 3922.73;   FM = 0.825
!Region 3: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  6 18  5  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  2  3  1  0  0  0    0  0  1 13 30 12  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  7 13  4  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 3: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  3  0  0  0  0    0  0  0  3  4  1  0  0  0    0  0  0  2  3  1  0  0  0  
  0  0  1 15 43 12  0  0  0    0  0  1 22 56 13  0  0  0    0  0  1 19 47  9  0  0  0  
  0  0  2 32 76 31  2  0  0    0  0  2 40100 38  2  0  0    0  0  2 32 82 28  1  0  0  
  0  0  1 17 35 11  1  0  0    0  0  1 21 50 16  1  0  0    0  0  1 16 39 12  1  0  0  
  0  0  0  1  3  1  0  0  0    0  0  0  2  5  2  0  0  0    0  0  0  1  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 3: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  6 17  3  0  0  0    0  0  0  1  3  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 12 30  9  0  0  0    0  0  0  2  6  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  5 11  3  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 87.06   Thresh = 0.020   Blend = F   #Contributing = 12   InitialProfileWt = 0.263
Region 4
Sum = 19500.2;   Maximum = 1395.79;   FM = 0.854
!Region 4: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  2  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  2  4  1  0  0  0    0  0  1 10 16  4  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  3  4  1  0  0  0    0  0  2 15 24  8  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  2  1  0  0  0    0  0  1  8 11  4  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 4: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  4  4  1  0  0  0    0  0  1  4  5  1  0  0  0    0  0  0  2  3  1  0  0  0  
  0  0  2 25 44 12  1  0  0    0  0  3 28 55 15  1  0  0    0  0  1 16 40 12  1  0  0  
  0  0  4 40 78 32  2  0  0    0  0  4 45100 42  3  0  0    0  0  2 27 75 33  2  0  0  
  0  0  2 23 42 16  2  0  0    0  0  2 26 57 23  2  0  0    0  0  1 15 43 17  1  0  0  
  0  0  0  3  6  3  0  0  0    0  0  0  3  9  4  1  0  0    0  0  0  2  8  3  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 4: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  6 18  6  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 11 35 16  1  0  0    0  0  0  1  4  2  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  6 19  8  1  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 88.81   Thresh = 0.020   Blend = F   #Contributing = 33   InitialProfileWt = 0.041
Region 5
Sum = 24343.3;   Maximum = 1410.43;   FM = 0.895
!Region 5: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  1  3  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  3  3  1  0  0  0    0  0  3 17 18  6  1  0  0  
  0  0  0  1  0  0  0  0  0    0  0  1  4  4  2  1  0  0    0  0  5 24 28 11  2  1  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  2  1  1  0  0    0  0  3 13 15  6  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  2  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 5: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  1  2  1  0  0  0  
  0  0  1  5  5  1  0  0  0    0  0  1  7  8  3  0  0  0    0  0  1  4  7  3  1  0  0  
  0  0  5 32 42 15  2  0  0    0  0  4 35 61 26  3  0  0    0  0  2 22 49 24  3  0  0  
  0  0  7 46 68 31  4  1  0    0  0  5 47100 55  7  0  0    0  0  3 28 78 50  7  0  0  
  0  0  4 25 38 18  3  1  0    0  0  3 26 61 36  5  0  0    0  0  1 15 48 32  4  0  0  
  0  0  1  4  7  4  1  0  0    0  0  1  4 13  9  2  0  0    0  0  0  3 10  8  1  0  0  
  0  0  0  1  1  1  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 5: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  2  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  5 16 11  2  0  0    0  0  0  1  3  3  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  6 25 20  3  0  0    0  0  1  1  6  5  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  3 14 11  1  0  0    0  0  0  1  3  3  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  3  1  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 61.96   Thresh = 0.020   Blend = F   #Contributing = 32   InitialProfileWt = 0.079
Region 6
Sum = 13815.2;   Maximum = 700.297;   FM = 0.91
!Region 6: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  3  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  3  3  1  1  0  0    0  0  3 12 15  7  1  0  0  
  0  0  0  1  1  1  0  0  0    0  0  2  7  6  2  1  0  0    0  0  6 27 29 11  2  1  0  
  0  0  0  1  1  0  0  0  0    0  0  2  5  3  1  1  0  0    0  0  5 19 16  5  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  0  2  5  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 6: Section 4->6
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  2  2  1  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  1  1  1  1  0  0  
  0  0  1  5  8  4  1  0  0    0  0  1  6 12  8  2  0  0    0  0  0  3 11  9  2  0  0  
  0  0  6 31 45 23  3  0  0    0  0  5 33 64 38  6  0  0    0  0  2 16 51 38  7  0  0  
  0  1 10 56 76 36  5  1  0    0  1  8 55100 55  8  0  0    0  1  3 28 75 52  8  0  0  
  0  0  9 39 42 16  2  0  0    0  0  6 38 57 26  4  0  0    0  0  2 20 47 28  5  0  0  
  0  0  3  9  8  3  0  0  0    0  0  2 10 11  5  1  0  0    0  0  1  5  9  5  1  0  0  
  0  0  1  1  1  1  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  1  2  1  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  1  0  0  0  
!Region 6: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  4  4  1  0  0    0  0  0  0  0  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4 19 18  3  0  0    0  0  0  1  3  3  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  8 28 25  4  0  0    0  0  1  1  5  5  1  0  0    0  0  0  0  0  1  0  0  0  
  0  0  1  5 19 15  3  0  0    0  0  0  1  3  3  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  4  3  1  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  1  1  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 62.49   Thresh = 0.020   Blend = F   #Contributing = 34   InitialProfileWt = 0.079
Region 7
Sum = 15706.9;   Maximum = 942.881;   FM = 0.875
!Region 7: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  1  3  2  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  1  1  0    0  0  1  6 15  8  1  1  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  3  1  1  1  0    0  0  1 14 27 12  2  1  0  
  0  0  0  0  1  0  0  0  0    0  0  0  1  3  1  0  0  0    0  0  1 13 19  5  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  1  5  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 7: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  2  9  6  1  0  0    0  0  0  3 15 11  2  0  0    0  0  0  2 14 10  1  0  0  
  0  0  1 17 44 23  2  0  0    0  0  1 19 64 35  3  0  0    0  0  1 12 52 30  3  0  0  
  0  0  3 38 74 31  3  0  0    0  0  3 40100 43  4  0  0    0  0  2 26 82 38  3  0  0  
  0  0  3 32 48 13  1  0  0    0  0  3 36 63 18  1  0  0    0  0  2 25 52 15  1  0  0  
  0  0  1 11 12  2  0  0  0    0  0  1 12 13  2  0  0  0    0  0  1  8 10  2  0  0  0  
  0  0  1  2  1  0  0  0  0    0  0  0  2  1  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 7: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  4  3  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4 17 11  1  0  0    0  0  0  1  3  2  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  8 29 16  1  0  0    0  0  0  1  5  4  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  7 18  6  0  0  0    0  0  0  1  3  2  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  2  4  1  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 93.16   Thresh = 0.020   Blend = F   #Contributing = 22   InitialProfileWt = 0.118
Region 8
Sum = 29290.8;   Maximum = 2626.58;   FM = 0.816
!Region 8: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  1  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  4 12  4  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  6 20  9  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  3 11  6  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  1  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 8: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  6  2  0  0  0    0  0  0  3  8  3  0  0  0    0  0  0  2  5  1  0  0  0  
  0  0  0 16 40 12  1  0  0    0  0  1 24 54 15  1  0  0    0  0  1 16 33  8  0  0  0  
  0  0  1 21 69 26  1  0  0    0  0  1 35100 31  1  0  0    0  0  1 27 69 18  1  0  0  
  0  0  0 10 37 13  1  0  0    0  0  1 17 54 15  1  0  0    0  0  1 15 40  8  0  0  0  
  0  0  0  2  5  2  0  0  0    0  0  0  3  7  2  0  0  0    0  0  0  2  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 8: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  5  9  2  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 11 25  5  0  0  0    0  0  0  2  3  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  6 14  2  0  0  0    0  0  0  1  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 82.16   Thresh = 0.020   Blend = F   #Contributing = 4   InitialProfileWt = 0.670
Region 9
Sum = 19478.8;   Maximum = 1679.49;   FM = 0.782
!Region 9: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  4 16  6  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  4  2  0  0  0    0  0  0  6 42 25  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  2  1  0  0  0    0  0  0  3 20 10  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 9: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  1  4  1  0  0  0    0  0  0  1  4  1  0  0  0  
  0  0  0  8 25  9  1  0  0    0  0  0 17 52 14  0  0  0    0  0  0 17 51 13  0  0  0  
  0  0  0 11 61 32  1  0  0    0  0  1 33100 33  1  0  0    0  0  1 35 97 29  1  0  0  
  0  0  0  5 30 13  0  0  0    0  0  1 16 56 14  0  0  0    0  0  1 18 56 12  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  2  5  1  0  0  0    0  0  0  2  5  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 9: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  4 11  3  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0 10 24  6  0  0  0    0  0  0  2  3  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  5 14  3  0  0  0    0  0  0  1  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (200 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       200         0       200    2.4559    0.9411    36.590   110.008

Orientation ('UB') matrix:
  -0.0355999   0.0176211   0.0619110
  -0.0281820  -0.0063099  -0.1680549
  -0.0230008  -0.0195422   0.1100872

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6471   36.9555    4.7568    90.000    90.000    90.000       3453.77
    0.0020    0.0038    0.0005     0.000     0.000     0.000          0.77
Corrected for goodness of fit:
    0.0020    0.0038    0.0005     0.000     0.000     0.000          0.76

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.776      58.422     -32.035
Goniometer zeros (deg):          0.0000*     0.0685      0.0000*     0.1280    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                      -0.3758  -0.2359  -0.0013  -0.3638  -0.1710  -0.2216

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        6.20461e+002  5.83262e+002    1.00       2         5       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 200             200             200
 Average input ESD (pix, pix, deg):          0.20125         0.18420         0.04022
 Goodness of fit:                            1.11461         1.18165         0.52694


Old XYZ spot size:              1.365   1.293   1.014
New XYZ spot size:              1.357   1.285   1.022
Average missing volume:         0.085
% with too much missing I:      5.714
Fractional overlap in H,K,L:    0.001   0.005   0.000

Integration ============================= 01/23/2020 16:55:04

Unsorted reflections will be written to d:\Frames\guest\BruecknerJK_153F40\work\unsorted.raw
Spatially corrected beam center:          386.24  506.40
Input monochromator 2Th, roll (deg):        0.00    0.00
Input spot-size bias:              1.000
Unbiased XYZ spot size (deg):      1.357   1.285   1.022
Spot size used (deg):              1.357   1.285   1.022
Scale for orientation update length:     1.00000
#Frames running average for orientation update:       16
Frames between full refinements of orientation:       50
N, where every Nth strong spot included in LS:         1

LS profile fitting will be used
   to worst resolution of 9999.000 A
   up to I/sigma(I) of       8.000
   unweighted fit

Accurate-timing indicator is set in the frame headers:
   Velocity normalization will be computed for each frame
Pixel spacing (deg):              0.111
Profile X,Y,Z spacing (deg):      0.226   0.214   0.180
Profile convolver halfwidth:       1.00    1.00    1.66
Background pixels updated = 97.08%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
    0_0001    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   21 0.00 0.00 1.02 1.000
    1_0002    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   21 0.00 0.00 1.02 1.000
    2_0003    1 -0.11 -0.05  0.10  0.11  0.05  0.10 4180.7  13    0  0.95   28 0.69 0.60 1.02 1.000
    3_0004    7 -0.17 -0.03 -0.03  0.41  0.13  0.06  65932  42    0  0.93   30 1.09 0.95 1.02 1.000
    4_0005   15  0.08 -0.08 -0.04  0.20  0.23  0.07  81382  46    0  0.94   33 1.08 0.95 1.02 1.000
    5_0006   11  0.08  0.01 -0.04  0.18  0.12  0.09 130644  56    0  0.94   32 1.12 1.03 1.02 1.000
    6_0007   14  0.11 -0.13 -0.07  0.34  0.47  0.16  35775  30    7  0.90   34 1.13 1.04 1.03 1.000
    7_0008    3 -0.03 -0.11  0.10  0.27  0.25  0.18  99397  56   33  0.82   36 1.16 1.07 1.03 1.000
    8_0009    8 -0.02  0.02  0.01  0.14  0.10  0.17  33791  23    0  0.95   35 1.15 1.05 1.03 1.000
    9_0010    6  0.08 -0.08 -0.08  0.13  0.15  0.14  62372  39    0  0.95   36 1.15 1.08 1.03 1.000
   10_0011   18 -0.06 -0.02  0.02  0.17  0.17  0.09  67371  41    0  0.93   32 1.21 1.13 1.02 1.000
   11_0012   19  0.21  0.05 -0.03  0.64  0.31  0.15  75600  39    5  0.92   34 1.22 1.13 1.02 1.000
   12_0013    8 -0.01 -0.01 -0.00  0.07  0.06  0.05  69375  42   13  0.89   32 1.21 1.12 1.02 1.000
   13_0014    9 -0.03  0.06  0.02  0.13  0.25  0.07  34963  33    0  0.96   33 1.20 1.12 1.02 1.000
   14_0015   10  0.00 -0.02  0.01  0.06  0.11  0.10  43470  31   10  0.89   33 1.20 1.13 1.02 1.000
   15_0016   12  0.01 -0.02  0.02  0.11  0.09  0.05  94379  40    0  0.95   31 1.21 1.12 1.01 1.000
   16_0017   10  0.08 -0.10 -0.04  0.28  0.35  0.12  98638  44    0  0.96   33 1.22 1.12 1.02 1.000
   17_0018    9  0.01 -0.03 -0.03  0.06  0.11  0.07 108825  60    0  0.95   30 1.22 1.12 1.02 1.000
   18_0019   12  0.02  0.00 -0.01  0.08  0.05  0.04 125157  62    0  0.96   33 1.22 1.12 1.02 1.000
   19_0020   12  0.13  0.02 -0.03  0.27  0.29  0.11 102955  51    0  0.97   35 1.23 1.14 1.02 1.000
Background pixels updated = 96.94%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   20_0021   10 -0.11 -0.01  0.06  0.19  0.13  0.11  65515  41    0  0.94   32 1.23 1.14 1.02 1.000
   21_0022    5  0.01  0.02  0.04  0.06  0.06  0.06  54895  43    0  0.97   36 1.23 1.14 1.02 1.000
   22_0023   13  0.05 -0.18  0.01  0.25  0.49  0.13  55590  37    0  0.94   35 1.24 1.14 1.02 1.000
   23_0024    9 -0.01  0.05  0.02  0.09  0.11  0.09  97989  49    0  0.92   34 1.24 1.15 1.02 1.000
   24_0025    8  0.07  0.01 -0.07  0.12  0.10  0.15 101719  48   13  0.90   32 1.24 1.15 1.02 1.000
   25_0026   15  0.09  0.01 -0.04  0.35  0.24  0.14  57055  39    0  0.92   30 1.23 1.14 1.02 1.000
   26_0027   10  0.04 -0.01 -0.00  0.15  0.09  0.07  41323  36   10  0.90   34 1.22 1.13 1.02 1.000
   27_0028    7 -0.00  0.02  0.00  0.05  0.05  0.01  84620  54    0  0.97   36 1.22 1.14 1.02 1.000
   28_0029   18  0.02  0.05  0.02  0.17  0.14  0.11  62514  43    0  0.94   33 1.22 1.13 1.01 1.000
   29_0030    8 -0.07  0.05  0.00  0.35  0.09  0.11 190113  67    0  0.88   33 1.23 1.14 1.02 1.000
   30_0031    9 -0.04  0.12  0.02  0.29  0.18  0.10  37310  28   11  0.91   35 1.22 1.13 1.01 1.000
   31_0032    6  0.05  0.02 -0.05  0.18  0.07  0.14  18712  20   17  0.89   34 1.22 1.12 1.01 1.000
   32_0033    8  0.08  0.10 -0.03  0.12  0.15  0.08  59465  41    0  0.94   31 1.22 1.13 1.01 1.000
   33_0034   10  0.08  0.04 -0.03  0.11  0.09  0.11  35673  29    0  0.94   32 1.21 1.12 1.01 1.000
   34_0035   12  0.02  0.07  0.01  0.21  0.10  0.07  82739  52    0  0.97   34 1.21 1.13 1.01 1.000
   35_0036    6 -0.04  0.05  0.02  0.14  0.10  0.06  80094  50    0  0.97   31 1.20 1.12 1.01 1.000
   36_0037   11  0.23  0.02 -0.00  0.76  0.11  0.10  61944  37    9  0.86   31 1.20 1.12 1.01 1.000
   37_0038   14  0.03  0.02 -0.02  0.10  0.08  0.08  49876  35    0  0.93   31 1.19 1.11 1.01 1.000
   38_0039   11  0.07  0.15 -0.02  0.33  0.31  0.12  93365  50    0  0.94   32 1.20 1.12 1.01 1.000
   39_0040   10  0.02  0.10 -0.00  0.26  0.14  0.10  77977  50   10  0.92   31 1.20 1.12 1.01 1.000
Background pixels updated = 97.42%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   40_0041    9 -0.01  0.05  0.02  0.07  0.11  0.05  79449  49   11  0.90   32 1.19 1.12 1.01 1.000
   41_0042   13 -0.01  0.06  0.02  0.10  0.08  0.05  41799  37    0  0.95   32 1.19 1.11 1.01 1.000
   42_0043   10  0.02  0.06  0.02  0.08  0.11  0.05  46359  33    0  0.93   35 1.18 1.11 1.01 1.000
   43_0044    6 -0.04  0.02  0.01  0.18  0.13  0.04  83549  51    0  0.97   36 1.18 1.11 1.01 1.000
   44_0045   14  0.01  0.04 -0.01  0.09  0.10  0.07  54357  39    0  0.95   33 1.18 1.10 1.01 1.000
   45_0046    9  0.10  0.06 -0.02  0.20  0.13  0.07  32434  34   11  0.90   31 1.17 1.10 1.01 1.000
   46_0047    8  0.04  0.07 -0.02  0.07  0.09  0.05  66676  44    0  0.95   31 1.18 1.10 1.01 1.000
   47_0048    8  0.06  0.11 -0.01  0.10  0.14  0.06 189780  83    0  0.97   34 1.18 1.10 1.01 1.000
   48_0049    9  0.19  0.10 -0.10  0.27  0.21  0.14  52137  33    0  0.94   33 1.18 1.10 1.01 1.000
   49_0050   11 -0.09  0.02  0.02  0.27  0.26  0.15  43786  31    0  0.91   32 1.18 1.10 1.01 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (415 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       415         0       415    2.4558    0.9334    36.591   111.370

Orientation ('UB') matrix:
  -0.0355968   0.0176191   0.0619499
  -0.0281880  -0.0063041  -0.1680481
  -0.0230014  -0.0195416   0.1100679

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6466   36.9598    4.7569    90.000    90.000    90.000       3454.14
    0.0011    0.0023    0.0003     0.000     0.000     0.000          0.50
Corrected for goodness of fit:
    0.0016    0.0035    0.0005     0.000     0.000     0.000          0.74

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.764      58.427     -32.033
Goniometer zeros (deg):          0.0000*     0.0696      0.0000*     0.1292    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                      -0.3542  -0.1822  -0.0027  -0.3712  -0.1675  -0.2101

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        2.72951e+003  2.70603e+003    1.48       2         5       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 415             415             414
 Average input ESD (pix, pix, deg):          0.20297         0.18631         0.03983
 Goodness of fit:                            1.94045         1.53890         0.62285

Background pixels updated = 97.36%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   50_0051   11  0.18  0.11 -0.02  0.56  0.14  0.08  59727  44    0  0.95   33 1.18 1.10 1.01 1.000
   51_0052   11 -0.06  0.04  0.07  0.17  0.10  0.15  34909  30    9  0.92   33 1.18 1.10 1.01 1.000
   52_0053    8  0.03  0.01 -0.02  0.17  0.16  0.06  67556  38    0  0.84   31 1.18 1.10 1.01 1.000
   53_0054    8  0.06  0.06 -0.04  0.11  0.12  0.09  36994  35    0  0.96   31 1.18 1.10 1.01 1.000
   54_0055   10  0.04  0.02  0.03  0.32  0.18  0.13  63384  44    0  0.95   34 1.18 1.09 1.01 1.000
   55_0056    9 -0.08  0.12  0.05  0.19  0.15  0.10  37497  26   22  0.80   30 1.18 1.09 1.01 1.000
   56_0057   15 -0.02  0.07 -0.01  0.19  0.13  0.10 198059  62    0  0.95   33 1.18 1.10 1.01 1.000
   57_0058   10 -0.08  0.08  0.04  0.27  0.11  0.15  47166  32    0  0.91   31 1.18 1.09 1.01 1.000
   58_0059    7  0.01  0.09  0.02  0.07  0.10  0.05  80841  52    0  0.97   34 1.18 1.09 1.01 1.000
   59_0060    6  0.03  0.18 -0.00  0.21  0.25  0.06  71522  50    0  0.95   33 1.18 1.09 1.01 1.000
Background pixels updated = 97.48%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   60_0061    9  0.00  0.04  0.00  0.15  0.12  0.04  31520  27    0  0.92   31 1.18 1.09 1.01 1.000
   61_0062   12  0.04  0.10 -0.02  0.10  0.15  0.06  62328  39    8  0.92   32 1.18 1.09 1.01 1.000
   62_0063   12  0.09  0.10 -0.00  0.21  0.24  0.10  61102  43    8  0.92   34 1.18 1.09 1.01 1.000
   63_0064    9  0.04  0.07 -0.05  0.11  0.13  0.10  42519  36    0  0.94   32 1.18 1.09 1.01 1.000
   64_0065   14 -0.01 -0.00  0.03  0.21  0.21  0.14  21801  24    0  0.91   32 1.18 1.09 1.01 1.000
   65_0066    6  0.04  0.05  0.00  0.11  0.08  0.06 133458  69    0  0.96   32 1.17 1.09 1.01 1.000
   66_0067    7 -0.08  0.09  0.03  0.27  0.13  0.14  26246  30   14  0.89   32 1.18 1.09 1.01 1.000
   67_0068   13  0.00  0.03  0.02  0.26  0.15  0.12  35651  31    0  0.91   31 1.17 1.09 1.01 1.000
   68_0069   11  0.26  0.07 -0.08  0.67  0.17  0.17  25147  26    0  0.95   33 1.17 1.09 1.01 1.000
   69_0070    9  0.07  0.14 -0.03  0.22  0.20  0.13  22943  26    0  0.95   35 1.17 1.09 1.01 1.000
   70_0071    9  0.08  0.16 -0.03  0.28  0.24  0.13  66430  43    0  0.94   30 1.17 1.09 1.01 1.000
   71_0072    9 -0.02  0.15  0.02  0.19  0.15  0.14  54659  37    0  0.93   31 1.17 1.09 1.01 1.000
   72_0073    6  0.04  0.11 -0.01  0.09  0.13  0.05  61611  46    0  0.97   33 1.17 1.09 1.01 1.000
   73_0074   11  0.03  0.03 -0.02  0.28  0.13  0.12  14018  17    9  0.88   31 1.17 1.09 1.01 1.000
   74_0075   10 -0.08  0.05  0.05  0.54  0.18  0.15  43776  36    0  0.93   32 1.17 1.09 1.01 1.000
   75_0076   13  0.09  0.16 -0.02  0.26  0.24  0.11 101067  61    0  0.96   33 1.18 1.09 1.01 1.000
   76_0077    8  0.02  0.05 -0.06  0.27  0.17  0.19  26745  25    0  0.91   32 1.17 1.09 1.01 1.000
   77_0078    7  0.07  0.07 -0.06  0.20  0.20  0.13  24275  28    0  0.91   33 1.17 1.08 1.01 1.000
   78_0079   12  0.19 -0.04 -0.05  0.54  0.36  0.15  73323  41    0  0.90   31 1.18 1.08 1.01 1.000
   79_0080   10 -0.06  0.01  0.08  0.18  0.20  0.23  63226  33    0  0.86   30 1.17 1.09 1.01 1.000
Background pixels updated = 97.59%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
   80_0081    5  0.07  0.13  0.00  0.08  0.14  0.02  43282  38    0  0.97   35 1.17 1.09 1.01 1.000
   81_0082    9  0.05  0.11 -0.04  0.16  0.18  0.10  19446  21   11  0.91   32 1.17 1.08 1.01 1.000
   82_0083   12  0.03  0.12  0.01  0.16  0.14  0.07 102712  54    0  0.93   30 1.17 1.09 1.01 1.000
   83_0084    8  0.03  0.17 -0.01  0.07  0.20  0.05  43224  39    0  0.96   33 1.17 1.08 1.01 1.000
   84_0085    9  0.24  0.06 -0.04  0.39  0.16  0.09  45174  33    0  0.91   31 1.17 1.08 1.01 1.000
   85_0086    7 -0.06  0.13 -0.00  0.19  0.22  0.11  24327  28    0  0.95   31 1.17 1.08 1.01 1.000
   86_0087   11  0.04  0.12 -0.04  0.11  0.13  0.08  40226  36    0  0.94   31 1.17 1.08 1.01 1.000
   87_0088   11 -0.03  0.12 -0.03  0.17  0.16  0.21  53396  38    0  0.91   32 1.17 1.08 1.01 1.000
   88_0089   12 -0.07  0.10  0.04  0.27  0.16  0.12  52307  35    0  0.94   32 1.17 1.08 1.01 1.000
   89_0090    3 -0.50  0.21  0.22  0.61  0.55  0.23 3572.1   8    0  0.72   31 1.17 1.08 1.01 1.000
   90_0091    9 -0.01  0.09 -0.01  0.12  0.11  0.08  77521  43    0  0.93   31 1.17 1.08 1.01 1.000
   91_0092   11  0.03  0.20 -0.05  0.23  0.27  0.12  61379  39    9  0.89   33 1.18 1.08 1.01 1.000
   92_0093    7  0.13  0.10 -0.10  0.23  0.19  0.18  25205  24    0  0.89   33 1.18 1.08 1.01 1.000
   93_0094   12  0.08  0.19 -0.01  0.52  0.34  0.13  47189  37    0  0.94   32 1.18 1.08 1.01 1.000
   94_0095    8  0.02  0.19  0.01  0.13  0.26  0.07  68734  48    0  0.97   34 1.18 1.08 1.01 1.000
   95_0096   13 -0.18  0.08  0.04  0.43  0.20  0.13  91972  47    0  0.90   32 1.18 1.08 1.01 1.000
   96_0097    9 -0.03  0.13  0.04  0.11  0.16  0.09 143157  54    0  0.95   33 1.18 1.09 1.01 1.000
   97_0098    8  0.01  0.13 -0.02  0.08  0.15  0.05  31273  30    0  0.95   31 1.19 1.09 1.01 1.000
   98_0099   10  0.04  0.10 -0.00  0.15  0.13  0.06  63425  47    0  0.95   31 1.19 1.09 1.01 1.000
   99_0100    9  0.04  0.14  0.01  0.08  0.16  0.05  53196  43    0  0.95   33 1.18 1.09 1.00 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.5537    0.9281    35.142   112.331

Orientation ('UB') matrix:
  -0.0355861   0.0176291   0.0620889
  -0.0282110  -0.0062945  -0.1680024
  -0.0229949  -0.0195598   0.1100247

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6457   36.9360    4.7573    90.000    90.000    90.000       3452.06
    0.0009    0.0035    0.0003     0.000     0.000     0.000          0.60
Corrected for goodness of fit:
    0.0013    0.0049    0.0005     0.000     0.000     0.000          0.84

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.717      58.438     -32.017
Goniometer zeros (deg):          0.0000*     0.0775      0.0000*     0.1464    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                      -0.2341  -0.0737  -0.0027  -0.3467  -0.1563  -0.2120

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        4.14047e+003  2.95663e+003    1.39      25         2       1

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             510
 Average input ESD (pix, pix, deg):          0.19595         0.17051         0.03882
 Goodness of fit:                            1.57966         1.66832         0.70567

Background pixels updated = 97.49%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  100_0101   12  0.01  0.12 -0.02  0.15  0.18  0.06  66630  46    0  0.96   32 1.19 1.09 1.00 1.000
  101_0102    9  0.06 -0.03 -0.03  0.15  0.13  0.08  52765  38   11  0.91   33 1.19 1.09 1.00 1.000
  102_0103   15  0.03  0.13 -0.06  0.20  0.15  0.12  61897  37    0  0.95   33 1.19 1.09 1.01 1.000
  103_0104    5 -0.05  0.03  0.03  0.09  0.11  0.05 141704  57    0  0.96   32 1.19 1.09 1.01 1.000
  104_0105    3  0.26  0.08 -0.10  0.29  0.12  0.13  57557  41    0  0.96   30 1.19 1.09 1.01 1.000
  105_0106    8 -0.02  0.12  0.05  0.15  0.16  0.09  60426  38    0  0.92   33 1.19 1.09 1.01 1.000
  106_0107   17 -0.04  0.08 -0.01  0.25  0.25  0.10  26659  26    6  0.93   32 1.19 1.09 1.01 1.000
  107_0108    9  0.03  0.12 -0.04  0.08  0.16  0.09 101147  46    0  0.96   33 1.19 1.09 1.01 1.000
  108_0109   11  0.09  0.00 -0.07  0.15  0.11  0.10  65950  42    0  0.94   32 1.19 1.09 1.01 1.000
  109_0110    7  0.01  0.07 -0.02  0.15  0.13  0.06  42342  32    0  0.96   30 1.19 1.09 1.01 1.000
  110_0111    5 -0.12  0.05  0.03  0.20  0.07  0.09  30295  27    0  0.92   32 1.19 1.09 1.01 1.000
  111_0112    9  0.03  0.05 -0.02  0.13  0.09  0.07  43168  32    0  0.94   31 1.19 1.09 1.01 1.000
  112_0113   13 -0.01  0.14 -0.01  0.11  0.19  0.06  78422  52    0  0.96   31 1.19 1.09 1.00 1.000
  113_0114   11  0.06  0.06 -0.04  0.15  0.10  0.07  77371  49    0  0.95   30 1.19 1.09 1.00 1.000
  114_0115   16  0.13  0.09 -0.04  0.48  0.20  0.13  56973  39    0  0.90   33 1.19 1.09 1.00 1.000
  115_0116    4  0.12 -0.02 -0.08  0.16  0.08  0.09  49343  36    0  0.86   33 1.19 1.09 1.00 1.000
  116_0117    8  0.23 -0.20 -0.07  0.53  0.40  0.12  19622  22    0  0.92   32 1.19 1.09 1.00 1.000
  117_0118    6  0.04  0.07 -0.01  0.13  0.13  0.07  52560  37    0  0.93   32 1.19 1.08 1.00 1.000
  118_0119   11  0.15  0.05 -0.02  0.60  0.24  0.11  51416  36    0  0.95   33 1.19 1.09 1.00 1.000
  119_0120    8  0.04  0.06 -0.05  0.08  0.09  0.13  65338  40    0  0.95   33 1.19 1.09 1.00 1.000
Background pixels updated = 97.58%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  120_0121   11  0.08  0.05 -0.05  0.16  0.14  0.08  76780  47    9  0.92   32 1.19 1.09 1.00 1.000
  121_0122    9  0.09 -0.01 -0.03  0.39  0.23  0.07  51970  40   11  0.89   32 1.19 1.09 1.00 1.000
  122_0123    6 -0.01  0.06 -0.03  0.11  0.17  0.05  43315  41    0  0.94   31 1.19 1.09 1.00 1.000
  123_0124   11  0.01  0.08 -0.00  0.17  0.11  0.06  27905  29    0  0.92   32 1.19 1.09 1.00 1.000
  124_0125   11 -0.06  0.03  0.02  0.18  0.10  0.06  44309  34    0  0.94   30 1.19 1.09 1.00 1.000
  125_0126   10 -0.05  0.15  0.01  0.09  0.22  0.03  95173  52    0  0.96   33 1.19 1.09 1.00 1.000
  126_0127    4  0.03  0.05 -0.00  0.04  0.06  0.02  39816  35    0  0.95   32 1.19 1.09 1.00 1.000
  127_0128    6  0.01  0.12 -0.02  0.04  0.14  0.05  64160  43    0  0.96   33 1.20 1.09 1.00 1.000
  128_0129   17  0.04  0.13 -0.04  0.23  0.27  0.11  53573  39    6  0.90   31 1.19 1.09 1.00 1.000
  129_0130   11  0.06 -0.00 -0.04  0.14  0.14  0.11  47643  31    0  0.93   32 1.20 1.09 1.00 1.000
  130_0131    2  0.02 -0.01  0.01  0.05  0.09  0.06  56665  31   50  0.68   30 1.20 1.09 1.00 1.000
  131_0132   12  0.06  0.20 -0.01  0.19  0.32  0.09 137672  59    0  0.96   34 1.20 1.09 1.00 1.000
  132_0133   13 -0.02  0.02 -0.01  0.14  0.10  0.06  72267  49    0  0.93   33 1.20 1.09 1.00 1.000
  133_0134    5  0.13  0.11 -0.09  0.38  0.15  0.19  35131  27    0  0.89   31 1.20 1.09 1.00 1.000
  134_0135   10  0.07 -0.02 -0.03  0.30  0.27  0.13  81153  40    0  0.95   34 1.20 1.09 1.00 1.000
  135_0136   13 -0.04  0.14  0.02  0.29  0.25  0.19  40264  31   15  0.89   33 1.20 1.09 1.00 1.000
  136_0137   12 -0.04  0.13  0.01  0.25  0.24  0.12  71595  42    0  0.97   35 1.20 1.09 1.00 1.000
  137_0138    9 -0.13  0.11  0.02  0.35  0.24  0.13  78965  53   11  0.92   33 1.20 1.09 1.00 1.000
  138_0139   12  0.16  0.30 -0.05  0.47  0.80  0.18  32652  26    8  0.89   35 1.20 1.09 1.00 1.000
  139_0140   10  0.06  0.02 -0.03  0.13  0.13  0.07  28208  27    0  0.92   29 1.20 1.09 1.00 1.000
Background pixels updated = 97.35%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  140_0141    7  0.00  0.03 -0.01  0.09  0.10  0.07  47672  35    0  0.95   34 1.20 1.09 1.00 1.000
  141_0142   13 -0.00  0.09 -0.01  0.11  0.10  0.05  95764  54    0  0.96   31 1.20 1.09 1.00 1.000
  142_0143    8  0.06  0.27 -0.04  0.31  0.45  0.21  20498  19   13  0.81   33 1.20 1.09 1.00 1.000
  143_0144   11 -0.02  0.09  0.01  0.13  0.13  0.09 113667  42    0  0.94   30 1.20 1.09 1.00 1.000
  144_0145   14  0.10  0.17 -0.06  0.22  0.22  0.09  49183  41    0  0.94   33 1.20 1.09 1.00 1.000
  145_0146   11 -0.02  0.09 -0.02  0.11  0.15  0.06  69005  44    0  0.96   36 1.20 1.09 1.00 1.000
  146_0147    9  0.23 -0.03 -0.05  0.56  0.18  0.17  33665  29    0  0.93   34 1.20 1.09 0.99 1.000
  147_0148    6 -0.10  0.04  0.06  0.19  0.17  0.10  79526  46    0  0.96   33 1.20 1.09 0.99 1.000
  148_0149   11 -0.04  0.05  0.02  0.10  0.14  0.05 107590  54    0  0.95   30 1.20 1.09 0.99 1.000
  149_0150   10  0.45  0.19 -0.10  0.84  0.58  0.17  39645  23    0  0.92   36 1.20 1.09 0.99 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.5592    0.9289    35.064   112.182

Orientation ('UB') matrix:
  -0.0355747   0.0176401   0.0621043
  -0.0282219  -0.0062946  -0.1679472
  -0.0229966  -0.0195635   0.1100360

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6461   36.9226    4.7581    90.000    90.000    90.000       3451.43
    0.0009    0.0038    0.0003     0.000     0.000     0.000          0.62
Corrected for goodness of fit:
    0.0012    0.0054    0.0004     0.000     0.000     0.000          0.86

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.706      58.429     -32.024
Goniometer zeros (deg):          0.0000*     0.0743      0.0000*     0.1530    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                      -0.1587   0.0369  -0.0020  -0.2806  -0.1468  -0.2081

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        3.23667e+003  2.95958e+003    1.40       3         5       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             507
 Average input ESD (pix, pix, deg):          0.20459         0.18134         0.03843
 Goodness of fit:                            1.57654         1.66991         0.71508

Background pixels updated = 97.22%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  150_0151   13 -0.03 -0.01  0.02  0.32  0.21  0.13 102401  53    0  0.94   34 1.20 1.09 0.99 1.000
  151_0152   11  0.18 -0.13 -0.10  0.49  0.75  0.21  13816  17    9  0.82   36 1.20 1.09 0.99 1.000
  152_0153    8  0.06  0.09 -0.04  0.14  0.23  0.07  60947  37    0  0.95   33 1.20 1.09 0.99 1.000
  153_0154   10  0.09  0.04 -0.04  0.13  0.21  0.12  32381  28    0  0.96   34 1.20 1.09 0.99 1.000
  154_0155    7  0.14  0.25 -0.02  0.27  0.33  0.20  11786  15   14  0.86   31 1.20 1.09 0.99 1.000
  155_0156   14  0.11  0.47  0.20  0.15  0.54  0.25  97171  55    0  0.76   35 1.20 1.09 0.99 1.000
  156_0157   11  0.18  0.59  0.16  0.26  0.63  0.21  58160  37    9  0.55   33 1.20 1.09 1.00 1.000
  157_0158   13  0.16  0.71  0.24  0.29  0.96  0.34  63759  37    8  0.53   32 1.21 1.09 1.00 1.000
  158_0159    9  0.03  0.82  0.39  0.11  0.90  0.43  53755  44    0  0.63   34 1.21 1.09 1.00 1.000
  159_0160   11  0.01  0.77  0.29  0.35  0.89  0.35  28180  27    9  0.63   32 1.21 1.09 1.00 1.000
Background pixels updated = 97.30%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  160_0161    6  0.10  0.62  0.15  0.25  0.71  0.30  30583  28   17  0.67   34 1.21 1.09 1.00 1.000
  161_0162   13  0.20  0.53  0.16  0.40  0.86  0.28  49847  34    0  0.74   33 1.21 1.09 1.00 1.000
  162_0163   14 -0.04  0.60  0.27  0.14  0.67  0.33  76444  43    0  0.81   34 1.21 1.09 0.99 1.000
  163_0164    8  0.11  0.49  0.15  0.21  0.73  0.26  28165  28   13  0.80   32 1.21 1.09 0.99 1.000
  164_0165   11 -0.02  0.48  0.29  0.29  0.53  0.36 119335  53    9  0.82   32 1.21 1.09 0.99 1.000
  165_0166   14  0.24  0.70  0.14  0.53  0.89  0.28  36430  30    0  0.90   34 1.21 1.09 1.00 1.000
  166_0167   10  0.04  0.62  0.17  0.25  0.77  0.22  20863  22    0  0.90   33 1.21 1.09 1.00 1.000
  167_0168    7  0.02  0.32  0.15  0.11  0.37  0.18  29266  23   14  0.83   34 1.21 1.09 1.00 1.000
  168_0169   11 -0.05  0.44  0.26  0.14  0.47  0.29 179896  75    0  0.92   31 1.21 1.09 1.00 1.000
  169_0170    9  0.08  0.48  0.23  0.13  0.54  0.31  79999  44    0  0.90   36 1.21 1.09 1.00 1.000
  170_0171   11  0.08  0.50  0.14  0.28  0.64  0.25  69622  42    0  0.94   33 1.22 1.09 0.99 1.000
  171_0172   13  0.07  0.39  0.20  0.17  0.43  0.25  69041  48    8  0.90   31 1.22 1.09 0.99 1.000
  172_0173    9 -0.03  0.37  0.22  0.33  0.62  0.26  35318  32    0  0.96   33 1.21 1.09 0.99 1.000
  173_0174    7  0.09  0.60  0.21  0.22  0.66  0.31  72465  47    0  0.93   38 1.21 1.09 0.99 1.000
  174_0175   13  0.08  0.44  0.17  0.17  0.49  0.23  65371  44    0  0.95   36 1.21 1.09 0.99 1.000
  175_0176    7 -0.00  0.28  0.18  0.17  0.33  0.23 115948  47    0  0.93   33 1.21 1.09 0.99 1.000
  176_0177    8  0.08  0.54  0.11  0.16  0.61  0.14  55060  44    0  0.95   33 1.21 1.09 0.99 1.000
  177_0178   17  0.04  0.31  0.13  0.14  0.39  0.18  46061  34    6  0.92   31 1.22 1.09 0.99 1.000
  178_0179    8  0.05  0.34  0.15  0.21  0.38  0.21  51691  40   13  0.92   33 1.22 1.09 0.99 1.000
  179_0180    9  0.08  0.31  0.11  0.14  0.38  0.20  43694  38    0  0.95   34 1.22 1.09 0.99 1.000
Background pixels updated = 97.35%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  180_0181   10 -0.01  0.41  0.18  0.35  0.51  0.26  45061  32   10  0.90   33 1.22 1.09 0.99 1.000
  181_0182   14  0.16  0.31  0.03  0.44  0.48  0.17  46124  34    7  0.90   35 1.22 1.09 0.99 1.000
  182_0183    7  0.02  0.21  0.15  0.07  0.25  0.19 146122  73    0  0.91   30 1.22 1.09 0.99 1.000
  183_0184   12  0.12  0.39  0.09  0.26  0.41  0.14  66171  46    0  0.95   33 1.22 1.09 0.99 1.000
  184_0185   11  0.14  0.32  0.16  0.32  0.42  0.23  42748  33    0  0.96   34 1.22 1.09 0.99 1.000
  185_0186    8  0.05  0.18  0.08  0.18  0.33  0.17  46380  30    0  0.93   29 1.22 1.09 0.99 1.000
  186_0187   11  0.09  0.28  0.07  0.23  0.32  0.16  53745  35    0  0.94   34 1.22 1.09 1.00 1.000
  187_0188   11  0.06  0.32  0.09  0.17  0.42  0.17  76201  42    0  0.92   35 1.22 1.09 1.00 1.000
  188_0189   11  0.02  0.25  0.11  0.16  0.28  0.20  19305  23    0  0.93   33 1.22 1.09 1.00 1.000
  189_0190   11  0.09  0.32  0.10  0.21  0.40  0.17  66055  47    0  0.93   31 1.22 1.09 1.00 1.000
  190_0191    9 -0.04  0.21  0.14  0.16  0.40  0.17  38346  32    0  0.94   33 1.22 1.09 1.00 1.000
  191_0192    9  0.21  0.20  0.05  0.46  0.41  0.21  35564  31   11  0.87   32 1.22 1.09 1.00 1.000
  192_0193    7 -0.01  0.23  0.03  0.12  0.25  0.14  51618  38   14  0.90   33 1.22 1.09 0.99 1.000
  193_0194    9  0.06  0.30  0.09  0.12  0.34  0.19  71191  50    0  0.96   34 1.22 1.09 0.99 1.000
  194_0195   12  0.15  0.27  0.05  0.29  0.33  0.11  72974  45    0  0.94   33 1.22 1.09 0.99 1.000
  195_0196   14  0.16  0.32  0.11  0.26  0.43  0.19  70209  33    0  0.95   34 1.22 1.09 0.99 1.000
  196_0197    7  0.06  0.07  0.05  0.34  0.60  0.18  61231  42    0  0.95   37 1.22 1.09 0.99 1.000
  197_0198    8  0.03  0.19  0.01  0.09  0.25  0.10  46395  31   13  0.90   34 1.22 1.09 0.99 1.000
  198_0199   11  0.03  0.23  0.04  0.14  0.37  0.16  89212  52    9  0.91   33 1.22 1.09 0.99 1.000
  199_0200    7  0.07  0.31 -0.00  0.10  0.33  0.07  71362  42    0  0.96   34 1.22 1.09 0.99 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.5459    0.9271    35.253   112.512

Orientation ('UB') matrix:
  -0.0356261   0.0176086   0.0622103
  -0.0282032  -0.0063161  -0.1679199
  -0.0229114  -0.0196056   0.1099701

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6510   36.9023    4.7586    90.000    90.000    90.000       3450.81
    0.0009    0.0030    0.0003     0.000     0.000     0.000          0.54
Corrected for goodness of fit:
    0.0034    0.0112    0.0010     0.000     0.000     0.000          2.01

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.672      58.446     -31.894
Goniometer zeros (deg):          0.0000*     0.0545      0.0000*     0.2210    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.0080   0.7207  -0.0023  -0.1905  -0.0881  -0.1513

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        2.62443e+004  2.11614e+004    3.73       2         5       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             509
 Average input ESD (pix, pix, deg):          0.21453         0.21632         0.04007
 Goodness of fit:                            2.30744         5.35891         2.70771

Background pixels updated = 97.38%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  200_0201   12  0.05  0.04  0.09  0.20  0.21  0.25  36872  30    8  0.84   33 1.22 1.09 0.99 1.000
  201_0202   12  0.20  0.08  0.03  0.54  0.30  0.16  60080  45    0  0.91   32 1.22 1.09 0.99 1.000
  202_0203   10  0.08  0.02  0.07  0.17  0.33  0.19  65331  40   10  0.89   34 1.22 1.09 0.99 1.000
  203_0204    7  0.20  0.14  0.01  0.23  0.27  0.19  34916  29    0  0.93   37 1.22 1.09 0.99 1.000
  204_0205   10  0.12  0.11  0.07  0.47  0.32  0.20  26456  29   10  0.89   31 1.22 1.09 0.99 1.000
  205_0206   14  0.09  0.08  0.06  0.14  0.15  0.15  70247  50    7  0.91   33 1.22 1.09 0.99 1.000
  206_0207    9  0.07  0.10  0.03  0.12  0.18  0.20  47557  42    0  0.93   33 1.22 1.08 0.99 1.000
  207_0208   10  0.19 -0.02  0.14  0.42  0.38  0.28  75362  43   10  0.89   35 1.22 1.08 0.99 1.000
  208_0209    8  0.15  0.00  0.02  0.19  0.20  0.17  22491  24   13  0.87   30 1.22 1.08 1.00 1.000
  209_0210    8  0.26  0.26  0.06  0.38  0.49  0.26  49560  35    0  0.95   36 1.22 1.09 1.00 1.000
  210_0211   15  0.00  0.09  0.06  0.26  0.32  0.18  56273  40    7  0.90   32 1.22 1.09 1.00 1.000
  211_0212    9 -0.09  0.11  0.05  0.48  0.18  0.21  35092  27   11  0.87   33 1.22 1.08 1.00 1.000
  212_0213   10  0.20  0.17 -0.09  0.24  0.30  0.23  40717  30    0  0.94   36 1.22 1.08 1.00 1.000
  213_0214    9  0.18  0.01  0.01  0.28  0.15  0.17  35342  32    0  0.94   32 1.22 1.08 1.00 1.000
  214_0215   14  0.10  0.10  0.07  0.19  0.25  0.18  87595  52    0  0.94   33 1.22 1.08 1.00 1.000
  215_0216   11  0.14  0.13 -0.04  0.30  0.30  0.21  39791  31    0  0.92   34 1.22 1.08 1.00 1.000
  216_0217   10 -0.05  0.18  0.07  0.33  0.25  0.24  51094  35    0  0.91   35 1.22 1.08 1.00 1.000
  217_0218    8  0.22  0.20  0.03  0.29  0.33  0.14  32191  27    0  0.95   33 1.22 1.08 1.00 1.000
  218_0219   10  0.14  0.01  0.01  0.20  0.06  0.11  49978  37    0  0.95   32 1.22 1.08 1.00 1.000
  219_0220   10  0.03 -0.02  0.02  0.11  0.12  0.13 107539  59    0  0.92   33 1.22 1.08 1.00 1.000
Background pixels updated = 97.39%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  220_0221   14  0.03  0.09  0.05  0.23  0.24  0.18  27806  26    0  0.93   34 1.22 1.08 1.00 1.000
  221_0222    4  0.11  0.03  0.11  0.13  0.08  0.18  41841  37    0  0.96   33 1.22 1.08 1.00 1.000
  222_0223   12  0.05  0.02  0.08  0.18  0.17  0.20  59554  42    0  0.92   32 1.22 1.08 1.00 1.000
  223_0224   15  0.11  0.05 -0.01  0.20  0.12  0.17  51717  42    0  0.94   33 1.22 1.08 1.00 1.000
  224_0225   14  0.23  0.03  0.02  0.67  0.23  0.19  84769  47    0  0.94   33 1.22 1.08 1.00 1.000
  225_0226    4  0.38  0.27 -0.22  0.62  0.48  0.25  38720  31   25  0.89   33 1.22 1.08 1.00 1.000
  226_0227    6  0.09  0.06  0.06  0.17  0.34  0.19  29967  23    0  0.92   33 1.22 1.08 1.00 1.000
  227_0228   13  0.04  0.03  0.04  0.13  0.15  0.17  34266  32    0  0.96   35 1.22 1.08 1.00 1.000
  228_0229   11  0.17 -0.03 -0.05  0.31  0.19  0.20  33961  32    0  0.95   30 1.22 1.08 1.00 1.000
  229_0230   15  0.10  0.05  0.03  0.24  0.27  0.17  91677  41    7  0.91   32 1.22 1.08 1.00 1.000
  230_0231    6  0.01  0.09 -0.00  0.31  0.40  0.25 7874.5  14    0  0.89   34 1.22 1.08 1.00 1.000
  231_0232    8 -0.04 -0.01  0.05  0.29  0.30  0.18  28945  25   13  0.88   36 1.22 1.08 1.00 1.000
  232_0233    8  0.18  0.09  0.04  0.26  0.23  0.14  16896  20    0  0.92   34 1.22 1.08 1.00 1.000
  233_0234   15  0.10  0.04 -0.01  0.22  0.25  0.16  30728  27    7  0.93   34 1.22 1.08 1.00 1.000
  234_0235   11  0.17  0.01  0.03  0.47  0.23  0.16  42769  33    0  0.94   32 1.22 1.08 1.00 1.000
  235_0236   13  0.12  0.06  0.02  0.17  0.16  0.12  28475  27    0  0.95   33 1.22 1.08 1.00 1.000
  236_0237    3 -0.21  0.06  0.09  0.57  0.24  0.35  35688  34    0  0.83   33 1.22 1.08 1.00 1.000
  237_0238   11  0.04 -0.00 -0.02  0.08  0.09  0.10  55920  41    9  0.90   32 1.22 1.07 1.00 1.000
  238_0239   14  0.12  0.00 -0.02  0.19  0.11  0.13  40591  34    0  0.96   34 1.22 1.07 1.00 1.000
  239_0240   10  0.09 -0.02  0.06  0.17  0.13  0.13  32995  29    0  0.95   34 1.22 1.07 1.00 1.000
Background pixels updated = 97.34%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  240_0241   10  0.25  0.05 -0.06  0.34  0.26  0.14  32213  23    0  0.89   34 1.22 1.07 1.00 1.000
  241_0242   13  0.22 -0.04  0.03  0.49  0.13  0.14  46774  38    0  0.92   31 1.22 1.07 1.00 1.000
  242_0243    6  0.00  0.04  0.12  0.19  0.27  0.20  58939  42    0  0.93   32 1.22 1.07 1.00 1.000
  243_0244   13  0.06  0.01  0.03  0.20  0.18  0.13  35336  32    0  0.95   34 1.22 1.07 1.00 1.000
  244_0245   11  0.09  0.03 -0.01  0.19  0.13  0.08  38203  29    0  0.94   32 1.22 1.07 1.00 1.000
  245_0246    9 -0.05 -0.01  0.03  0.25  0.20  0.19  74118  40    0  0.95   33 1.22 1.07 1.00 1.000
  246_0247    7  0.00 -0.11  0.10  0.36  0.42  0.26  37743  31    0  0.95   35 1.22 1.07 1.00 1.000
  247_0248   13  0.22  0.07 -0.05  0.41  0.27  0.17  30546  27    0  0.89   32 1.22 1.07 1.00 1.000
  248_0249   11  0.18  0.06 -0.08  0.25  0.23  0.12  43353  31    0  0.91   35 1.22 1.07 1.00 1.000
  249_0250   10  0.22 -0.01 -0.07  0.29  0.11  0.14  72813  41    0  0.93   31 1.22 1.07 1.00 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.6130    0.9250    34.318   112.899

Orientation ('UB') matrix:
  -0.0356292   0.0175883   0.0624516
  -0.0282660  -0.0063414  -0.1677387
  -0.0228186  -0.0196074   0.1102701

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6529   36.9103    4.7567    90.000    90.000    90.000       3450.50
    0.0010    0.0024    0.0003     0.000     0.000     0.000          0.49
Corrected for goodness of fit:
    0.0017    0.0040    0.0004     0.000     0.000     0.000          0.80

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.579      58.364     -31.784
Goniometer zeros (deg):          0.0000*     0.0686      0.0000*     0.1921    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.3134   0.7871  -0.0032  -0.2057  -0.1104  -0.1996

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        6.07893e+003  4.04615e+003    1.63       3         3       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             510
 Average input ESD (pix, pix, deg):          0.22802         0.21558         0.04144
 Goodness of fit:                            1.82244         1.90983         0.96828

Background pixels updated = 97.32%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  250_0251   14 -0.11  0.13  0.03  0.42  0.27  0.22  23405  23    7  0.90   36 1.22 1.07 1.00 1.000
  251_0252    7 -0.08 -0.00  0.00  0.22  0.07  0.08  38658  31   14  0.88   30 1.22 1.07 1.00 1.000
  252_0253    7  0.06  0.09  0.01  0.16  0.20  0.12  55786  42    0  0.94   33 1.22 1.07 1.00 1.000
  253_0254    9  0.07  0.12 -0.03  0.21  0.23  0.15  43384  33    0  0.91   31 1.22 1.07 1.00 1.000
  254_0255   12  0.10  0.07  0.02  0.16  0.12  0.10 119306  57    8  0.93   35 1.22 1.07 1.00 1.000
  255_0256   12  0.14  0.07  0.01  0.27  0.12  0.13  61781  35    0  0.91   31 1.22 1.07 1.00 1.000
  256_0257    7  0.16 -0.01  0.01  0.37  0.37  0.16  25721  22    0  0.90   36 1.22 1.07 1.00 1.000
  257_0258   12  0.10  0.13  0.03  0.19  0.19  0.13  26212  21   17  0.87   32 1.22 1.07 1.00 1.000
  258_0259    9  0.08  0.09  0.00  0.13  0.18  0.13  92384  62    0  0.94   34 1.22 1.07 1.00 1.000
  259_0260   12  0.22  0.05 -0.07  0.32  0.30  0.13  37666  31    0  0.93   32 1.22 1.07 1.00 1.000
Background pixels updated = 97.40%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  260_0261   12 -0.04  0.06  0.07  0.26  0.11  0.13  54327  40    0  0.96   34 1.22 1.07 1.00 1.000
  261_0262   10  0.08  0.04  0.01  0.18  0.11  0.08  75412  51   10  0.92   30 1.22 1.07 1.00 1.000
  262_0263   13  0.07  0.17  0.03  0.21  0.24  0.16  43199  36    8  0.94   35 1.22 1.07 1.00 1.000
  263_0264   10  0.22  0.11 -0.04  0.34  0.20  0.13  59731  41    0  0.94   33 1.22 1.07 1.00 1.000
  264_0265    9  0.05  0.07  0.01  0.18  0.11  0.09  47111  37   11  0.90   32 1.22 1.07 1.00 1.000
  265_0266   14  0.08  0.08  0.02  0.14  0.14  0.10  42734  31    7  0.91   32 1.22 1.07 1.00 1.000
  266_0267   12  0.18  0.17 -0.03  0.44  0.40  0.18  56234  39    0  0.96   33 1.22 1.07 1.00 1.000
  267_0268    7  0.07  0.11 -0.05  0.18  0.19  0.11  39853  32    0  0.94   33 1.22 1.07 1.00 1.000
  268_0269    7  0.09  0.15  0.07  0.22  0.21  0.17  33247  30    0  0.91   35 1.22 1.07 1.00 1.000
  269_0270   10  0.02  0.10  0.03  0.12  0.16  0.14  31853  29   10  0.90   33 1.22 1.07 1.00 1.000
  270_0271   14  0.06  0.15 -0.00  0.15  0.22  0.13  52536  35    7  0.92   33 1.22 1.07 1.00 1.000
  271_0272    9  0.14  0.11 -0.00  0.27  0.17  0.10  75967  36    0  0.88   30 1.22 1.07 1.00 1.000
  272_0273    8  0.19  0.10 -0.07  0.30  0.21  0.15  35568  29   13  0.90   30 1.22 1.07 1.00 1.000
  273_0274   10 -0.02  0.05  0.01  0.13  0.09  0.12 111506  63    0  0.94   32 1.22 1.07 1.00 1.000
  274_0275   10  0.11  0.17  0.02  0.15  0.21  0.11  50842  39    0  0.96   34 1.22 1.07 1.00 1.000
  275_0276    8  0.12  0.14  0.04  0.14  0.20  0.09  39204  34    0  0.96   34 1.22 1.07 1.00 1.000
  276_0277   12  0.14  0.14  0.01  0.35  0.29  0.16  78157  44    0  0.93   31 1.22 1.07 1.00 1.000
  277_0278    9  0.06  0.21 -0.01  0.17  0.51  0.20 105406  58    0  0.96   35 1.22 1.07 1.00 1.000
  278_0279   12  0.08  0.06  0.03  0.15  0.18  0.12  72609  49    0  0.96   33 1.22 1.07 1.00 1.000
  279_0280   13  0.02  0.11  0.03  0.16  0.21  0.19 126256  58   15  0.88   33 1.22 1.07 1.00 1.000
Background pixels updated = 97.54%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  280_0281    8  0.17  0.01  0.01  0.31  0.25  0.06  76781  43   13  0.90   33 1.22 1.07 1.00 1.000
  281_0282   17  0.17  0.11 -0.01  0.48  0.20  0.10 116496  59    0  0.95   32 1.22 1.07 1.00 1.000
  282_0283   14 -0.01  0.10  0.06  0.15  0.19  0.12  57681  43    7  0.92   33 1.22 1.07 1.00 1.000
  283_0284    8  0.03  0.04  0.05  0.08  0.10  0.15  14010  17    0  0.92   33 1.22 1.07 1.00 1.000
  284_0285    6  0.05  0.08  0.03  0.10  0.10  0.08  29519  29    0  0.95   30 1.22 1.07 1.00 1.000
  285_0286   11  0.12  0.07 -0.04  0.25  0.18  0.13  45783  36    9  0.92   34 1.22 1.07 1.00 1.000
  286_0287   10  0.08  0.09  0.01  0.20  0.16  0.11  43802  32    0  0.95   33 1.22 1.07 1.00 1.000
  287_0288   11  0.38 -0.03 -0.03  0.85  0.46  0.23  24410  23    9  0.87   34 1.22 1.07 1.00 1.000
  288_0289    5  0.08  0.06 -0.02  0.10  0.09  0.09  15074  21    0  0.96   35 1.22 1.07 1.00 1.000
  289_0290   12  0.12  0.16 -0.07  0.27  0.29  0.20  30585  29    0  0.95   33 1.22 1.06 1.00 1.000
  290_0291    3  0.20  0.14  0.03  0.25  0.14  0.15  49484  38    0  0.97   28 1.22 1.06 1.00 1.000
  291_0292   14  0.00  0.16  0.02  0.29  0.40  0.17  98930  50    0  0.92   33 1.22 1.07 1.00 1.000
  292_0293   14  0.06  0.13  0.03  0.23  0.23  0.12  68214  45    7  0.91   32 1.22 1.07 1.00 1.000
  293_0294   11  0.15  0.06 -0.06  0.28  0.09  0.12  33398  31    0  0.95   32 1.22 1.06 1.00 1.000
  294_0295    7 -0.05 -0.05  0.07  0.30  0.11  0.15  73742  49    0  0.95   31 1.22 1.06 1.00 1.000
  295_0296   16  0.09  0.06  0.02  0.48  0.21  0.14  52280  39   13  0.91   34 1.22 1.06 1.00 1.000
  296_0297    9 -0.05  0.10  0.08  0.19  0.26  0.13  39954  32    0  0.93   33 1.22 1.06 1.00 1.000
  297_0298   14  0.08  0.12  0.01  0.18  0.28  0.15  28362  27    0  0.94   34 1.22 1.06 1.00 1.000
  298_0299   13  0.10  0.15 -0.01  0.36  0.40  0.15  26184  30    0  0.94   32 1.22 1.06 1.00 1.000
  299_0300   12  0.03  0.05  0.01  0.14  0.09  0.07  81426  50    0  0.95   32 1.22 1.06 1.00 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.6142    0.9250    34.302   112.911

Orientation ('UB') matrix:
  -0.0356484   0.0175680   0.0627053
  -0.0283118  -0.0063268  -0.1677691
  -0.0227991  -0.0196125   0.1102891

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6412   36.9280    4.7543    90.000    90.000    90.000       3448.31
    0.0020    0.0017    0.0002     0.000     0.000     0.000          0.53
Corrected for goodness of fit:
    0.0032    0.0028    0.0004     0.000     0.000     0.000          0.85

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.506      58.376     -31.728
Goniometer zeros (deg):          0.0000*     0.0807      0.0000*     0.1824    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.2859   0.7434  -0.0085  -0.2221  -0.1306  -0.1683

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        5.41698e+003  3.91377e+003    1.61      15         5       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             509
 Average input ESD (pix, pix, deg):          0.22042         0.21188         0.04111
 Goodness of fit:                            1.63542         2.07519         0.81667

Background pixels updated = 97.52%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  300_0301    7 -0.10 -0.01 -0.01  0.37  0.11  0.19  38379  33    0  0.93   33 1.22 1.06 1.00 1.000
  301_0302   10 -0.13  0.09  0.03  0.28  0.20  0.16  37504  31    0  0.91   32 1.22 1.06 1.00 1.000
  302_0303   14 -0.01  0.11  0.02  0.18  0.20  0.10  38188  32    0  0.95   33 1.22 1.06 1.00 1.000
  303_0304    9  0.05  0.03 -0.06  0.16  0.11  0.14  62133  40   11  0.88   32 1.22 1.06 1.00 1.000
  304_0305    5 -0.18  0.30  0.13  0.32  0.36  0.19  28491  27    0  0.93   35 1.22 1.06 1.00 1.000
  305_0306    9  0.08  0.09 -0.04  0.23  0.22  0.14  34298  25   11  0.85   31 1.22 1.06 1.00 1.000
  306_0307    8  0.11  0.11 -0.02  0.33  0.17  0.13  37290  29    0  0.93   31 1.22 1.06 1.00 1.000
  307_0308    9  0.01  0.14 -0.03  0.18  0.35  0.15  32978  30    0  0.93   33 1.22 1.06 1.00 1.000
  308_0309    9  0.10  0.21 -0.02  0.22  0.33  0.12  38308  31    0  0.96   35 1.22 1.06 1.00 1.000
  309_0310   13  0.01  0.05 -0.00  0.16  0.17  0.08  63474  38    8  0.92   32 1.22 1.06 1.00 1.000
  310_0311   12  0.02  0.02 -0.02  0.14  0.11  0.09  34770  33    0  0.95   32 1.22 1.06 1.00 1.000
  311_0312   10  0.00  0.07 -0.00  0.09  0.10  0.12  50477  38    0  0.96   34 1.22 1.06 1.00 1.000
  312_0313   12 -0.04  0.02  0.05  0.25  0.16  0.13  43556  33    8  0.92   33 1.22 1.06 1.00 1.000
  313_0314    8  0.07  0.04  0.02  0.30  0.07  0.06  29311  32    0  0.94   31 1.22 1.06 1.00 1.000
  314_0315   11  0.05  0.11 -0.04  0.10  0.14  0.10  31269  33    0  0.92   30 1.21 1.06 1.00 1.000
  315_0316   13 -0.05  0.18  0.02  0.28  0.31  0.14  26289  23    0  0.94   32 1.21 1.06 1.00 1.000
  316_0317    9  0.10  0.09  0.00  0.30  0.18  0.16  37945  37    0  0.95   34 1.21 1.06 1.00 1.000
  317_0318    6  0.40  0.51 -0.11  0.99  0.90  0.19  35343  33    0  0.94   34 1.21 1.06 1.00 1.000
  318_0319   10  0.10  0.20 -0.02  0.24  0.33  0.15  50187  35    0  0.95   33 1.21 1.06 1.00 1.000
  319_0320    7 -0.00  0.15  0.01  0.07  0.25  0.08 108436  52    0  0.95   32 1.21 1.06 1.00 1.000
Background pixels updated = 97.06%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  320_0321    9 -0.07  0.08  0.04  0.13  0.16  0.09  35216  30    0  0.93   33 1.21 1.06 1.00 1.000
  321_0322    7  0.03  0.09 -0.01  0.43  0.22  0.14  57906  32    0  0.93   33 1.21 1.06 1.00 1.000
  322_0323   10  0.12  0.10 -0.05  0.24  0.17  0.09  38558  32   20  0.86   32 1.21 1.06 1.00 1.000
  323_0324    7 -0.10  0.04  0.02  0.17  0.06  0.08  65557  48    0  0.93   32 1.21 1.06 1.00 1.000
  324_0325    9  0.04  0.29 -0.04  0.22  0.60  0.14  32409  30    0  0.96   31 1.21 1.06 1.00 1.000
  325_0326   17 -0.01  0.06  0.02  0.29  0.12  0.10  50863  34    0  0.95   33 1.21 1.06 1.00 1.000
  326_0327   11  0.44  0.42 -0.11  1.11  1.04  0.24  37305  29    9  0.91   34 1.21 1.06 1.00 1.000
  327_0328   14  0.20  0.18 -0.07  0.50  0.48  0.19  36080  31   14  0.91   31 1.21 1.06 1.00 1.000
  328_0329   12 -0.12  0.21  0.02  0.25  0.29  0.15  56473  35    0  0.93   36 1.22 1.06 0.99 1.000
  329_0330    8  0.03  0.04 -0.02  0.12  0.07  0.05  23230  24    0  0.92   30 1.21 1.06 0.99 1.000
  330_0331    9  0.18  0.04 -0.03  0.33  0.49  0.10  58963  45   11  0.91   34 1.21 1.06 1.00 1.000
  331_0332   10  0.12  0.19 -0.06  0.25  0.42  0.13  49837  37    0  0.96   33 1.21 1.06 0.99 1.000
  332_0333    7  0.03  0.10 -0.06  0.13  0.12  0.12  12728  15    0  0.90   30 1.21 1.06 0.99 1.000
  333_0334    6  0.33  0.34 -0.08  0.56  0.87  0.23  19029  18   17  0.88   35 1.21 1.06 0.99 1.000
  334_0335   11  0.01  0.06 -0.02  0.16  0.15  0.08 178694  66    0  0.94   31 1.21 1.06 0.99 1.000
  335_0336    9  0.04  0.13 -0.02  0.15  0.15  0.09  57788  38    0  0.91   29 1.22 1.06 0.99 1.000
  336_0337    6 -0.02  0.13  0.03  0.10  0.19  0.05  45114  33    0  0.89   31 1.22 1.06 0.99 1.000
  337_0338   11  0.08  0.15 -0.04  0.14  0.17  0.09  80258  45    0  0.94   32 1.22 1.06 0.99 1.000
  338_0339   13  0.09  0.02 -0.06  0.23  0.18  0.14  97782  50    0  0.96   32 1.22 1.06 1.00 1.000
  339_0340   10  0.06  0.04 -0.07  0.12  0.09  0.13  33328  30    0  0.87   32 1.22 1.06 1.00 1.000
Background pixels updated = 97.89%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  340_0341   13  0.02  0.15  0.01  0.33  0.21  0.11  51920  37    0  0.94   34 1.22 1.06 1.00 1.000
  341_0342   12  0.04  0.09 -0.01  0.14  0.17  0.06 133552  64    0  0.95   31 1.22 1.06 0.99 1.000
  342_0343    8  0.02  0.10 -0.03  0.16  0.11  0.08  15478  18    0  0.94   32 1.22 1.06 1.00 1.000
  343_0344    9  0.00  0.21  0.03  0.42  0.33  0.14  37843  37    0  0.92   34 1.22 1.06 1.00 1.000
  344_0345   10  0.04  0.12 -0.02  0.16  0.17  0.09  46150  31    0  0.95   29 1.22 1.06 1.00 1.000
  345_0346    7 -0.06  0.08  0.06  0.13  0.18  0.10 129600  62    0  0.97   33 1.22 1.06 1.00 1.000
  346_0347    5  0.03  0.19 -0.01  0.08  0.20  0.07  27455  26    0  0.90   32 1.22 1.06 1.00 1.000
  347_0348    7 -0.02  0.13 -0.00  0.16  0.17  0.07  42440  33    0  0.96   31 1.22 1.06 1.00 1.000
  348_0349   12  0.08  0.09 -0.04  0.18  0.18  0.10  89542  58    8  0.93   33 1.22 1.06 1.00 1.000
  349_0350    9 -0.02  0.15  0.02  0.11  0.19  0.05 102247  57    0  0.97   32 1.22 1.06 1.00 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.6905    0.9246    33.301   112.982

Orientation ('UB') matrix:
  -0.0356509   0.0175604   0.0628397
  -0.0283281  -0.0063143  -0.1677800
  -0.0227918  -0.0196198   0.1102410

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6383   36.9315    4.7537    90.000    90.000    90.000       3447.74
    0.0024    0.0016    0.0003     0.000     0.000     0.000          0.69
Corrected for goodness of fit:
    0.0039    0.0027    0.0005     0.000     0.000     0.000          1.15

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.467      58.395     -31.705
Goniometer zeros (deg):          0.0000*     0.0696      0.0000*     0.1873    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.2932   0.7515  -0.0094  -0.2313  -0.1372  -0.1530

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        4.97083e+003  4.12891e+003    1.65      25         2       1

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             508
 Average input ESD (pix, pix, deg):          0.22194         0.20700         0.04108
 Goodness of fit:                            1.80297         2.05002         0.78475

Background pixels updated = 97.96%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  350_0351   12 -0.03  0.16  0.02  0.13  0.27  0.08  36592  35    0  0.96   32 1.22 1.06 1.00 1.000
  351_0352   10  0.07  0.08  0.00  0.17  0.18  0.15  36400  29    0  0.93   33 1.22 1.06 1.00 1.000
  352_0353    8  0.03  0.18 -0.03  0.19  0.25  0.15  79073  45    0  0.95   36 1.22 1.06 1.00 1.000
  353_0354   14  0.03  0.08 -0.04  0.13  0.14  0.10  43017  34    0  0.94   32 1.22 1.06 1.00 1.000
  354_0355    9  0.01  0.06 -0.04  0.19  0.08  0.07  54737  42    0  0.94   32 1.22 1.06 1.00 1.000
  355_0356   11  0.01  0.04 -0.01  0.18  0.16  0.16  47870  37    0  0.96   34 1.22 1.06 1.00 1.000
  356_0357    8  0.03  0.12 -0.03  0.08  0.15  0.06  69618  50    0  0.96   32 1.22 1.06 1.00 1.000
  357_0358    9  0.24  0.04 -0.09  0.54  0.34  0.21  27729  24   11  0.89   32 1.22 1.06 1.00 1.000
  358_0359    6  0.05  0.07 -0.03  0.12  0.17  0.09  50057  33    0  0.95   32 1.22 1.06 1.00 1.000
  359_0360    6 -0.05  0.07  0.05  0.32  0.15  0.17  40303  41    0  0.92   31 1.22 1.06 1.00 1.000
Background pixels updated = 97.60%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  360_0361   13 -0.01  0.07 -0.00  0.15  0.14  0.08  31719  29    0  0.93   32 1.22 1.06 1.00 1.000
  361_0362   13 -0.06  0.09  0.03  0.14  0.15  0.07  56288  42    0  0.95   30 1.22 1.06 1.00 1.000
  362_0363    5  0.59  0.11 -0.11  0.92  0.18  0.20  23471  24   20  0.87   33 1.22 1.06 1.00 1.000
  363_0364   10 -0.08  0.07  0.04  0.22  0.10  0.10  80138  39    0  0.91   32 1.22 1.06 1.00 1.000
  364_0365   10  0.03  0.10 -0.03  0.28  0.14  0.13  24693  23   10  0.88   32 1.22 1.06 1.00 1.000
  365_0366   12  0.02  0.11 -0.04  0.10  0.13  0.09  74721  47    0  0.96   32 1.22 1.06 1.00 1.000
  366_0367   12  0.07  0.13 -0.07  0.17  0.18  0.15  65681  38    8  0.92   30 1.22 1.06 1.00 1.000
  367_0368   10  0.02  0.13  0.03  0.21  0.24  0.15  52463  37    0  0.95   31 1.22 1.06 1.00 1.000
  368_0369    4 -0.14 -0.13  0.08  0.41  0.32  0.26  14301  14    0  0.79   32 1.21 1.06 0.99 1.000
  369_0370    8 -0.07  0.15  0.03  0.13  0.24  0.06  34847  31    0  0.92   33 1.22 1.06 0.99 1.000
  370_0371    7  0.19  0.19 -0.07  0.31  0.28  0.11  34689  29    0  0.98   34 1.22 1.06 0.99 1.000
  371_0372   10  0.05  0.11  0.01  0.22  0.15  0.14  30691  28    0  0.90   30 1.21 1.06 0.99 1.000
  372_0373   13  0.03  0.08 -0.03  0.10  0.11  0.09  35711  32    0  0.94   33 1.21 1.06 0.99 1.000
  373_0374   11  0.01  0.12 -0.05  0.24  0.26  0.15  38191  29    0  0.96   32 1.21 1.06 0.99 1.000
  374_0375    8  0.31  0.05 -0.06  0.54  0.13  0.09  26529  26   13  0.83   30 1.21 1.06 0.99 1.000
  375_0376   11  0.06  0.04 -0.02  0.09  0.08  0.06 146644  64    0  0.95   30 1.21 1.06 0.99 1.000
  376_0377    7 -0.14  0.08  0.04  0.25  0.21  0.12  14647  15   14  0.86   31 1.21 1.06 0.99 1.000
  377_0378   12  0.06  0.11 -0.07  0.16  0.20  0.13  23281  26   17  0.89   34 1.21 1.06 0.99 1.000
  378_0379   13  0.03  0.09 -0.03  0.09  0.14  0.07  56945  46    0  0.97   33 1.21 1.06 0.99 1.000
  379_0380    9 -0.20  0.08  0.09  0.41  0.17  0.21  43630  37   11  0.86   31 1.21 1.06 0.99 1.000
Background pixels updated = 97.77%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  380_0381    7  0.14  0.03 -0.08  0.24  0.12  0.12  24901  25    0  0.95   31 1.21 1.06 0.99 1.000
  381_0382    8  0.07  0.09  0.02  0.40  0.23  0.13  24665  26    0  0.96   33 1.21 1.06 0.99 1.000
  382_0383    6 -0.01  0.11 -0.06  0.05  0.12  0.09  95837  55    0  0.96   33 1.21 1.06 0.99 1.000
  383_0384   18 -0.01  0.12  0.03  0.18  0.17  0.09  59183  37    6  0.91   32 1.21 1.06 1.00 1.000
  384_0385    9 -0.01  0.09  0.04  0.12  0.18  0.07  26231  27    0  0.95   29 1.21 1.06 1.00 1.000
  385_0386    6  0.10  0.03 -0.06  0.25  0.10  0.11  19661  25    0  0.96   33 1.21 1.06 1.00 1.000
  386_0387   10  0.14  0.18 -0.01  0.67  0.27  0.09  46593  37    0  0.91   31 1.21 1.06 1.00 1.000
  387_0388    5  0.05  0.06 -0.03  0.07  0.12  0.06  40048  34    0  0.96   34 1.21 1.06 1.00 1.000
  388_0389    7  0.06 -0.01 -0.02  0.13  0.20  0.09  38345  36    0  0.94   30 1.21 1.06 1.00 1.000
  389_0390   15  0.15  0.15 -0.07  0.47  0.31  0.14  50474  36    0  0.96   33 1.21 1.06 1.00 1.000
  390_0391    9  0.01  0.08 -0.01  0.05  0.13  0.03  83820  51    0  0.97   34 1.21 1.06 0.99 1.000
  391_0392   12  0.00  0.03 -0.00  0.22  0.16  0.11  57563  37    8  0.91   32 1.21 1.06 0.99 1.000
  392_0393    7 -0.03  0.18 -0.07  0.13  0.25  0.10  45138  39    0  0.97   34 1.21 1.06 1.00 1.000
  393_0394   10 -0.04  0.07 -0.00  0.14  0.12  0.04  41985  38    0  0.88   30 1.21 1.06 0.99 1.000
  394_0395   15  0.00  0.11 -0.01  0.12  0.16  0.09 137228  52    0  0.95   34 1.21 1.06 1.00 1.000
  395_0396   12 -0.02  0.10  0.04  0.28  0.20  0.11  53284  38    0  0.95   31 1.21 1.06 1.00 1.000
  396_0397    9  0.06  0.11  0.02  0.14  0.18  0.19  34424  28   11  0.86   33 1.21 1.06 1.00 1.000
  397_0398    5  0.09 -0.12  0.05  0.44  0.23  0.23 9589.2  13    0  0.85   32 1.21 1.06 1.00 1.000
  398_0399    7  0.10 -0.01 -0.02  0.21  0.15  0.13  13626  19    0  0.94   36 1.21 1.06 1.00 1.000
  399_0400    7 -0.05  0.07  0.01  0.10  0.14  0.06  73932  48    0  0.92   30 1.21 1.06 1.00 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.6908    0.9226    33.297   113.361

Orientation ('UB') matrix:
  -0.0356414   0.0175554   0.0629585
  -0.0283317  -0.0063007  -0.1678145
  -0.0227846  -0.0196269   0.1101858

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6413   36.9332    4.7529    90.000    90.000    90.000       3447.87
    0.0018    0.0017    0.0004     0.000     0.000     0.000          0.66
Corrected for goodness of fit:
    0.0029    0.0027    0.0006     0.000     0.000     0.000          1.07

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.436      58.419     -31.690
Goniometer zeros (deg):          0.0000*     0.0624      0.0000*     0.1940    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.2975   0.7488  -0.0098  -0.2622  -0.1426  -0.1639

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        4.84614e+003  4.02054e+003    1.63       5         5       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             511
 Average input ESD (pix, pix, deg):          0.19097         0.16987         0.03921
 Goodness of fit:                            1.99980         1.78164         0.82492

Background pixels updated = 97.48%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  400_0401    8  0.09  0.04 -0.01  0.22  0.12  0.10  23852  26   25  0.84   28 1.21 1.06 1.00 1.000
  401_0402   12  0.03  0.13 -0.05  0.15  0.19  0.09  58960  42    0  0.95   33 1.21 1.06 1.00 1.000
  402_0403   13  0.16  0.08 -0.03  0.43  0.25  0.16  62134  32    8  0.88   33 1.21 1.06 1.00 1.000
  403_0404   10  0.08  0.07 -0.07  0.13  0.18  0.11  38472  32    0  0.97   34 1.21 1.06 1.00 1.000
  404_0405    9  0.00  0.14  0.00  0.04  0.16  0.05  36674  30    0  0.93   33 1.21 1.06 1.00 1.000
  405_0406   16  0.01  0.10 -0.02  0.14  0.15  0.08  79973  49    0  0.95   34 1.21 1.06 1.00 1.000
  406_0407   10  0.12  0.20 -0.05  0.42  0.39  0.15  74630  41    0  0.95   32 1.21 1.06 1.00 1.000
  407_0408    9  0.06  0.08 -0.05  0.27  0.15  0.13  68357  42    0  0.95   33 1.21 1.06 1.00 1.000
  408_0409    5 -0.09  0.08  0.01  0.18  0.12  0.07  41912  33    0  0.95   31 1.21 1.06 1.00 1.000
  409_0410    7  0.02  0.11  0.03  0.33  0.15  0.11 162907  68    0  0.91   31 1.21 1.06 1.00 1.000
  410_0411   11  0.02  0.18  0.00  0.20  0.27  0.11  26278  28    0  0.96   36 1.21 1.06 1.00 1.000
  411_0412    7  0.25  0.20  0.05  0.72  0.31  0.20  42711  36    0  0.93   31 1.21 1.06 1.00 1.000
  412_0413   12 -0.02  0.18 -0.02  0.07  0.23  0.12  62383  46    0  0.97   35 1.21 1.06 1.00 1.000
  413_0414    8 -0.03  0.05  0.03  0.15  0.12  0.10  42900  38    0  0.96   35 1.21 1.06 1.00 1.000
  414_0415   17  0.04  0.19 -0.02  0.15  0.27  0.08  72314  43    0  0.97   33 1.21 1.06 1.00 1.000
  415_0416   11  0.02  0.20 -0.03  0.18  0.30  0.10  73773  48    0  0.97   36 1.21 1.06 1.00 1.000
  416_0417   13 -0.02  0.05  0.00  0.09  0.12  0.08  60126  37    0  0.93   30 1.21 1.06 1.00 1.000
  417_0418   11  0.19  0.35  0.00  0.68  0.53  0.18  65006  37    0  0.94   33 1.21 1.06 1.00 1.000
  418_0419   13  0.17  0.20 -0.02  0.44  0.26  0.10  65934  47    0  0.94   37 1.21 1.06 1.00 1.000
  419_0420    9  0.01  0.17 -0.02  0.05  0.31  0.08  85908  55    0  0.97   35 1.21 1.07 1.00 1.000
Background pixels updated = 97.01%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  420_0421    5 -0.03  0.15 -0.01  0.19  0.18  0.10  25337  26    0  0.97   33 1.21 1.07 1.00 1.000
  421_0422    9  0.05  0.24 -0.03  0.15  0.46  0.19  58143  44    0  0.93   36 1.21 1.07 1.00 1.000
  422_0423    9  0.17 -0.05  0.03  0.64  0.24  0.16  45850  34    0  0.81   33 1.21 1.07 1.00 1.000
  423_0424    6 -0.07  0.09  0.07  0.09  0.11  0.11 384885  91    0  0.91   30 1.21 1.07 1.00 1.000
  424_0425   12  0.04  0.10 -0.00  0.26  0.21  0.11  72106  46    8  0.93   34 1.21 1.07 1.00 1.000
  425_0426   11 -0.02  0.20 -0.03  0.18  0.25  0.16  80120  45    0  0.97   33 1.21 1.07 1.00 1.000
  426_0427   11 -0.04  0.07  0.02  0.09  0.16  0.11  33617  27   18  0.85   34 1.21 1.07 1.00 1.000
  427_0428   20  0.09  0.07 -0.06  0.21  0.20  0.13  36171  29    5  0.91   34 1.21 1.07 1.00 1.000
  428_0429   13  0.09  0.21  0.02  0.27  0.36  0.11  42495  35   15  0.88   33 1.21 1.07 1.00 1.000
  429_0430    7  0.36  0.14 -0.06  1.01  0.37  0.19  11100  16    0  0.90   32 1.21 1.07 1.00 1.000
  430_0431   10 -0.06  0.09  0.03  0.25  0.16  0.12 101667  50    0  0.95   32 1.21 1.07 1.00 1.000
  431_0432    9  0.03  0.16 -0.02  0.16  0.26  0.11  39877  35    0  0.96   35 1.21 1.07 1.00 1.000
  432_0433    4 -0.05  0.07  0.06  0.13  0.11  0.14  22436  24    0  0.94   36 1.21 1.07 1.00 1.000
  433_0434   11  0.08  0.25 -0.05  0.20  0.46  0.18  75438  49    0  0.97   35 1.21 1.07 1.00 1.000
  434_0435    8 -0.08  0.10  0.02  0.12  0.16  0.08  47653  38    0  0.97   32 1.21 1.07 1.00 1.000
  435_0436   15  0.05  0.16 -0.01  0.25  0.25  0.10  33235  29    7  0.91   38 1.21 1.07 1.00 1.000
  436_0437    8  0.09  0.21 -0.01  0.14  0.23  0.07  38063  32    0  0.96   37 1.21 1.07 1.00 1.000
  437_0438   15 -0.00  0.08 -0.00  0.15  0.15  0.07  74921  45    0  0.94   32 1.21 1.07 1.00 1.000
  438_0439   15  0.12  0.09 -0.01  0.35  0.24  0.13  37548  29   13  0.89   33 1.21 1.07 1.00 1.000
  439_0440   10  0.06  0.09 -0.02  0.27  0.18  0.16  34978  29    0  0.91   34 1.21 1.07 1.00 1.000
Background pixels updated = 97.08%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  440_0441   10  0.10  0.13  0.01  0.50  0.43  0.14  31648  27   10  0.89   32 1.21 1.07 1.00 1.000
  441_0442   11 -0.04  0.07  0.04  0.12  0.17  0.11  48757  36    0  0.95   32 1.21 1.07 1.00 1.000
  442_0443    6  0.12  0.03 -0.05  0.29  0.18  0.18  39641  27   17  0.80   32 1.21 1.07 1.00 1.000
  443_0444   11 -0.03  0.14  0.07  0.12  0.26  0.14  32012  31    0  0.95   38 1.21 1.07 1.00 1.000
  444_0445   12  0.00  0.21 -0.02  0.15  0.31  0.12  44721  38    0  0.97   35 1.21 1.07 1.00 1.000
  445_0446   11 -0.03  0.13  0.00  0.08  0.20  0.05 121589  55    0  0.97   34 1.21 1.07 1.00 1.000
  446_0447   10 -0.05  0.15  0.09  0.17  0.22  0.16  31125  31   20  0.87   31 1.21 1.07 1.00 1.000
  447_0448   11 -0.06  0.14  0.08  0.33  0.21  0.22  53162  41    0  0.93   33 1.21 1.07 1.00 1.000
  448_0449    7  0.11  0.10 -0.05  0.38  0.16  0.17  31401  25    0  0.89   31 1.21 1.07 1.00 1.000
  449_0450   15 -0.33  0.04  0.07  0.71  0.24  0.17  31628  26   13  0.87   34 1.21 1.07 1.00 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.6230    0.9239    34.185   113.112

Orientation ('UB') matrix:
  -0.0356387   0.0175524   0.0630313
  -0.0283356  -0.0062883  -0.1678396
  -0.0227886  -0.0196310   0.1101207

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6406   36.9357    4.7528    90.000    90.000    90.000       3447.84
    0.0013    0.0016    0.0003     0.000     0.000     0.000          0.45
Corrected for goodness of fit:
    0.0021    0.0026    0.0004     0.000     0.000     0.000          0.75

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.417      58.441     -31.686
Goniometer zeros (deg):          0.0000*     0.0574      0.0000*     0.1921    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.3004   0.8422  -0.0100  -0.1990  -0.1362  -0.1430

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        4.49293e+003  4.20114e+003    1.66       2         5       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             512
 Average input ESD (pix, pix, deg):          0.20727         0.20658         0.04066
 Goodness of fit:                            1.81989         1.99106         0.96386

Background pixels updated = 97.58%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  450_0451   11  0.00  0.13 -0.01  0.14  0.20  0.09  59051  39    0  0.95   33 1.21 1.07 1.00 1.000
  451_0452    7  0.07  0.15 -0.03  0.12  0.19  0.11  30020  26    0  0.93   34 1.21 1.07 1.00 1.000
  452_0453   10 -0.02  0.11  0.05  0.09  0.20  0.12  54413  39    0  0.93   36 1.21 1.07 1.00 1.000
  453_0454   11  0.04  0.14 -0.02  0.10  0.23  0.09  61771  41    0  0.96   32 1.21 1.07 1.00 1.000
  454_0455   12  0.10  0.30 -0.02  0.59  0.66  0.19  34426  33    0  0.93   34 1.21 1.07 1.00 1.000
  455_0456   14 -0.11  0.20 -0.01  0.29  0.24  0.10  97435  48    0  0.91   33 1.21 1.07 1.00 1.000
  456_0457   15 -0.02  0.26 -0.00  0.11  0.62  0.17  21756  23    7  0.93   34 1.21 1.07 1.00 1.000
  457_0458    3  0.21  0.55 -0.05  0.44  0.76  0.19  23726  25    0  0.97   38 1.21 1.07 1.00 1.000
  458_0459    6  0.01  0.16  0.01  0.07  0.27  0.07  57888  41    0  0.95   32 1.21 1.07 1.00 1.000
  459_0460    8  0.04  0.15  0.01  0.08  0.26  0.13  43827  27    0  0.95   36 1.21 1.07 1.00 1.000
Background pixels updated = 97.44%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  460_0461   14 -0.05  0.05 -0.00  0.18  0.22  0.12  53287  39    0  0.93   33 1.21 1.07 1.00 1.000
  461_0462   18  0.27  0.18 -0.04  0.67  0.24  0.14  60456  36    6  0.90   33 1.21 1.07 1.00 1.000
  462_0463   12  0.13  0.10  0.01  0.27  0.15  0.10  64165  42    8  0.90   33 1.21 1.08 1.00 1.000
  463_0464   11  0.04  0.19 -0.01  0.19  0.37  0.13  41894  31    0  0.97   36 1.21 1.08 1.00 1.000
  464_0465    5  0.00  0.09 -0.01  0.16  0.13  0.10  36352  32   20  0.87   31 1.21 1.08 1.00 1.000
  465_0466   16  0.05  0.18  0.01  0.23  0.32  0.10  67913  34    6  0.90   33 1.21 1.08 1.00 1.000
  466_0467   10 -0.02  0.20  0.00  0.09  0.25  0.08 103208  49    0  0.98   35 1.21 1.08 1.00 1.000
  467_0468    6 -0.10  0.02  0.04  0.16  0.07  0.08  54714  39    0  0.95   33 1.21 1.08 1.00 1.000
  468_0469   11  0.03  0.27 -0.02  0.16  0.48  0.11 119157  58    0  0.96   33 1.21 1.08 1.00 1.000
  469_0470   10  0.06  0.06 -0.04  0.12  0.11  0.09  89179  51    0  0.97   33 1.21 1.08 1.00 1.000
  470_0471   10  0.03 -0.09  0.08  0.68  0.84  0.27  29851  26    0  0.93   34 1.21 1.08 1.01 1.000
  471_0472    8  0.03  0.13  0.02  0.21  0.20  0.10  39392  33    0  0.95   35 1.21 1.08 1.01 1.000
  472_0473    7  0.08  0.07  0.01  0.28  0.11  0.12  61501  47    0  0.94   37 1.21 1.08 1.01 1.000
  473_0474   11 -0.04  0.15  0.09  0.20  0.19  0.18  51310  33    9  0.91   32 1.21 1.08 1.01 1.000
  474_0475    8  0.06  0.04 -0.02  0.09  0.12  0.09  51311  36    0  0.97   34 1.21 1.08 1.01 1.000
  475_0476   11  0.08  0.16  0.01  0.40  0.30  0.10  91715  54    0  0.94   30 1.21 1.08 1.01 1.000
  476_0477   16 -0.22  0.09  0.08  0.42  0.20  0.16  30471  26    6  0.88   31 1.21 1.08 1.01 1.000
  477_0478    5 -0.02  0.09  0.01  0.05  0.14  0.06  54944  43    0  0.97   35 1.21 1.08 1.01 1.000
  478_0479   12  0.06  0.14  0.01  0.17  0.17  0.10  78332  53    0  0.97   34 1.21 1.08 1.01 1.000
  479_0480   13 -0.11  0.12  0.05  0.31  0.18  0.11 115131  51    0  0.93   31 1.21 1.08 1.01 1.000
Background pixels updated = 97.67%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  480_0481    7 -0.04  0.07 -0.01  0.14  0.19  0.12  86522  33   29  0.85   34 1.21 1.08 1.01 1.000
  481_0482    6 -0.02  0.17  0.00  0.14  0.21  0.08  25333  21   17  0.88   31 1.21 1.08 1.01 1.000
  482_0483    7 -0.00  0.13 -0.00  0.08  0.17  0.06  73083  51    0  0.97   30 1.21 1.08 1.01 1.000
  483_0484    9  0.03  0.08 -0.02  0.11  0.15  0.09  18789  22    0  0.96   32 1.21 1.08 1.01 1.000
  484_0485   12 -0.02  0.04  0.01  0.31  0.20  0.18  53481  37    0  0.96   33 1.21 1.08 1.01 1.000
  485_0486    5  0.03  0.03  0.07  0.08  0.05  0.09  68103  57    0  0.97   33 1.21 1.08 1.01 1.000
  486_0487   12  0.17  0.11  0.01  0.74  0.18  0.16  55044  35    0  0.91   33 1.21 1.08 1.01 1.000
  487_0488    9  0.10  0.07 -0.04  0.30  0.12  0.11  20186  20   11  0.89   30 1.21 1.08 1.01 1.000
  488_0489   11  0.04  0.09  0.03  0.18  0.18  0.08  79978  45    0  0.94   31 1.21 1.08 1.01 1.000
  489_0490   11  0.04  0.09  0.01  0.31  0.22  0.12  45349  33    0  0.91   33 1.21 1.08 1.01 1.000
  490_0491   10  0.06  0.05  0.01  0.19  0.09  0.08  72429  50    0  0.95   32 1.21 1.08 1.01 1.000
  491_0492   12  0.01  0.05 -0.04  0.11  0.24  0.09  25506  26    8  0.93   34 1.21 1.08 1.01 1.000
  492_0493    7 -0.13  0.13  0.10  0.17  0.24  0.12  12579  18    0  0.90   32 1.21 1.08 1.01 1.000
  493_0494   11  0.01  0.05  0.06  0.12  0.10  0.13  66651  47    0  0.97   36 1.21 1.08 1.01 1.000
  494_0495   12  0.01  0.06 -0.01  0.19  0.15  0.12  23293  23    0  0.94   33 1.21 1.08 1.01 1.000
  495_0496    9 -0.03  0.04  0.07  0.09  0.07  0.08  53888  45    0  0.94   30 1.21 1.08 1.01 1.000
  496_0497    8  0.04  0.13  0.02  0.15  0.23  0.08  21073  23   13  0.89   30 1.21 1.08 1.01 1.000
  497_0498    9  0.02  0.09  0.01  0.07  0.11  0.08 149032  74    0  0.97   32 1.21 1.08 1.01 1.000
  498_0499    7  0.07  0.07 -0.03  0.12  0.13  0.08  63422  41    0  0.97   34 1.21 1.08 1.01 1.000
  499_0500    9  0.02  0.05  0.01  0.21  0.14  0.12  28604  24   11  0.89   33 1.21 1.08 1.01 1.000

................
Refinement, sample 1 of 1 -- single-component data
This sample is a single crystal with 3 indices (HKL)
Orientation LS for Sample 1 of 1, component 1 in sample, 1 in .p4p/.spin file (512 input reflections)...

Frame rows, columns:               1024  768
Frame width (deg):                     0.400
Relative SVD-filter threshold:     0.0000500
Starting gradient-expansion term:  0.0020000
Weighting multiplier for Z terms:  1.0000000
Minimum elements to filter:                0
Maximum number of LS cycles:              25
Vertical tilt of beam (deg):          0.1000
Individual reflection weights will be used in the refinement

Wavelength, relative uncertainty:  1.5418400,  0.0000058

Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file

Reflection Summary:
 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
    1.1(1)       512         0       512    2.4552    0.9278    36.601   112.393

Orientation ('UB') matrix:
  -0.0356443   0.0175476   0.0630291
  -0.0283178  -0.0062791  -0.1679078
  -0.0227978  -0.0196362   0.1100169

         A         B         C     Alpha      Beta     Gamma           Vol
   19.6413   36.9377    4.7528    90.000    90.000    90.000       3448.16
    0.0011    0.0020    0.0003     0.000     0.000     0.000          0.48
Corrected for goodness of fit:
    0.0018    0.0033    0.0005     0.000     0.000     0.000          0.80

Crystal system constraint:            5  (Orthorhombic)
Parameter constraint mask:            T  (512 = 200[hex])
                                      T: Crystal Translations

Eulerian angles (deg):         -159.425      58.474     -31.689
Goniometer zeros (deg):          0.0000*     0.0565      0.0000*     0.1921    (*=never refined)
Crystal translations (pixels):               0.1101      0.0978     -0.0162

Detector corrections:   X-Cen    Y-Cen     Dist    Pitch     Roll      Yaw
                       0.2523   0.8937  -0.0097  -0.1982  -0.1317  -0.1615

Refinement statistics:   StartingRes      FinalRes     GOF #Cycles #Filtered    Code
                        4.79931e+003  4.24690e+003    1.67       4         4       0

Overall statistics for terms in X, Y, and Z:       X               Y               Z
 Number of nonzero-weight terms:                 512             512             509
 Average input ESD (pix, pix, deg):          0.21277         0.19852         0.04020
 Goodness of fit:                            1.92538         1.92560         0.94066

Background pixels updated = 97.66%            Port, connections: 2000, 1
Integration of BruecknerJK_153F40
    # File #Ref  ErrX  ErrY  ErrZ  RmsX  RmsY  RmsZ Inorm #Sig %<2s <Cor> %Ful XSiz YSiz ZSiz  Beam
  500_0501   11 -0.06  0.18  0.05  0.25  0.22  0.09  59398  41    0  0.94   30 1.21 1.09 1.01 1.000
  501_0502   12  0.11  0.03 -0.01  0.50  0.17  0.16  30220  30    8  0.91   31 1.21 1.08 1.01 1.000
  502_0503    6  0.11  0.12 -0.01  0.18  0.14  0.09  54450  38    0  0.97   32 1.21 1.08 1.01 1.000
  503_0504   14 -0.02  0.03  0.04  0.20  0.23  0.11  33402  29    7  0.89   32 1.21 1.08 1.01 1.000
  504_0505    8  0.12  0.13  0.02  0.30  0.16  0.11  47924  40    0  0.95   31 1.21 1.08 1.01 1.000
  505_0506    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   23 1.21 1.08 1.01 1.000
  506_0507    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   20 1.21 1.08 1.01 1.000
  507_0508    0  0.00  0.00  0.00  0.00  0.00  0.00      0   0    0  0.00   19 1.21 1.08 1.01 1.000

Requested number of frames processed: cu_BruecknerJK_153F40_01_0508.sfrm


I/Sigma = 120.01   Thresh = 0.020   Blend = F   #Contributing = 1348   InitialProfileWt = 0.000
Region 1
Sum = 37484.5;   Maximum = 3153.1;   FM = 0.83
!Region 1: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  1  3  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  2  6  3  0  0  0    0  0  0  4 17  8  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  2  9  5  0  0  0    0  0  0  7 27 14  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  4  3  0  0  0    0  0  0  4 14  8  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  1  3  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  2  5  2  0  0  0    0  0  0  2  7  2  0  0  0    0  0  0  1  4  1  0  0  0  
  0  0  1 11 35 13  1  0  0    0  0  1 18 51 17  1  0  0    0  0  1 12 30  9  0  0  0  
  0  0  1 23 64 24  1  0  0    0  0  2 41100 31  1  0  0    0  0  1 28 62 17  1  0  0  
  0  0  0 11 37 15  1  0  0    0  0  1 19 57 20  1  0  0    0  0  1 12 34 11  1  0  0  
  0  0  0  2  8  4  0  0  0    0  0  0  2 11  6  0  0  0    0  0  0  1  6  3  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 1: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  5 10  2  0  0  0    0  0  0  1  3  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 14 26  5  0  0  0    0  0  0  4  7  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  5 13  3  0  0  0    0  0  0  2  3  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  2  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 213.84   Thresh = 0.020   Blend = F   #Contributing = 20   InitialProfileWt = 0.069
Region 2
Sum = 135494;   Maximum = 10238.7;   FM = 0.8
!Region 2: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  3  2  0  0  0  
  0  0  0  0  0  1  0  0  0    0  0  0  1  3  3  0  0  0    0  0  0  3 22 14  1  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  1  5  5  1  0  0    0  0  0  6 39 27  2  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  2  2  0  0  0    0  0  0  3 21 15  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  3  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 2: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  5  3  0  0  0    0  0  0  1  4  2  0  0  0    0  0  0  1  3  1  0  0  0  
  0  0  0  8 42 23  1  0  0    0  0  0 13 46 17  1  0  0    0  0  0 16 42 10  0  0  0  
  0  0  0 15 81 47  3  0  0    0  0  1 33100 36  1  0  0    0  0  1 43 99 21  0  0  0  
  0  0  0  6 43 27  2  0  0    0  0  0 12 51 21  1  0  0    0  0  0 15 48 13  0  0  0  
  0  0  0  1  5  3  0  0  0    0  0  0  1  5  3  0  0  0    0  0  0  1  5  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 2: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  6 15  3  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 18 37  7  0  0  0    0  0  0  2  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  6 17  4  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  2  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 149.46   Thresh = 0.020   Blend = F   #Contributing = 95   InitialProfileWt = 0.000
Region 3
Sum = 70706.6;   Maximum = 6981.9;   FM = 0.791
!Region 3: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  2  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  3  3  0  0  0    0  0  0  1 12 10  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  5  5  0  0  0    0  0  0  3 27 16  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  3  2  0  0  0    0  0  0  2 15  8  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 3: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  4  3  0  0  0    0  0  0  1  6  3  0  0  0    0  0  0  1  4  1  0  0  0  
  0  0  0  7 35 19  1  0  0    0  0  1 16 55 20  1  0  0    0  0  1 14 33  8  0  0  0  
  0  0  0 19 74 28  1  0  0    0  0  1 41100 27  1  0  0    0  0  1 33 52  9  0  0  0  
  0  0  0  8 38 12  1  0  0    0  0  0 15 45 12  0  0  0    0  0  0 11 20  4  0  0  0  
  0  0  0  1  3  1  0  0  0    0  0  0  1  4  2  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 3: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  6  9  1  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 14 13  1  0  0  0    0  0  0  3  3  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  4  4  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 73.48   Thresh = 0.020   Blend = F   #Contributing = 357   InitialProfileWt = 0.000
Region 4
Sum = 18964.5;   Maximum = 1426.29;   FM = 0.825
!Region 4: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  2  5  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  3  2  0  0  0    0  0  0  5 20  9  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  4  2  0  0  0    0  0  1  9 32 12  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  3  2  0  0  0    0  0  0  6 20  7  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  1  4  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 4: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  3  9  4  0  0  0    0  0  0  3  8  3  0  0  0    0  0  0  2  4  1  0  0  0  
  0  0  1 15 48 17  1  0  0    0  0  1 23 54 15  1  0  0    0  0  1 17 32  7  0  0  0  
  0  0  1 30 83 25  1  0  0    0  0  3 52100 24  1  0  0    0  0  3 43 65 11  0  0  0  
  0  0  1 17 49 14  1  0  0    0  0  1 28 61 13  1  0  0    0  0  2 25 41  6  0  0  0  
  0  0  0  3  8  3  0  0  0    0  0  0  3  9  2  0  0  0    0  0  0  2  5  1  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 4: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  5  9  2  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 15 19  3  0  0  0    0  0  1  2  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 10 13  2  0  0  0    0  0  0  2  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 60.39   Thresh = 0.020   Blend = F   #Contributing = 654   InitialProfileWt = 0.000
Region 5
Sum = 15095.5;   Maximum = 895.726;   FM = 0.867
!Region 5: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  1  1  0  0  0  0    0  0  1  1  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  2  1  0  0  0    0  0  1  5  6  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  5  2  0  0  0    0  0  1 11 19  6  1  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  3  7  2  1  0  0    0  0  1 14 28 10  2  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  2  5  2  1  0  0    0  0  1 10 20  8  1  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  1  3  1  0  0  0    0  0  0  3  7  4  1  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  1  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 5: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  1  1  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  1  1  0  0  0  0  
  0  0  1  9 11  3  0  0  0    0  0  1  7 10  3  0  0  0    0  0  1  3  5  2  0  0  0  
  0  0  2 29 47 15  1  0  0    0  0  2 29 51 16  1  0  0    0  0  2 15 30  9  1  0  0  
  0  0  3 42 78 28  2  0  0    0  0  3 49100 35  3  0  0    0  0  2 31 70 24  2  0  0  
  0  0  2 26 56 22  2  0  0    0  0  2 30 74 30  3  0  0    0  0  2 22 60 24  2  0  0  
  0  0  1  7 17  8  1  0  0    0  0  0  6 20 10  1  0  0    0  0  0  4 14  7  1  0  0  
  0  0  0  1  3  2  0  0  0    0  0  0  1  2  2  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 5: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  1  2  3  1  0  0  0    0  0  1  1  2  1  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  1  5 10  3  0  0  0    0  0  1  1  2  1  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  2 11 26  9  1  0  0    0  0  1  1  3  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  9 26 10  1  0  0    0  0  0  1  4  2  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  6  3  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 44.59   Thresh = 0.020   Blend = F   #Contributing = 653   InitialProfileWt = 0.000
Region 6
Sum = 8435.88;   Maximum = 450.19;   FM = 0.895
!Region 6: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  1  1  0  0  0  0  0    0  1  1  2  2  0  0  0  0    0  0  1  4  4  2  0  0  0  
  0  0  1  1  1  0  0  0  0    0  0  1  5  5  2  0  0  0    0  0  3 15 18  6  1  0  0  
  0  0  0  1  1  0  0  0  0    0  0  1  5  7  2  1  0  0    0  0  3 21 29  9  1  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  3  5  2  0  0  0    0  0  1 14 19  7  1  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  1  5  8  3  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  1  2  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0  
!Region 6: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  2  3  2  1  0  0    0  0  0  1  3  2  1  0  0  
  0  0  1  6  8  3  1  0  0    0  0  1  5 10  5  1  0  0    0  0  1  3  7  4  1  0  0  
  0  0  3 25 38 15  2  0  0    0  0  2 25 52 24  3  0  0    0  0  1 12 34 20  4  0  0  
  0  0  4 42 67 27  3  0  0    0  0  4 49100 47  6  0  0    0  0  2 27 74 41  6  1  0  
  0  0  3 28 47 20  2  0  0    0  0  3 33 70 34  4  0  0    0  0  2 18 51 29  4  0  0  
  0  0  1 10 18  9  1  0  0    0  0  1 10 25 13  2  0  0    0  0  0  4 15  9  1  0  0  
  0  0  0  3  5  2  1  0  0    0  0  0  2  6  4  1  0  0    0  0  0  1  3  2  0  0  0  
  0  0  0  1  1  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 6: Section 7->9
  0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  2  1  0  0    0  0  0  1  2  1  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  1  3  3  1  0  0    0  0  0  1  1  1  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  3 13 10  2  0  0    0  0  1  1  3  3  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  8 32 23  3  0  0    0  0  1  2  7  7  1  0  0    0  0  0  0  1  1  0  0  0  
  0  0  1  5 21 15  2  0  0    0  0  1  2  5  4  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  5  4  1  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 51.36   Thresh = 0.020   Blend = F   #Contributing = 750   InitialProfileWt = 0.000
Region 7
Sum = 11464.1;   Maximum = 702.863;   FM = 0.872
!Region 7: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  1  2  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  2  1  0  0  0    0  0  1  6 13  6  1  0  0  
  0  0  1  1  1  0  0  0  0    0  0  1  3  5  2  1  0  0    0  0  2 14 26 10  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  1  2  3  1  1  0  0    0  0  1 10 17  6  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0    0  0  1  3  6  3  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 7: Section 4->6
  0  0  0  0  1  1  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  1  2  2  1  0  0    0  0  0  0  1  1  1  0  0  
  0  0  0  2  5  4  1  0  0    0  0  0  2  7  6  1  0  0    0  0  0  1  6  5  1  0  0  
  0  0  1 12 32 18  2  0  0    0  0  1 15 52 31  4  0  0    0  0  1 10 45 29  3  0  0  
  0  0  3 31 65 27  3  0  0    0  0  2 39100 46  5  0  0    0  0  2 25 82 41  4  0  0  
  0  0  2 22 42 16  2  0  0    0  0  2 28 62 26  3  0  0    0  0  1 17 48 23  2  0  0  
  0  0  1  8 15  7  1  0  0    0  0  1 10 22 11  1  0  0    0  0  1  6 16  9  1  0  0  
  0  0  0  2  3  2  0  0  0    0  0  0  3  5  2  0  0  0    0  0  0  2  4  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  1  0  0  0  0    0  0  0  1  1  0  0  0  0  
!Region 7: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  2  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4 21 14  2  0  0    0  0  0  1  5  4  1  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  7 33 19  2  0  0    0  0  1  2  7  5  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  4 16 10  1  0  0    0  0  0  1  3  3  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  2  5  4  1  0  0    0  0  0  1  1  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 78.03   Thresh = 0.020   Blend = F   #Contributing = 364   InitialProfileWt = 0.000
Region 8
Sum = 20092.6;   Maximum = 1585.5;   FM = 0.825
!Region 8: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  3 13  6  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  2  5  2  0  0  0    0  0  1  8 27 11  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  3 13  7  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  1  2  2  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 8: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  4  2  0  0  0    0  0  0  1  6  3  0  0  0    0  0  0  1  5  2  0  0  0  
  0  0  0  8 34 14  1  0  0    0  0  1 16 53 18  1  0  0    0  0  1 17 46 12  1  0  0  
  0  0  1 21 66 24  1  0  0    0  0  2 39100 30  1  0  0    0  0  2 35 82 21  1  0  0  
  0  0  1 10 35 16  1  0  0    0  0  1 18 52 21  1  0  0    0  0  1 14 41 15  1  0  0  
  0  0  0  2  7  5  0  0  0    0  0  0  3 11  7  1  0  0    0  0  0  2  9  5  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  1  2  1  0  0  0    0  0  0  1  2  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0  
!Region 8: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  2  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0 10 21  4  0  0  0    0  0  0  2  4  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 16 34  7  0  0  0    0  0  0  3  7  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  5 16  6  0  0  0    0  0  0  1  3  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  4  2  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  1  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

I/Sigma = 164.41   Thresh = 0.020   Blend = F   #Contributing = 142   InitialProfileWt = 0.000
Region 9
Sum = 79405.5;   Maximum = 7028.67;   FM = 0.803
!Region 9: Section 1->3
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  2  1  0  0  0    0  0  0  2 13  6  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  1  4  2  0  0  0    0  0  0  4 23 12  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0    0  0  0  2  8  6  1  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  1  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 9: Section 4->6
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  1  0  0  0    0  0  0  1  4  1  0  0  0    0  0  0  1  2  1  0  0  0  
  0  0  0  7 34 13  1  0  0    0  0  0 16 48 13  1  0  0    0  0  0 17 35  6  0  0  0  
  0  0  0 18 65 26  1  0  0    0  0  1 40100 28  1  0  0    0  0  1 43 82 16  0  0  0  
  0  0  0  7 28 16  1  0  0    0  0  0 16 50 22  1  0  0    0  0  1 15 44 15  1  0  0  
  0  0  0  1  3  3  0  0  0    0  0  0  1  7  5  0  0  0    0  0  0  1  7  4  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  1  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
!Region 9: Section 7->9
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  9 12  1  0  0  0    0  0  0  2  2  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1 21 31  4  0  0  0    0  0  0  4  5  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  1  7 18  5  0  0  0    0  0  0  1  3  1  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  1  3  1  0  0  0    0  0  0  0  1  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  
  0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0    0  0  0  0  0  0  0  0  0  

Overall Integration Statistics for this run ("*" => excluded from output)

Spots with topped/rescanned pixels:             1
Total topped/rescanned pixels:                  1
Minimum pixel ceiling(frame):              163809(cu_BruecknerJK_153F40_01_0001.sfrm)
Maximum pixel ceiling(frame):              163809(cu_BruecknerJK_153F40_01_0001.sfrm)

Total spots predicted:                       6077
Spots with absolute HKL > 511:                  0*
Spots outside resolution limit:                 0*
Spots outside active detector area:          1003*
Outside frame limits:                          54*
Spots exceeding frame queue size:               0*
Collisions(same XY, adjacent frame):            0*
Spots exceeding dynamic range:                  0*
Spots with too many spot components:            0*
Spots with large Lorentz factor:                0*
Spots with too much missing I:                  0*
Spots with too few BG pixels:                   0*
Spots below I/sigma threshold:                  0*
Spots left in Write-Behind Cache:               0*
Spots with unwanted components:                 0*
Total unwanted components:                      0*
Good spots written:                          5011
Total spot components written:               5011
Twin overlaps integrated:                       0
Partial, strong, full overlaps:                 0       0       0
Full overlaps collapsed to singlet:             0
Singlets (used in stats below):              5011
Twin overlaps written:                          0

Average Intensity:                       57584.51
Average I/sigma:                           55.758
% over "strong" threshold:                  83.48
% less than 2 sigma:                         2.85
% which spanned more than 1 frame:          93.83

Average X,Y,Z positional errors:             0.05    0.12    0.01
RMS X,Y,Z positional errors:                 0.29    0.29    0.14
% X,Y,Z more than 0.5 pixel:                 5.81    6.65    0.74
% X,Y,Z more than 1.0 pixel:                 1.48    1.18    0.00

Avg % profile volume populated:             93.63
Avg % profile volume integrated:            11.05
Avg % profile missing I:                     6.15
Avg % profile missing volume:                6.37
Avg % volume overlap in H,K,L:               0.01    0.06    0.00
Percent of profile used in X,Y,Z:           66.67   77.78   88.89
Max % intensity on XYZ boundaries:           2.34    2.57    4.89

Average spot-shape correlation:             0.912
RMS spot-shape correlation:                 0.924

Profile Shape Correlation
I/sigma from     to    Correl       +/-       #
         0.0    1.0     0.219     0.183      74
         1.0    2.0     0.391     0.157      69
         2.0    4.0     0.627     0.138     163
         4.0    8.0     0.855     0.084     300
         8.0   16.0     0.937     0.067     735
        16.0   32.0     0.952     0.052    1319
        32.0   64.0     0.955     0.052    1631
        64.0  128.0     0.955     0.042     584
       128.0  256.0     0.942     0.053     136

Write-behind Cache Diagnostics
Entered in Write-Behind Cache:                  0
Removed from WBC:                               0
Partial overlaps from WBC:                      0
Exceeding queue size from WBC:                  0
With > 12 components from WBC:                  0

Elapsed since program start (sec):          8.827
Elapsed since INTEGRATE command (sec):      7.199
Integration time, this run (sec):           5.149
Time in unit-cell LS (sec):                 0.403
Per-frame integration time (sec):           0.009


Integration completed normally ======================== 01/23/2020 16:55:09


Applying profile correlation filter from d:\Frames\guest\BruecknerJK_153F40\work\unsorted.raw to d:\Frames\guest\BruecknerJK_153F40\work\corrfilt.raw
Scale of 1.0547342 will be applied to LS-fit intensities

Number of spots read:                         5011
Number of LS-fit intensities scaled:           649
Number rejected due to poor spot shape:         64
Number unwritable (I, sigma too large):          0
Number written:                               4947

Sorting Reflection File ============================== 01/23/2020 16:55:09
Integration of BruecknerJK_153F40

Sorting input files:
              1 corrfilt.raw

Sorting to output file cu_BruecknerJK_153F40_01.raw

Component 1 in sample 1 (1 in file):
Point group "mmm", #10 (internal number)
8 symmetry operators
    1 0 0   -1 0 0   -1 0 0    1 0 0   -1 0 0    1 0 0    1 0 0   -1 0 0
    0 1 0    0-1 0    0 1 0    0-1 0    0-1 0    0 1 0    0-1 0    0 1 0
    0 0 1    0 0 1    0 0-1    0 0-1    0 0-1    0 0-1    0 0 1    0 0 1

Beginning sort with 128MB memory requested...
      4947 spot components in 4947 spots read from file   1--d:\Frames\guest\BruecknerJK_153F40\work\corrfilt.raw
      4947 spot components in 4947 spots written to file d:\Frames\guest\BruecknerJK_153F40\work\cu_BruecknerJK_153F40_01.raw

Computing Reflection File Statistics ========== 01/23/2020 16:55:09
Integration of BruecknerJK_153F40

...................................................................................
Statistics for reflections in cu_BruecknerJK_153F40_01.raw
File is in BrukerAXS area detector ASCII format
File contains a single sample component

Number of lines read (incl comments) =             4947
Number of reflection records read =                4947
Number of records with bad component number =         0
Number of records with bad status value =             0
Number of spots used =                             4947
Number of spot components used =                   4947

...................................................................................
Integration of BruecknerJK_153F40
Statistics for sample 1 of 1 in cu_BruecknerJK_153F40_01.raw

Lattice:  P (Primitive)
Point group "mmm", #10 (internal number)
8 symmetry operators
    1 0 0   -1 0 0   -1 0 0    1 0 0   -1 0 0    1 0 0    1 0 0   -1 0 0
    0 1 0    0-1 0    0 1 0    0-1 0    0-1 0    0 1 0    0-1 0    0 1 0
    0 0 1    0 0 1    0 0-1    0 0-1    0 0-1    0 0-1    0 0 1    0 0 1


Component numbers S.C(F) below: S=sample, C=component in sample, F=component in file
Cell constants are constrained so that consistent sin(theta) is computed for symmetry equivalents.
Components in the sample map (* marks current component)
   Component   Wanted        A        B        C    Alpha     Beta    Gamma   PointGp         Constraints
     1.1(1)*        Y   19.641   36.938    4.753   90.000   90.000   90.000       mmm        Orthorhombic

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
     Det X      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    258     87    160    197  5.0 13800.665  18.91   19.01 0.067 -0.005  1.1 0.068 0.103  1.39 .44 .15-.06 .88 .48 .19
    32.000    376    128    203    328  9.0 16191.817  22.65   19.07 0.059  0.003  1.1 0.066 0.088  1.49 .09 .13-.02 .40 .36 .15
    64.000    438    127    204    393  5.3 27899.261  31.49   19.02 0.056 -0.001  1.4 0.060 0.076  1.09 .05 .16-.01 .32 .36 .14
    96.000    554    140    232    495  1.4 39470.244  37.50   19.13 0.052  0.000  1.5 0.055 0.065  1.09 .05 .14-.02 .22 .30 .13
   128.000    560    132    226    505  2.3 52919.404  44.85   19.46 0.051  0.001  1.7 0.056 0.060  0.96 .02 .13 .01 .17 .26 .13
   160.000    609    166    265    557  1.0 72310.512  56.40   19.53 0.050  0.001  2.0 0.058 0.062  0.87 .04 .12 .01 .15 .23 .13
   192.000    569    181    271    528  2.8 39503.372  41.81   19.38 0.042 -0.000  1.5 0.049 0.037  0.59 .02 .10 .03 .11 .23 .13
   224.000    494    179    249    474  2.8 43242.968  47.51   19.37 0.043  0.003  1.6 0.050 0.037  0.63 .04 .09 .02 .11 .22 .13
   256.000    416    169    226    403  2.6 55870.733  59.91   19.40 0.042 -0.000  2.0 0.052 0.031  0.58 .03 .07 .03 .10 .18 .13
   288.000    314    138    186    295  1.0 122187.73  98.73   19.55 0.051  0.001  3.5 0.066 0.057  0.63 .02 .06 .03 .12 .15 .13
   320.000    193     96    132    174  0.5 187563.63 131.78   19.64 0.056 -0.001  7.4 0.070 0.059  0.74-.06 .04 .04 .26 .14 .15
   352.000    166     64    108    139  0.6 157472.75 124.32   19.50 0.055 -0.004  5.4 0.073 0.064  0.74-.08 .03 .04 .18 .12 .16
   384.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   416.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   448.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   480.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   512.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
     Det Y      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    116     50    115     51  1.7 37827.931  36.32   19.02 0.069 -0.009  2.0 0.089 0.053  0.52 .19 .51-.15 .56 .86 .24
    32.000    195     78    188     85  1.0 41505.140  45.28   19.01 0.054  0.003  2.2 0.066 0.062  0.62 .09 .26-.06 .33 .48 .17
    64.000    214    115    200    129  0.5 52788.844  53.50   19.07 0.043  0.019  2.1 0.070 0.054  0.85 .08 .16-.06 .31 .35 .15
    96.000    255    224    243    238  2.0 59814.936  58.87   19.30 0.074 -0.017  3.2 0.114 0.053  0.60 .04 .11-.04 .26 .23 .13
   128.000    348    298    323    323  0.9 56799.770  53.77   19.33 0.048 -0.020  2.0 0.094 0.041  0.46 .02 .09-.03 .23 .18 .11
   160.000    415    360    384    392  2.4 49520.703  47.91   19.35 0.028 -0.003  1.1 0.041 0.048  0.82 .05 .10-.02 .25 .18 .11
   192.000    509    439    471    481  2.4 70874.563  64.78   19.47 0.067  0.019  3.0 0.075 0.065  0.76 .04 .10 .00 .31 .17 .10
   224.000    499    330    443    482  2.0 61537.892  58.06   19.60 0.044  0.002  1.7 0.039 0.045  0.75 .02 .06 .01 .22 .11 .10
   256.000    450    294    438    428  3.1 60340.206  54.42   19.54 0.044  0.012  1.5 0.039 0.065  0.93 .05 .07 .02 .27 .15 .12
   288.000    530    259    466    491  5.5 72819.298  71.54   19.45 0.055  0.003  2.4 0.085 0.072  0.67 .03 .04 .04 .28 .11 .13
   320.000    372    162    357    354  4.3 60218.301  55.77   19.37 0.023 -0.008  1.0 0.039 0.073  1.45 .03 .09 .05 .20 .17 .15
   352.000    276    190    273    272  6.2 44775.060  46.28   19.15 0.059  0.021  1.9 0.062 0.043  0.58 .06 .08 .03 .35 .23 .14
   384.000    301    246    277    296  4.0 52073.197  53.51   19.11 0.054  0.002  2.1 0.046 0.044  0.56 .08 .10 .03 .29 .23 .14
   416.000    244    239    240    243  0.8 55903.245  55.40   19.11 0.049 -0.024  2.1 0.037 0.048  0.77 .04 .21 .12 .21 .32 .21
   448.000    137    134    135    137  2.9 42362.858  42.77   19.04 0.071 -0.059  4.4 0.058 0.042  0.56 .04 .26 .08 .38 .50 .19
   480.000     86     85     86     86  4.7 40002.453  40.67   19.19 0.056 -0.029  1.8 0.050 0.053  0.77 .18 .04 .02 .40 .62 .19
   512.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
     Det R      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    131     79    129    130  2.3 55073.122  56.30   19.71 0.030  0.008  1.4 0.032 0.021  0.55 .02 .05 .04 .08 .10 .10
    30.000    392    178    274    378  4.1 57685.312  59.18   19.62 0.056  0.009  2.4 0.064 0.032  0.52 .01 .04 .03 .09 .09 .10
    60.000    541    200    391    516  3.1 101512.57  84.39   19.63 0.049  0.003  2.5 0.056 0.057  0.73 .01 .05 .04 .15 .11 .12
    90.000    695    413    550    661  1.2 79557.559  66.50   19.58 0.043  0.009  2.0 0.055 0.059  0.83 .01 .07 .02 .13 .14 .12
   120.000    733    425    529    705  1.1 66678.732  58.07   19.41 0.051 -0.002  2.2 0.067 0.054  0.73 .02 .09 .00 .15 .15 .11
   150.000    694    455    538    667  2.4 48672.841  47.96   19.19 0.050 -0.005  1.8 0.057 0.045  0.67 .03 .10 .01 .18 .19 .14
   180.000    569    354    427    545  3.2 48114.068  49.83   19.13 0.056 -0.002  2.0 0.056 0.053  0.78 .03 .15 .02 .24 .25 .16
   210.000    545    277    436    424  5.0 33871.622  38.79   19.08 0.056 -0.015  2.3 0.060 0.052  0.70 .03 .15-.01 .31 .31 .15
   240.000    418    202    340    303  4.5 28019.816  32.51   19.03 0.061 -0.019  1.5 0.061 0.056  0.71 .20 .21-.05 .55 .43 .17
   270.000    229    110    188    159  4.4 21634.151  25.44   18.96 0.075 -0.005  1.6 0.067 0.073  0.85 .32 .27-.06 .74 .77 .21
   300.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   Quadrnt      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     1.000   1906    702   1028   1849  4.5 43405.003  43.41   19.27 0.046 -0.003  1.5 0.048 0.065  0.92 .06 .11 .03 .30 .27 .14
     2.000    490    233    358    458  2.7 114969.09 100.42   19.45 0.052 -0.000  4.2 0.059 0.063  0.68-.00 .04 .09 .20 .14 .17
     3.000   1952    909   1298   1628  2.2 40223.650  40.23   19.29 0.053  0.004  1.6 0.064 0.058  0.90 .07 .14-.03 .32 .32 .13
     4.000    599    270    353    553  0.5 112879.09  96.52   19.54 0.051 -0.002  3.6 0.070 0.055  0.65-.01 .07-.01 .11 .17 .11
     5.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
    Region      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     1.000   1130    350    588   1087  3.3 80854.509  73.32   19.63 0.049  0.006  2.3 0.056 0.050  0.69 .01 .05 .03 .12 .11 .11
     2.000     41      6     30     30  2.4 185642.14 136.02   19.64 0.056 -0.004  5.9 0.089 0.153  0.96-.14 .02 .05 .17 .08 .12
     3.000    107     71     91    102  0.0 152317.50 118.26   19.37 0.060 -0.002  5.9 0.059 0.056  0.66-.04 .00 .11 .18 .11 .20
     4.000    385    319    320    385  1.6 50078.261  52.18   19.18 0.047 -0.018  2.7 0.040 0.038  0.60 .07 .18 .10 .18 .29 .18
     5.000    871    462    675    847  4.7 44515.612  43.28   19.19 0.044 -0.009  1.4 0.050 0.071  1.01 .06 .12 .02 .33 .34 .15
     6.000    898    430    590    845  4.2 31440.832  33.71   19.24 0.058  0.016  1.4 0.053 0.073  1.12 .10 .10-.01 .41 .18 .12
     7.000    912    462    676    698  1.9 40293.381  38.91   19.24 0.052 -0.001  1.6 0.077 0.051  0.65 .08 .19-.04 .35 .40 .14
     8.000    434    210    297    347  0.7 52430.113  54.68   19.20 0.046  0.002  2.1 0.077 0.046  0.58 .02 .11-.05 .12 .32 .14
     9.000    169     89    115    147  0.0 142791.15 112.05   19.58 0.052 -0.010  4.8 0.091 0.048  0.53-.02 .08-.03 .15 .15 .12
    10.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
    Frame#      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     2.530    261    236    237    260  2.7 75322.002  64.18   19.46 0.096  0.095  4.1 0.086 0.076  0.76 .04-.02-.01 .26 .23 .11
    27.628    249    207    208    249  2.8 64292.947  57.82   19.39 0.097  0.096  4.0 0.091 0.069  0.69 .04 .06-.00 .26 .15 .09
    52.725    241    157    190    221  2.5 57984.662  58.85   19.39 0.049  0.044  1.8 0.063 0.050  0.60 .03 .07-.01 .30 .19 .12
    77.823    241    151    185    226  1.2 61921.513  57.38   19.39 0.034  0.025  1.5 0.049 0.065  0.84 .01 .11-.01 .23 .19 .11
   102.920    224    152    189    213  1.3 54633.456  51.23   19.40 0.032  0.012  1.3 0.040 0.060  0.76 .04 .06-.02 .27 .18 .09
   128.018    255    166    237    216  3.1 64957.853  59.91   19.33 0.032  0.006  1.4 0.036 0.058  0.74 .05 .09-.02 .31 .33 .13
   153.115    208    125    206    165  4.8 66103.027  60.71   19.34 0.044  0.019  1.9 0.043 0.049  0.84 .06 .43 .16 .25 .56 .25
   178.213    254    149    251    198  3.5 57696.719  54.62   19.34 0.029  0.001  1.2 0.026 0.044  1.22 .09 .24 .08 .27 .37 .18
   203.310    258    153    258    208  2.7 51506.231  51.60   19.29 0.025 -0.007  1.1 0.027 0.036  0.82 .11 .08 .03 .31 .25 .19
   228.408    251    143    251    195  2.4 41935.106  46.07   19.28 0.024 -0.006  0.9 0.022 0.034  0.67 .09 .03 .01 .29 .22 .16
   253.505    264    143    255    203  3.8 59863.686  56.51   19.32 0.019 -0.009  1.0 0.024 0.026  0.70 .10 .10 .01 .24 .23 .13
   278.603    267    162    252    225  3.7 55851.077  56.03   19.28 0.023 -0.006  1.0 0.032 0.028  0.60 .06 .08 .01 .32 .24 .14
   303.700    247    155    230    225  3.2 43478.060  45.72   19.27 0.027  0.012  1.0 0.027 0.037  1.16 .05 .14-.01 .38 .36 .14
   328.798    239    170    237    231  1.3 63826.296  59.93   19.31 0.027 -0.003  1.1 0.039 0.040  0.72 .05 .11-.02 .21 .26 .11
   353.895    237    170    237    230  3.4 49440.773  51.99   19.32 0.030 -0.005  1.3 0.023 0.041  0.89 .04 .09-.02 .27 .18 .12
   378.993    236    173    236    229  3.0 51962.728  51.66   19.37 0.027 -0.005  1.0 0.033 0.033  0.71 .04 .09-.01 .28 .19 .11
   404.090    263    190    260    252  2.3 67678.442  60.34   19.32 0.043 -0.034  1.7 0.047 0.047  0.80 .05 .14-.01 .32 .26 .12
   429.188    255    198    249    246  3.5 50363.556  54.37   19.26 0.056 -0.050  3.3 0.076 0.054  0.65 .01 .14 .01 .30 .28 .13
   454.285    261    233    236    260  2.7 63582.960  59.04   19.25 0.105 -0.104  4.2 0.088 0.092  0.78 .01 .14 .01 .31 .33 .13
   479.383    236    202    202    236  3.8 49499.655  50.44   19.32 0.133 -0.132  5.0 0.123 0.088  0.70 .02 .08 .01 .28 .18 .11
   504.480

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   Rot.Ang      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    252    159    235    223  2.4 43285.906  46.76   19.27 0.029  0.002  1.1 0.030 0.039  0.99 .03 .11 .00 .29 .27 .13
    10.000    247    173    241    235  2.8 57681.974  56.60   19.28 0.027  0.002  1.1 0.038 0.039  0.78 .07 .13-.03 .35 .36 .13
    20.000    231    165    231    224  2.2 54317.825  54.10   19.33 0.031 -0.005  1.3 0.030 0.043  0.76 .03 .10-.01 .25 .19 .12
    30.000    244    176    244    240  2.9 52996.223  52.23   19.34 0.024 -0.001  1.0 0.024 0.029  0.75 .04 .10-.02 .27 .19 .10
    40.000    251    182    250    238  1.6 59274.043  54.19   19.34 0.033 -0.021  1.4 0.041 0.043  0.80 .05 .13-.01 .30 .24 .12
    50.000    258    196    252    249  4.3 56381.729  58.68   19.27 0.052 -0.046  2.0 0.064 0.058  0.77 .03 .12-.00 .28 .25 .13
    60.000    258    220    242    254  3.5 59784.086  58.83   19.24 0.095 -0.093  4.6 0.086 0.084  0.70 .02 .14 .00 .35 .36 .13
    70.000    244    209    209    244  2.9 53796.654  52.79   19.30 0.113 -0.112  4.5 0.111 0.068  0.61-.00 .09 .02 .29 .19 .13
    80.000     90     88     88     90  4.4 52908.428  52.93   19.36 0.138 -0.138  5.5 0.122 0.107  0.82 .03 .08 .02 .26 .17 .11
    90.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   100.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   110.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   120.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   130.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   140.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   150.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   160.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   170.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   180.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   190.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   200.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   210.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   220.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   230.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   240.000    186    184    184    186  2.7 77906.519  66.56   19.47 0.093  0.092  4.0 0.082 0.077  0.75 .04-.02-.02 .28 .23 .11
   250.000    250    212    214    249  2.8 65361.291  57.93   19.41 0.101  0.100  4.2 0.094 0.059  0.60 .03 .03-.00 .24 .17 .09
   260.000    242    179    198    231  2.9 61825.448  59.87   19.40 0.065  0.061  2.4 0.075 0.070  0.81 .03 .07-.00 .27 .16 .11
   270.000    231    144    180    211  1.3 56785.729  55.99   19.38 0.039  0.031  1.6 0.051 0.050  0.67 .03 .11-.01 .29 .22 .13
   280.000    238    159    194    227  1.3 60058.767  54.21   19.39 0.029  0.016  1.3 0.044 0.071  0.88 .04 .07-.02 .26 .18 .09
   290.000    243    158    220    214  3.3 62268.065  58.47   19.34 0.032  0.003  1.4 0.032 0.061  0.80 .02 .10-.02 .23 .27 .11
   300.000    203    124    195    163  4.4 65743.797  60.60   19.35 0.047  0.021  1.9 0.050 0.057  0.76 .07 .29 .08 .34 .52 .22
   310.000    256    154    253    202  2.7 57841.778  54.46   19.33 0.027  0.008  1.2 0.025 0.045  1.19 .08 .33 .12 .25 .43 .20
   320.000    253    150    253    200  4.0 56305.206  54.23   19.32 0.027 -0.007  1.2 0.028 0.035  0.85 .10 .11 .04 .28 .30 .19
   330.000    260    151    260    208  1.9 45194.476  48.19   19.28 0.025 -0.008  1.0 0.026 0.037  0.72 .11 .04 .01 .30 .21 .16
   340.000    261    148    259    200  4.2 49565.538  50.82   19.30 0.021 -0.007  0.9 0.022 0.025  0.66 .09 .08 .00 .27 .22 .14
   350.000    249    138    237    200  3.2 65879.651  60.44   19.32 0.019 -0.006  1.0 0.029 0.023  0.57 .10 .09 .00 .30 .25 .14
   360.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
     Hours      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    367    304    306    366  2.7 72598.445  62.87   19.45 0.096  0.095  4.1 0.088 0.075  0.76 .04 .00-.01 .28 .21 .11
     0.050    409    271    307    387  2.4 60073.198  58.17   19.39 0.068  0.064  2.6 0.077 0.065  0.72 .03 .07-.00 .27 .17 .11
     0.100    407    245    308    383  1.5 58115.864  54.17   19.39 0.031  0.018  1.4 0.044 0.067  0.87 .03 .09-.02 .26 .19 .10
     0.150    379    230    343    319  4.0 62792.926  59.30   19.33 0.040  0.012  1.6 0.042 0.061  0.79 .05 .17 .02 .30 .40 .16
     0.200    430    234    402    343  3.7 60728.280  56.10   19.34 0.029  0.003  1.3 0.027 0.041  1.07 .08 .27 .11 .26 .41 .21
     0.250    441    234    421    347  2.0 46716.409  49.03   19.28 0.024 -0.006  1.0 0.024 0.033  0.73 .10 .05 .01 .30 .23 .17
     0.300    540    260    458    434  3.7 57263.236  55.93   19.30 0.021 -0.008  1.0 0.028 0.029  0.67 .08 .10 .01 .28 .23 .14
     0.350    333    203    300    308  3.0 50952.567  51.92   19.27 0.028  0.005  1.1 0.035 0.041  0.92 .06 .13-.02 .35 .36 .13
     0.400    484    303    437    472  2.3 51392.529  52.10   19.33 0.027 -0.003  1.1 0.027 0.038  0.74 .04 .10-.02 .26 .19 .11
     0.450    333    225    316    317  1.5 68149.658  60.61   19.36 0.037 -0.023  1.5 0.040 0.041  0.75 .04 .12-.01 .27 .23 .11
     0.500    462    335    405    450  4.3 51806.997  54.07   19.24 0.072 -0.067  3.2 0.077 0.070  0.74 .03 .14-.00 .31 .29 .13
     0.550    362    293    293    362  3.0 56418.738  54.51   19.31 0.119 -0.119  4.8 0.110 0.092  0.76 .01 .09 .02 .29 .24 .12
     0.600      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.650      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.700      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.750      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.800      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.850      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.900      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.950      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     1.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
    Batch#      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     1.000   4947   1181   1998   4488  2.9 57650.279  55.72   19.33 0.050 -0.000  2.1 0.059 0.058  0.80 .05 .11 .01 .29 .27 .14
     2.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
    Correl      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000     34      9     26     28100.0   -21.569  -0.09   19.2913.268-86.995 12.115.42923.471  0.59-.02-.08 .03 .61 .48 .24
     0.100     21      9     19     18100.0   259.075   0.97   19.17 0.589 -0.054  0.6 0.479 1.315  1.71 .19 .06-.06 .48 .44 .21
     0.200     30     14     27     27 96.7   267.437   0.99   19.14 0.539 -0.146  0.6 0.442 0.787  1.10 .02 .01-.03 .46 .48 .22
     0.300     37     19     35     27 75.7   433.842   1.56   19.22 0.395 -0.215  0.7 0.379 0.596  1.11 .17-.04-.02 .63 .37 .24
     0.400     41     22     37     39 39.0   674.682   2.41   19.19 0.255  0.026  0.6 0.284 0.335  0.49 .00 .07 .00 .60 .28 .20
     0.500     46     22     41     41 19.6   784.237   2.74   19.24 0.267 -0.022  0.7 0.220 0.518  1.88 .11-.01-.00 .64 .27 .22
     0.600     71     27     57     64  5.6  1070.172   3.40   19.21 0.176 -0.029  0.6 0.199 0.216  1.16 .13-.01-.02 .66 .32 .21
     0.700     76     35     65     64  2.6  2479.624   7.16   19.26 0.147  0.084  0.7 0.134 0.158  1.04 .03 .10 .01 .39 .29 .20
     0.800    399    204    322    353  0.0 42332.742  55.86   19.39 0.054  0.016  1.8 0.052 0.068  0.89 .07 .13 .03 .37 .36 .19
     0.900   4192   1087   1737   3827  0.0 63918.943  56.88   19.33 0.050 -0.001  2.1 0.059 0.058  0.80 .05 .12 .01 .24 .26 .12
     1.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   Missing      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000   4389   1144   1850   4037  2.7 58328.740  56.92   19.34 0.049  0.001  2.0 0.058 0.058  0.80 .03 .10 .01 .22 .24 .13
     0.050    122     75    109     96  4.9 38779.115  42.11   19.23 0.065  0.002  1.6 0.070 0.047  0.51 .22 .14-.04 .52 .35 .16
     0.100     56     39     54     45  0.0 53347.129  53.04   19.32 0.044  0.007  1.9 0.069 0.057  0.66 .11 .25-.04 .43 .60 .18
     0.150     70     46     63     61  2.9 80110.490  71.67   19.26 0.052  0.002  2.8 0.073 0.046  0.60 .10 .09 .01 .35 .33 .14
     0.200     88     62     85     71  6.8 50478.090  46.44   19.24 0.071 -0.028  6.2 0.081 0.065  0.68 .16 .13-.04 .66 .51 .21
     0.250     44     32     44     35  6.8 34859.205  39.99   19.29 0.046 -0.016  1.6 0.049 0.049  0.85 .27 .11-.04 .79 .39 .20
     0.300     18     12     17     15 16.7 39718.987  36.03   19.21 0.065 -0.011  1.9 0.053 0.061  0.97 .31 .25-.06 .65 .77 .20
     0.350     37     30     37     32  0.0 46424.400  40.89   19.33 0.070  0.044  2.0 0.062 0.047  0.55 .16 .13-.02 .60 .30 .15
     0.400     38     27     38     30  2.6 72730.801  52.39   19.38 0.065 -0.033  1.9 0.072 0.033  0.38 .14 .13-.03 .40 .36 .11
     0.450     28     17     27     22  0.0 27925.877  23.29   19.10 0.086  0.004  1.4 0.092 0.057  0.42 .49 .14-.11 .85 .44 .20
     0.500     28     15     27     21 10.7 39857.108  31.76   19.16 0.071 -0.027  1.3 0.054 0.049  0.76 .11 .29 .05 .52 .52 .19
     0.550     29     18     29     23  3.4 96367.067  49.05   19.26 0.072 -0.023  2.4 0.062 0.074  0.73 .29 .44-.06 .91 .83 .24
     0.600      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.650      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.700      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.750      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.800      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.850      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.900      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.950      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     1.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
    Frac Z      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    292    195    275    267  2.7 43165.679  48.55   19.31 0.061  0.012  2.0 0.070 0.070  0.74 .04 .09 .00 .23 .20 .12
     0.050    226    149    215    202  3.5 58393.034  55.84   19.35 0.047 -0.001  1.8 0.064 0.043  0.55 .06 .11 .01 .33 .24 .13
     0.100    242    178    232    222  2.9 60662.369  57.23   19.32 0.049 -0.001  2.0 0.058 0.047  0.69 .06 .11 .01 .30 .26 .13
     0.150    161    118    159    149  1.9 61798.790  57.11   19.32 0.044  0.005  1.8 0.063 0.057  0.74 .03 .12 .02 .29 .29 .14
     0.200    190    145    183    173  1.1 64658.597  56.77   19.33 0.054 -0.015  2.4 0.060 0.065  0.85 .06 .11 .02 .30 .23 .12
     0.250    235    163    223    210  5.1 63681.759  58.95   19.38 0.053  0.013  2.1 0.062 0.059  0.81 .05 .07 .02 .31 .25 .13
     0.300    215    158    206    196  2.8 77513.862  68.44   19.33 0.048  0.019  2.3 0.048 0.046  0.63 .06 .11 .02 .39 .33 .15
     0.350    301    209    287    271  2.0 49756.282  49.68   19.34 0.051 -0.008  1.8 0.053 0.049  0.63 .06 .12 .02 .31 .30 .15
     0.400    257    196    249    235  3.9 54181.900  55.07   19.32 0.043 -0.001  1.9 0.051 0.057  0.87 .05 .10 .00 .27 .27 .14
     0.450    293    218    281    258  4.8 56454.974  57.42   19.31 0.046 -0.015  1.8 0.059 0.048  0.74 .07 .12-.02 .28 .23 .14
     0.500    344    248    325    313  1.5 58244.979  57.97   19.33 0.060 -0.002  2.2 0.065 0.061  0.74 .03 .14 .00 .24 .31 .14
     0.550    288    209    268    266  2.8 48166.707  49.49   19.33 0.051  0.009  1.8 0.063 0.044  0.61 .05 .10-.00 .25 .22 .13
     0.600    302    217    276    279  2.6 49693.125  50.32   19.33 0.039  0.000  1.5 0.043 0.047  0.85 .03 .09 .02 .23 .27 .16
     0.650    197    143    192    184  2.5 69760.047  60.30   19.38 0.052 -0.003  2.4 0.071 0.061  0.74 .07 .10 .01 .33 .38 .15
     0.700    191    142    183    172  3.1 69085.773  59.43   19.37 0.049 -0.005  2.2 0.063 0.056  0.78 .05 .17 .01 .33 .33 .15
     0.750    245    182    228    226  0.8 71323.867  60.74   19.36 0.051  0.001  2.4 0.055 0.057  0.68 .05 .16 .01 .26 .33 .13
     0.800    197    140    187    176  2.5 67444.571  60.27   19.34 0.039  0.006  2.0 0.053 0.040  0.53 .05 .11 .01 .27 .20 .13
     0.850    270    190    255    244  2.6 63354.372  59.76   19.32 0.050 -0.014  3.5 0.058 0.047  0.69 .06 .10 .01 .33 .27 .15
     0.900    239    165    228    210  2.5 41507.053  44.37   19.27 0.057  0.003  1.8 0.061 0.059  0.63 .04 .12 .01 .25 .24 .13
     0.950    262    177    247    235  5.7 44907.588  48.27   19.30 0.060 -0.001  2.0 0.067 0.062  0.76 .03 .10-.01 .23 .25 .13
     1.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   PeakCts      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
   786.078      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
  1572.156      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
  3144.313      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
  6288.625      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
 12577.250    978    423    626    948  5.7 19647.897  27.94   19.51 0.049  0.007  1.2 0.051 0.044  0.67 .02 .05 .02 .18 .12 .12
 25154.500   2556   1008   1402   2422  2.5 46202.589  45.16   19.33 0.047  0.003  1.7 0.057 0.057  0.88 .04 .09 .01 .27 .18 .12
 50309.000   1254    612    924    987  1.6 82358.921  68.99   19.20 0.056 -0.004  3.4 0.066 0.050  0.67 .07 .19 .01 .34 .40 .17
100618.000    149     82    120    122  1.3 243330.48 128.00   19.32 0.042 -0.003  4.5 0.046 0.050  0.59 .13 .23-.03 .50 .66 .20
201236.000     10      6      9      9  0.0 835213.93 234.82   19.64 0.069  0.012 14.3 0.056 0.061  0.65 .07 .14 .16 .16 .23 .30
402472.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   BgndCts      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     2.052      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     4.104      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     6.156      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     8.208      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    10.260      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    12.311      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    14.363      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    16.415      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    18.467   4947   1181   1998   4488  2.9 57650.279  55.72   19.33 0.050 -0.000  2.1 0.059 0.058  0.80 .05 .11 .01 .29 .27 .14
    20.519

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
      ErrX      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
    -1.500      2      2      2      2 50.0   447.100   1.46   18.9844.297-66.401158.6208.49828.739  0.58-2.0-.35 .40 2.0 .41 .41
    -1.380      1      1      1      1100.0   111.170   0.40   19.06 2.109 -2.109  0.8 1.498 1.833  0.87-1.3 .16 .48 1.3 .16 .48
    -1.260      1      1      1      1  0.0  7728.400  12.43   19.10 0.081 -0.081  1.0 0.076 0.008  0.05-1.1-.49 .35 1.1 .49 .35
    -1.140      6      3      6      4 16.7  4466.835  10.59   19.32 0.269 -0.181  2.5 0.189 0.218  0.82-1.1 .14 .32 1.1 .53 .39
    -1.020      4      3      4      4 25.0  1110.225   3.73   19.16 0.302  0.181  1.2 0.270 0.216  0.25-.97-.03 .15 .97 .33 .29
    -0.900     13      9     13     10 23.1  4941.258  11.28   19.20 0.142  0.007  0.7 0.236 0.200  1.43-.82-.03 .35 .82 .54 .37
    -0.780     17     11     17     13 17.6  7676.305  14.64   19.10 0.458 -0.397  5.3 0.098 0.656 12.52-.72 .05 .25 .72 .38 .30
    -0.660     31     20     31     26  3.2  7622.411  14.21   19.07 0.083 -0.009  1.2 0.088 0.077  0.56-.59 .09 .23 .59 .49 .27
    -0.540     47     31     45     44 17.0  9719.117  19.28   19.08 0.071  0.018  0.9 0.059 0.057  0.61-.48 .04 .24 .48 .31 .26
    -0.420     93     64     88     84 10.8 20920.459  35.38   19.21 0.080 -0.029  1.4 0.098 0.128  0.88-.35 .05 .16 .35 .23 .20
    -0.300    203    123    189    171  6.9 37270.862  48.61   19.25 0.034 -0.006  1.2 0.040 0.049  0.64-.23 .14 .13 .23 .33 .17
    -0.180    663    381    535    596  2.0 72550.013  69.28   19.37 0.053 -0.007  2.4 0.059 0.066  0.87-.11 .09 .06 .11 .21 .11
    -0.060   2028    835   1180   1907  0.9 76187.152  62.70   19.42 0.053  0.003  2.5 0.064 0.058  0.78 .00 .10 .02 .03 .17 .09
     0.060   1082    607    830    999  1.2 51375.307  49.10   19.31 0.040  0.002  1.6 0.046 0.044  0.69 .11 .13-.01 .12 .23 .13
     0.180    332    216    302    301  5.1 29794.395  36.19   19.21 0.047  0.005  1.2 0.049 0.052  0.81 .23 .14-.07 .23 .29 .16
     0.300    173    113    165    136  6.9 22977.408  32.15   19.15 0.037 -0.016  0.9 0.029 0.046  1.13 .35 .15-.12 .35 .33 .19
     0.420     76     42     72     57 11.8 12326.227  19.72   19.07 0.087 -0.007  1.2 0.097 0.115  1.20 .47 .21-.16 .47 .45 .20
     0.540     63     38     61     48 12.7 10255.475  16.69   19.09 0.046  0.000  0.6 0.070 0.052  0.63 .60 .11-.21 .60 .51 .23
     0.660     27     18     26     23  3.7 11489.094  17.89   19.04 0.065  0.003  1.0 0.069 0.122  1.63 .72 .18-.21 .72 .75 .25
     0.780     19     14     19     15 10.5  9809.815  16.05   19.02 0.053 -0.031  0.8 0.059 0.069  0.79 .84-.04-.26 .84 .59 .29
     0.900      8      3      8      5  0.0 14140.512  18.13   18.95 0.031  0.005  0.5 0.000 0.080  0.00 .97 .14-.14 .97 .49 .15
     1.020      7      3      7      3 14.3 18955.911  20.25   18.92 0.051 -0.003  0.8 0.056 0.059  0.77 1.1 .58-.24 1.1 1.1 .27
     1.140      8      6      8      6 25.0  8198.758  13.01   18.94 0.126  0.073  1.4 0.172 0.061  0.31 1.2 .07-.32 1.2 1.1 .36
     1.260      6      3      6      3  0.0 12585.816  17.46   19.03 0.095 -0.037  0.9 0.109 0.009  0.07 1.3 .57-.30 1.3 .85 .33
     1.380     37     20     30     29 10.8  6135.739   9.86   19.09 0.092  0.017  0.7 0.163 0.142  0.59 2.0 .29-.36 2.0 1.2 .39
     1.500

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
      ErrY      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
    -1.500      4      4      4      4 50.0  5541.578   8.70   19.25 0.234  0.010  1.9 0.236 0.146  0.67 1.4-2.0-.48 1.5 2.1 .49
    -1.380      1      0      1      1  0.0   981.582   2.49   18.82 0.390  0.390  1.0 0.000 0.000  0.00 2.6-1.3-.61 2.6 1.3 .61
    -1.260      3      3      3      3  0.0  4287.933   7.39   19.19 0.075 -0.005  0.6 0.034 0.091  1.08 1.0-1.2-.26 1.2 1.2 .28
    -1.140      1      1      1      1  0.0  4145.900   7.19   19.26 0.030 -0.030  0.2 0.054 0.209  3.50 .86-1.1-.35 .86 1.1 .35
    -1.020      2      0      2      0  0.0  7666.450  13.64   19.16 0.000  0.000  0.0 0.000 0.000  0.00-.65-.98 .49 .67 .98 .49
    -0.900      2      2      2      2  0.0  2794.300   6.02   18.99 0.170  0.048  1.0 0.068 0.248  0.73 1.6-.80-.33 1.8 .80 .34
    -0.780     10      8     10      8  0.0  7833.751  12.53   19.04 0.099  0.007  1.3 0.106 0.078  0.86 .37-.72-.05 1.0 .72 .28
    -0.660     13     10     13     11 15.4  9202.961  15.92   19.11 0.626 -0.483 29.9 0.520 0.381  0.56-.13-.61 .13 .94 .61 .33
    -0.540     25     16     25     21 32.0  5542.896  11.27   18.99 0.081 -0.006  0.8 0.086 0.052  0.47 .27-.48-.11 .63 .48 .27
    -0.420     35     21     35     29 17.1  7335.521  14.21   19.08 0.103 -0.001  1.0 0.100 0.085  0.71 .25-.35-.05 .72 .35 .25
    -0.300    124     76    117    103 13.7 11719.944  21.56   19.17 0.078  0.007  1.1 0.079 0.061  0.61 .05-.23-.00 .49 .23 .19
    -0.180    353    243    326    324  6.2 37230.034  51.86   19.29 0.046  0.009  1.6 0.058 0.064  0.73 .04-.11 .01 .30 .11 .15
    -0.060   1555    778   1090   1453  2.2 68668.765  64.93   19.45 0.051  0.011  2.2 0.061 0.056  0.80 .02 .01 .01 .16 .04 .10
     0.060   1606    772   1068   1509  1.7 65197.208  57.58   19.38 0.051 -0.004  2.2 0.063 0.060  0.79 .03 .11-.00 .16 .12 .09
     0.180    571    392    505    517  1.4 45649.124  44.09   19.21 0.047 -0.013  1.7 0.048 0.049  0.73 .05 .23 .02 .23 .23 .14
     0.300    296    214    272    264  2.0 52595.648  48.52   19.20 0.047 -0.010  1.7 0.049 0.044  0.61 .06 .35 .06 .30 .35 .18
     0.420    139     94    133    111  2.2 56616.203  51.18   19.14 0.042 -0.017  1.6 0.041 0.042  0.78 .12 .48 .05 .44 .48 .22
     0.540     75     42     73     49  2.7 47225.176  45.01   19.13 0.032 -0.002  1.4 0.034 0.047  0.97 .14 .60 .04 .34 .60 .25
     0.660     45     28     45     30  4.4 36877.047  37.11   19.04 0.050 -0.027  1.6 0.056 0.076  1.28 .19 .71 .04 .59 .71 .28
     0.780     25     12     25     12  0.0 54926.800  45.50   19.05 0.045 -0.021  1.7 0.031 0.042  1.05 .08 .83 .07 .31 .83 .22
     0.900     25     17     25     17  4.0 57586.800  48.97   19.04 0.051 -0.023  2.1 0.032 0.048  1.18 .48 .94 .03 .91 .94 .35
     1.020      7      3      7      3  0.0 60955.701  45.51   18.98 0.010 -0.003  0.5 0.012 0.040  2.25 .25 1.1-.03 .43 1.1 .24
     1.140      5      3      5      3  0.0 19911.300  23.11   18.96 0.056  0.021  0.8 0.000 0.112  0.00 .88 1.2-.29 1.1 1.2 .32
     1.260      5      3      5      3  0.0 22195.019  28.42   18.92 0.080 -0.021  1.1 0.119 0.107  0.78 .62 1.3-.34 .78 1.3 .38
     1.380     20     10     20     10 10.0 15220.279  17.87   18.97 0.082 -0.010  1.1 0.116 0.091  0.40 .94 1.9-.30 1.4 1.9 .44
     1.500

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
      ErrZ      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
    -1.500      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -1.380      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -1.260      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -1.140      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -1.020      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -0.900      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    -0.780      1      0      1      0  0.0 10270.900   9.42   19.00 0.000  0.000  0.0 0.000 0.000  0.00 3.6 2.9-.66 3.6 2.9 .66
    -0.660      5      2      5      3 40.0   629.412   1.74   19.18 0.659 -0.032  0.8 1.571 0.342  0.14 1.5 .11-.58 1.7 1.9 .58
    -0.540     21     13     21     14 14.3 11458.696  18.19   19.02 0.097 -0.011  0.7 0.148 0.128  0.84 1.2 .66-.48 1.5 1.4 .49
    -0.420     76     42     74     53 10.5  7550.183  13.90   19.18 0.060 -0.003  0.7 0.104 0.092  0.73 .69 .31-.35 .91 .72 .35
    -0.300    233    128    207    176 10.7 14638.721  24.11   19.16 0.050 -0.006  0.9 0.086 0.054  0.63 .41 .11-.23 .58 .40 .23
    -0.180    861    516    701    732  3.6 37060.397  41.78   19.23 0.048 -0.014  1.5 0.078 0.049  0.63 .18 .10-.11 .28 .24 .11
    -0.060   2409    949   1366   2260  0.8 72755.399  61.11   19.40 0.053  0.009  2.4 0.061 0.059  0.80 .02 .08 .00 .11 .15 .03
     0.060    894    532    721    836  2.6 55013.402  55.62   19.33 0.045 -0.019  1.8 0.051 0.048  0.68-.06 .12 .11 .17 .22 .11
     0.180    287    180    273    266  4.9 51112.468  57.25   19.31 0.031 -0.005  1.3 0.037 0.045  0.95-.17 .18 .23 .31 .35 .23
     0.300    119     71    112    110 12.6 53308.995  59.44   19.29 0.060 -0.042  5.1 0.048 0.076  1.12-.21 .25 .35 .45 .43 .35
     0.420     34     25     34     31  5.9 58754.910  64.99   19.20 0.091  0.063  3.3 0.067 0.105  1.10-.25 .19 .47 .52 .58 .47
     0.540      6      5      6      6 16.7 103512.65  94.40   19.18 0.012 -0.012  1.3 0.011 0.007  0.39-.21 .64 .57 .53 .93 .58
     0.660      1      1      1      1  0.0 966712.00 274.63   19.42 0.023 -0.023  6.2 0.012 0.021  1.13 .31 .53 .72 .31 .53 .72
     0.780      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     0.900      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     1.020      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     1.140      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     1.260      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     1.380      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     1.500

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   #Equivs      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    459      0    459      0  4.8 42507.099  45.91   19.16 0.000  0.000  0.0 0.000 0.000  0.00 .12 .23-.06 .43 .48 .18
     1.000   1500    392    750   1500  4.2 60091.948  61.11   19.35 0.029  0.000  1.1 0.000 0.052  0.00 .07 .08 .00 .35 .22 .14
     2.000   1038    346    346   1038  2.4 63195.008  58.96   19.33 0.058  0.000  2.7 0.055 0.090  1.13 .03 .10 .02 .24 .21 .13
     3.000   1316    329    329   1316  1.1 52116.866  50.08   19.33 0.044  0.000  1.8 0.042 0.034  0.63 .04 .12 .03 .19 .26 .14
     4.000    305     61     61    305  4.6 41082.916  43.73   19.32 0.092 -0.000  2.8 0.090 0.050  0.40 .03 .11-.00 .29 .35 .13
     5.000    270     45     45    270  1.9 79706.665  58.34   19.46 0.087  0.000  4.1 0.084 0.027  0.23 .01 .09-.00 .15 .24 .09
     6.000     35      5      5     35  0.0 82824.397  80.09   19.57 0.112 -0.000  6.3 0.109 0.048  0.36 .03 .05-.02 .08 .09 .09
     7.000     24      3      3     24  0.0 183962.13  98.60   19.58 0.106  0.000  9.9 0.106 0.008  0.06 .05 .06 .00 .06 .08 .05
     8.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     9.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    10.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   Compon#      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     1.000   4947   1181   1998   4488  2.9 57650.279  55.72   19.33 0.050 -0.000  2.1 0.059 0.058  0.80 .05 .11 .01 .29 .27 .14
     2.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     3.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     4.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     5.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     6.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     7.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     8.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
     9.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   Angstms      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
  9999.000    509    117    229    448  0.4 171616.27 123.83   19.69 0.053 -0.000  5.1 0.070 0.064  0.70-.05 .04 .04 .16 .12 .14
     1.793    660    158    235    641  2.3 60693.212  63.44   19.40 0.046  0.000  2.6 0.055 0.039  0.59 .03 .06 .03 .14 .14 .13
     1.501    580    140    202    566  3.3 42946.345  46.53   19.36 0.045  0.000  1.6 0.052 0.043  0.62 .04 .09 .02 .12 .19 .13
     1.338    593    132    218    551  2.0 50560.243  48.72   19.42 0.046 -0.000  1.6 0.052 0.062  0.98 .02 .12 .02 .12 .27 .14
     1.228    534    119    217    469  0.9 68401.247  52.32   19.49 0.050  0.000  1.9 0.057 0.056  0.81 .03 .14 .00 .15 .25 .13
     1.147    542    124    215    486  2.6 50106.558  44.43   19.40 0.049 -0.000  1.7 0.055 0.057  0.96 .03 .14 .00 .19 .27 .14
     1.084    459    110    188    409  1.3 37726.440  36.47   19.10 0.054  0.000  1.6 0.057 0.071  1.14 .05 .14-.02 .22 .32 .13
     1.033    443    108    189    391  6.3 27820.954  31.31   19.01 0.058 -0.000  1.4 0.060 0.071  1.06 .06 .15-.02 .35 .41 .15
     0.991    361     95    163    315  6.9 17045.999  23.04   19.06 0.057 -0.000  1.1 0.063 0.085  1.59 .08 .14-.01 .41 .35 .15
     0.954    266     78    142    212  6.4 12841.645  18.33   19.04 0.064 -0.000  1.0 0.075 0.108  1.43 .42 .14-.05 .85 .42 .18
     0.923

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
    Intens      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    777    174    367    687 18.4  1965.587   5.68   19.25 0.152 -0.051  1.1 0.178 0.256  0.71 .08 .03-.02 .48 .32 .21
  4525.391    503    156    245    446  0.0  6687.352  12.40   19.23 0.065 -0.004  0.8 0.063 0.090  1.02 .07 .08-.01 .41 .31 .16
  9050.781    660    196    318    575  0.0 13492.874  19.49   19.23 0.058 -0.005  1.2 0.059 0.083  0.93 .06 .12-.00 .31 .32 .13
 18101.563    930    268    417    838  0.0 26239.571  29.41   19.31 0.049 -0.005  1.5 0.056 0.057  0.81 .07 .14 .01 .24 .27 .11
 36203.125    996    285    408    928  0.0 50963.586  42.96   19.34 0.045 -0.001  2.0 0.050 0.054  0.89 .04 .14 .02 .12 .23 .10
 72406.250    597    160    255    557  0.0 101392.83  61.63   19.41 0.051 -0.002  3.2 0.059 0.063  0.85 .03 .15 .02 .10 .24 .11
144812.500    347    100    141    329  0.0 198323.42  96.31   19.55 0.052  0.001  5.2 0.067 0.050  0.69-.01 .10 .04 .09 .18 .11
289625.000    103     28     48     97  0.0 377236.35 136.28   19.71 0.043 -0.002  5.9 0.055 0.056  0.56-.02 .10 .05 .11 .19 .14
579250.000     32      9     17     29  0.0 740844.00 202.82   19.90 0.051  0.016 10.9 0.055 0.090  0.79-.02 .05 .07 .09 .13 .17
 1158500.0      2      0      1      2  0.0 2162500.0 375.26   20.49 0.071  0.000 26.8 0.000 0.000  0.00-.03 .02 .03 .05 .02 .04
 2317000.0

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   #Sigmas      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000    134     35     82    113100.0   214.101   0.82   19.20 2.447 -2.467  3.5 3.559 4.317  0.64 .06 .01-.01 .57 .42 .24
     1.816    109     42     88     99  8.3   753.535   2.59   19.26 0.283 -0.042  0.7 0.272 0.383  1.00 .06-.03 .00 .54 .29 .22
     3.298    214     70    137    185  0.0  1566.740   4.65   19.23 0.123  0.015  0.6 0.145 0.190  0.95 .11 .08-.02 .52 .36 .20
     5.989    450    134    238    391  0.0  4151.787   8.74   19.24 0.077 -0.012  0.7 0.077 0.116  0.96 .11 .05-.02 .52 .34 .19
    10.877    730    235    357    654  0.0  9699.623  15.61   19.22 0.064 -0.003  1.0 0.064 0.093  1.00 .08 .12-.01 .33 .33 .14
    19.753   1282    375    584   1148  0.0 25004.530  28.18   19.30 0.049 -0.004  1.4 0.054 0.059  0.88 .05 .14 .01 .20 .26 .11
    35.872   1341    368    545   1249  0.0 63812.565  48.78   19.37 0.048 -0.001  2.3 0.054 0.056  0.89 .03 .14 .02 .11 .23 .11
    65.145    514    156    227    489  0.0 166845.37  87.09   19.52 0.050  0.000  4.4 0.061 0.058  0.81 .01 .11 .04 .09 .18 .12
   118.305    158     48     80    145  0.0 362487.56 150.81   19.70 0.049  0.002  7.3 0.070 0.059  0.62-.04 .06 .05 .12 .15 .13
   214.847     15      5      8     15  0.0 1009385.4 270.65   19.95 0.054  0.015 14.5 0.038 0.084  0.86-.01 .09 .09 .11 .17 .22
   390.171

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
      Rsym      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000   1754    781    956   1754  0.3 69778.980  59.57   19.37 0.013  0.001  0.6 0.022 0.040  0.85 .05 .11 .02 .20 .20 .12
     0.030   1014    574    662   1014  0.3 52780.003  51.75   19.34 0.043  0.001  1.7 0.046 0.051  0.73 .04 .13 .02 .26 .26 .13
     0.060    601    400    447    601  0.5 61805.588  62.03   19.34 0.075  0.013  2.8 0.071 0.067  0.65 .05 .09 .01 .29 .25 .13
     0.090    444    292    314    444  1.4 69444.802  61.90   19.38 0.105  0.023  4.3 0.092 0.092  0.77 .03 .10 .01 .27 .23 .11
     0.120    268    202    223    268  1.1 57556.230  52.91   19.34 0.132 -0.056  4.9 0.118 0.098  0.76 .03 .08 .01 .27 .19 .11
     0.150    133    112    127    133  1.5 25592.098  34.11   19.25 0.162 -0.097  3.8 0.137 0.093  0.64 .02 .04 .01 .32 .27 .16
     0.180     64     46     62     64  7.8 27850.035  44.80   19.31 0.190  0.039  4.0 0.141 0.158  0.92 .12 .03-.03 .38 .27 .17
     0.210     31     23     30     31  6.5 22751.110  35.90   19.25 0.218 -0.141  4.4 0.147 0.192  1.39-.03 .18 .04 .30 .41 .19
     0.240     16      9     16     16  6.3  2433.395   6.80   19.15 0.255 -0.106  1.4 0.171 0.258  1.17 .12 .11-.06 .46 .35 .26
     0.270     18     14     18     18 11.1  2596.329   7.39   19.22 0.285 -0.084  1.8 0.239 0.207  0.72 .11-.13-.07 .54 .62 .20
     0.300     15      9     15     15 40.0  6579.296  17.06   19.21 0.303  0.254  2.4 0.195 0.457  0.60 .03 .12-.02 .52 .47 .21
     0.330     12      9     12     12  8.3  2413.000   7.06   19.29 0.336 -0.129  2.0 0.239 0.315  0.92 .22-.11-.01 .92 .32 .22
     0.360      8      6      8      8 25.0 12839.506  27.53   19.16 0.364  0.321  4.4 0.474 0.420  0.63-.01-.01-.01 .33 .14 .12
     0.390      6      5      6      6 16.7   740.062   2.29   18.94 0.409  0.139  0.9 0.272 0.489  1.57 .34-.39-.11 1.2 .59 .30
     0.420      5      2      5      5 20.0   650.476   2.46   19.12 0.439 -0.069  1.1 0.266 0.552  2.01-.03 .07 .06 .24 .11 .24
     0.450      6      2      6      6 66.7   791.207   2.51   18.99 0.471 -0.366  1.1 0.482 0.139  0.31-.03-.05-.02 .44 .42 .23
     0.480      5      3      5      5 40.0   770.611   2.72   19.09 0.497  0.148  1.3 0.340 0.714 13.87-.01-.04 .01 .24 .17 .14
     0.510      4      4      4      4 50.0  1313.123   3.37   19.08 0.519 -0.413  1.7 0.432 0.237  0.47 .41-.08-.09 .62 .41 .13
     0.540      6      5      6      6 33.3 13835.157  31.30   19.16 0.551 -0.526  7.7 0.404 0.451  0.77-.09-.03 .04 .48 .25 .19
     0.570     78     37     55     78 85.9   745.820   2.79   19.24 2.004 -2.111  5.9 3.847 2.239  1.56-.03-.05 .03 .53 .40 .24
     0.600

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
      dI/I      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
    -0.500     76     44     67     76 76.3  1904.455   6.51   19.20 1.162 -1.214  6.7 0.916 1.134  1.24 .00-.05 .02 .55 .42 .22
    -0.460      5      3      5      5 60.0   523.352   1.81   19.04 0.444 -0.444  0.9 0.347 0.608  1.50-.11 .03 .03 .46 .29 .30
    -0.420      2      2      2      2  0.0   731.185   2.40   18.95 0.411 -0.411  1.0 0.208 0.609  2.08-.25-.03 .07 .74 .15 .22
    -0.380      5      4      5      5 20.0  1916.476   5.33   19.26 0.357 -0.357  1.6 0.241 0.345  1.27 .14-.05 .01 .21 .10 .17
    -0.340     10      5     10     10 20.0  2464.978   6.93   19.29 0.323 -0.323  1.8 0.235 0.320  0.78 .00-.06-.02 .69 .22 .18
    -0.300     10      8     10     10  0.0  4273.206   9.54   19.05 0.280 -0.280  2.4 0.228 0.153  0.64 .32-.18-.12 .71 .85 .23
    -0.260     18     11     17     18  5.6  7436.038  15.20   19.26 0.228 -0.228  2.4 0.182 0.129  0.75 .02 .16 .07 .30 .48 .25
    -0.220     47     39     47     47  6.4 24770.634  35.45   19.30 0.201 -0.202  4.4 0.163 0.115  0.72 .13 .06-.04 .39 .31 .15
    -0.180    141    126    135    141  0.7 45737.143  47.04   19.28 0.152 -0.152  5.1 0.136 0.090  0.60 .01 .08 .01 .27 .20 .14
    -0.140    248    201    214    248  1.6 62233.617  57.78   19.30 0.119 -0.119  4.7 0.101 0.100  0.76 .02 .11 .01 .26 .22 .12
    -0.100    347    281    323    347  0.9 55477.037  58.14   19.24 0.079 -0.079  2.8 0.068 0.073  0.65 .04 .13 .02 .29 .30 .15
    -0.060    693    512    626    693  0.4 55593.963  53.41   19.27 0.038 -0.038  1.5 0.041 0.052  0.87 .04 .15 .03 .25 .28 .15
    -0.020   1299    635    769   1299  0.2 72676.043  61.23   19.38 0.010  0.001  0.5 0.020 0.035  0.80 .04 .11 .02 .19 .20 .12
     0.020    776    565    688    776  0.5 55384.610  52.06   19.41 0.036  0.036  1.4 0.038 0.040  0.65 .05 .10 .00 .24 .21 .11
     0.060    409    322    362    409  0.5 69189.325  65.74   19.44 0.080  0.080  3.2 0.077 0.074  0.70 .04 .06 .00 .26 .22 .11
     0.100    231    189    208    231  0.9 69022.695  58.69   19.43 0.113  0.113  4.7 0.100 0.070  0.75 .05 .07 .00 .30 .19 .10
     0.140     70     60     69     70  2.9 20448.378  28.21   19.29 0.152  0.152  2.9 0.142 0.084  0.61 .03 .02 .00 .38 .31 .16
     0.180     29     20     28     29  6.9 41189.071  68.69   19.32 0.191  0.191  5.0 0.119 0.182  1.01 .08 .07 .01 .29 .19 .21
     0.220     10      4     10     10 20.0  1448.982   4.28   19.13 0.234  0.234  0.9 0.245 0.058  0.24-.07 .00 .02 .43 .29 .18
     0.260     15     11     15     15 13.3  1572.098   5.16   19.28 0.277  0.277  1.3 0.226 0.331  0.95-.02 .09-.08 .40 .28 .18
     0.300     12      9     12     12 41.7  7884.130  19.98   19.21 0.304  0.304  2.7 0.412 0.457  0.60 .30 .11-.06 .87 .57 .26
     0.340      7      5      7      7 14.3 14206.424  31.72   19.19 0.363  0.363  4.7 0.483 0.414  0.61-.15 .03 .04 .34 .18 .12
     0.380      5      4      5      5 20.0  1010.560   2.93   18.93 0.399  0.399  1.1 0.145 0.561  2.87 .47-.48-.15 1.2 .64 .29
     0.420      2      0      2      2  0.0   687.318   2.61   19.05 0.438  0.438  1.1 0.000 0.000  0.00-.04 .02 .08 .09 .05 .11
     0.460     21     11     18     21 81.0   455.241   1.75   19.25 0.661  0.661  1.1 0.552 0.619  1.52-.05-.06 .03 .37 .20 .24
     0.500

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
    dI/sig      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000   2221    867   1100   2221  4.2 33523.590  39.97   19.31 0.012  0.001  0.5 0.021 0.036  0.78 .06 .10 .01 .31 .24 .14
     1.000    992    550    627    992  2.3 52489.527  50.53   19.34 0.029  0.003  1.4 0.035 0.051  0.95 .05 .10 .01 .26 .26 .13
     2.000    436    295    326    436  0.7 63936.145  56.51   19.34 0.043 -0.001  2.4 0.048 0.053  0.81 .03 .12 .03 .21 .29 .13
     3.000    258    185    200    258  0.0 67898.738  57.66   19.39 0.060 -0.002  3.5 0.066 0.051  0.68 .02 .12 .03 .16 .23 .11
     4.000    157    113    123    157  0.0 85004.048  63.35   19.39 0.070  0.005  4.4 0.070 0.048  0.57-.01 .09 .03 .10 .18 .10
     5.000    104     77     84    104  0.0 100775.06  69.51   19.43 0.079  0.002  5.5 0.085 0.060  0.61 .01 .09 .01 .10 .16 .07
     6.000     82     63     67     82  0.0 146155.19  80.56   19.46 0.080 -0.011  6.5 0.067 0.058  0.66 .01 .13 .04 .10 .23 .12
     7.000     53     43     44     53  0.0 145120.94  82.40   19.46 0.090 -0.008  7.5 0.096 0.093  0.89-.04 .09 .02 .19 .16 .07
     8.000     46     37     38     46  0.0 173762.74  87.77   19.47 0.097  0.000  8.5 0.090 0.069  0.73-.02 .09 .02 .10 .16 .09
     9.000     30     25     27     30  0.0 248648.09 111.92   19.62 0.085  0.015  9.5 0.077 0.056  0.63-.00 .05 .02 .06 .08 .10
    10.000     15     13     13     15  0.0 226651.47 104.38   19.54 0.099  0.004 10.3 0.088 0.077  0.73-.00 .07 .03 .07 .11 .07
    11.000     22     18     19     22  0.0 224253.45 113.85   19.64 0.101 -0.001 11.5 0.101 0.077  0.62 .01 .06 .01 .08 .09 .05
    12.000     13      7     10     13  0.0 321981.00 138.72   19.92 0.090  0.009 12.5 0.101 0.051  0.47-.03 .06 .03 .06 .08 .05
    13.000     10      8      8     10  0.0 219987.80 116.72   19.51 0.116 -0.023 13.6 0.114 0.067  0.51 .02 .06 .01 .08 .08 .06
    14.000     12      9     10     12  0.0 339390.43 141.41   19.70 0.102  0.022 14.4 0.107 0.062  0.57 .01 .04-.01 .04 .10 .06
    15.000      5      5      5      5  0.0 267504.20 126.30   19.78 0.123 -0.007 15.6 0.104 0.078  0.48-.03 .07 .02 .06 .08 .03
    16.000      3      3      3      3  0.0 178344.33 106.41   19.80 0.157  0.051 16.7 0.094 0.178  2.04-.02 .10-.03 .05 .10 .04
    17.000      5      5      5      5  0.0 297408.60 134.74   19.66 0.128  0.019 17.4 0.132 0.060  0.44-.03 .06-.01 .05 .12 .07
    18.000      4      4      4      4  0.0 385467.00 144.34   19.79 0.127 -0.127 18.3 0.099 0.119  0.74-.04 .07 .01 .08 .10 .06
    19.000      2      2      2      2  0.0 607361.50 167.52   19.98 0.117 -0.004 19.6 0.146 0.114  0.03-.02 .04-.02 .02 .07 .03
    20.000      4      4      4      4  0.0 432740.00 190.26   19.79 0.108 -0.004 20.5 0.098 0.187  1.81-.04 .06 .16 .10 .12 .24
    21.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    22.000      4      4      4      4  0.0 383528.50 166.46   19.50 0.135 -0.102 22.5 0.169 0.212  0.56-.03 .07-.03 .08 .09 .06
    23.000      0      0      0      0  0.0     0.000   0.00    0.00 0.000  0.000  0.0 0.000 0.000  0.00 .00 .00 .00 .00 .00 .00
    24.000     10      6      7     10 10.0 663779.96 260.37   19.68 0.121  0.011 61.3 0.173 0.216  0.95-.34-.00 .17 .81 .23 .25
    25.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   Overall      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000   4947   1181   1998   4488  2.9 57650.279  55.72   19.33 0.050 -0.000  2.1 0.059 0.058  0.80 .05 .11 .01 .29 .27 .14
     1.000

Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
   Centric      #  Pairs   Uniq   Merg %<2s       <I> <#Sig>    <Bg>  Rsym   dI/I dI/s    R+ Ranom Canom ErX ErY ErZ RmX RmY RmZ
     0.000   1326    173    683   1169  6.3 65487.919  66.10   19.42 0.048 -0.000  1.9 0.072 0.134  1.44 .04 .06 .02 .31 .19 .14
     1.000

Coverage Statistics
Integration of BruecknerJK_153F40
 ...1.1(1):  component 1 in sample 1 (component 1 in cu_BruecknerJK_153F40_01.raw)
                                                           .......Shell......
  Angstrms   #Obs Theory %Compl Redund   Rsym Pairs %Pairs Rshell #Sigma %<2s
 to  1.793    229    446  51.35   2.22  0.053   117  26.23  0.053 123.83  0.4
 to  1.501    464    715  64.90   2.52  0.051   275  38.46  0.046  63.44  2.3
 to  1.338    666    987  67.48   2.63  0.050   415  42.05  0.045  46.53  3.3
 to  1.228    884   1236  71.52   2.65  0.049   547  44.26  0.046  48.72  2.0
 to  1.147   1101   1502  73.30   2.61  0.049   666  44.34  0.050  52.32  0.9
 to  1.084   1316   1776  74.10   2.60  0.049   790  44.48  0.049  44.43  2.6
 to  1.033   1504   2026  74.23   2.58  0.050   900  44.42  0.054  36.47  1.3
 to  0.991   1693   2272  74.52   2.55  0.050  1008  44.37  0.058  31.31  6.3
 to  0.954   1856   2497  74.33   2.52  0.050  1103  44.17  0.057  23.04  6.9
 to  0.923   1998   2776  71.97   2.48  0.050  1181  42.54  0.064  18.33  6.4
