
(defun c:TP_define_elements ( / A_el E_el selection ln_element old_env_vars counter
							    entname)

	(setq old_env_vars (env_get))
	(setvar "cmdecho" 0)

	(setq ln_element "TRUSSPY_elements")
	(command-s "._LAYER" "M" ln_element "C" "4" "" "")
	
	(setq A_el (getreal "\nEnter cross section area [m^2]: "))
	(setq E_el (getreal "\nEnter elasticity modulus [kN/m^2]: "))
	(setq selection (ssget '((0 . "LINE"))))
	
	(command "_.chprop" selection "" "_LA" ln_element "")
	
	(setq counter 0)
	(repeat (sslength selection)
		(setq entname (ssname selection counter))
		(vlax-ldata-put entname "E" E_el)
		(vlax-ldata-put entname "A" A_el)	
		(setq counter (+ 1 counter))
			
	)	

	(env_set old_env_vars)
	(princ)
)

