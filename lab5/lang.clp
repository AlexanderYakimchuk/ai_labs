;Start CLIPS

;define characteristics to be used in rules:
(deftemplate Level (slot LangLevel))
(deftemplate CanBeExecuted (slot LangCanBeExecuted))
(deftemplate Style (slot LangStyle))
(deftemplate Typing (slot LangTyping))
(deftemplate WebDev (slot LangWebDev))
(deftemplate GameDev (slot LangGameDev))
(deftemplate Side (slot LangSide))
(deftemplate HasPointers (slot LangHasPointers))
(deftemplate Expertise (slot LangExpertise))
(deftemplate Lang (slot LangType))

;rules to define to which category the bacteria belongs(if bacteria)
(defrule MachineCode
	(Level (LangLevel low))
        (CanBeExecuted (LangCanBeExecuted yes))
=>
	(assert (Lang (LangType MachineCode)))
	(printout t "The language might be machine code." crlf)
	(halt))

(defrule Assembly
	(Level (LangLevel low))
	(CanBeExecuted (LangCanBeExecuted no))
=>
	(assert (Lang (LangType Assembly)))
	(printout t "The language might be Assembly" crlf)
	(halt))


(defrule Java
	(Level (LangLevel high))
	(Style (LangStyle oop))
	(Typing (LangTyping strong))
	(WebDev (LangWebDev yes))
	(GameDev (LangGameDev no))
	(Side (LangSide server))
=>
	(assert (Lang (LangType Java)))
	(printout t "The language might be Java" crlf)
	(halt))

(defrule CPlusPlus
	(Level (LangLevel high))
	(Style (LangStyle oop))
	(Typing (LangTyping strong))
	(WebDev (LangWebDev no))
	(GameDev (LangGameDev yes))
=>
	(assert (Lang (LangType CPlusPlus)))
	(printout t "The language might be C++" crlf)
	(halt))

(defrule CSharp
	(Level (LangLevel high))
	(Style (LangStyle oop))
	(Typing (LangTyping strong))
	(WebDev (LangWebDev yes))
	(GameDev (LangGameDev yes))
	(Side (LangSide server))
=>
	(assert (Lang (LangType CSharp)))
	(printout t "The language might be C#" crlf)
	(halt))

(defrule Python
	(Level (LangLevel high))
	(Style (LangStyle oop))
	(Typing (LangTyping dynamic))
	(WebDev (LangWebDev yes))
	(GameDev (LangGameDev no))
	(Side (LangSide server))
=>
	(assert (Lang (LangType Python)))
	(printout t "The language might be Python" crlf)
	(halt))

(defrule JS
	(Level (LangLevel high))
	(Style (LangStyle oop))
	(Typing (LangTyping dynamic))
	(WebDev (LangWebDev yes))
	(GameDev (LangGameDev no))
	(Side (LangSide client))
=>
	(assert (Lang (LangType JS)))
	(printout t "The language might be JavaScript" crlf)
	(halt))

(defrule C
	(Level (LangLevel high))
	(Style (LangStyle imperative))
	(HasPointers (LangHasPointers yes))
=>
	(assert (Lang (LangType C)))
	(printout t "The language might be C" crlf)
	(halt))

(defrule Pascal
	(Level (LangLevel high))
	(Style (LangStyle imperative))
	(HasPointers (LangHasPointers no))
=>
	(assert (Lang (LangType Pascal)))
	(printout t "The language might be Pascal" crlf)
	(halt))

(defrule Prolog
	(Level (LangLevel high))
	(Style (LangStyle logic))
	(Expertise (LangExpertise problem_solving))
=>
	(assert (Lang (LangType Prolog)))
	(printout t "The language might be Prolog" crlf)
	(halt))

(defrule CLIPS
	(Level (LangLevel high))
	(Style (LangStyle logic))
	(Expertise (LangExpertise expert_system))
=>
	(assert (Lang (LangType CLIPS)))
	(printout t "The language might be CLIPS" crlf)
	(halt))

(defrule LISP
	(Level (LangLevel high))
	(Style (LangStyle functional))
=>
	(assert (Lang (LangType LISP)))
	(printout t "The language might be LISP" crlf)
	(halt))

;constructs dealing with the dialog with the user
(defrule welcome
=>
	(printout t "Welcome. " crlf crlf))

(defrule enter_Level
=>
	(printout t "Please enter the level (low or high)" crlf)
	(bind ?the_LangLevel (read))
	(assert (Level (LangLevel ?the_LangLevel))))

(defrule enter_CanBeExecuted
	(Level (LangLevel low))
	=>
	(printout t "Please enter if language can be directly executed (yes or no)" crlf)
	(bind ?executable (read))
	(assert (CanBeExecuted (LangCanBeExecuted ?executable))))

(defrule enter_Style
	(Level (LangLevel high))
	=>
	(printout t "Please enter language style (oop, imperative, logic or functional)" crlf)
	(bind ?style (read))
	(assert (Style (LangStyle ?style))))

(defrule enter_Typing
	(Level (LangLevel high))
	(Style (LangStyle oop))
	=>
	(printout t "Please enter language typing (strong or dynamic)" crlf)
	(bind ?typing (read))
	(assert (Typing (LangTyping ?typing))))

(defrule enter_WebDev
	(Level (LangLevel high))
	(Style (LangStyle oop))
	=>
	(printout t "Please enter whether language is used for web development (yes or no)" crlf)
	(bind ?web (read))
	(assert (WebDev (LangWebDev ?web))))

(defrule enter_GameDev
	(Level (LangLevel high))
	(Style (LangStyle oop))
	=>
	(printout t "Please enter whether language is used for game development (yes or no)" crlf)
	(bind ?game (read))
	(assert (GameDev (LangGameDev ?game))))

(defrule enter_Side
	(Level (LangLevel high))
	(Style (LangStyle oop))
	(WebDev (LangWebDev yes))
	=>
	(printout t "Please enter whether language is server-side or client-side (server or client)" crlf)
	(bind ?side (read))
	(assert (Side (LangSide ?side))))

(defrule enter_HasPointers
	(Level (LangLevel high))
	(Style (LangStyle imperative))
	=>
	(printout t "Please enter if language has pointers (yes or no)" crlf)
	(bind ?has_pointers (read))
	(assert (HasPointers (LangHasPointers ?has_pointers))))

(defrule enter_Expertise
	(Level (LangLevel high))
	(Style (LangStyle logic))
	=>
	(printout t "Please enter language's expertise (problem_solving or expert_system)" crlf)
	(bind ?expertise (read))
	(assert (Expertise (LangExpertise ?expertise))))

;End CLIPS
