#!/bin/bash

rm -rf *.spi

function rep(){
SOURCEFILE=${1}
OUTFILE=${2}
CIRNAME=${3}
PINST=${4}
PLMIN=${5}
PWMAG=${6}
PWMAX=${7}
PWMID=${8}
PWMIN=${9}
NINST=${10}
NLMIN=${11}
NWMAG=${12}
NWMAX=${13}
NWMID=${14}
NWMIN=${15}

sed -e "s/%CIRNAME%/${CIRNAME}/g" ${1} > ${2}
sed -i "s/%P%/${PINST}/g;s/%LP%/${PLMIN}/g;s/%MP%/${PWMAG}/g;s/%WP%/${PWMAX}/g;s/%WPMID%/${PWMID}/g;s/%WPMIN%/${PWMIN}/g" ${2}
sed -i "s/%N%/${NINST}/g;s/%LN%/${NLMIN}/g;s/%MN%/${NWMAG}/g;s/%WN%/${NWMAX}/g;s/%WNMID%/${NWMID}/g;s/%WNMIN%/${NWMIN}/g" ${2}

}

#-----------------------------------------------------------------
#prepare
BDIR=NETLIST_BASE
ODIR=./

\rm -rf $ODIR
mkdir   $ODIR

echo " creating spi file from $BDIR ---> $ODIR."

#-----------------------------------------------------------------
#create spi file

PINST=p
PLMIN=350
PWMAG=1
PWMAX=1800
PWMID=1350
PWMIN=900
NINST=n
NLMIN=350
NWMAG=1
NWMAX=1200
NWMID=900
NWMIN=600

rep $BDIR/INV_1X.spi     $ODIR/INV_1X.spi     INV_1X      $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/NAND2_1X.spi   $ODIR/NAND2_1X.spi   NAND2_1X    $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/NAND3_1X.spi   $ODIR/NAND3_1X.spi   NAND3_1X    $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/NAND4_1X.spi   $ODIR/NAND4_1X.spi   NAND4_1X    $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/NOR2_1X.spi    $ODIR/NOR2_1X.spi    NOR2_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/NOR3_1X.spi    $ODIR/NOR3_1X.spi    NOR3_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/NOR4_1X.spi    $ODIR/NOR4_1X.spi    NOR4_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/AND2_1X.spi    $ODIR/AND2_1X.spi    AND2_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/AND3_1X.spi    $ODIR/AND3_1X.spi    AND3_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/AND4_1X.spi    $ODIR/AND4_1X.spi    AND4_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/OR2_1X.spi     $ODIR/OR2_1X.spi     OR2_1X      $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/OR3_1X.spi     $ODIR/OR3_1X.spi     OR3_1X      $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/OR4_1X.spi     $ODIR/OR4_1X.spi     OR4_1X      $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/AOI21_1X.spi   $ODIR/AOI21_1X.spi   AOI21_1X    $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/AOI22_1X.spi   $ODIR/AOI22_1X.spi   AOI22_1X    $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/OAI21_1X.spi   $ODIR/OAI21_1X.spi   OAI21_1X    $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/OAI22_1X.spi   $ODIR/OAI22_1X.spi   OAI22_1X    $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/AO21_1X.spi    $ODIR/AO21_1X.spi    AO21_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/AO22_1X.spi    $ODIR/AO22_1X.spi    AO22_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/OA21_1X.spi    $ODIR/OA21_1X.spi    OA21_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/OA22_1X.spi    $ODIR/OA22_1X.spi    OA22_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/SEL2_1X.spi    $ODIR/SEL2_1X.spi    SEL2_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/XOR2_1X.spi    $ODIR/XOR2_1X.spi    XOR2_1X     $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/XNOR2_1X.spi   $ODIR/XNOR2_1X.spi   XNOR2_1X    $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/DFFARAS_1X.spi $ODIR/DFFARAS_1X.spi DFFARAS_1X  $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/DFFAR_1X.spi   $ODIR/DFFAR_1X.spi   DFFAR_1X    $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/DFFAS_1X.spi   $ODIR/DFFAS_1X.spi   DFFAS_1X    $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
rep $BDIR/DFF_1X.spi     $ODIR/DFF_1X.spi     DFF_1X      $PINST $PLMIN $PWMAG $PWMAX $PWMID $PWMIN $NINST $NLMIN $NWMAG $NWMAX $NWMID $NWMIN
