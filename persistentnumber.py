#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
persistentnumber.py
~ based on episode of Numberphile ... cite:
    https://www.youtube.com/watch?v=Wim9WJeDTHQ
    

@Created on Wed Sep 18 11:54:31 2024
@author: dac

biggest persistent number on show:
    277 777 788 888 899
   2.7 e14 
   
   277777788888899

"""
# In[]
####  Import Packages
import os;
import math ;
import argparse ;

import time 
import math
import pandas as pd ;
import datetime ;

from multiprocessing import Pool  ## for multi-threading

###############################################################################
# In[]

inppath = os.getcwd();
inppath = inppath + ''
z0 = time.time();

###############################################################################
if 1: ## set parameters
    SETPATH = {
            'out' : inppath 
    }
    BATCHNUMBER = '0002' ;

    NRCORES = 2;
    begbit = 8;
    endbit = 8;
    beg    = 1; 
    EX = {
        'savetab': False,
        'timer'  : True,
        'dots'   : False,
        'begfaster':False,
    }
    PR = {
        'PREACH': False,
        'PRNEW' : False ,
    }
    rz = int(1); ## resolution scale for counter in Hz 

    BAT = {
        1 : [False, False],
        2 : [True , False],
        3 : [True , True ],
    }
    SETBAT = BAT.keys();
    SETBAT = [ 3,2,1 ] ;

    SETNCORES = [1,2,3,4,5,6] 
    SETNCORES = [5,6,7,8] 
    SETNCORES = [1,2,4,6] 
    SETNCORES = [ 4 ] 
    SETNCORES = [ 4,3,2,1 ] 

    SETBAT    = [ 1,2,3 ] ;
    SETNCORES = [ 5,6,7,8] ; 

    SETBAT = [ 3  ] ;  ## optimal opt
    SETNCORES = [ 4 ] ;## optimal opt else [ 1 ]  

###############################################################################
def osfss( ):   
    ''' ret: FSS <str> file-separator based on the operating system
    '''
    import platform; p = platform.uname();
    if p.system == 'Windows': FS  =  str('\u005c') ;  ## == "\" #if system is Windows:
    else: FS  =  str('\u002f') ;  ## == "/"  # if NOT windows
   #FSS =  str( 1*FS ) ;
    return str( 1*FS ) ;
FSS = osfss();
    
def dig( n ):
    digits = [int(i) for i in str(n)]
    return digits

def caldig( digits ):
    R = 1 ;
    for j in digits:
        R *= int( j )
    return R

def dotter01(n):
    dotdenom = 1000;
    DL = ['*','A','B','C']
    if (n % dotdenom) == 1 :
        print( '.',end='');
    return 1;

def dotter(n, e=1, emin=2, SHOW=True):
    if e == emin: e = emin -1;
    if n> 1:
        if (n % (10**e) ) == 1 :
            u = '.'            
            while ((n % (10**e) ) == 1 ):
                e+=1
                u = chr( 63 + e ) 
        if SHOW:
            if e==emin: print('.',end='')    
            if e >emin: print( f'{u}',end='')
    return e;
###############################################################################
def persist(n, SHOW=False, SKIP=True,SKIP_1=True,SKIP_2=False):
    CTR = 0;
    while len( str( n))>1:  
        digits = [int(i) for i in str(n)]
        if SKIP_1:
            if '0' in digits:
                CTR+=1; break;
        if SKIP_2:
            if '2' and '5' in digits:
                CTR+=2; break;
            if '4' and '5' in digits:
                CTR+=2; break;
            if '6' and '5' in digits:
                CTR+=2; break;
            if '8' and '5' in digits:
                CTR+=2; break;
        n = caldig( digits )
        CTR+=1
        if SHOW: print( CTR, n)
    return CTR;

###############################################################################
if 0: 
  if __name__=='__main__':
    
    if 1:
        n = '3333133'
    if 1:
        n = str(input( ' enter sereies digits of positive counting numbers: '));    
    persist(n)
###############################################################################    
def loop( beg, end, SKIP_1=True, SKIP_2=True  ):
    if 1: ## initializing variables
        tic = 1; 
        SMAG = list();
        DMAG = dict();
        cmag = 0;
        nmag = 0;
        nf = 0;
        dz = 0;
        TAB = [];
        EX['dots']=True;
    z0 = time.time();    
    for m in range( beg, end ): 
        n = int( m )
        #nf = dotter( n, e=3,emin=4, SHOW=EX['dots'] )
        #if nf>1: print('\n')
        if 1:            
            c = persist(n, SHOW=False, SKIP_1=True, SKIP_2=True )
            #if PR['PREACH']: print( n, c )
            #if EX['savetab']: TAB.append([ n, c ])
            if c> cmag: 
                cmag=c;
                nmag=n;
                
                if PR['PRNEW']: 
                    if nf>0: print('\n')
                    print(f' {n} counted {c} ')
                SMAG.append([c, n])
                DMAG[c] = n ;
                #nf=0;
            
        if EX['timer']:
            dz = ( rz**2 * (time.time() - z0)) ;
            if math.floor(dz) >  (tic * rz**1 ):
                tic += 1 ### DONT DO !!!  (tic * rz )
                pass;
                if EX['dots']: print( '.',end=''); nf+=1;                    
                if (tic % 60) == 0:
                    zmins = int(tic / 60);
                    #print( f'\n' +'*'*zmins ,end='')
                    #print( f'\n' +'*' ,end='')
                    y = datetime.time(0,zmins)
                    print( ' ... {} ... '.format( y ) ,end='\n')
    return DMAG;     #return SMAG;  #return SMAG, dz, nf;
####
####===========================================================================
#e = dotter( 100001 )
#print( f'\n{e}' )
        ###############################################################################          
        #BANK=[0,0]
def reconcile( SMAG ):
        for i, res in enumerate(SMAG):
            W = res.get()
            #print(W)
            if i ==0: BANK=W
            if i >0:
              for k in W.keys():
                 #print( type(ww))
                #print(k, W[k])
                if k in BANK.keys():
                    if W[k] < BANK[k]:
                       BANK[k] = W[k]
                else:
                       BANK[k] = W[k]
        #print(BANK)
        return BANK;
def endmag( dicto ):
    mu=0;
    for k in dicto.keys():
        if k>mu:
            mu=k
    L = [mu,dicto[mu]]
    return L 
        
# In[]    
STATS = []
if 1:
 if __name__=='__main__':
    for NRCORES in SETNCORES : 
    ## loop through set of NRCORES
     if 1:
            print( 0*'\n' + '*'*60 + 0*'\n' ,end='' )
            print( f'\n COMPUTING WITH NR CORES {NRCORES}:')
     for batopt in SETBAT: 
     ## loop through param of BATCH options
      if 1:
            print( 0*'\n' + '*'*60 + 0*'\n' ,end='' )
            print( f'\n BATCH OPTION# {batopt}:')
            print( f'\n   Options: Skip1 {BAT[batopt][0]}, Skip2 {BAT[batopt][1]}:')

      for ebit in range( begbit, endbit +1):  
        '''## loop through values of ebit which is the integer that composes
           of val = int( '10**' + (ebit) ) 
      '''
        z1 = time.time();  
        end = 1*int( '1' + '0' * (ebit-0) )
        end+= 0*int( '1' + '0' * (ebit-1) )
        end+= 0*int( '1' + '0' * (ebit-2) )
        
        if EX['begfaster']: beg =  1*int( '1' + '0' * (ebit-1) );
        else: 
            if beg==None:   beg =  1;
        
        if 1:
            print( 0*'\n' + '*'*60 + 0*'\n' ,end='' )
            print( f'\nCalculating Persistent Numbers ending at {end:1.2e}:')
        nf = 0;
        dz = 0;
        #SMAG, dz, nf = loop( beg, end, SKIP_1=BAT[batopt][0],SKIP_2=BAT[batopt][1])
       
        # In[]
        with Pool(processes= NRCORES ) as pool:
            '''
            Multi-thread processing...
             .. will process function (target) = loop
             with args fraction of beg, fraction of end
             where fraction is based on 1/NCORES
            
            SMAG = loop( beg, end, SKIP_1=BAT[batopt][0],SKIP_2=BAT[batopt][1])    
            
            # launching multiple evaluations asynchronously *may* use more processes
            multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
            print([res.get(timeout=1) for res in multiple_results])
            '''
            DMAG = [pool.apply_async(
                    loop, 
                    ( int(beg)+int(end*(i)/NRCORES), int(end*(i+1)/NRCORES)))
                    for i in range(0,NRCORES)]
            print([ res.get() for res in DMAG ])
            
            # for res in SMAG:
            #     X = res.get()
            #     for i,v in enumerate(X):
            #         print(v)
        dz = ( 1**2 * (time.time() - z1)) ;
        BANK = reconcile( DMAG );
        print( BANK );
        SMAG = endmag( BANK );
        print (SMAG)
        # In[]    
        ## summarize round  
        if 1:
            if nf>0: print('\n')
            #print( 0*'\n' +2*'\t' + '-'*40 + 0*'\n' ,end='' )
            print( f' >Summary of Persistent Numbers for endbit of {ebit} ending at {end:1.2e}:')
            print( '\t >>',end='')
            print(SMAG )
            #if EX['timer']:
            #print(  '\t >>total calculation H:M:S: {} '.format( datetime.time(0,0,int(dz))) )
            print( f'\t >>total calculation (sec): {dz} ' )
        if 0:
          if nf>0: print('\n')        
        if 1:
          STATS.append([ 
            NRCORES,
            batopt,
            ebit,
            end, 
            float(f'{1000*dz/rz**2:3.2f}'), 
            SMAG[0], # SMAG[-1][0], 
            SMAG[1], # SMAG[-1][1] 
        ])         
                
# In[] SUMMARIZING THE RESULTS AND SAVING RESULTS
    ###############################################################################          
    ## In[]    
    if 1:
        print( 0*'\n' + '#'*70 + 0*'\n' ,end='\n' )
        print( 'All the persistent numbers found:\nSTEPS PERSIS*NR')
        for b in BANK.keys():
            print('{}   {}'.format(  b, BANK[b]) ) 
        print( 0*'\n' + '#'*70 + 0*'\n' ,end='\n' ) 

        
    ###############################################################################          
    ## In[]
    if 1:
        columnnames=['NC','batopt','ebit','end', 'dz_msec','pCtr','pVal']
        print( 0*'\n' + '#'*70 + 0*'\n' ,end='\n' )
        
        #print( STATS )
        STATSDF = pd.DataFrame( STATS, columns=columnnames)    
        print( STATSDF )
        print( 0*'\n' + '#'*70 + 0*'\n' ,end='\n' ) 

        
    ## In[]
    if 1:
        save_file = \
        (SETPATH['out'] + FSS + \
            1 * ".." + FSS +\
            1 * "results" +\
            1 * "_" +\
            1 * "statsdf" +\
            0 * "_" +\
            1 * BATCHNUMBER +\
            ".csv"
        );
        print(">>writing to file :\n{}".format(save_file))
        STATSDF.to_csv( 
                      save_file,
    #                 float_format='%4.3f',
                      columns=columnnames,
                      sep=',',
                      mode='w',
                      encoding='utf-8',
    #                 lineterminator='\r\n', ## Windows
                      lineterminator='\n'  , ## nonWin
        );
    ###############################################################################          

###############################################################################        
    