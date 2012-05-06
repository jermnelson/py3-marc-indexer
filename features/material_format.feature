Feature: Determine material format from a MARC21 record
    In order to display a record in a Library App or Discovery Layer
    As catalogers
    we need to define formats with matching scenarios for the MARC indexer

    Scenario: The entity is an Atlas
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | a     |
        | 007  | 1        | d     |
        Then the entity is an Atlas

    Scenario: The entity is a Blu-ray Video 
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | v     |
        | 007  | 1        | d     |
        | 007  | 4        | s     |
        Then the entity is a Blu-ray Video

    Scenario: The entity is a Book
        Given we have a MARC record
        When "<code>" field "<position>" not "<value>"
        | code | position | value |
        | 008  | 23       | d     |
        | 008  | 23       | s     |
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 7        | s     |
        | 008  | 21       | m     |
        But if "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 6        | t     |
        | 008  | 24       | b     |
        Then the entity is a Book


    Scenario: The entity is a Book On Cassette
        Given we have a MARC record
        When "<code>" field "<position>" not "<value>"
        | code | position | value |
        | 007  | 0        | s     |
        | 007  | 1        | s     |
        When the leader position 6 is i
        Then the entity is a Book On Cassette

    Scenario: The entity is a Book On CD
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | s     |
        | 007  | 1        | d     |
        | 007  | 6        | g     |
        | 007  | 6        | z     |
        When the leader position 6 is i
        Then the entity is a Book On CD

    Scenario: The entity is a Cassette
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | s     |
        | 007  | 1        | s     |
        When the leader position 6 is j
        Then the entity is a Cassette

    Scenario: The entity is a CDROM
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | c     |
        | 007  | 1        | r     |
        | 007  | 1        | m     |
        Then the entity is a CDROM

    Scenario: The entity is a Chart
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | k     |
        | 007  | 1        | n     |
        But if "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 6        | k     |
        | 008  | 33       | n     |
        Then the entity is a Chart

    Scenario: The entity is a Collage
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | k     |
        | 007  | 1        | c     |
        Then the entity is a Collage

    Scenario: The entity is a Collection
        Given we have a MARC record
        When "<code>" field "<position>" are "<value>"
        | code | position | value |
        | LDR  | 6        | a     |
        | LDR  | 7        | c     |
        But if "<code>" field "<position>" are "<value>"
        | code | position | value |
        | LDR  | 6        | p     |
        | LDR  | 7        | c     |
        Then the entity is a Collection

    Scenario: The entity is a Drawing
        Given we have a MARC record
<<<<<<< HEAD
        When "<code>" field "<position>" is "<value>"
=======
        When "<code>" field "<position>" are "<value>"
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        | code | position | value |
        | 007  | 0        | k     |
        | 007  | 1        | d     |
        | 007  | 1        | l     |
        Then the entity is a Drawing

    Scenario: The entity is a DVD Video 
        Given we have a MARC record
<<<<<<< HEAD
        When "<code>" field "<position>" is "<value>"
=======
        When "<code>" field "<position>" are "<value>"
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        | code | position | value |
        | 007  | 0        | v     |
        | 007  | 1        | d     |
        | 007  | 4        | v     |
        | 007  | 4        | g     |
        Then the entity is a DVD Video

    Scenario: The entity is an Electronic
        Given we have a MARC record
<<<<<<< HEAD
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 7        | m     |
        | 008  | 23       | s     |
=======
        When "<code>" field "<position>" are "<value>"
        | code | position | value |
        | 007  | 0        | c     |
        | 007  | 1        | r     |
        But if "<code>" field "<position>" are "<value>"
        | code | position | value |
        | LDR  | 7        | m     |
        | 008  | 23       | s     |
        But if "<code>" field "<position>" are "<value>"
        | code | position | value |
        | LDR  | 6        | m     |
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        Then the entity is an Electronic

    Scenario: The entity is a Filmstrip 
        Given we have a MARC record
<<<<<<< HEAD
        And we have leader and 007 fields
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | m     |
=======
        When "<code>" field "<position>" are "<value>"
        | code | position | value |
        | 007  | 0        | c     |
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        | 007  | 1        | r     |
        Then the entity is a Filmstrip

    Scenario: The entity is a Flash Card
        Given we have a MARC record
<<<<<<< HEAD
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | k     |
        | 007  | 1        | o     |
=======
        When "<code>" field "<position>" are "<value>"
        | code | position | value |
        | 007  | 1        | o     |
        But if "<code>" field "<position>" are "<value>"
        | code | position | value |
        | LDR  | 6        | k     |
        | 008  | 33       | o     |
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        Then the entity is a Flash Card

    Scenario: The entity is a Floppy Disk
        Given we have a MARC record
<<<<<<< HEAD
        When "<code>" field "<position>" is "<value>"
=======
        When "<code>" field "<position>" are "<value>"
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        | code | position | value |
        | 007  | 0        | c     |
        | 007  | 1        | j     |
        Then the entity is a Floppy Disk

    Scenario: The entity is a Game
        Given we have a MARC record
        When "<code>" field "<position>" are "<value>"
        | code | position | value |
        | LDR  | 6        | r     |
        | 008  | 33       | b     |
        Then the entity is a Game

    Scenario: The entity is a Globe
        Given we have a MARC record
<<<<<<< HEAD
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | d     |
=======
        When "<code>" field "<position>" are "<value>"
        | code | position | value |
        | 00   | 0        | d     | 
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        Then the entity is a Globe

    Scenario: The entity is a Journal
        Given we have a MARC record
<<<<<<< HEAD
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 7        | s     |
        When "<code>" field "<position>" not "<value>"
        | code | position | value |
        | 008  | 21       | m     |
        Then the entity is a Journal

    Scenario: The entity is a Journal
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 7        | s     |
        Then the entity is a Journal

    Scenario: The entity is a kit
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
=======
        When "<code>" field "<position>" are "<value>"
        | code | position | value |
        | LDR  | 7        | s     |    
        | 008  | 21       | m     |
        But if "<code>" field "<position>" are "<value>"
        | code | position | value |
        | LDR  | 7        | s     |    
        Then the entity is a Journal


    Scenario: The entity is a kit
        Given we have a MARC record
        When "<code>" field "<position>" are "<value>"
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        | code | position | value |
        | 007  | 0        | o     |
        Then the entity is a kit

    Scenario: The entity is a Large Print Book
        Given we have a MARC record
<<<<<<< HEAD
        When "<code>" field "<position>" is "<value>"
=======
        When "<code>" field "<position>" are "<value>"
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        | code | position | value |
        | LDR  | 7        | m     |
        | 008  | 23       | d     |
        Then the entity is a Large Print Book

    Scenario: The entity is a LP Record
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
<<<<<<< HEAD
        | code | position | value |
        | 007  | 0        | s     |
        | 007  | 1        | d     |
        | 007  | 6        | e     |
        When the leader position 6 is j
=======
        | code | position | value|
        | LDR  | 6        | j    |
        | 007  | 0        | s    |
        | 007  | 1        | d    |
        | 007  | 6        | e    |
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        Then the entity is a LP Record

    Scenario: The entity is a Manuscript
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
<<<<<<< HEAD
        | code | position | value |
        | LDR  | 6        | b     |
=======
        | code | position | value|
        | LDR  | 6        | b    |
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        Then the entity is a Manuscript

    Scenario: The entity is a Manuscript noted music
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value|
        | LDR  | 6        | d    |
        Then the entity is a Manuscript noted music

    Scenario: The entity is a Map
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value | 
        | LDR  | 6        | e     |
        | 007  | 0        | a     | 
        When "<code>" field "<position>" not "<value>"
<<<<<<< HEAD
        | code | position | value |
        | 007  | 1        | d     |
=======
        | code | position | value|
        | 007  | 1        | d    |
        But if "<code>" field "<position>" is "<value>"
        | code | position | value|
        | LDR  | 6        | e    |
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        Then the entity is a Map

 
    Scenario: The entity is a Microfilm
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | h     |
        Then the entity is a Microfilm

    Scenario: The entity is a Mixed Materials
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 6        | p     |
        When "<code>" field "<position>" not "<value>"
        | code | position | value |
        | LDR  | 7        | c     |
        Then the entity is a Mixed Materials

    Scenario: The entity is a Motion picture
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | m     |
        When "<code>" field "<position>" not "<value>"
        | code | position | value |
        | f    | 1        | f     |
        | f    | 1        | r     |
        Then the entity is a Motion picture

    Scenario: The entity is a Music CD
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 6        | j     |
        | 007  | 0        | s     |
        | 007  | 1        | d     |
        | 007  | 6        | g     |
        | 007  | 6        | z     |
        Then the entity is a Music CD

    Scenario: The entity is a Musical Score 
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | a     |
        But if "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 6        | g     |
        Then the entity is a Musical Score

    Scenario: The entity is a Music Sound Recording 
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 6        | j     |
        Then the entity is a Music Sound Recording 

    Scenario: The entity is a Painting 
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | k     |
        | 007  | 1        | e     |
        Then the entity is a Painting

    Scenario: The entity is a Photo 
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | k     | 
        When "<code>" field "<position>" not "<value>"
        | code | position | value |
        | 007  | 1        | c     |
        | 007  | 1        | d     |
        | 007  | 1        | e     |
        | 007  | 1        | f     |
        | 007  | 1        | k     |
        | 007  | 1        | l     |
        | 007  | 1        | o     |
        | 007  | 1        | n     |
        Then the entity is a Photo

    Scenario: The entity is a Photonegative 
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | k     | 
        | 007  | 1        | g     | 
        Then the entity is a Photonegative

    Scenario: The entity is a Poster
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 6        | k     |
        | 008  | 33       | i     |
        Then the entity is a Poster

    Scenario: The entity is a Print 
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | k     | 
        | 007  | 1        | f     | 
        | 007  | 1        | j     | 
        Then the entity is a Print

    Scenario: The entity is a Series
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
<<<<<<< HEAD
        | LDR  | 6        | a     |        
=======
        | LDR  | 6        | a     | 
>>>>>>> fba05a50d57a7932b604855091b50a76b1a07f35
        | LDR  | 7        | c     |
        Then the entity is a Series

    Scenario: The entity is a Spoken Sound Recording
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 6        | i     |
        When "<code>" field "<position>" not "<value>"
        | code | position | value |
        | LDR  | 6        | \#    |
        Then the entity is a Spoken Sound Recording

    Scenario: The entity is a Thesis
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | LDR  | 6        | t     |
        | 008  | 24       | m     |
        Then the entity is a Thesis
 
    Scenario: The entity is a VHS Video 
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | v     |
        | 007  | 1        | f     |
        | 007  | 1        | d     |
        | 007  | 4        | b     |
        | 007  | 4        | None  |
        Then the entity is a VHS Video

    Scenario: The entity is a Videocassette 
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | m     |
        | 007  | 1        | f     |
        Then the entity is a Videocassette

    Scenario: The entity is a Video Reel
        Given we have a MARC record
        When "<code>" field "<position>" is "<value>"
        | code | position | value |
        | 007  | 0        | v     |
        | 007  | 1        | r     |
        Then the entity is a Video Reel

