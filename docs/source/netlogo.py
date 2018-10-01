## description: A lexer and style for NetLogo syntax to be used with Pygments
## author: Jan C. Thiele
##         Department Ecoinformatics, Biometrics and Forest Growth
##         University of Goettingen
## contact: <jthiele at gwdg dot de>
## copyright: JC Thiele, 2011
## version: 0.1.2, for NetLogo 4.1.2 (and before ?)
## license: GPL v2

import re

from pygments.lexer import Lexer, DelegatingLexer, RegexLexer, bygroups, \
     include, using, this

from pygments.lexer import RegexLexer
from pygments.token import *

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace



class NetLogoLexer(RegexLexer):
    """
    For `NetLogo <http://ccl.sesp.northwestern.edu/netlogo/>`_ source code.
    """

    name = 'NetLogo'
    aliases = ['NetLogo']
    filenames = ['*.nlogo', '*.nls']
    mimetypes = ['text/x-netlogo']

    flags = re.IGNORECASE # ignore case

    operants = ['\+','\*','\-','\/','\^','\<','\>','\=','\!\=','\<\=','\>\=']
    
    keywords = ['__includes','directed-link-breed','extensions','end','globals','links-own',
                'patches-own','to-report','to','turtles-own','undirected-link-breed']

    constants = ['false','true','black','gray','white','red','orange','brown','yellow','green','lime',
                 'turquoise','cyan','sky','blue','violet','magenta','pink','e','pi','nobody']

    commands = ['__layout-magspring','__set-line-thickness','ask','ask-concurrent','auto-plot-off','auto-plot-on',
                'back','beep','bk','ca','carefully','cd','clear-all','clear-all-plots','clear-drawing','clear-links',
                'clear-output','clear-patches','clear-plot','clear-turtles','cp','create-link-from','create-links-from',
                'create-links-to','create-links-with','create-link-to','create-link-with','create-ordered-turtles',
                'create-temporary-plot-pen','create-turtles','cro','crt','ct','die','diffuse','diffuse4','display',
                'downhill','downhill4','every','export-all-plots','export-interface','export-output','export-plot',
                'export-view','export-world','face','facexy','fd','file-close','file-close-all','file-delete','file-flush',
                'file-open','file-print','file-show','file-type','file-write','follow','follow-me','foreach','forward','hatch',
                'hide-link','hide-turtle','histogram','home','ht','hubnet-broadcast','hubnet-broadcast-clear-output',
                'hubnet-broadcast-message','hubnet-broadcast-view','hubnet-clear-override','hubnet-clear-overrides',
                'hubnet-fetch-message','hubnet-reset','hubnet-reset-perspective','hubnet-send','hubnet-send-clear-output',
                'hubnet-send-follow','hubnet-send-message','hubnet-send-override','hubnet-send-watch',
                'hubnet-set-client-interface','if','ifelse','import-drawing','import-pcolors','import-pcolors-rgb',
                'import-world','inspect','jump','layout-circle','layout-radial','layout-spring','layout-tutte','left','let',
                'loop','lt','move-to','movie-cancel','movie-close','movie-grab-interface','movie-grab-view','movie-set-frame-rate',
                'movie-start','no-display','output-print','output-show','output-type','output-write','pd','pe','pen-down',
                'pen-erase','pen-up','plot','plot-pen-down','plot-pen-reset','plot-pen-up','plotxy','print','pu','random-seed',
                'repeat','report','reset-perspective','reset-ticks','reset-timer','resize-world','ride','ride-me','right','rp','rt',
                'run','set','set-current-directory','set-current-plot','set-current-plot-pen','set-default-shape',
                'set-histogram-num-bars','set-patch-size','set-plot-pen-color','set-plot-pen-interval','set-plot-pen-mode',
                'set-plot-x-range','set-plot-y-range','setxy','show','show-link','show-turtle','sprout','st','stamp','stamp-erase',
                'stop','tick','tick-advance','tie','type','untie','uphill','uphill4','wait','watch','watch-me','while',
                'with-local-randomness','without-interruption','write']

    reporter = ['breed','abs','acos','all\?','and','any\?','approximate-hsb','approximate-rgb','asin','atan','at-points','autoplot\?',
                'base-colors','behaviorspace-run-number','bf','bl','both-ends','butfirst','but-first','butlast','but-last',
                'can-move\?','ceiling','color','cos','count','date-and-time','distance','distancexy','dx','dy','empty\?','end1',
                'end2','error-message','exp','extract-hsb','extract-rgb','file-at-end\?','file-exists\?','file-read',
                'file-read-characters','file-read-line','filter','first','floor','fput','heading','hidden\?','hsb',
                'hubnet-enter-message\?','hubnet-exit-message\?','hubnet-message','hubnet-message-source','hubnet-message-tag',
                'hubnet-message-waiting\?','ifelse-value','in-cone','in-link-from','in-link-neighbor\?','in-link-neighbors',
                'in-radius','int','is-agent\?','is-agentset\?','is-boolean\?','is-directed-link\?','is-link\?','is-link-set\?',
                'is-list\?','is-number\?','is-patch\?','is-patch-set\?','is-string\?','is-turtle\?','is-turtle-set\?',
                'is-undirected-link\?','item','label','label-color','last','length','link','link-heading','link-length',
                'link-neighbor\?','link-neighbors','links','link-set','link-shapes','link-with','list','ln','log','lput','map',
                'max','max-n-of','max-one-of','max-pxcor','max-pycor','mean','median','member\?','min','min-n-of','min-one-of',
                'min-pxcor','min-pycor','mod','modes','mouse-down\?','mouse-inside\?','mouse-xcor','mouse-ycor','movie-status',
                'my-in-links','my-links','my-out-links','myself','neighbors','neighbors4','netlogo-applet\?','netlogo-version',
                'new-seed','n-of','no-links','no-patches','not','no-turtles','n-values','of','one-of','or','other','other-end',
                'out-link-neighbor\?','out-link-neighbors','out-link-to','patch','patch-ahead','patch-at',
                'patch-at-heading-and-distance','patches','patch-here','patch-left-and-ahead','patch-right-and-ahead',
                'patch-set','patch-size','pcolor','pen-mode','pen-size','plabel','plabel-color','plot-name','plot-pen-exists\?',
                'plot-x-max','plot-x-min','plot-y-max','plot-y-min','position','precision','pxcor','pycor','random',
                'random-exponential','random-float','random-gamma','random-normal','random-poisson','random-pxcor',
                'random-pycor','random-xcor','random-ycor','read-from-string','reduce','remainder','remove','remove-duplicates',
                'remove-item','replace-item','reverse','rgb','round','runresult','scale-color','se','self','sentence',
                'shade-of\?','shape','shapes','shuffle','sin','size','sort','sort-by','sqrt','standard-deviation','subject',
                'sublist','substring','subtract-headings','sum','tan','thickness','ticks','tie-mode','timer','towards',
                'towardsxy','turtle','turtles','turtles-at','turtle-set','turtles-here','turtles-on','user-directory',
                'user-file','user-input','user-new-file','user-one-of','user-yes-or-no\?','variance','who','with','with-max',
                'with-min','word','world-height','world-width','wrap-color','xcor','xor','ycor']

    extension_commands = ['gis:APPLY-COVERAGES','gis:SET-SAMPLING-METHOD','gis:PAINT','gis:SET-TRANSFORMATION',
                          'gis:SET-WORLD-ENVELOPE','gis:SET-COVERAGE-MINIMUM-THRESHOLD','gis:APPLY-RASTER',
                          'gis:SET-COORDINATE-SYSTEM','gis:APPLY-COVERAGE','gis:FILL','gis:MYWORLD-SEND-DATASET',
                          'gis:SET-TRANSFORMATION-DS','gis:SET-RASTER-VALUE','gis:SET-DRAWING-COLOR','gis:IMPORT-WMS-DRAWING',
                          'gis:LOAD-COORDINATE-SYSTEM','gis:SET-COVERAGE-MAXIMUM-THRESHOLD','gis:SET-WORLD-ENVELOPE-DS',
                          'gis:STORE-DATASET','gis:DRAW','gogo:OPEN','gogo:SET-BURST-MODE','gogo:OUTPUT-PORT-THISWAY',
                          'gogo:TALK-TO-OUTPUT-PORTS','gogo:OUTPUT-PORT-ON','gogo:CLOSE','gogo:OUTPUT-PORT-OFF',
                          'gogo:SET-OUTPUT-PORT-POWER','gogo:STOP-BURST-MODE','gogo:OUTPUT-PORT-REVERSE','gogo:OUTPUT-PORT-THATWAY',
                          'gogo:OUTPUT-PORT-COAST','sound:PLAY-SOUND-LATER','sound:START-NOTE','sound:STOP-SOUND','sound:STOP-MUSIC',
                          'sound:PLAY-NOTE','sound:STOP-INSTRUMENT','sound:PLAY-NOTE-LATER','sound:PLAY-SOUND','sound:STOP-NOTE',
                          'sound:PLAY-SOUND-AND-WAIT','sound:LOOP-SOUND','sound:PLAY-DRUM','profiler:START',
                          'profiler:STOP','profiler:RESET','bitmap:COPY-TO-PCOLORS','bitmap:COPY-TO-DRAWING',
                          'bitmap:EXPORT','qtj:camera-start','qtj:camera-stop','qtj:camera-select','qtj:movie-open','qtj:movie-start',
                          'qtj:movie-stop','qtj:movie-open-player','qtj:movie-close','qtj:movie-image','qtj:movie-set-time',
                          'table:REMOVE','table:PUT','table:CLEAR','array:SET','r:STOPDEBUG','r:STARTJRIDEBUG','r:EVAL',
                          'r:INTERACTIVESHELL','r:PUTLIST','r:STOPJRIDEBUG','r:PUTAGENT','r:STARTDEBUG','r:PUTNAMEDLIST',
                          'r:PUTDATAFRAME','r:PUTAGENTDF','r:MESSAGEWINDOW','r:PUT','r:CLEAR','multiview:close','multiview:rename',
                          'multiview:repaint']


    extension_reporter = ['gis:RASTER-SAMPLE','gis:RASTER-WORLD-ENVELOPE','gis:COVERAGE-MINIMUM-THRESHOLD','gis:PROPERTY-MAXIMUM',
                          'gis:LOAD-DATASET','gis:INTERSECTS\?','gis:MYWORLD-GET-DATASET','gis:CONTAINED-BY\?','gis:HEIGHT-OF',
                          'gis:FIND-ONE-FEATURE','gis:LOCATION-OF','gis:LINK-DATASET','gis:PROPERTY-VALUE','gis:FIND-RANGE',
                          'gis:CONTAINS\?','gis:PATCH-DATASET','gis:FIND-LESS-THAN','gis:RESAMPLE','gis:TYPE-OF','gis:ENVELOPE-UNION-OF',
                          'gis:COVERAGE-MAXIMUM-THRESHOLD','gis:VERTEX-LISTS-OF','gis:WIDTH-OF','gis:DRAWING-COLOR','gis:CREATE-RASTER',
                          'gis:PROPERTY-MINIMUM','gis:RELATIONSHIP-OF','gis:INTERSECTING','gis:MINIMUM-OF','gis:MYWORLD-LAYERS',
                          'gis:WORLD-ENVELOPE','gis:ENVELOPE-OF','gis:HAVE-RELATIONSHIP\?','gis:MAXIMUM-OF','gis:TURTLE-DATASET',
                          'gis:PROPERTY-NAMES','gis:FIND-GREATER-THAN','gis:CONVOLVE','gis:CENTROID-OF','gis:SHAPE-TYPE-OF',
                          'gis:FEATURE-LIST-OF','gis:SAMPLING-METHOD-OF','gis:FIND-FEATURES','gis:RASTER-VALUE','gogo:SENSOR',
                          'gogo:BURST-VALUE','gogo:PING','gogo:PORTS','gogo:OPEN\?','sound:__SYNTH-DUMP','sound:DRUMS',
                          'sound:INSTRUMENTS','profiler:REPORT','profiler:INCLUSIVE-TIME','profiler:CALLS','profiler:EXCLUSIVE-TIME',
                          'bitmap:CHANNEL','bitmap:AVERAGE-COLOR','bitmap:IMPORT','bitmap:TO-GRAYSCALE','bitmap:HEIGHT',
                          'bitmap:DIFFERENCE-RGB','bitmap:FROM-VIEW','bitmap:SCALED','bitmap:WIDTH','qtj:camera-image',
                          'table:MAKE','table:FROM-LIST','table:TO-LIST','table:GET','table:HAS-KEY\?','table:KEYS','table:LENGTH',
                          'array:TO-LIST','array:FROM-LIST','array:ITEM','array:LENGTH','r:GET','multiview:newView']

    tokens = {
        'root': [
            (r';.*\n', Comment.Single), # line comment
            (r'["].*?["]', String), # strings "..."
            (r'(?<=\s)[+*/<>=!#%^&|`?^-]+(?=\s)', Operator), # operators
            #(r'(?<=\s)(breed)(\s*)(\[)(\s*)(?<=[\s\(\[])[.\S]+?(?=[\s\)\]])(\s+)(?<=[\s\(\[])[.\S]+?(?=[\s\)\]])(\])', Keyword), # usage of breed as keyword
            # this pattern is a reconstruction of the (more or less) bug in NetLogo, indicating breed as if it is in front of a new line 
            (r'(?<=\n)(breed)(\s*)(\[)(\s*)([.\S]+)(\s+)([.\S]+)(\s*)(\])', bygroups(Keyword,Whitespace,Name.Namespace,Whitespace,Name,Whitespace,Name,Whitespace,Name.Namespace)), # usage of breed as keyword
            (r'(%s)(?=[\s\]\)])' % '|'.join(keywords), Keyword), # keywords
            (r'(?<=[\s\[\(])(%s)(?=[\s\]\)])' % '|'.join(commands), Name.Tag), # commands
            (r'(?<=[\s\[\(])(%s)(?=[\s\]\)])' % '|'.join(reporter), Name.Function), # reporter
            (r'(?<=[\s\[\(])(%s)(?=[\s\]\)])' % '|'.join(constants), Name.Constant), # constants
            (r'(?<=[\s\[\(])(%s)(?=[\s\]\)])' % '|'.join(extension_commands), Name.Tag), # command (extensions)
            (r'(?<=[\s\[\(])(%s)(?=[\s\]\)])' % '|'.join(extension_reporter), Name.Function), # reporter (extensions)
            (r'(?<=[\s\[\(])[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?(?=[\s\]\)])', Number.Float), # float
            (r'(?<=[\s\[\(])[0-9]+L?(?=[\s\]\)])', Number.Integer), # integer
            (r'\s+', Whitespace), # whitespace
            (r'[\(\)\[\]]', Name.Namespace), # brace
            (r'(?<=[\s\(\[])[.\S]+?(?=[\s\)\]])', Name) # variable and procedure names
        ],
    }

    def get_tokens_unprocessed(self, text):
        # cut at the beginning of the interface and information tab stuff
        substrings = text.partition('@#$#@#$#@')
        text = substrings[0]
        stack = ['root']
        for item in RegexLexer.get_tokens_unprocessed(self, text, stack):
            yield item


class NetLogoStyle(Style):
    """
    A NetLogo style, according to the NetLogo Editor Highlighting.
    """

    default_style = ""

    styles = {
        Whitespace:                "#ffffff",

        Comment:                   "#5a5a5a",

        Operator:                  "#660096",

        Keyword:                   "#007f69",

        Name:                      "#090909",
        Name.Function:             "#660096",
        Name.Namespace:            "#090909",
        Name.Constant:             "#963700",        
        Name.Tag:                  "#0000aa",

        Number:                    "#963700",

        String:                    "#963700",

        #Error:                     "#F00 bg:#FAA"
    }
