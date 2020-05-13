# -*- coding: utf-8 -*-


[OGL_ASSOCIATION, OGL_AGGREGATION, OGL_COMPOSITION, OGL_CANCEL, OGL_INTERFACE, 
 OGL_NOTELINK, OGL_SD_MESSAGE, OGL_EXPECTED_STATE, OGL_MODIFY, OGL_TRY,
 OGL_PROCESS] = range(11)

[OGL_NOTE, OGL_TITLE, OGL_TITLEEND, OGL_FOR, OGL_WHILE, OGL_LOG, OGL_STATEMENT,
 OGL_FIXLOG, OGL_IMPORT] = range(9)
OBJECT_NAME = ['NOTE','FUNCTION','FUNCTION_END','STATEMENT','LOG','FIXLOG','FOR_LOOP','WHILE_LOOP','IMPORT_XML']

[IF, ELIF, ELSE, TRY, EXCEPT, FINALLY] = range(6)

[NORTH, EAST, SOUTH, WEST] = range(4)

[CLASS_DIAGRAM, SEQUENCE_DIAGRAM, USECASE_DIAGRAM, UNKNOWN_DIAGRAM] = range(4)

DiagramLabels = {
        CLASS_DIAGRAM : "Class Diagram", 
        SEQUENCE_DIAGRAM: "Sequence Diagram", 
        USECASE_DIAGRAM: "Usecase Diagram", 
        UNKNOWN_DIAGRAM: "Unknown Diagram"
        }

DiagramStrings = {
        CLASS_DIAGRAM : "CLASS_DIAGRAM", 
        SEQUENCE_DIAGRAM: "SEQUENCE_DIAGRAM", 
        USECASE_DIAGRAM: "USECASE_DIAGRAM", 
        UNKNOWN_DIAGRAM: "UNKNOWN_DIAGRAM"
        }

def diagramTypeAsString(Type):
    return DiagramStrings[Type]

def diagramTypeFromString(string):
    for key in DiagramStrings:
        if string == DiagramStrings[key]:
            return key
    return UNKNOWN_DIAGRAM

DefaultFileName = ("Untitled.xml")

deltaAnchor = 40

orderWay = ["BUY","SELL","CROSS","UNKNOWN_WAY","BIDASK"]
expected = ["Ack","Exec","Reject","Cancel","Modify","Nack"]
states = ["ACK","CANCEL","EXEC","NACK","REJECT","UNDEF"]
try_type = ["cancel_order","expect_exec","expect_cancel","cmd_states"]

account = ["UNDEF","NONE","CLIENT","BROKER","HOUSE","NON_MEMBER","MARKET_MAKER","ISSUER","GIVE_UP","BEST_EXEC"]
validity = ["TODAY","GTC","GTD"]
restriction = ["NONE","IMMEDIATE_AND_CANCEL","FILL_OR_KILL","ALL_OR_NOTHING","STOP","GHOST","TAKE_PROFIT"]
prcMode = ["LIMIT","BEST","MARKET","MARKET_ON_OPEN","LIMIT_ON_OPEN","OPENING_OFFSET","MARKET_ON_CLOSE", "CLOSING_OFFSET"]
process = ["start","stop","all_greens"]
    