

from    debug           import *

import  copy

import  let




class Library:

    def __init__( self ):
        self.dict = {}

    
    def __setitem__( self, key, value ):
        self.dict[ key ] = isinstance( value, let.Expression )  \
                               and value  \
                               or  self.parser.parse( value )

    def __getitem__( self, key ):

        if key in self.dict:
            #return copy.deepcopy( self.dict[ key ] )
            debug( 4, 'library. asked', key, self.dict[ key ] )
            return self.dict[ key ].copy( ({},{}) )

        elif 'PLUS' in self.dict  and  key.isdigit():
            return self.number( int( key ) )

        else:
            raise KeyError, key

        
    def __iter__( self ):
        return self.dict.__iter__()



    def init( self, parser ):
    
        self.parser = parser
    
        self.initCombinators()
        self.initLogic()
        self.initPairs()
        self.initArithmetic()
        self.initLists()
        self.initElse()


    def initCombinators( self ):
        self['I'] = '\\x.x'
        self['K'] = '\\x y. x'
        self['S'] = '\\x y z. x z (y z)'

        self['W'] = '\\x.x x'
        self['Y'] = '\\f.(\\x. f (x x)) (\\x. f (x x))'
        self['OO'] = '(\\x y. y (x x y))(\\x y. y (x x y))'

    def initLogic( self ):
        self['T']    = '\\x y. x'
        self['F']    = '\\x y. y'
        self['NOT']  = '\\p. p F T'
        self['AND']  = '\\p q. p q F'
        self['OR']   = '\\p q. p T q'
        self['COND'] = '\\p x y. p x y'


    def initPairs( self ):
        self['FST']  = '\\p. p T'
        self['SND']  = '\\p. p F'
        self['PAIR'] = '\\a b f. f a b'
        self[',']    = '\\a b f. f a b'

    def initArithmetic( self ):
        self['ISZERO'] = '\\n. n (\\x. F) T'
        self['SUCC']   = '\\n f x. f (n f x)'
        self['PLUS']   = '\\m n f x. n f (m f x)'
        self['+']      = '\\m n f x. n f (m f x)'
        self['MULT']   = '\\m n f. m (n f)'
        self['*']      = '\\m n f. m (n f)'
        self['POW']    = '\\m n. n m'
        self['PRED']   = '\\n f x. n (\\g h. h (g f)) (\\u. x) I'
        self['PREFN']  = '\\f p. \\x. x F ((p T) (p F) (f (p F)))'
        self['PRED_']  = '\\n f x. (n (PREFN f) (\\y. y T x)) F'
        

    def initLists( self ):
        self['NIL']  = '\\z. z'                         # = I
        self['CONS']  = '\\x y. , F (, x y)'
        self[':']     = '\\x y. , F (, x y)'
        self['NULL']  = '\\z. z T'                      # = FST
        self['HEAD']  = '\\z. FST (SND z)'
        self['TAIL']  = '\\z. SND (SND z)'

    def initElse( self ):
        self['FACT'] = 'Y (\\f n. (ISZERO n) 1 (MULT (f (PRED n)) n))'
        #self['REC1'] = 'Y (\\f n. (ISZERO n) (f (SUCC n)) I)'
        self['REC1'] = 'Y (\\f n. (NULL n) I (f (TAIL n)))'

        self['LOOP'] = 'W W'
        #self['ERROR'] = 'FST (PAIR I LOOP)'
        


    def number( self, n ):
        "Generates Number Expression"
        lf = let.Abstraction( expr=None )
        lx = let.Abstraction( expr=None )
        
        x = let.Variable( lx )

        for _ in range( n ):
            
            f = let.Variable( lf )
            x = let.Application( func= f, arg= x )

        lx.expr = x
        lf.expr = lx

        return lf
        
