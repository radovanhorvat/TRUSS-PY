(load "f_functions")
(vl-load-com)

(defun c:TP_define_elements (/ A E selection element_layer old_env_vars counter
							   entitydata pt_start pt_end)

	(setq old_env_vars (env_get))
	(setvar "cmdecho" 0)

	(setq element_layer "TRUSSPY_elements")
	(command-s "._LAYER" "M" element_layer "C" "4" "" "")
	
	(setq A (getreal "\nEnter cross section area [m^2]: "))
	(setq E (getreal "\nEnter elasticity modulus [kN/m^2]: "))
	(setq selection (ssget '((0 . "LINE"))))
	
	(command "_.chprop" selection "" "_LA" element_layer "")
	
	(setq counter 0)
	(repeat (sslength selection)
		(setq entitydata (entget (ssname selection counter)))
		(setq entname (ssname selection counter))
		(vlax-ldata-put entname "E" E)
		(vlax-ldata-put entname "A" A)
		
		;(princ (vlax-ldata-get entname "E"))
		;(princ (vlax-ldata-get entname "A"))
		
		;(setq pt_start (cdr (assoc 10 entitydata)))
		;(setq pt_end (cdr (assoc 11 entitydata)))
		;(princ pt_start)
		;(princ pt_end)
		(setq counter (+ 1 counter))
			
	 )
	
	
	
	
	(env_set old_env_vars)
	(princ)
)

